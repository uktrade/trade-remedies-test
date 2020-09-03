from datetime import datetime, timezone
import os

import pytest

from caseworker import Caseworker
from configuration import EMAIL_ACCOUNT, EMAIL_PASSWORD
from constants import PUBLIC_NOTICE_TYPES
from customer import Customer
from email_client import check_for_email
from functional_tests.helpers import create_new_case_initiate_case_and_register_interest
from fixtures import factory_reset_before_each_test, browser

# TODO: Also test publishing via the 'publish current version' button. Two ways of publishing to public file.


@pytest.mark.parametrize("submission_type", PUBLIC_NOTICE_TYPES)
def test_caseworker_publishes_to_public_file(browser, submission_type):
    """
    TODO: Upgrade this test to check the following:
        Two users with separate accounts have registered interest in the case. Both should get email.
        One user has registered interest in a different case. Should not get an email.
        A multi-user account has registered interest in the case. All users should get email.
    """

    # Customer has registered interest in a case
    caseworker = Caseworker()
    customer = Customer(email=EMAIL_ACCOUNT, auto=True, browser=browser)
    case = create_new_case_initiate_case_and_register_interest(
        browser=browser,
        customer=customer,
        caseworker=caseworker,
        case_type='Transition anti-subsidy review')

    # Caseworker publishes to the public file
    submission_time = datetime.now(timezone.utc)
    caseworker.submissions.publish_documents(
        submission_type=submission_type,
        files=[{'file_path': os.getcwd() + '/dummy_files/document 1.docx', 'confidential': True}],
        name='My Public Submission',
        description='for automated testing',
        case=case,
        browser=browser
    )

    # Customer receives an email notification
    email = check_for_email(
        later_than=submission_time,
        with_subject=f"Update to public file: TS0001 – {case}",
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )
    assert customer.company_name in email.body

    # Customer can view the submission on the public file
    customer.sign_in(browser)
    browser.find_element_by_partial_link_text(case).click()
    tabs = browser.find_elements_by_class_name('tab')
    archived_tab = [tab for tab in tabs if tab.text == 'Public file'][0]
    archived_tab.click()
    browser.find_element_by_link_text(submission_type).click()
    assert 'My Public Submission' in browser.find_element_by_tag_name('h1').text
