# TODO: Refactor this module

from datetime import datetime, timezone
import os

from selenium.common.exceptions import NoSuchElementException
import pytest

from caseworker import Caseworker
from configuration import EMAIL_ACCOUNT, EMAIL_PASSWORD
from customer import Customer
from email_client import check_for_email, get_emails
from fixtures import factory_reset_before_each_test, browser


def test_multiple_deficiency_corrections_and_approval(browser):
    """
    Check emails:
    1. When customer submits draft application for review
    2. When caseworker marks it as deficient (first time)
    3. When customer responds to deficiency notice (first time)
    4. When caseworker marks it as deficient (second time)
    5. When customer responds to deficiency notice (second time)
    6. When caseworker approves draft application
    """

    submission_name = 'Application'
    caseworker = Caseworker()
    customer = Customer(email=EMAIL_ACCOUNT, auto=True, browser=browser)

    # Customer creates a case
    case_type = 'Anti-dumping investigation'
    start_time = datetime.now(timezone.utc)
    case = customer.apply_for_trade_remedy.create_case(
        case_type=case_type,
        auto=True,
        browser=browser
    )

    customer.apply_for_trade_remedy.upload_documents(
        browser=browser,
        case=case,
        files=[os.getcwd() + '/dummy_files/document 1.docx']
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
        pytest.fail(f"Unexpected email(s) received before draft review requested: {emails}")

    # Request draft application review
    review_request_time = datetime.now(timezone.utc)
    customer.apply_for_trade_remedy.request_review_of_draft_application(
        browser=browser,
        case=case
    )

    # 1. Customer gets an email to confirm receipt of draft
    check_for_email(
        with_subject='Draft application received',
        later_than=review_request_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )

    # Caseworker sees draft application
    case_summary = caseworker.tasks.parse_case_summary(browser, case)
    assert case_summary['Current stage'] == 'Draft received'
    application_status = caseworker.submissions.applicant.get(browser, case)[0]['status']
    assert application_status == 'Review'

    # Caseworker marks draft as deficient
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

    # Customer sees 'Awaiting information' status
    # TODO: Similar code block appears twice in this test refactor!
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
            assert row['status'] == 'Awaiting information'
            break
    else:
        raise ValueError(f"No 'Application' submission with name '{submission_name}' found in my case record")

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

    # Check no unexpected emails
    emails = get_emails(
        later_than=last_expected_email_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD,
        delay=5
    )
    if emails:
        pytest.fail(f"Unexpected email(s) received before amended draft review submitted: {emails}")

    # And submits the amended draft application
    first_correction_time = datetime.now(timezone.utc)
    customer.apply_for_trade_remedy.request_review_of_draft_application(
        browser=browser,
        case=case
    )

    # 3. Customer gets an email confirmation
    check_for_email(
        with_subject='Draft application received',
        later_than=first_correction_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )

    # Caseworker sees draft application
    case_summary = caseworker.tasks.parse_case_summary(browser, case)
    assert case_summary['Current stage'] == 'Draft received'
    application_status = caseworker.submissions.applicant.get(browser, case)[0]['status']
    assert application_status == 'Review'

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

    # Customer sees 'Awaiting information' status
    # TODO: Similar code block appears twice in this test refactor!
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
            assert row['status'] == 'Awaiting information'
            break
    else:
        raise ValueError(f"No 'Application' submission with name '{submission_name}' found in my case record")

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

    # Check no unexpected emails
    emails = get_emails(
        later_than=last_expected_email_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD,
        delay=5
    )
    if emails:
        pytest.fail(f"Unexpected email(s) received before amended draft review submitted: {emails}")

    # And submits the amended application
    second_correction_time = datetime.now(timezone.utc)
    customer.apply_for_trade_remedy.request_review_of_draft_application(
        browser=browser,
        case=case
    )

    # 5. Customer receives an email confirmation
    check_for_email(
        later_than=second_correction_time,
        with_subject='Draft application received',
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
    check_for_email(
        with_subject='Draft application reviewed',
        later_than=approval_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )

    # Customer sees 'proceed' status
    # TODO: Similar code block appears in other tests, refactor
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
            assert row['status'] == 'Proceed'
            break
    else:
        raise ValueError(f"No 'Application' submission with name '{submission_name}' found in my case record")
