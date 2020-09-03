from datetime import datetime, timedelta, timezone
import os

import pytest
from selenium.common.exceptions import NoSuchElementException

from caseworker import Caseworker
from configuration import EMAIL_ACCOUNT, EMAIL_PASSWORD
from customer import Customer
from email_client import check_for_email, get_emails
from error_handling import DjangoDebugError
from fixtures import factory_reset_before_each_test, browser
from functional_tests.helpers import create_new_case_initiate_case_and_register_interest


@pytest.mark.parametrize(
    ['information_request_type', 'expected_email_subject_prefix'],
    [
        ('Ad-hoc', 'Information request'),
        ('Application report', 'Questionnaire to complete'),
        ('Hearing notification', 'Questionnaire to complete'),
        ('Pre-Sampling Questionnaire', 'Questionnaire to complete'),
        ('Questionnaire', 'Questionnaire to complete'),
        ('Visit Report', 'Questionnaire to complete'),  # Non safeguarding cases
        ('Authentication report', 'Questionnaire to complete')  # Safeguarding cases
    ])
def test_multiple_deficiency_corrections(browser, information_request_type, expected_email_subject_prefix):
    """
    1. Check email when customer receives information request.
    2. Check email when customer responds to information request.
    3. Check email when caseworker marks submission as deficient (first time)
    4. Check email when customer responds to deficiency notice (first time)
    5. Check email when caseworker marks submission as deficient (second time)
    6. Check email when customer responds to deficiency notice (second time)
    NB. We don't expect an email when caseworker marks the submission as sufficient
    """

    caseworker = Caseworker()
    customer = Customer(email=EMAIL_ACCOUNT, auto=True, browser=browser)
    case = create_new_case_initiate_case_and_register_interest(browser, caseworker, customer, 'Anti-dumping investigation')

    # Caseworker makes an information request
    deadline_days_from_now = 10
    expected_deadline_string = (datetime.now() + timedelta(days=deadline_days_from_now)).strftime('%-d %B %Y')
    submission_time = datetime.now(timezone.utc)
    submission = caseworker.submissions.domestic_producer.request_information(
        browser=browser,
        case=case,
        party=customer.company_name,
        submission_type=information_request_type,
        files=[{
            'file_path': os.getcwd() + '/dummy_files/document 3.docx',
            'confidential': True
        }],
        name='An information request for you',
        description='with all my love',
        response_window_days=deadline_days_from_now
    )

    # 1. Customer gets an email about the information request
    email = check_for_email(
        later_than=submission_time,
        with_subject=f'{expected_email_subject_prefix} for AD0001 {case}',
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )
    last_expected_email_time = datetime.now(timezone.utc)
    if expected_deadline_string not in email.body:
        pytest.fail(f"Deadline {expected_deadline_string} not seen in email body {email.body}")

    # Customer sees an indicator alerting them about the submission
    customer.sign_in(browser=browser)
    indicator = browser.find_element_by_class_name('number-circle')
    assert indicator.text == '1'

    # TODO: Check due date on customer 'my case record' page (need a page object for this)

    # Customer responds to information request
    customer.respond_to_submission.download_submission(
        browser=browser, case=case, submission=submission, file_names=['document 3.docx'])
    customer.respond_to_submission.upload_response(
        browser=browser, case=case, submission=submission, files=[os.getcwd() + '/dummy_files/document 4.docx'])
    customer.respond_to_submission.upload_non_confidential_response(
        browser=browser, case=case, submission=submission, files=[os.getcwd() + '/dummy_files/document 5.docx'])
    customer.respond_to_submission.final_check(browser=browser, case=case, submission=submission)
    # Check no unexpected emails
    emails = get_emails(
        later_than=last_expected_email_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD,
        delay=5
    )
    if emails:
        pytest.fail(f"Unexpected email(s) received before response to information request submitted: {emails}")
    response_time = datetime.now(timezone.utc)
    customer.respond_to_submission.submit(browser=browser, case=case, submission=submission)

    # 2. Customer gets an email to confirm receipt of their response
    check_for_email(
        later_than=response_time,
        with_subject='Your submission has been received',
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )

    # Caseworker marks submission as deficient (first time)
    rejection_time = datetime.now(timezone.utc)
    caseworker.submissions.domestic_producer.reject(
        browser=browser,
        case=case,
        party=customer.company_name,
        submission_name='An information request for you',
        deficient_documents=['document 4.docx'],
        deficiency_documents=[os.getcwd() + '/dummy_files/document 6.docx']
    )

    # 3. Customer gets an email about the deficiency
    email = check_for_email(
        later_than=rejection_time,
        with_subject='Further information required: Deficiency Notice',
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )
    last_expected_email_time = datetime.now(timezone.utc)
    # Check deadline in email
    expected_deadline_string = (datetime.now() + timedelta(days=deadline_days_from_now)).strftime('%-d %B %Y')
    if expected_deadline_string not in email.body:
        pytest.fail(f"Deadline {expected_deadline_string} not seen in email body {email.body}")

    # Customer sees an indicator alerting them about the deficiency
    customer.sign_in(browser=browser)

    indicator = browser.find_element_by_class_name('number-circle')
    assert indicator.text == '1'
    indicator_container_class = indicator.find_element_by_xpath('..').get_attribute('class')
    assert indicator_container_class == 'aggregate-status'  # aggregate-status is styled red by JS

    # TODO: Check the status is marked 'deficient' in red on the case record page
    # TODO: Check the submission due date on the case record page (broken, wrong date, bug TR-1475)

    # Customer responds to deficiency notice (first time)
    customer.respond_to_submission.download_deficiency_notices(
        browser=browser,
        case=case,
        submission=submission,
        file_names=['document 6.docx'])

    customer.respond_to_submission.replace_deficient_documents(
        browser=browser,
        case=case,
        submission=submission,
        replacement_file_for_deficient_file_name={'document 4.docx': os.getcwd() + '/dummy_files/document 7.docx'})
    customer.respond_to_submission.final_check(browser=browser, case=case, submission=submission)
    # Check no unexpected emails
    emails = get_emails(
        later_than=last_expected_email_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD,
        delay=5
    )
    if emails:
        pytest.fail(f"Unexpected email(s) received before amended response to information request submitted: {emails}")
    correction_time = datetime.now(timezone.utc)
    customer.respond_to_submission.submit(browser=browser, case=case, submission=submission)

    # 4. Customer gets an email to confirm receipt of their response
    check_for_email(
        later_than=correction_time,
        with_subject='Your submission has been received',
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )

    # Caseworker rejects response as deficient (second time)
    second_rejection_time = datetime.now(timezone.utc)
    caseworker.submissions.domestic_producer.reject(
        browser=browser,
        case=case,
        party=customer.company_name,
        submission_name='An information request for you (version 2)',
        deficient_documents=['document 7.docx'],
        deficiency_documents=[os.getcwd() + '/dummy_files/document 8.docx']
    )

    # 5. Customer gets an email about the deficiency (second time)
    check_for_email(
        later_than=second_rejection_time,
        with_subject='Further information required: Deficiency Notice',
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )
    last_expected_email_time = datetime.now(timezone.utc)

    # Customer sees an indicator alerting them about the second deficiency
    customer.sign_in(browser=browser)
    indicator = browser.find_element_by_class_name('number-circle')
    assert indicator.text == '1'
    indicator_container_class = indicator.find_element_by_xpath('..').get_attribute('class')
    assert indicator_container_class == 'aggregate-status'  # aggregate-status is styled red by JS

    # Customer responds to second deficiency notice
    customer.respond_to_submission.download_deficiency_notices(
        browser=browser,
        case=case,
        submission=submission,
        file_names=['document 8.docx'])
    customer.respond_to_submission.replace_deficient_documents(
        browser=browser,
        case=case,
        submission=submission,
        replacement_file_for_deficient_file_name={'document 7.docx': os.getcwd() + '/dummy_files/document 9.docx'})
    customer.respond_to_submission.final_check(browser=browser, case=case, submission=submission)
    # Check no unexpected emails
    emails = get_emails(
        later_than=last_expected_email_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD,
        delay=5
    )
    if emails:
        pytest.fail(f"Unexpected email(s) received before amended response to information request submitted: {emails}")
    second_correction_time = datetime.now(timezone.utc)
    customer.respond_to_submission.submit(browser=browser, case=case, submission=submission)

    # 6. Customer gets an email to confirm receipt of their response
    check_for_email(
        later_than=second_correction_time,
        with_subject='Your submission has been received',
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )

    # Caseworker approves response
    caseworker.submissions.domestic_producer.approve(
        browser=browser,
        case=case,
        party=customer.company_name,
        submission_name='An information request for you (version 3)'
    )

    # Customer sees sufficient status
    customer.sign_in(browser)
    case_list = browser.find_element_by_class_name('dashboard-case-list')
    try:
        case_link = case_list.find_element_by_partial_link_text(case)
    except NoSuchElementException:
        raise ValueError("No case link found on dashboard for {}".format(case))

    case_link.click()
    from helpers import parse_table
    table_element = browser.find_element_by_class_name('my-case')
    parsed_table = parse_table(browser=browser, table_element=table_element)
    for row in parsed_table:
        if row['type'] == information_request_type and row['name'] == submission:
            assert row['status'] == 'Sufficient'
            break
    else:
        raise ValueError(f"No '{information_request_type}' submission with name '{submission}' found in my case record")
