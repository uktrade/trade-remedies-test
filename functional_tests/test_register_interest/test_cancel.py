import os

import pytest

from caseworker import Caseworker
from customer import Customer
from constants import CASE_TYPES
from fixtures import factory_reset_before_each_test, browser


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_cancel(browser, case_type):

    caseworker = Caseworker()

    # Caseworker creates a case
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Caseworker uploads registration of interest documents
    caseworker.upload.upload_case_documents(
        browser=browser,
        case=case,
        files=[
            {'file_path': os.getcwd() + '/dummy_files/document 1.docx', 'confidential': False}, # RoI template
            {'file_path': os.getcwd() + '/dummy_files/document 2.docx', 'confidential': False}  # LoA template
        ],
        submission_type='Registration of Interest',
        description="RoI & LoA templates"
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

    # Cancels registration of interest
    customer.register_interest.cancel_registration(case=case, browser=browser)
