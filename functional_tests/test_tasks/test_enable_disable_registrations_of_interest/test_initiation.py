import os

import pytest
from selenium.common.exceptions import NoSuchElementException

from constants import CASE_TYPES
from workflows import EXPECTED_WORKFLOWS
from caseworker import Caseworker
from customer import Customer
from fixtures import browser, factory_reset_before_test_module


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_initiation_enables_registrations_of_interest(browser, case_type):
    """It should not be possible to register interest in a case before the case is initiated"""
    caseworker = Caseworker()

    # Caseworker creates ex-officio case
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
    # Caseworker completes all but one of the initiation task groups
    if 'Assessment of the application' in EXPECTED_WORKFLOWS[case_type]['Initiation']:
        caseworker.tasks.initiation.assessment_of_the_application(
            auto=True,
            case=case,
            browser=browser
        )
    elif 'Assessment of the case' in EXPECTED_WORKFLOWS[case_type]['Initiation']:
        caseworker.tasks.initiation.assessment_of_the_case(
            auto=True,
            case=case,
            browser=browser
        )
    else:
        raise ValueError
    caseworker.tasks.initiation.initiation_preparation(
        auto=True,
        case=case,
        browser=browser
    )
    caseworker.tasks.initiation.initiation_decision(
        auto=True,
        case=case,
        browser=browser
    )
    # Don't complete the last task group
    caseworker.tasks.initiation.publish_initiation_notices(
        notice_of_initiation_published=True,  # (Most signifcant task, most likely to falsely trigger ROIs)
        case=case,
        browser=browser
    )

    # Customer creates an account
    customer = Customer(auto=True, browser=browser)

    # Customer should not see the case link when they try to register interest
    try:
        customer.register_interest.start_registration(case=case, browser=browser)
    except NoSuchElementException:
        pass
    else:
        pytest.fail("It was possible to register interest in a case before the case was initiated")
