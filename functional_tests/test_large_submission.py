from itertools import cycle
import os

from caseworker import Caseworker
from customer import Customer
from fixtures import factory_reset_before_each_test, browser

NUM_DOCUMENTS_TO_UPLOAD = 100


def test_large_submission(browser):
    """Upload a large number of documents in response to a questionnaire"""

    # Caseworker initiates a case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type='Anti-dumping investigation', browser=browser, auto=True)
    caseworker.upload.upload_case_documents(
        browser=browser,
        case=case,
        files=[{'file_path': os.getcwd() + '/dummy_files/document 1.docx', 'confidential': False}],  # RoI template
        submission_type='Registration of Interest',
        description="RoI template"
    )
    caseworker.tasks.initiation.publish_initiation_notices(
        auto=True,
        case=case,
        browser=browser)

    # Domestic producer registers interest in the case
    customer = Customer(auto=True, browser=browser)
    customer.register_interest.start_registration(case=case, browser=browser)
    customer.register_interest.download_registration_documents(
        case=case,
        browser=browser,
        file_names=['document 1.docx']
    )
    customer.register_interest.upload_registration_documents(
        case=case,
        files=[os.getcwd() + '/dummy_files/document 2.docx'],
        browser=browser
    )
    customer.register_interest.submit_registration(case=case, browser=browser)

    # Caseworker approves ROI and party
    caseworker.submissions.awaiting_approval.approve(
        browser=browser,
        case=case,
        party=customer.company_name,
        submission_name='Registration of Interest'
    )
    caseworker.parties.awaiting_approval.approve(
        browser=browser,
        case=case,
        party=customer.company_name,
        approve_as='Domestic Producer'
    )

    # Caseworker submits a questionnaire
    submission = caseworker.submissions.domestic_producer.request_information(
        browser=browser,
        case=case,
        party=customer.company_name,
        submission_type='Questionnaire',
        files=[{
            'file_path': os.getcwd() + '/dummy_files/document 3.docx',
            'confidential': True
        }],
        name='Questionnaire',
        description='Respond with lots of documents please'
    )

    # Customer responds to questionnaire
    customer.respond_to_submission.download_submission(
        browser=browser, case=case, submission=submission, file_names=['document 3.docx'])
    dummy_documents_cycle = cycle([
        os.getcwd() + '/dummy_files/document 4.docx',
        os.getcwd() + '/dummy_files/document 5.docx',
        os.getcwd() + '/dummy_files/document 6.docx',
        os.getcwd() + '/dummy_files/document 7.docx',
        os.getcwd() + '/dummy_files/document 8.docx',
        os.getcwd() + '/dummy_files/document 9.docx'
    ])

    documents_to_upload = [next(dummy_documents_cycle) for _ in range(int(NUM_DOCUMENTS_TO_UPLOAD))]
    customer.respond_to_submission.upload_response(
        browser=browser, case=case,  submission=submission, files=documents_to_upload)
    customer.respond_to_submission.upload_non_confidential_response(
        browser=browser, case=case,  submission=submission, files=documents_to_upload)
    customer.respond_to_submission.final_check(browser=browser, submission=submission, case=case)
    customer.respond_to_submission.submit(browser=browser, submission=submission, case=case)
