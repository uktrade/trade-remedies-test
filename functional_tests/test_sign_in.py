from copy import copy

import pytest
from selenium.common.exceptions import NoSuchElementException

from customer import Customer
from error_handling import UIErrorMessage
from helpers import fail_fast
from fixtures import reset_db_before_test_module, flush_redis_before_each_test, browser
from constants import DASHBOARD_EXPECTED_LINKS


def test_sign_in(browser):
    customer = Customer(auto=True, browser=browser)
    customer.sign_in(browser=browser)

    assert f"This is your dashboard to interact with".lower() in browser.page_source.lower()

    for expected_link in DASHBOARD_EXPECTED_LINKS:
        try:
            browser.find_element_by_link_text(expected_link)
        except NoSuchElementException:
            pytest.fail(f"'{expected_link}' link was missing from dashboard after login")


def test_failed_sign_in_no_credentials(browser):
    """It should not be possible to log in without supplying any credentials"""

    no_credentials_customer = Customer(
        email=None,
        password=None,
        create_account=False,
        browser=browser)

    with fail_fast(browser):
        try:
            no_credentials_customer.sign_in(
                browser=browser
            )
        except UIErrorMessage as error:
            assert error.summary == [
                'You must enter your email address',
                'You must enter your password'
            ]
        else:
            pytest.fail("Expected an error when signing in with no credentials")


def test_failed_sign_in_no_account(browser):
    """It should not be possible to log in without first creating an account"""

    non_existent_customer = Customer(
        email='this_account_doesnt_exist@test.com',
        password='password',
        create_account=False,
        browser=browser)

    with fail_fast(browser):
        try:
            non_existent_customer.sign_in(
                browser=browser
            )
        except UIErrorMessage as error:
            assert error.summary == [
                'You have entered an incorrect email address or password. Please try again or click on the Forgotten '
                'password link below.'
            ]
        else:
            pytest.fail("Expected an error when signing in with a non-existent user account")


def test_failed_sign_in_locked_out(browser):
    """After three failed sign in attempts, a user should be locked out"""
    # TODO: What happens if another user tries to sign in with the same browser?
    # TODO: What happens if you clear your cookies?

    customer = Customer(auto=True, browser=browser)
    hacker = copy(customer)
    hacker.password = 'wrong_password'

    # Fail to log in three times using the wrong password
    with fail_fast(browser):
        for attempt in range(3):
            try:
                hacker.sign_in(
                    browser=browser
                )
            except UIErrorMessage:
                pass
            else:
                pytest.fail("Expected an error when signing in with the wrong password")
        try:
            hacker.sign_in(
                browser=browser
            )
        except UIErrorMessage as error:
            assert error.summary == ['Account locked: too many login attempts. Please try again later']
        else:
            pytest.fail("Expected a lock-out error after fourth failed sign-in attempt")

        # Check that the lock out is enforced
        try:
            customer.sign_in(
                browser=browser
            )
        except UIErrorMessage as error:
            assert error.summary == ['Account locked: too many login attempts. Please try again later']
        else:
            pytest.fail("It was possible to log in immediately after being locked out")


# TODO: Test waiting for lock-out period to expire, then logging in with correct password?
# TODO: Test closing/reopening browser (It should work on IP). Test logging in as different user after lockout.
# TODO: Test caseworker also logged out after public lockout on same IP (but maybe not in test_customer?)
