import pytest
from selenium.common.exceptions import NoSuchElementException

from caseworker import Caseworker
from constants import CASE_TYPES
from workflows import EXPECTED_WORKFLOWS
from fixtures import browser, factory_reset_before_test_module


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_decision_not_to_initiate_forces_case_dismissal_or_application_rejection(browser, case_type):
    """Dismiss case / reject application task is the only way to close case once decision to initiate (NO) is made"""

    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Decide not to initiate the case
    caseworker.tasks.initiation.initiation_decision(
        decide_to_initiate=False,
        case=case,
        browser=browser
    )

    # Check case can't be closed
    try:
        caseworker.tasks.close_case.close_case(browser=browser, case=case, auto=True)
    except NoSuchElementException:
        pass
    else:
        pytest.fail("Close case link should have been disabled after decision not to initiate the case")

    # Check case can't be set in appeal
    try:
        caseworker.tasks.close_case.case_in_appeal(browser=browser, case=case, auto=True)
    except NoSuchElementException:
        pass
    else:
        pytest.fail(
            "Case in appeal link should have been disabled after decision not to initiate the case")

    # Dismiss case / reject application should be the only working option to close the case
    if 'Dismiss case' in EXPECTED_WORKFLOWS[case_type]['Close case']:
        caseworker.tasks.close_case.dismiss_case(browser=browser, case=case, auto=True)
    elif 'Reject application' in EXPECTED_WORKFLOWS[case_type]['Close case']:
        caseworker.tasks.close_case.reject_application(browser=browser, case=case, auto=True)
    else:
        raise ValueError("Expected either 'Dismiss case' or 'Reject application'")


# TODO: Decide what to do with this test:
# @pytest.mark.parametrize('case_type', CASE_TYPES)
# def test_appeals(browser, case_type):
#     """
#     When an investigator marks 'YES' to appeals, the other close case tasks should be disabled.
#     When a request for appeal is granted, case status should update.
#     TODO: Split this test into two?
#     """
#     caseworker = Caseworker()
#     case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)
#     caseworker.tasks.initiation.initiation_decision(
#         auto=True,
#         case=case,
#         browser=browser
#     )
#     caseworker.tasks.transition_safeguarding_review.reconsideration.appeals(
#         appeal_request_received=True,  # TODO: Suspicious - are there missing tasks here?
#         case=case,
#         browser=browser
#     )
#     check_task_statuses(
#         statuses_to_check={'Appeals': 'completed'},
#         caseworker=caseworker,
#         case=case,
#         browser=browser
#     )
#
#     # Check case can't be dismissed
#     try:
#         caseworker.tasks.close_case.dismiss_case(browser=browser, case=case, auto=True)
#     except NoSuchElementException:
#         pass
#     else:
#         pytest.fail("Dismiss case link should have been disabled after appeal request received")
#
#     # Check case can't be closed
#     try:
#         caseworker.tasks.close_case.close_case(browser=browser, case=case, auto=True)
#     except NoSuchElementException:
#         pass
#     else:
#         pytest.fail("Close case link should have been disabled after appeal request received")
#
#     # Case in appeal should be the only working option to close the case
#     caseworker.tasks.close_case.case_in_appeal(
#         request_for_appeal_granted=True,
#         case=case,
#         browser=browser)
#
#     # Request for appeal granted = Yes should update the case status
#     error = check_case_summary(
#         browser=browser,
#         caseworker=caseworker,
#         case=case,
#         expected_case_summary={
#             'Current stage': 'Case in appeal',
#             'Next action': 'Await outcomes',
#             'Next notice due': 'n/a'
#         }
#     )
#     if error:
#         pytest.fail(error)
