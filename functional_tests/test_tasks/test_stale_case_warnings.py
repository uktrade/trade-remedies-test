"""
Test that a caseworker is prompted to contact the applicant when the applicant has left a case dormant for 6 months
"""
import pytest

from caseworker import Caseworker
from customer import Customer
from functional_tests.test_tasks.helpers import check_case_summary


@pytest.mark.skip("Unfinished test")
def _test_stale_case_warning_no_submission(browser):
    """
    When a customer creates a case but doesn't submit anything for 6 months, caseworker should see a warning to
    contact the applicant
    """

    # Customer creates a case
    customer = Customer(browser=browser, auto=True)
    case = customer.apply_for_trade_remedy.create_case(browser=browser, auto=True)

    # Customer does not submit either a draft or a full application within 6 months
    raise NotImplemented

    # Caseworker should be warned
    caseworker = Caseworker()
    check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Next action': 'Contact applicant'
        }
    )

    # TODO: Check next action on the table of cases (caseworker landing page)


@pytest.mark.skip("Unfinished test")
def _test_stale_case_warning_draft_deficient(browser):
    """
    When a caseworker reviews a draft as deficient but the customer does not respond within 6 months, caseworker should
    see a warning to contact the applicant
    """

    # Customer creates a case
    customer = Customer(browser=browser, auto=True)
    case = customer.apply_for_trade_remedy.create_case(browser=browser, auto=True)

    # Customer submits a draft for review
    raise NotImplemented

    # Caseworker responds to review (deficient)
    raise NotImplemented

    # Customer does not submit either a draft or a full application within 6 months
    raise NotImplemented

    # Caseworker should be warned
    caseworker = Caseworker()
    check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Next action': 'Contact applicant'
        }
    )


@pytest.mark.skip("Unfinished test")
def _test_stale_case_warning_draft_good(browser):
    """
    When a caseworker reviews a draft as good but the customer does not respond within 6 months, caseworker should see
    a warning to contact the applicant
    """

    # Customer creates a case
    customer = Customer(browser=browser, auto=True)
    case = customer.apply_for_trade_remedy.create_case(browser=browser, auto=True)

    # Customer submits a draft for review
    raise NotImplemented

    # Caseworker responds to review (good)
    raise NotImplemented

    # Customer does not submit a full application within 6 months
    raise NotImplemented

    # Caseworker should be warned
    caseworker = Caseworker()
    check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Next action': 'Contact applicant'
        }
    )
