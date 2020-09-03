import os

import pytest

from caseworker import Caseworker
from customer import Customer
from constants import CASE_TYPES, CUSTOMER_CREATEABLE_CASE_TYPES
from workflows import EXPECTED_WORKFLOWS
from functional_tests.test_tasks.helpers import check_case_summary
from fixtures import browser, factory_reset_before_test_module

# NB. Probably not worth writing more tests here for other cases (eg to cover the publication of every notice type)
# because we decided to prevent going backwards for ALL workflow statuses by default. So if that's been done, you're
# unlikely to find new bugs here, but worth keeping some tests as a check in case that entire mechanism breaks.


@pytest.mark.parametrize('case_type', CUSTOMER_CREATEABLE_CASE_TYPES)
def test_draft_application_received(browser, case_type):

    # Customer creates a new case
    caseworker = Caseworker()
    customer = Customer(auto=True, browser=browser)

    # Customer submits a draft application for review
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
    customer.apply_for_trade_remedy.request_review_of_draft_application(
        browser=browser,
        case=case
    )

    # Check case status
    case_status_before = caseworker.tasks.parse_case_summary(
        browser=browser,
        case=case
    )

    # Check tasks prior to draft review don't trigger status changes
    caseworker.tasks.assign_team(
        browser=browser,
        case=case,
        auto=True
    )

    case_status_after = caseworker.tasks.parse_case_summary(
        browser=browser,
        case=case
    )

    if case_status_after != case_status_before:
        pytest.xfail("TR-1783 - Completing assign team tasks after receipt of draft application caused status widget "
                     f"change from {case_status_before} to {case_status_after}")


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_publish_initiation_notices(browser, case_type):

    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Publish initiation notices
    caseworker.tasks.initiation.publish_initiation_notices(
        auto=True,
        case=case,
        browser=browser
    )
    # Next notice due date varies by case type, but we will check that it doesn't change
    expected_next_notice_due = caseworker.tasks.parse_case_summary(browser, case)['Next notice due']

    def _check_case_summary():
        check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Case initiated',
                'Next action': 'Issue questionnaires',
                'Next notice due': expected_next_notice_due
            },
            fail_on_error=True
        )

    _check_case_summary()

    # Check that previous tasks don't trigger status changes
    caseworker.tasks.assign_team(
        assign_manager=True,
        case=case,
        browser=browser
    )
    _check_case_summary()
    caseworker.tasks.assign_team(
        assign_team_members=True,
        case=case,
        browser=browser
    )
    try:
        _check_case_summary()
    except:
        pytest.xfail("TR-1699 - see comments. Assigning team members replaces next action 'issue questionnaires' with n/a")
    caseworker.tasks.initiation.assessment_of_the_case(
        auto=True,
        case=case,
        browser=browser
    )
    _check_case_summary()
    caseworker.tasks.initiation.initiation_preparation(
        auto=True,
        case=case,
        browser=browser
    )
    _check_case_summary()
    caseworker.tasks.initiation.initiation_decision(
        auto=True,
        case=case,
        browser=browser
    )
    _check_case_summary()


@pytest.mark.skip("Unwritten test")
@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_publish_provisional_determination(browser, case_type):
    raise NotImplementedError()


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_publish_final_determination(browser, case_type):

    expected_workflow = EXPECTED_WORKFLOWS[case_type]

    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Publish final determination notices
    caseworker.tasks.final_determination.publish_final_determination(
        auto=True,
        case=case,
        browser=browser
    )

    def _check_case_summary():
        error = check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Final determination published',
                'Next action': 'Check for reconsideration requests',
                'Next notice due': 'n/a'
            }
        )
        if error:
            pytest.xfail('TR-1699')
            #pytest.fail(error)

    _check_case_summary()

    # Check that previous tasks don't trigger status changes
    caseworker.tasks.assign_team(
        assign_manager=True,
        case=case,
        browser=browser
    )
    _check_case_summary()
    caseworker.tasks.assign_team(
        assign_team_members=True,
        case=case,
        browser=browser
    )
    _check_case_summary()
    caseworker.tasks.initiation.assessment_of_the_case(
        auto=True,
        case=case,
        browser=browser
    )
    _check_case_summary()
    caseworker.tasks.initiation.initiation_preparation(
        auto=True,
        case=case,
        browser=browser
    )
    _check_case_summary()
    caseworker.tasks.initiation.initiation_decision(
        auto=True,
        case=case,
        browser=browser
    )
    _check_case_summary()
    caseworker.tasks.investigation.issue_questionnaires(
        auto=True,
        case=case,
        browser=browser
    )
    _check_case_summary()
    caseworker.tasks.investigation.process_questionnaires(
        auto=True,
        case=case,
        browser=browser
    )
    _check_case_summary()
    if 'Authentication' in expected_workflow['Investigation']:
        caseworker.tasks.investigation.pre_authentication_data_analysis(
            auto=True,
            case=case,
            browser=browser
        )
        _check_case_summary()
        caseworker.tasks.investigation.authentication(
            auto=True,
            case=case,
            browser=browser
        )
        _check_case_summary()
        caseworker.tasks.investigation.post_authentication_analysis(
            auto=True,
            case=case,
            browser=browser
        )
    elif 'Verification' in expected_workflow['Investigation']:
        caseworker.tasks.investigation.pre_verification_data_analysis(
            auto=True,
            case=case,
            browser=browser
        )
        _check_case_summary()
        caseworker.tasks.investigation.verification(
            auto=True,
            case=case,
            browser=browser
        )
        _check_case_summary()
        caseworker.tasks.investigation.post_verification_data_analysis(
            auto=True,
            case=case,
            browser=browser
        )
    else:
        raise ValueError("Expected Authentication or Verification")
    _check_case_summary()
