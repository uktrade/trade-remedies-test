import pytest

from caseworker import Caseworker
from constants import CASE_TYPES, CASE_TYPE_PREFIXES
from functional_tests.test_tasks.helpers import get_case_number_for_case_name
from fixtures import browser, factory_reset_before_each_test


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_case_reference_changes_on_decision_to_initiate(browser, case_type):
    """
    When the decision to initiate is made, a case reference ID should be set (2 letter case type abbreviation
    plus 4 digit number)
    """

    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)
    case_number = get_case_number_for_case_name(browser=browser, caseworker=caseworker, case_name=case)
    assert case_number == '0001'

    caseworker.tasks.initiation.initiation_decision(
        decide_to_initiate=True,
        case=case,
        browser=browser
    )

    case_number = get_case_number_for_case_name(browser=browser, caseworker=caseworker, case_name=case)
    assert case_number == CASE_TYPE_PREFIXES[case_type] + '0001'


@pytest.mark.parametrize('case_type', CASE_TYPES)
def _test_case_reference_doesnt_change_on_decision_not_to_initiate(browser, case_type):
    """
    When the decision not to initiate is made, a case reference ID should not be set
    """

    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)
    case_number = get_case_number_for_case_name(browser=browser, caseworker=caseworker, case_name=case)
    assert case_number == '0001'

    caseworker.tasks.initiation.initiation_decision(
        decide_to_initiate=False,
        case=case,
        browser=browser
    )

    case_number = get_case_number_for_case_name(browser=browser, caseworker=caseworker, case_name=case)
    assert case_number == '0001'
