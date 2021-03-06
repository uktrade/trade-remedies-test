from selenium.common.exceptions import NoSuchElementException
import pytest

from caseworker import Caseworker
from error_handling import UIErrorMessage
from fixtures import browser, factory_reset_before_test_module


@pytest.mark.parametrize("case_details, expected_errors", [
    ({'case_type': 'Please select ...'}, ['Case type is required']),
    ({'product_sector': None}, ['Product sector is required']),
    ({'product_name': None}, ['Product name is required']),
    ({'product_classification_codes': None}, ['Product code is required']),
    ({'product_description': None}, ['Product description is required']),
    ({'sources_of_exports': None}, ['Export country is required']),
    # When you only supply the mandatory fields, expect no errors
    ({
        'product_sector': '11: Textiles',
        'product_name': 'Crew-neck Sweater',
        'product_classification_codes': ['000001'],
        'product_description': 'Melange Sweater',
        'sources_of_exports': ['Netherlands'],
        'case_type': 'Anti-dumping investigation',
        'company': None,  # Accept the default
        'case_name': None  # Case name should be generated by the system
    }, None),
    #   Source of exports should not be required for safeguarding cases
    ({'case_type': 'Safeguard discontinuation', 'sources_of_exports': None}, None),
    ({'case_type': 'Safeguard extension review', 'sources_of_exports': None}, None),
    ({'case_type': 'Safeguard mid-term review', 'sources_of_exports': None}, None),
    ({'case_type': 'Safeguard suspension review', 'sources_of_exports': None}, None),
    ({'case_type': 'Transition safeguarding review', 'sources_of_exports': None}, None),
])
def test_required_fields(browser, case_details, expected_errors):
    caseworker = Caseworker()
    if 'case_type' not in case_details:
        case_details['case_type'] = 'Anti-dumping investigation'
    try:
        caseworker.new_ex_officio_case(
            **case_details,
            auto=True,
            browser=browser
        )
    except NoSuchElementException:
        if case_details == {'product_name': None}:
            pytest.xfail("Bug TR-1238")
        else:
            raise
    except UIErrorMessage as error:
        if expected_errors is None:
            raise
        assert error.summary == expected_errors


def test_case_name(browser):
    """The system shouldn't automatically generate a case name when one is provided by a caseworker"""
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(
        case_name="Custom case name",
        case_type='Anti-dumping investigation',
        auto=True,
        browser=browser
    )
    assert case == "Custom case name"
