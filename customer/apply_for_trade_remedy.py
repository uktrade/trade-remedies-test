from random import choice, randint
from time import sleep

from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from helpers import input_hs_codes, click_button_with_text
from constants import INDUSTRY_SECTORS, COUNTRIES
from configuration import EXPLICIT_WAIT_SECONDS
from customer.base import Flow
from error_handling import error_handler
from words import words


class ApplyForTradeRemedy(Flow):

    def _go_to_case(self, browser, case):
        super()._go_to_case(browser=browser, case=case)
        browser.find_element_by_link_text('Application').click()

    def cancel_application(self, browser, case):
        self._go_to_case(browser=browser, case=case)
        sleep(3)  # Wait for JS to load, otherwise the overlay confirmation gets bypassed
        click_button_with_text(browser, button_text='Cancel application')
        overlay = WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(ec.visibility_of_element_located((By.CLASS_NAME, 'overlay')))
        click_button_with_text(overlay, button_text='Yes')

        # Check we're on dashboard
        assert browser.find_element_by_class_name('box-alert').text == 'Your submission has been cancelled'
        assert 'Welcome' in browser.page_source
        assert 'Your cases' in browser.page_source

    @error_handler
    def create_case(self, browser, auto=False, **case_details):
        """Create a new case"""
        if auto:
            case_details = self._auto_generate_case_details(**case_details)

        return self._create_case(browser=browser, **case_details)

    def _create_case(self, browser, product_name, sector, commodity_codes, source_of_exports, case_type):

        self.customer.sign_in(browser=browser)
        browser.find_element_by_link_text('Apply for a new investigation').click()

        browser.find_element_by_link_text('Company Information').click()
        # TODO: Don't just accept the defaults
        click_button_with_text(browser, 'Save and continue')

        browser.find_element_by_link_text('About the product').click()
        browser.find_element_by_name('product_name').send_keys(product_name or '')
        Select(browser.find_element_by_name('sector')).select_by_visible_text(sector)
        # browser.find_element_by_name('description').send_keys(description, '')
        input_hs_codes(browser, commodity_codes)
        click_button_with_text(browser, 'Save and continue')

        browser.find_element_by_link_text('Source of the exports').click()
        Select(browser.find_element_by_id('country-1')).select_by_visible_text(source_of_exports)  # Only one originating country
        if case_type == 'Anti-dumping investigation':
            browser.find_element_by_id('evidence_of_subsidy_no').click()
        elif case_type == 'Anti-subsidy investigation':
            browser.find_element_by_id('evidence_of_subsidy_yes').click()
        else:
            raise ValueError(f"Unhandled case type {case_type}")
        click_button_with_text(browser, 'Save and continue')

        case_name = browser.find_element_by_class_name('heading-medium').text.split('\n')[-1]

        return case_name

    @error_handler
    def download_application_forms(self, browser, case, file_names):
        self._go_to_case(
            case=case,
            browser=browser
        )
        browser.find_element_by_link_text('Download application forms').click()
        self._download_documents(
            browser=browser,
            file_names=file_names
        )

    @error_handler
    def upload_documents(self, browser, case, files):
        self._go_to_case(browser, case)
        browser.find_element_by_link_text('Upload your documents').click()
        self._upload_documents_one_by_one(
            browser=browser,
            files=files
        )
        # TODO: Check it worked

    @error_handler
    def upload_documents_for_public_file(self, browser, case, files):
        self._go_to_case(browser, case)
        browser.find_element_by_link_text('Upload your documents for the public file').click()
        self._upload_public_versions_of_confidential_documents(
            browser=browser,
            files=files
        )
        # TODO: Check it worked

    @error_handler
    def request_review_of_draft_application(self, browser, case):
        self._go_to_case(browser, case)
        browser.find_element_by_link_text('Request a review of your draft application').click()
        browser.find_element_by_id('terms').click()
        click_button_with_text(browser, 'Submit')

        # TODO: Check it worked. We should see the case on the dashboard under 'Your applications'. NOT 'Your cases'.

    @error_handler
    def check_application(self, browser, case):
        self._go_to_case(browser, case)
        browser.find_element_by_link_text('Check your application').click()
        browser.find_element_by_name('documents_reviewed').click()
        click_button_with_text(browser, 'Save and continue')
        # TODO: Check it worked

    @error_handler
    def submit_application(self, browser, case):
        self._go_to_case(browser, case)
        browser.find_element_by_link_text('Submit your application').click()
        browser.find_elements_by_name('non_conf')[-1].click()
        browser.find_elements_by_name('confirm')[-1].click()
        click_button_with_text(browser, 'Submit')
        # TODO: Check it worked

    @staticmethod
    def _auto_generate_case_details(**kwargs):
        # TODO: Prevent collisions
        case_details = dict(
            product_name=kwargs.get('product_name', choice(words.LOWER_WORDS).title()),
            sector=kwargs.get('sector', choice(INDUSTRY_SECTORS)),
            commodity_codes=kwargs.get('commodity_codes', [str(randint(0,999999)).zfill(6), str(randint(0,999999)).zfill(6)]),
            source_of_exports=kwargs.get('source_of_exports', choice(COUNTRIES)),
            case_type='Anti-dumping investigation'
        )
        return case_details
