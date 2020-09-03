from datetime import date, timedelta
import os

import pytest

from caseworker import Caseworker
from customer import Customer
from constants import CASE_TYPES
from fixtures import factory_reset_before_each_test, browser


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_happy_path(browser, case_type):
    """Happy path for registration of interest & approval"""

    caseworker = Caseworker()

    # Caseworker creates a case
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Caseworker uploads registration of interest documents
    caseworker.upload.upload_case_documents(
        browser=browser,
        case=case,
        files=[
            {'file_path': os.getcwd() + '/dummy_files/document 1.docx', 'confidential': False},  # RoI template
            {'file_path': os.getcwd() + '/dummy_files/document 2.docx', 'confidential': False}  # LoA template
        ],
        submission_type='Registration of Interest',
        description="RoI and LoA templates"
    )

    # Caseworker initiates the case
    caseworker.tasks.initiation.publish_initiation_notices(
        auto=True,
        case=case,
        browser=browser)

    # Customer creates an account
    customer = Customer(auto=True, browser=browser)

    # Starts registration of interest
    customer.register_interest.start_registration(case=case, browser=browser)

    # Downloads registration of interest documents
    customer.register_interest.download_registration_documents(
        case=case,
        browser=browser,
        file_names=['document 1.docx', 'document 2.docx']
    )

    # Fills them out and uploads them
    customer.register_interest.upload_registration_documents(
        case=case,
        files=[
            os.getcwd() + '/dummy_files/document 1.docx',
            os.getcwd() + '/dummy_files/document 2.docx'
        ],
        browser=browser
    )

    # ROI should not be visible to caseworker yet
    customers_awaiting_approval = caseworker.parties.awaiting_approval.get(case=case, browser=browser)
    assert customers_awaiting_approval is None
    submissions_awaiting_approval = caseworker.submissions.awaiting_approval.get(case=case, browser=browser)
    assert submissions_awaiting_approval is None

    # Submits the registration of interest
    customer.register_interest.submit_registration(case=case, browser=browser)

    # Caseworker sees the registration of interest
    submission_name = 'Registration of Interest'
    customers_awaiting_approval = caseworker.parties.awaiting_approval.get(case=case, browser=browser)
    assert customers_awaiting_approval == {customer.company_name: [{'name': customer.name, 'email': customer.email}]}
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

    # Caseworker approves the registration of interest
    caseworker.submissions.awaiting_approval.approve(
        browser=browser,
        case=case,
        party=customer.company_name,
        submission_name=submission_name
    )

    # Customer sees update to registration of interest status
    customer.sign_in(browser=browser)
    dashboard_case_list = browser.find_element_by_class_name('dashboard-case-list')
    case_link = dashboard_case_list.find_element_by_partial_link_text(case)
    case_link.click()
    assert 'This registration of interest was sufficient' in browser.page_source

    # Caseworker approves party
    caseworker.parties.awaiting_approval.approve(
        browser=browser,
        case=case,
        party=customer.company_name,
        approve_as='Contributor'
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
