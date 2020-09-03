from caseworker import Caseworker
from functional_tests.test_tasks.helpers import get_case_number_for_case_name
from fixtures import browser, factory_reset_before_each_test


def test_case_reference_index_generation_order(browser):
    """
    When the decision to initiate is made, a case reference ID should be set with number 1 greater than the
    case reference ID of the previously initiated case (regardless of case type).
    """

    # Decide to initiate cases of different types in a different order to when they were created
    caseworker = Caseworker()
    case_1_name = caseworker.new_ex_officio_case(case_type='Transition safeguarding review', auto=True, browser=browser)
    case_1_number = get_case_number_for_case_name(browser=browser, caseworker=caseworker, case_name=case_1_name)
    assert case_1_number == '0001'
    case_2_name = caseworker.new_ex_officio_case(case_type='Anti-dumping investigation', auto=True, browser=browser)
    case_2_number = get_case_number_for_case_name(browser=browser, caseworker=caseworker, case_name=case_2_name)
    assert case_2_number == '0002'
    case_3_name = caseworker.new_ex_officio_case(case_type='Transition anti-subsidy review', auto=True, browser=browser)
    case_3_number = get_case_number_for_case_name(browser=browser, caseworker=caseworker, case_name=case_3_name)
    assert case_3_number == '0003'
    caseworker.tasks.transition_safeguarding_review.initiation.initiation_decision(
        decide_to_initiate=True,
        case=case_1_name,
        browser=browser
    )
    caseworker.tasks.transition_anti_subsidy_review.initiation.initiation_decision(
        decide_to_initiate=True,
        case=case_3_name,
        browser=browser
    )
    caseworker.tasks.anti_dumping_investigation.initiation.initiation_decision(
        decide_to_initiate=True,
        case=case_2_name,
        browser=browser
    )

    # Check case numbers are set as expected
    case_1_number = get_case_number_for_case_name(browser=browser, caseworker=caseworker, case_name=case_1_name)
    case_2_number = get_case_number_for_case_name(browser=browser, caseworker=caseworker, case_name=case_2_name)
    case_3_number = get_case_number_for_case_name(browser=browser, caseworker=caseworker, case_name=case_3_name)

    assert case_1_number == 'TF0001'
    assert case_3_number == 'TS0002'
    assert case_2_number == 'AD0003'

