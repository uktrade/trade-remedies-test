# TODO: Refactor this module

from datetime import datetime, timezone
import os

import pytest
from selenium.common.exceptions import NoSuchElementException

from caseworker import Caseworker
from configuration import EMAIL_ACCOUNT, EMAIL_PASSWORD
from customer import Customer
from email_client import check_for_email, get_emails
from fixtures import factory_reset_before_each_test, browser


@pytest.mark.skip(reason='Case cancelled email not implemented yet')
def test_dismiss_case(browser):
    """Caseworker dismisses the case from the task list"""

    submission_name = 'Application'
    caseworker = Caseworker()
    customer = Customer(email=EMAIL_ACCOUNT, auto=True, browser=browser)

    # Customer submits a full application
    start_time = datetime.now(timezone.utc)
    case = customer.apply_for_trade_remedy.create_case(
        case_type='Anti-dumping investigation',
        auto=True,
        browser=browser
    )

    customer.apply_for_trade_remedy.upload_documents(
        browser=browser,
        case=case,
        files=[os.getcwd() + '/dummy_files/document 1.docx']
    )

    customer.apply_for_trade_remedy.upload_documents_for_public_file(
        browser=browser,
        case=case,
        files={'document 1.docx': os.getcwd() + '/dummy_files/document 2.docx'}
    )

    customer.apply_for_trade_remedy.check_application(
        browser=browser,
        case=case
    )

    customer.apply_for_trade_remedy.submit_application(
        browser=browser,
        case=case
    )

    caseworker.tasks.close_case.dismiss_case(browser=browser, auto=True, case=case)

    # Customer receives an email to notify of the dismissal

    # Check customer dashboard (not sure what's meant to happen, either it stays there with status 'deficient' or it disappears)


@pytest.mark.skip("TR-1739. This email is getting sent when application docs are marked sufficient, needs to get sent when case is initiated.")
def test_initiate_case(browser):
    """
    Customer makes a full application
    Caseworker initiates it
    Check for email
    """


def test_multiple_deficiency_corrections_and_approval(browser):
    """
    Check emails:
    1. When customer submits full application
    2. When caseworker marks it as deficient (first time)
    3. When customer responds to deficiency notice (first time)
    4. When caseworker marks it as deficient (second time)
    5. When customer responds to deficiency notice (second time)
    6. When caseworker approves full application
    """
    submission_name = 'Application'
    caseworker = Caseworker()
    customer = Customer(email=EMAIL_ACCOUNT, auto=True, browser=browser)

    # Customer submits a full application
    start_time = datetime.now(timezone.utc)
    case = customer.apply_for_trade_remedy.create_case(
        case_type='Anti-dumping investigation',
        auto=True,
        browser=browser
    )

    customer.apply_for_trade_remedy.upload_documents(
        browser=browser,
        case=case,
        files=[os.getcwd() + '/dummy_files/document 1.docx']
    )

    customer.apply_for_trade_remedy.upload_documents_for_public_file(
        browser=browser,
        case=case,
        files={'document 1.docx': os.getcwd() + '/dummy_files/document 2.docx'}
    )

    customer.apply_for_trade_remedy.check_application(
        browser=browser,
        case=case
    )

    # Check no unexpected emails
    emails = get_emails(
        later_than=start_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD,
        delay=5
    )
    if emails:
        pytest.fail(f"Unexpected email(s) received before application submitted: {emails}")

    submission_time = datetime.now(timezone.utc)
    customer.apply_for_trade_remedy.submit_application(
        browser=browser,
        case=case
    )

    # 1. Customer receives an email to confirm receipt of full application
    check_for_email(
        with_subject='Final application received',
        later_than=submission_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )

    # Caseworker sees full application
    case_summary = caseworker.tasks.parse_case_summary(browser, case)
    assert case_summary['Current stage'] == 'Application received'
    application_status = caseworker.submissions.applicant.get(browser, case)[0]['status']
    assert application_status == 'Received'

    # # Caseworker marks application as deficient
    first_rejection_time = datetime.now(timezone.utc)
    caseworker.submissions.applicant.reject(
        browser=browser,
        case=case,
        party=customer.company_name,
        submission_name=submission_name,
        deficiency_documents=[os.getcwd() + f'/dummy_files/document 3.docx'],
        deficient_documents=['document 1.docx']
    )

    # 2. Customer receives an email notification
    check_for_email(
        with_subject='Incomplete application: more information needed'.format(case),
        later_than=first_rejection_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )
    last_expected_email_time = datetime.now(timezone.utc)

    # TODO: Bug. Put a break point here and see that the submission is now version 2, even though the customer only
    #   ever submitted one version.

    # Customer downloads deficiency notices
    customer.respond_to_submission.download_deficiency_notices(
        browser=browser,
        case=case,
        submission=submission_name,
        file_names=['document 3.docx']
    )

    # Customer replaces the deficient documents with new ones
    customer.respond_to_submission.replace_deficient_documents(
        browser=browser,
        case=case,
        submission=submission_name,
        replacement_file_for_deficient_file_name={'document 1.docx': os.getcwd() + '/dummy_files/document 4.docx'}
    )

    # 3. And submits the amended application
    customer.respond_to_submission.final_check(browser, case, submission=submission_name)
    # Check no unexpected emails
    emails = get_emails(
        later_than=last_expected_email_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD,
        delay=5
    )
    if emails:
        pytest.fail(f"Unexpected email(s) received before amended application submitted: {emails}")
    first_correction_time = datetime.now(timezone.utc)
    customer.respond_to_submission.submit(browser, case, submission=submission_name)

    # Customer gets an email confirmation
    check_for_email(
        later_than=first_correction_time,
        with_subject='Final application received',
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )

    # Caseworker sees full application
    case_summary = caseworker.tasks.parse_case_summary(browser, case)
    assert case_summary['Current stage'] == 'Application received'
    application_status = caseworker.submissions.applicant.get(browser, case)[0]['status']
    assert application_status == 'Received'

    # Caseworker marks application as deficient
    second_rejection_time = datetime.now(timezone.utc)
    caseworker.submissions.applicant.reject(
        browser=browser,
        case=case,
        party=customer.company_name,
        submission_name=f'{submission_name} (version 2)',
        deficiency_documents=[os.getcwd() + f'/dummy_files/document 5.docx'],
        deficient_documents=['document 4.docx']
    )

    # 4. Customer receives an email notification
    check_for_email(
        with_subject='Incomplete application: more information needed'.format(case),
        later_than=second_rejection_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )
    last_expected_email_time = datetime.now(timezone.utc)

    # TODO: Bug. Put a break point here and see that the submission is now version 2, even though the customer only
    #   ever submitted one version.

    # Customer downloads deficiency notices
    customer.respond_to_submission.download_deficiency_notices(
        browser=browser,
        case=case,
        submission=submission_name,
        file_names=['document 5.docx']
    )

    # Customer replaces the deficient documents with new ones
    customer.respond_to_submission.replace_deficient_documents(
        browser=browser,
        case=case,
        submission=submission_name,
        replacement_file_for_deficient_file_name={'document 4.docx': os.getcwd() + '/dummy_files/document 6.docx'}
    )

    # And submits the amended application
    customer.respond_to_submission.final_check(browser, case, submission=submission_name)
    # Check no unexpected emails
    emails = get_emails(
        later_than=last_expected_email_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD,
        delay=5
    )
    if emails:
        pytest.fail(f"Unexpected email(s) received before amended application submitted: {emails}")
    second_correction_time = datetime.now(timezone.utc)
    customer.respond_to_submission.submit(browser, case, submission=submission_name)

    # 5. Customer receives an email confirmation
    check_for_email(
        later_than=second_correction_time,
        with_subject='Final application received',
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )

    # Caseworker approves the application
    approval_time = datetime.now(timezone.utc)
    caseworker.submissions.applicant.approve(
        browser=browser,
        case=case,
        party=customer.company_name,
        submission_name=f'{submission_name} (version 3)'
    )

    # 6. Customer gets an email to notify of the application success
    try:
        check_for_email(
            with_subject='Application successful',
            later_than=approval_time,
            addressed_to=customer.name,
            account=EMAIL_ACCOUNT,
            password=EMAIL_PASSWORD
        )
        pytest.xfail("TR-1739")
    except TimeoutError:
        pytest.fail("TR-1739 may have been fixed, need to add a check for the new email we expect here!")

    # Customer sees 'sufficient' status
    customer.sign_in(browser)
    # TODO: Check it appears under the right heading ('Your applications')
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
        if row['type'] == 'Application' and row['name'] == submission_name:
            assert row['status'] == 'Sufficient'
            break
    else:
        raise ValueError(f"No 'Application' submission with name '{submission_name}' found in my case record")
