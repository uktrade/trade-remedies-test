import pytest

from caseworker import Caseworker
from constants import CASE_TYPES
from workflows import EXPECTED_WORKFLOWS
from functional_tests.test_tasks.helpers import check_task_statuses, check_case_is_archived
from fixtures import browser, factory_reset_before_test_module


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_task_group_status_close_case(browser, case_type):
    """Close case task group should show COMPLETED if any of the close case tasks is COMPLETED"""

    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Initiate and close the case
    caseworker.tasks.initiation.initiation_decision(
        auto=True,
        case=case,
        browser=browser
    )
    caseworker.tasks.close_case.close_case(
        auto=True,
        case=case,
        browser=browser
    )

    check_task_statuses(
        statuses_to_check={
            'Close case': ['completed', 'completed']
        },
        caseworker=caseworker,
        case=case,
        browser=browser
    )

    check_case_is_archived(caseworker=caseworker, case_name=case, browser=browser)


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_task_group_status_dismiss_case_or_reject_application(browser, case_type):

    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Dismiss case / reject application
    caseworker.tasks.initiation.initiation_decision(
        decide_to_initiate=False,
        case=case,
        browser=browser
    )
    if 'Dismiss case' in EXPECTED_WORKFLOWS[case_type]['Close case']:
        caseworker.tasks.close_case.dismiss_case(
            auto=True,
            case=case,
            browser=browser
        )
        check_task_statuses(
            statuses_to_check={
                'Close case': ['completed', None],
                'Dismiss case': 'completed'
            },
            caseworker=caseworker,
            case=case,
            browser=browser
        )
    elif 'Reject application' in EXPECTED_WORKFLOWS[case_type]['Close case']:
        caseworker.tasks.close_case.reject_application(
            auto=True,
            case=case,
            browser=browser
        )
        check_task_statuses(
            statuses_to_check={
                'Close case': ['completed', None],
                'Reject application': 'completed'
            },
            caseworker=caseworker,
            case=case,
            browser=browser
        )
    else:
        raise ValueError("Expected either 'Dismiss case' or 'Reject application'")

    check_case_is_archived(caseworker=caseworker, case_name=case, browser=browser)


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_task_group_status_case_in_appeal(browser, case_type):

    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Initiate and set the case in appeal
    caseworker.tasks.initiation.initiation_decision(
        auto=True,
        case=case,
        browser=browser
    )
    caseworker.tasks.close_case.case_in_appeal(
        auto=True,
        case=case,
        browser=browser
    )

    check_task_statuses(
        statuses_to_check={
            'Close case': ['completed', None],
            'Case in appeal': 'completed'
        },
        caseworker=caseworker,
        case=case,
        browser=browser
    )

    check_case_is_archived(caseworker=caseworker, case_name=case, browser=browser)
