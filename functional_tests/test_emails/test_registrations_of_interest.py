from datetime import date, datetime, timezone, timedelta
import os

import pytest
from selenium.common.exceptions import NoSuchElementException

from caseworker import Caseworker
from configuration import EMAIL_ACCOUNT, EMAIL_PASSWORD
from customer import Customer
from email_client import check_for_email, get_emails
from fixtures import factory_reset_before_each_test, browser


def test_caseworker_rejects_party(browser):

    caseworker = Caseworker()

    # Caseworker creates ex-officio case
    case = caseworker.new_ex_officio_case(case_type='Anti-dumping investigation', auto=True, browser=browser)

    # Caseworker initiates the case
    caseworker.tasks.initiation.publish_initiation_notices(
        auto=True,
        case=case,
        browser=browser)

    # Customer creates an account
    customer = Customer(email=EMAIL_ACCOUNT, auto=True, browser=browser)

    # Starts registration of interest
    customer.register_interest.start_registration(case=case, browser=browser)

    # Uploads a document
    customer.register_interest.upload_registration_documents(
        case=case,
        files=[
            os.getcwd() + '/dummy_files/document 1.docx'
        ],
        browser=browser
    )

    # Submits the registration of interest
    customer.register_interest.submit_registration(case=case, browser=browser)

    # Caseworker rejects party
    rejection_time = datetime.now(timezone.utc)
    caseworker.parties.awaiting_approval.reject(
        browser=browser,
        case=case,
        party=customer.company_name
    )

    # Customer gets an email to notify of the rejection
    email = check_for_email(
        later_than=rejection_time,
        with_subject='Registration of interest request',
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )
    assert 'has not been approved' in email.body


def test_multiple_deficiency_corrections_and_approval(browser):
    """
    Check emails:
    1. When customer submits ROI
    2. When caseworker marks the submission as deficient (first time)
    3. When customer responds to deficiency notice (first time)
    4. When caseworker marks it as deficient (second time)
    5. When customer responds to deficiency notice (second time)
    6. When caseworker approves the party (they approve the ROI first, but it doesn't trigger an email).

    NB. Business process is to only approve the party once the ROI submission has been approved.
    """
    submission_name = 'Registration of Interest'

    caseworker = Caseworker()

    # Caseworker creates ex-officio case
    start_time = datetime.now(timezone.utc)
    case = caseworker.new_ex_officio_case(case_type='Anti-dumping investigation', auto=True, browser=browser)

    # Caseworker initiates the case
    caseworker.tasks.initiation.publish_initiation_notices(
        auto=True,
        case=case,
        browser=browser)

    # Customer creates an account
    customer = Customer(email=EMAIL_ACCOUNT, auto=True, browser=browser)

    # Starts registration of interest
    customer.register_interest.start_registration(case=case, browser=browser)

    # Uploads a document
    customer.register_interest.upload_registration_documents(
        case=case,
        files=[
            os.getcwd() + '/dummy_files/document 1.docx'
        ],
        browser=browser
    )

    # Submits the registration of interest
    emails = get_emails(
        later_than=start_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD,
        delay=5
    )
    if emails:
        pytest.fail(f"Unexpected email(s) received before RoI submitted: {emails}")
    submission_time = datetime.now(timezone.utc)
    customer.register_interest.submit_registration(case=case, browser=browser)

    # 1. Customer gets an email confirmation
    check_for_email(
        later_than=submission_time,
        with_subject='Your submission has been received',
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
            password=EMAIL_PASSWORD
    )

    # Caseworker sees the registration of interest
    customers_awaiting_approval = caseworker.parties.awaiting_approval.get(case=case, browser=browser)
    assert customers_awaiting_approval == {
        customer.company_name: [{'name': customer.name, 'email': customer.email}]}
    submissions_awaiting_approval = caseworker.submissions.awaiting_approval.get(case=case, browser=browser)
    assert submissions_awaiting_approval == [
        {
            'party': customer.company_name,
            'submission': submission_name,
            'status': 'Received',
            'sent': 'n/a',
            'received': date.today().strftime('%d %b %Y'),
            'due': (date.today() + timedelta(days=15)).strftime('%d %b %Y')
        }
    ]

    # Caseworker rejects the registration of interest as deficient
    rejection_time = datetime.now(timezone.utc)
    caseworker.submissions.awaiting_approval.reject(
        browser=browser,
        case=case,
        party=customer.company_name,
        submission_name=submission_name,
        deficiency_documents=[os.getcwd() + '/dummy_files/document 2.docx'],
        deficient_documents=['document 1.docx']
    )

    # 2. Customer receives an email notification
    check_for_email(
        with_subject='Further information required: Deficiency Notice'.format(case),
        later_than=rejection_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )
    last_expected_email_time = datetime.now(timezone.utc)

    # Customer downloads deficiency notices
    customer.respond_to_submission.download_deficiency_notices(
        browser=browser,
        case=case,
        submission=submission_name,
        file_names=['document 2.docx']
    )

    # Customer replaces the deficient documents with new ones
    customer.respond_to_submission.replace_deficient_documents(
        browser=browser,
        case=case,
        submission=submission_name,
        replacement_file_for_deficient_file_name={'document 1.docx': os.getcwd() + '/dummy_files/document 3.docx'}
    )

    # And submits the amended ROI
    emails = get_emails(
        later_than=last_expected_email_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD,
        delay=5
    )
    if emails:
        pytest.fail(f"Unexpected email(s) received before amended RoI submitted: {emails}")
    first_correction_time = datetime.now(timezone.utc)
    customer.register_interest.submit_registration(case=case, browser=browser)

    # 3. Customer gets an email confirmation
    check_for_email(
        later_than=first_correction_time,
        with_subject='Your submission has been received',
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )

    # Caseworker sees updated submission
    submissions_awaiting_approval = caseworker.submissions.awaiting_approval.get(case=case, browser=browser)
    assert submissions_awaiting_approval == [{
        'party': customer.company_name,
        'submission': 'Registration of Interest (version 2)',
        'status': 'Received',
        'sent': 'n/a',
        'received': date.today().strftime('%d %b %Y'),
        'due': (date.today() + timedelta(days=15)).strftime('%d %b %Y')
    }]

    # Caseworker rejects the registration of interest as deficient again
    second_rejection_time = datetime.now(timezone.utc)
    caseworker.submissions.awaiting_approval.reject(
        browser=browser,
        case=case,
        party=customer.company_name,
        submission_name='Registration of Interest (version 2)',
        deficiency_documents=[os.getcwd() + '/dummy_files/document 4.docx'],
        deficient_documents=['document 3.docx']
    )

    # 4. Customer receives a second email notification (same as the first)
    check_for_email(
        with_subject='Further information required: Deficiency Notice'.format(case),
        later_than=second_rejection_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )
    last_expected_email_time = datetime.now(timezone.utc)

    # Customer downloads deficiency notices again
    try:
        customer.respond_to_submission.download_deficiency_notices(
            browser=browser,
            case=case,
            submission=submission_name,
            file_names=['document 4.docx'])
    except NoSuchElementException:
        pytest.xfail('Bug TR-1294')

    # Customer replaces the deficient documents with new ones
    customer.respond_to_submission.replace_deficient_documents(
        browser=browser,
        case=case,
        submission=submission_name,
        replacement_file_for_deficient_file_name={'document 3.docx': os.getcwd() + '/dummy_files/document 5.docx'}
    )

    # And submits the amended ROI
    emails = get_emails(
        later_than=last_expected_email_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD,
        delay=5
    )
    if emails:
        pytest.fail(f"Unexpected email(s) received before amended RoI submitted: {emails}")
    second_correction_time = datetime.now(timezone.utc)
    customer.register_interest.submit_registration(case=case, browser=browser)

    # 5. Customer gets an email confirmation
    check_for_email(
        later_than=second_correction_time,
        with_subject='Your submission has been received',
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )
    last_expected_email_time = datetime.now(timezone.utc)

    # Caseworker approves the corrected registration of interest  - No is email expected to trigger for this
    caseworker.submissions.awaiting_approval.approve(
        browser=browser,
        case=case,
        party=customer.company_name,
        submission_name='Registration of Interest (version 3)'
    )
    emails = get_emails(
        later_than=last_expected_email_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD,
        delay=5
    )
    if emails:
        pytest.fail(f"Unexpected email(s) received after RoI approval: {emails}")

    # Caseworker approves party
    approval_time = datetime.now(timezone.utc)
    caseworker.parties.awaiting_approval.approve(
        browser=browser,
        case=case,
        party=customer.company_name,
        approve_as='Contributor'
    )

    # 6. Customer gets an email confirmation to notify of their successful registration of interest
    check_for_email(
        later_than=approval_time,
        with_subject='Your request to be an interested party in a trade remedies case',
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )

    # Customer sees initiated case
    customer.sign_in(browser=browser)
    dashboard_case_list = browser.find_element_by_class_name('dashboard-case-list')
    dashboard_case_list_links = dashboard_case_list.find_elements_by_tag_name('a')
    assert len(dashboard_case_list_links) == 1
    assert case in dashboard_case_list_links[0].text
    dashboard_case_list_links[0].click()
    highlight_box = browser.find_element_by_class_name('govuk-box-highlight')
    assert 'Case initiated' in highlight_box.text

