from time import sleep
from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from caseworker.submissions.base import upload_files
from caseworker.submissions.applicant import Applicant
from caseworker.submissions.awaiting_approval import AwaitingApproval
from caseworker.submissions.domestic_producer import DomesticProducer
from error_handling import error_handler
from helpers import click_button_with_text


class Submissions:

    def __init__(self, caseworker):
        self.caseworker = caseworker
        self.applicant = Applicant(caseworker=caseworker)
        self.awaiting_approval = AwaitingApproval(caseworker=caseworker)
        self.domestic_producer = DomesticProducer(caseworker=caseworker)

    def _go_to(self, browser, case):
        # Navigate to case
        self.caseworker.sign_in(browser=browser)
        browser.find_element_by_partial_link_text(case).click()

        # Submissions tab
        browser.find_element_by_link_text('Submissions').click()

    @error_handler
    def publish_documents(self, browser, case, submission_type, files, name, description):

        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text('+ Publish documents').click()

        Select(browser.find_element_by_id('submissionType')).select_by_visible_text(submission_type)
        click_button_with_text(browser, 'Save and continue')

        # Type of content
        # TODO: Make it possible to test URL
        browser.find_element_by_id('url-type-1').click()  # Choose 'Documents'

        # Upload files
        upload_files(browser, files)

        # TODO: We could have a form validation test for the mandatory name field
        browser.find_element_by_id('name').send_keys(name)
        browser.find_element_by_id('submission_description').send_keys(description)
        click_button_with_text(browser, 'Save and continue')

        # Final confirm
        sleep(15)  # JS event handler on confirm box must load so that click triggers enabling of publish button
        try:
            browser.find_element_by_id('issue_confirm').click()
        except NoSuchElementException:
            assert 'This must be reviewed by a lead investigator before it can be published' in browser.page_source
            raise PermissionError

        click_button_with_text(browser, 'Publish')

        # Check submission status
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'govuk-box-highlight'), 'Your public notice has been published')
        )
