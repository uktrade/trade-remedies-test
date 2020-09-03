from random import choice
from time import sleep

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.webdriver.support.ui import Select
from selenium.common.exceptions import NoSuchElementException

from configuration import CASEWORKER_BASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD, EXPLICIT_WAIT_SECONDS
from constants import COUNTRIES
from caseworker.upload import Upload
from caseworker.tasks import Tasks
from caseworker.parties import Parties
from caseworker.submissions import Submissions
from caseworker.users import Users
from error_handling import error_handler
from helpers import parse_table, input_hs_codes, click_button_with_text
from words import words


class Caseworker:

    def __init__(self, email=ADMIN_EMAIL, password=ADMIN_PASSWORD):
        self.upload = Upload(caseworker=self)
        self.tasks = Tasks(caseworker=self)
        self.parties = Parties(caseworker=self)
        self.submissions = Submissions(caseworker=self)
        self.users = Users(caseworker=self)
        self.email = email
        self.password = password

    @error_handler
    def sign_in(self, browser):
        browser.get(CASEWORKER_BASE_URL)

        # Log out if necessary
        try:
            browser.find_element_by_link_text('Log out').click()
        except NoSuchElementException:
            pass

        # Log in as caseworker
        email_field = browser.find_element_by_id('email')
        password_field = browser.find_element_by_id('password')
        email_field.send_keys(self.email or '')
        password_field.send_keys(self.password or '')
        click_button_with_text(browser, 'Log in')

    def get_cases(self, browser):
        cases = {}
        self.sign_in(browser=browser)
        table_element = browser.find_element_by_class_name('cases')
        cases['current'] = parse_table(browser=browser, table_element=table_element)
        tabs = browser.find_elements_by_class_name('tab')
        archived_tab = [tab for tab in tabs if tab.text == 'Archived'][0]
        archived_tab.click()
        table_element = browser.find_element_by_class_name('cases')
        cases['archived'] = parse_table(browser=browser, table_element=table_element)
        return cases

    @error_handler
    def new_ex_officio_case(self, browser, case_type, auto=False, **case_details):
        """Create a new ex-officio case"""
        if auto:
            case_details = self._auto_generate_ex_officio_case_details(**case_details)

        return self._new_ex_officio_case(browser=browser, case_type=case_type, **case_details)

    def _new_ex_officio_case(
            self, browser, case_type, case_name, company, product_sector, product_classification_codes,
            product_name, product_description, sources_of_exports):

        # Navigate to new case flow
        self.sign_in(browser=browser)
        browser.find_element_by_link_text('New ex-officio case').click()

        # Fill form
        if case_type:
            Select(browser.find_element_by_id('case_type')).select_by_visible_text(case_type)
        browser.find_element_by_id('case_name').send_keys(case_name or '')
        if company:
            Select(browser.find_element_by_name('organisation_id')).select_by_visible_text(company)
        if product_sector:
            Select(browser.find_element_by_id('product_sector')).select_by_visible_text(product_sector)

        input_hs_codes(browser, hs_codes=product_classification_codes)

        browser.find_element_by_id('product_name').send_keys(product_name or '')
        browser.find_element_by_id('product_description').send_keys(product_description or '')
        for source_of_exports in sources_of_exports or []:
            # Export country dropdown
            source_dropdown = Select(browser.find_elements_by_name('export_country_code')[-1])
            source_dropdown.select_by_visible_text(source_of_exports)
            click_button_with_text(browser, 'Add')
            # Check source has been added to list of sources
            WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
                ec.text_to_be_present_in_element(locator=(By.TAG_NAME, 'ul'), text_=source_of_exports))

        click_button_with_text(browser, 'Create case')

        # Check case was created
        if case_name:
            expected_case_name = case_name
        else:
            # System is expected to generate a case name automatically
            if sources_of_exports:
                expected_case_name = '{} from {}'.format(product_name or '', sources_of_exports[0] if sources_of_exports else '')
            else:
                expected_case_name = product_name

        try:
            browser.find_element_by_link_text(expected_case_name)
        except NoSuchElementException:
            if 'safeguard' in case_type.lower():
                pytest.xfail("TR-1717, ex-officio safeguard cases not appearing on dashboard")
            else:
                raise

        return expected_case_name

    @staticmethod
    def _auto_generate_ex_officio_case_details(**kwargs):
        # TODO: Prevent collisions
        case_details = dict(
            case_name=kwargs.get('case_name', ''),  # Field is not mandatory
            company=kwargs.get('company', 'Secretary of State'),
            product_sector=kwargs.get('product_sector', '2: Vegetable products'),
            product_classification_codes=kwargs.get('product_classification_codes', ['000000', '000001']),
            product_name=kwargs.get('product_name', choice(words.LOWER_WORDS).title()),
            product_description=kwargs.get('product_description', 'a descriptive description'),
            sources_of_exports=kwargs.get('sources_of_exports', [choice(COUNTRIES), choice(COUNTRIES)])
        )
        return case_details

    @error_handler
    def assign_team_members(self, browser, case, caseworker):
        dashboard_assign_team_members_link_text = 'Edit'
        self.sign_in(browser)
        browser.find_element_by_partial_link_text(case).click()

        # Workaround for connection aborted
        browser.find_element_by_link_text(dashboard_assign_team_members_link_text).click()
        while 'Assign  team  members' not in browser.page_source:
            sleep(2)
            browser.refresh()

        labels = browser.find_elements_by_tag_name('label')
        for label in labels:
            if caseworker.email in label.text:
                label.click()
                break
        else:
            raise ValueError(f"Couldn't find label for team member with email {caseworker.email}")

        click_button_with_text(browser, 'Assign')

        # Check we're back on the dashboard
        browser.find_element_by_link_text(dashboard_assign_team_members_link_text)
