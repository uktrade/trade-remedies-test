from datetime import date, timedelta
import os


def create_new_case_initiate_case_and_register_interest(browser, caseworker, customer, case_type):

    # Caseworker creates ex-officio case
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Caseworker initiates the case
    caseworker.tasks.initiation.publish_initiation_notices(
        auto=True,
        case=case,
        browser=browser)

    # Customer registers interest
    customer.register_interest.start_registration(case=case, browser=browser)
    customer.register_interest.upload_registration_documents(
        case=case,
        files=[
            os.getcwd() + '/dummy_files/document 1.docx'
        ],
        browser=browser
    )

    # Submits the registration of interest
    customer.register_interest.submit_registration(case=case, browser=browser)

    # Caseworker sees the registration of interest
    customers_awaiting_approval = caseworker.parties.awaiting_approval.get(case=case, browser=browser)
    assert customers_awaiting_approval == {
        customer.company_name: [{'name': customer.name, 'email': customer.email}]}
    submissions_awaiting_approval = caseworker.submissions.awaiting_approval.get(case=case, browser=browser)
    assert submissions_awaiting_approval == [
        {
            'party': customer.company_name,
            'submission': 'Registration of Interest',
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
        submission_name='Registration of Interest'
    )

    # Caseworker approves party
    caseworker.parties.awaiting_approval.approve(
        browser=browser,
        case=case,
        party=customer.company_name,
        approve_as='Contributor'
    )

    # Customer sees the case on their dashboard and its initiated status
    customer.sign_in(browser=browser)
    dashboard_case_list = browser.find_element_by_class_name('dashboard-case-list')
    dashboard_case_list_links = dashboard_case_list.find_elements_by_tag_name('a')
    assert len(dashboard_case_list_links) == 1
    assert case in dashboard_case_list_links[0].text
    dashboard_case_list_links[0].click()
    highlight_box = browser.find_element_by_class_name('govuk-box-highlight')
    assert 'Case initiated' in highlight_box.text

    return case
