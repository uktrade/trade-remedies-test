from random import choice, randint

import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select, WebDriverWait

from configuration import CUSTOMER_BASE_URL
from constants import COUNTRIES
from customer.apply_for_trade_remedy import ApplyForTradeRemedy
from customer.register_interest import RegisterInterest
from customer.respond_to_submission import RespondToSubmission
from error_handling import error_handler
from helpers import click_button_with_text
from fixtures import validate_email_address

from time import sleep

from words import words

import logging

logger = logging.getLogger(__name__)


class Customer:

    def __init__(self, browser, auto=False, create_account=True, **account_details):
        """
        Set auto=True to automatically fill out any unspecified fields.
        Override individual fields by specifying a value for the field, or specify None to leave a field untouched.
        """
        # Initialise page objects
        self.apply_for_trade_remedy = ApplyForTradeRemedy(customer=self)
        self.register_interest = RegisterInterest(customer=self)
        self.respond_to_submission = RespondToSubmission(customer=self)

        # Initialise account details
        if auto:
            account_details = self._auto_generate_account_details(**account_details)
        self.__dict__.update(**account_details)

        # Create account
        if create_account:
            self.create_account(browser=browser, **account_details)

    @error_handler
    def create_account(
            self, browser,
            name, email, password, uk_company, company_country,
            company_name, company_number, company_address):

        # Navigate to start page
        browser.get(CUSTOMER_BASE_URL)

        # Log out if necessary
        if 'Logout' in browser.page_source:
            browser.find_element_by_link_text('Logout').click()
            browser.get(CUSTOMER_BASE_URL)

        # Create account
        browser.find_element_by_link_text('Create an account').click()

        browser.find_element_by_id('name').send_keys(name or '')
        browser.find_element_by_id('email').send_keys(email or '')

        # TODO: Remove password_confirm hack and write a test for password confirm mismatch error
        browser.find_element_by_id('password').send_keys(password or '')
        browser.find_element_by_id('password_confirm').send_keys(password or '')

        browser.find_element_by_id('terms').click()
        click_button_with_text(browser, 'Continue')

        # TODO: The account creation flow has changed, there is now a country dropdown for non uk.update this code.
        if uk_company is True:
            logger.debug("uk company")
            browser.find_element_by_id('uk_company-yes').click()
            click_button_with_text(browser, 'Continue')

            browser.find_element_by_id('organisation_name').send_keys(company_name or '')
            browser.find_element_by_id('company_number').send_keys(company_number or '')
            browser.find_element_by_id('full_address').send_keys(company_address or '')

        elif uk_company is False:
            browser.find_element_by_id('uk_company-no').click()
            click_button_with_text(browser, 'Continue')

            browser.find_element_by_id('organisation_name').send_keys(company_name or '')
            browser.find_element_by_name('organisation_address').send_keys(company_address or '')
            if company_country:
                Select(browser.find_element_by_name('organisation_country')).select_by_visible_text(company_country)

        # Default to same registered address as contact address
        browser.find_element_by_id('same_contact_address-yes').click()
        click_button_with_text(browser, 'Continue')

        # TODO: We are skipping over this page as all fields are optional
        browser.find_element_by_id('vat_number')

        click_button_with_text(browser, 'Continue')

        # Check successful account creation
        assert 'Verify your email address' in browser.page_source
        assert 'This browser tab can be closed.' in browser.page_source

        validate_email_address(email)
        # Hacky - but allow the ui to catch up with the db
        sleep(1)

    @error_handler
    def sign_in(self, browser):

        browser.get(CUSTOMER_BASE_URL)

        # cancel and logout appears when the page is waiting for email validation
        if 'Cancel and Logout' in browser.page_source:
            browser.find_element_by_link_text('Cancel and Logout').click()
            browser.get(CUSTOMER_BASE_URL)

        # Log out if necessary
        if 'Logout' in browser.page_source:
            browser.find_element_by_link_text('Logout').click()
            browser.get(CUSTOMER_BASE_URL)

        # Log in
        browser.find_element_by_id('email').send_keys(self.email or '')
        browser.find_element_by_id('password_id').send_keys(self.password or '')
        click_button_with_text(browser, 'Sign in')

        # Check for successful sign in
        browser.find_element_by_link_text("Logout")
        browser.find_element_by_link_text("Account details")

        # Check the dashboard loads after sign in
        assert 'dashboard' in browser.current_url


    @staticmethod
    def _auto_generate_account_details(**kwargs):
        # TODO: Prevent collisions
        class AutoFill:
            pass

        account_details = dict(
            name=kwargs.get('name', f'{choice(words.NAME_WORDS)} {choice(words.NAME_WORDS)}'),
            password=kwargs.get('password', 'MyR3ally$ecurePassw0rd'),
            uk_company=kwargs.get('uk_company', True),
            company_number=kwargs.get('company_number', str(randint(0, 99999999)).zfill(8)),
            company_address=kwargs.get(
                'company_address',
                f'{randint(1, 100)} Great Portland Street, London, W1W 7RT'),
            company_country=kwargs.get('company_country', choice(COUNTRIES)),
            company_name=kwargs.get('company_name', AutoFill),
            email=kwargs.get('email', AutoFill)
        )

        if account_details['company_name'] is AutoFill:
            account_details['company_name'] = choice(words.UPPER_WORDS) + ' Limited'

        if account_details['email'] is AutoFill:
            account_details['email'] = "{}@{}.com".format(
                str(account_details['name']).replace(' ', '_'),
                account_details['company_name']
            ).replace(' Limited', '').lower()

        return account_details
