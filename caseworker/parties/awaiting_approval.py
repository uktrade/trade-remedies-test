from datetime import datetime, timedelta
from time import sleep

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select

from helpers import fail_fast, click_button_with_text
from error_handling import error_handler


def _wait_for_text_in(element, timeout=2):
    """Return text if element contains any within timeout seconds, else raise an error"""
    start_time = datetime.now()
    while datetime.now() <= start_time + timedelta(seconds=timeout):
        if element.text:
            return element.text
    else:
        raise TimeoutError


class AwaitingApproval:

    domestic_producers_div_id = 'parties-2-sampled'
    contributors_div_id = 'parties-8-sampled'
    awaiting_approval_div_id = 'parties-9-sampled'
    rejected_div_id = 'parties-10-sampled'

    def __init__(self, caseworker):
        self.caseworker = caseworker

    def _go_to(self, browser, case):
        # Navigate to case
        self.caseworker.sign_in(browser=browser)
        browser.find_element_by_partial_link_text(case).click()

        # Parties tab
        browser.find_element_by_link_text('Parties').click()

        awaiting_approval_div = browser.find_element_by_id(self.awaiting_approval_div_id)
        sleep(1)  # Expanders won't work immediately
        return awaiting_approval_div

    @error_handler
    def get(self, browser, case):
        # TODO: Make this work for multiple companies and multiple contacts

        try:
            awaiting_approval_div = self._go_to(browser=browser, case=case)
        except NoSuchElementException:
            return None
        company_divs = awaiting_approval_div.find_elements_by_class_name('compact-section')
        awaiting_approval = {}
        for company_div in company_divs:
            company_name = company_div.text
            awaiting_approval[company_name] = []
            company_div.find_element_by_class_name('expander').click()
            sleep(2)  # Let the expanded section load
            contact_block = awaiting_approval_div.find_element_by_class_name('contact-block')
            contact_name_element = contact_block.find_element_by_class_name('bold')
            contact_name = _wait_for_text_in(element=contact_name_element)
            contact_email = contact_block.find_element_by_class_name('email').text
            awaiting_approval[company_name].append({'name': contact_name, 'email': contact_email})

        return awaiting_approval

    @error_handler
    def approve(self, browser, case, party, approve_as):
        awaiting_approval_div = self._go_to(browser=browser, case=case)
        for list_item in awaiting_approval_div.find_elements_by_tag_name('li'):
            if party in list_item.text:
                break
        else:
            raise ValueError("No party with name {} found in awaiting approval".format(party))

        list_item.find_element_by_class_name('expander').click()
        click_button_with_text(list_item, 'Approve registration')

        overlay = browser.find_element_by_class_name('overlay')
        approve_as_dropdown = Select(overlay.find_element_by_name('organisation_type'))
        approve_as_dropdown.select_by_visible_text(approve_as)
        click_button_with_text(overlay, 'Send')

        # Check party has moved from awaiting approval to the appropriate section
        if approve_as == 'Contributor':
            div = browser.find_element_by_id(self.contributors_div_id)
        elif approve_as == 'Domestic Producer':
            div = browser.find_element_by_id(self.domestic_producers_div_id)
        else:
            raise NotImplementedError("TODO: Implement this check for other party types")
        assert party in div.text

        try:
            awaiting_approval_div = browser.find_element_by_id(self.awaiting_approval_div_id)
        except NoSuchElementException:
            # Awaiting approval list is empty
            pass
        else:
            assert party not in awaiting_approval_div.text

    @error_handler
    def reject(self, browser, case, party):
        awaiting_approval_div = self._go_to(browser=browser, case=case)
        for list_item in awaiting_approval_div.find_elements_by_tag_name('li'):
            if party in list_item.text:
                break
        else:
            raise ValueError("No party with name {} found in awaiting approval".format(party))

        list_item.find_element_by_class_name('expander').click()
        click_button_with_text(list_item, 'Deny registration')

        overlay = browser.find_element_by_class_name('overlay')
        click_button_with_text(overlay, 'Send')

        # Check party appears in rejected
        rejected_div = browser.find_element_by_id(self.rejected_div_id)
        for list_item in rejected_div.find_elements_by_tag_name('li'):
            if party in list_item.text:
                break
        else:
            raise ValueError("No party with name {} found in rejected".format(party))
        # Check party is removed from awaiting approval
        with fail_fast(browser):
            try:
                awaiting_approval_div = browser.find_element_by_id(self.awaiting_approval_div_id)
            except NoSuchElementException:
                # Awaiting approval section is empty
                pass
            else:
                for list_item in awaiting_approval_div.find_elements_by_tag_name('li'):
                    if party in list_item.text:
                        raise ValueError("Party was still visible in awaiting approval after rejection")
