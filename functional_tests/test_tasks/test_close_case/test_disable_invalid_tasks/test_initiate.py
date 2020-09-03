import pytest
from selenium.common.exceptions import NoSuchElementException

from caseworker import Caseworker
from constants import CASE_TYPES
from workflows import EXPECTED_WORKFLOWS
from fixtures import browser, factory_reset_before_test_module


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_decision_to_initiate_prevents_case_dismissal_or_application_rejection(browser, case_type):
    """Dismiss case / reject application task cannot be interacted with once decision to initiate (YES) is made"""

    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Initiate the case
    caseworker.tasks.initiation.initiation_decision(
        auto=True,
        case=case,
        browser=browser
    )

    # Check case can't be dismissed / application rejected
    try:
        if 'Dismiss case' in EXPECTED_WORKFLOWS[case_type]['Close case']:
            caseworker.tasks.close_case.dismiss_case(browser=browser, case=case, auto=True)
        elif 'Reject application' in EXPECTED_WORKFLOWS[case_type]['Close case']:
            caseworker.tasks.close_case.reject_application(browser=browser, case=case, auto=True)
        else:
            raise ValueError("Expected either 'Dismiss case' or 'Reject application'")
    except NoSuchElementException:
        pass  # Dismiss case / reject application link is disabled
    else:
        pytest.fail("It was possible to dismiss the case / reject the application after initiation decision was made")
