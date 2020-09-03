import pytest

from customer import Customer
from error_handling import UIErrorMessage
from fixtures import browser, factory_reset_before_test_module
from helpers import fail_fast


@pytest.mark.parametrize(
    "account_details, expected_errors",
    [
        # Test happy paths
        ({'uk_company': True}, None),
        ({'uk_company': False, 'company_country': 'Japan'}, None),
        # Test user details page
        ({'name': None}, ['Name is mandatory']),
        ({'email': None}, ['Email is required']),
        ({'password': None}, ['You must provide a password', 'You must provide a password confirmation']),
        ({'password': 'password'}, ['Password must include both upper and lowercase characters']),  # nb. full password criteria covered by unit tests
        # UK company details page
        ({'company_name': None, 'uk_company': True}, ['Company name is mandatory']),
        # Foreign company details page
        ({'company_name': None, 'uk_company': False}, ['Company name is mandatory']),
        ({'company_country': None, 'uk_company': False}, ['Country is mandatory'])
    ]
)
def test_required_fields(browser, account_details, expected_errors):
    """Test form validation for the customer account creation flow"""
    with fail_fast(browser):
        try:
            # Create account
            customer = Customer(
                **account_details,
                auto=True,
                browser=browser
            )
        except AssertionError:
            if account_details == {'company_country': None, 'uk_company': False}:
                pytest.xfail("Bug TR-1272")
        except UIErrorMessage as error:
            if expected_errors is None:
                raise
            assert error.summary == expected_errors
        else:
            if expected_errors:
                pytest.fail("Account creation succeeded but was expected to fail")

            # Sign in
            customer.sign_in(browser=browser)


def test_create_account_foreign_company(browser):

    customer = Customer(
        uk_company=False,
        company_country='Japan',
        auto=True,
        browser=browser
    )
    customer.sign_in(browser=browser)


def test_create_account_with_existing_email_fails(browser):
    # Create account
    existing_customer = Customer(
        uk_company=True,
        auto=True,
        browser=browser
    )

    # Try to create another account with the same email address but all other details different
    with fail_fast(browser):
        try:
            Customer(
                name=existing_customer.name[::-1],  # Reversed
                email=existing_customer.email,
                password=existing_customer.password[::-1],
                company_name=existing_customer.company_name[::-1],
                company_number=existing_customer.company_number[::-1],
                company_address=existing_customer.company_address[::-1],
                uk_company=False,
                company_country='Japan',
                browser=browser
            )
        except UIErrorMessage as error:
            assert error.summary == ['Email already in use']
        else:
            pytest.fail("It was possible to create two customer accounts using the same email address")


# TODO: Test mismatched password confirm
# TODO: Test duplicate company?
