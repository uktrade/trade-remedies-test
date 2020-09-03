import pytest
from selenium.common.exceptions import NoSuchElementException

from customer.base import Flow
from error_handling import error_handler
from helpers import click_button_with_text


class RegisterInterest(Flow):

    @error_handler
    def start_registration(self, browser, case, own_company=True):
        # Navigate to register interest flow
        self.customer.sign_in(browser=browser)
        browser.find_element_by_link_text('Register interest in a case').click()

        # Select case
        browser.find_element_by_link_text('Select case').click()
        browser.find_element_by_partial_link_text(case).click()

        # Submit company information
        browser.find_element_by_link_text('Company information').click()
        if own_company:
            company_name = self.customer.company_name
            click_button_with_text(browser, 'Save and continue')  # Accept defaults (UK company, own company)
        else:
            company_name = 'The Company I Represent Limited'
            other_company = [i for i in browser.find_elements_by_name('representing') if
                             i.get_attribute('value') == 'other'].pop()
            other_company.click()
            browser.find_element_by_id('organisation_name').send_keys(company_name)
            browser.find_element_by_id('company_number').send_keys('000000')
            browser.find_element_by_id('address_snippet').send_keys('123 Street')
            click_button_with_text(browser, 'Save and continue')

        # Check company information is displayed
        organisation_block = browser.find_element_by_class_name('organisation-block')
        assert f"You are currently representing {company_name}".lower() in organisation_block.text.lower()

        # Confirm registration of interest is visible on dashboard
        browser.find_element_by_link_text('Back to dashboard').click()
        registrations_of_interest_div = browser.find_element_by_class_name('margin-top-2')
        assert 'Your draft registrations of interest' in registrations_of_interest_div.text
        case_list = registrations_of_interest_div.find_element_by_class_name('dashboard-case-list')
        case_list.find_element_by_partial_link_text(case)

    @error_handler
    def cancel_registration(self, browser, case):
        # Navigate to register interest flow
        self.customer.sign_in(browser=browser)

        # Select registration
        registrations_of_interest_div = browser.find_element_by_class_name('margin-top-2')
        assert 'Your draft registrations of interest' in registrations_of_interest_div.text
        case_list = registrations_of_interest_div.find_element_by_class_name('dashboard-case-list')
        case_list.find_element_by_partial_link_text(case).click()

        # Cancel
        cancel_button = browser.find_element_by_class_name('button')
        assert cancel_button.text == 'Cancel registration'
        cancel_button.click()
        pop_up = browser.find_element_by_class_name('pop-up')
        click_button_with_text(pop_up, 'Yes')

        # Check it was cancelled
        alert_box = browser.find_element_by_class_name('box-alert')
        assert 'Your submission has been cancelled' in alert_box.text
        assert case not in browser.page_source.replace('  ', ' ')

    @error_handler
    def download_registration_documents(self, browser, case, file_names):
        self._go_to_case(browser, case)
        browser.find_element_by_link_text('Download registration documents').click()
        self._download_documents(
            browser=browser,
            file_names=file_names
        )

    @error_handler
    def upload_registration_documents(self, browser, case, files):
        self._go_to_case(browser, case)
        browser.find_element_by_link_text('Upload registration documents').click()
        self._upload_documents_one_by_one(
            browser=browser,
            files=files
        )

    @error_handler
    def submit_registration(self, browser, case):

        self._go_to_case(
            case=case,
            browser=browser
        )
        browser.find_element_by_link_text('Final check and submission').click()
        browser.find_element_by_class_name('multiple-choice').find_element_by_name('confirm').click()
        browser.find_element_by_class_name('button').click()

        # Check case appears on dashboard under 'Your registrations of interest' heading
        case_list_containers = browser.find_elements_by_class_name('margin-top-2')
        for case_list_container in case_list_containers:
            if 'Your registrations of interest' in case_list_container.text:
                case_list = case_list_container.find_element_by_class_name('dashboard-case-list')
                break
        else:
            pytest.fail(
                "Unable to locate 'Your registrations of interest' heading on dashboard "
                "after submitting a registration of interest"
            )

        try:
            case_link = case_list.find_element_by_partial_link_text(case)
        except NoSuchElementException:
            pytest.fail("Unable to locate case link on dashboard after registering interest in the case")

        # Check case view indicates the organisation I represent
        case_link.click()
        try:
            organisation_block = browser.find_element_by_class_name('organisation-block')
        except NoSuchElementException:
            pytest.fail(
                "Unable to locate indicator for the represented organisation on case page after registering interest")
        expected_text = f"You are currently representing {self.customer.company_name}"
        if expected_text not in organisation_block.text:
            pytest.fail(f"Expected represented organisation indicator to contain text '{expected_text}', "
                        f"saw '{organisation_block.text}'")

        # Check case view contains a highlighted message
        try:
            highlight_box = browser.find_element_by_class_name('govuk-box-highlight')
        except NoSuchElementException:
            pytest.fail("Unable to locate a highlighted message on case page after registering interest")
        if ('We will consider the information provided by all the respondents and contact you if you are selected to '
                'complete a questionnaire.') not in highlight_box.text:
            pytest.fail(f"Unexpected message seen on case page after registering interest: {highlight_box.text}")

        # Check case name is shown in case view
        try:
            secondary_heading = browser.find_element_by_class_name('heading-secondary')
        except NoSuchElementException:
            pytest.fail("Unable to find heading on case page after registering interest")
        if case not in secondary_heading.text:
            pytest.fail(f"Expected to see case name '{case}' in heading on case page after registering interest. "
                        f"Heading text was '{secondary_heading.text}'")

        # Check for dashboard link
        expected_text = 'Back to dashboard'
        try:
            browser.find_element_by_link_text(expected_text)
        except NoSuchElementException:
            pytest.fail(f"No '{expected_text}' link found on case page after registering interest")
