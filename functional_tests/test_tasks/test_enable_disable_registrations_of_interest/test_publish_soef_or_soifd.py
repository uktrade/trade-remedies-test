import pytest
from selenium.common.exceptions import NoSuchElementException

from admin import Admin
from constants import CASE_TYPES
from workflows import EXPECTED_WORKFLOWS
from caseworker import Caseworker
from customer import Customer
from fixtures import browser, factory_reset_before_test_module


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_publish_soef_or_soifd_disables_registrations_of_interest_after_time_window(browser, case_type):

    # TODO: Check if these time windows are what Jo actually intended
    if 'transition safeguarding' in case_type.lower():
        window_days = 30
    elif 'transition' in case_type.lower() or 'safeguard' in case_type.lower():
        window_days = 15
    else:
        window_days = 10

    # Caseworker creates a case and initiates it
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)
    caseworker.tasks.initiation.publish_initiation_notices(
        auto=True,
        case=case,
        browser=browser)

    # Caseworker publishes the SoEF / SoIFD
    if 'The Statement of Essential Facts' in EXPECTED_WORKFLOWS[case_type]:
        caseworker.tasks.statement_of_essential_facts.statement_of_essential_facts(
            auto=True,
            case=case,
            browser=browser
        )
    elif 'Statement of Intended Final Determination' in EXPECTED_WORKFLOWS[case_type]:
        caseworker.tasks.statement_of_intended_final_determination.publish_soifd(
            auto=True,
            case=case,
            browser=browser
        )
    elif 'Statement of Intended Final Determination' in EXPECTED_WORKFLOWS[case_type]['Decisions and Reasons']:
        caseworker.tasks.decisions_and_reasons.statement_of_intended_final_determination(
            auto=True,
            case=case,
            browser=browser
        )
    else:
        raise ValueError

    # Check customers can still register interest
    customer_1 = Customer(auto=True, browser=browser)
    customer_1.register_interest.start_registration(case=case, browser=browser)

    # One day away from end of time window
    admin = Admin()
    admin.simulate_passage_of_time(browser=browser, case=case, days=window_days-1)
    
    # Check customers can still register interest
    customer_2 = Customer(auto=True, browser=browser)
    customer_2.register_interest.start_registration(case=case, browser=browser)

    # End of time window
    admin.simulate_passage_of_time(browser=browser, case=case, days=1)

    # Check customers can't register interest any more
    customer_3 = Customer(auto=True, browser=browser)
    try:
        customer_3.register_interest.start_registration(case=case, browser=browser)
    except NoSuchElementException:
        # Case is not displayed as an option when registering interest
        pass
    else:
        pytest.fail(
            "Customer was able to register interest in case {} days after SoEF/SoIFD published".format(window_days))

    # TODO: What happens to customer 1, who was part way through ROI when window closed?
