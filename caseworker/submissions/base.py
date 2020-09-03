from time import sleep
from datetime import datetime, timedelta
import re

from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from caseworker.upload import upload_files
from configuration import EXPLICIT_WAIT_SECONDS
from constants import WTO_MIN_QUESTIONNAIRE_RESPONSE_DAYS
from error_handling import error_handler
from helpers import parse_table, click_button_with_text


def suffix(day_number):
    return 'th' if 11 <= day_number <= 13 else {1: 'st', 2: 'nd', 3: 'rd'}.get(day_number % 10, 'th')


class SubmissionCategory:
    """
    Base class for Submission 'categories'
    eg. Applicant, Domestic Producer... Awaiting Approval
    """

    def __init__(self, caseworker):
        self.caseworker = caseworker

    def _go_to(self, browser, case):

        # Navigate to case
        self.caseworker.sign_in(browser=browser)
        browser.find_element_by_partial_link_text(case).click()

        # Submissions tab
        browser.find_element_by_link_text('Submissions').click()

    def _go_to_submission(self, browser, case, party, submission_name):
        table_element = self._go_to(browser=browser, case=case)
        parsed_table = parse_table(browser=browser, table_element=table_element, preserve_links=True)
        for row in parsed_table:
            if row['party'].text == party and row['submission'].text == submission_name:
                link_element = row['submission']
                link_element.click()
                break
        else:
            raise ValueError("No submission found for case {} with party {} and "
                             "submission name {}".format(case, party, submission_name))

    def _reject(
            self, browser, case, party, submission_name, deficiency_documents, deficient_documents,
            expected_status='Deficient'):
        self._go_to_submission(browser=browser, case=case, party=party, submission_name=submission_name)

        # Set deficient documents to deficient, and any others to sufficient
        sufficient_sliders = browser.find_elements_by_class_name('slider')
        for slider in sufficient_sliders:
            spans = slider.find_elements_by_tag_name('span')
            yes = [span for span in spans if span.text == 'Yes'][0]
            no = [span for span in spans if span.text == 'No'][0]
            filename = slider.find_element_by_xpath('../..').find_element_by_class_name('filename').text
            if filename in deficient_documents:
                no.click()
            else:
                yes.click()

        # Deny submission
        deny_button = click_button_with_text(browser, 'Deny submission')
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(ec.staleness_of(deny_button))

        # Upload deficiency documents
        upload_files(browser, [{'file_path': file_path, 'confidential': False} for file_path in deficiency_documents])

        # Set a name (use the same one)
        match = re.search(pattern=r'(.+) \(version (.+)\)', string=submission_name)
        if match:
            submission_name = match[1]  # Get rid of version
        browser.find_element_by_id('name').clear()
        browser.find_element_by_id('name').send_keys(submission_name)
        click_button_with_text(browser, 'Save and continue')

        # Set no response window / deadline
        sleep(15)  # Even after CW PR 340, clicking save and continue here gives JS in browser even with a 10 sec sleep sometimes!!!!!!!
        browser.find_element_by_id('response-window-2').click()
        click_button_with_text(browser, 'Save and continue')

        # Confirmation checkbox
        # Let JS load here otherwise sometimes the overlay doesn't appear when we click send button
        sleep(15)
        browser.find_element_by_id('issue_confirm').click()

        # Send submission request
        click_button_with_text(browser, 'Send the deficiency notice')

        # Send notification overlay
        overlay = browser.find_element_by_class_name('overlay')
        click_button_with_text(overlay, 'Send')

        # Check submission is rejected
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(ec.invisibility_of_element(overlay))
        match = re.search(pattern=r'(.+) \(version (.+)\)', string=submission_name)
        if match:
            expected_submission_name = f'{match[1]} (version {int(match[2]) + 1})'
        else:
            expected_submission_name = submission_name

        submissions_awaiting_approval = self.get(browser=browser, case=case)
        for submission_awaiting_approval in submissions_awaiting_approval:
            if (submission_awaiting_approval['party'] == party and
                    expected_submission_name in submission_awaiting_approval['submission']):
                # Match found
                assert submission_awaiting_approval['status'] == expected_status
                break
        else:
            raise ValueError("{} submission not found in list of submissions awaiting approval".format(expected_status))

    @error_handler
    def get(self, browser, case):
        try:
            table_element = self._go_to(browser=browser, case=case)
        except NoSuchElementException:
            if 'No non-sampled' in browser.page_source:
                return None
            else:
                raise
        return parse_table(browser, table_element)

    @error_handler
    def approve(self, browser, case, party, submission_name):
        self._go_to_submission(browser=browser, case=case, party=party, submission_name=submission_name)

        # Set all documents to sufficient
        sufficient_sliders = browser.find_elements_by_class_name('slider')
        for slider in sufficient_sliders:
            spans = slider.find_elements_by_tag_name('span')
            yes = [span for span in spans if span.text == 'Yes'][0]
            yes.click()

        # Approve submission
        approve_button = click_button_with_text(browser, 'Approve submission')
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(ec.staleness_of(approve_button))

    @error_handler
    def _add_a_submission(self, browser, party, submission_type, files, name, description, response_window_days):
        """
        :param files: [{'file_path': '...', 'confidential': True}, ...]
        """
        Select(browser.find_element_by_id('partyField')).select_by_visible_text(party)
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

        # Response window
        if submission_type == 'Questionnaire':
            # Expect a default response window to be set automatically
            WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
                ec.text_to_be_present_in_element(
                    (By.CLASS_NAME, 'bundle-builder'),
                    f"{WTO_MIN_QUESTIONNAIRE_RESPONSE_DAYS} days")
            )
            browser.find_elements_by_class_name('populated')[-1].find_element_by_class_name('edit').click()
        if response_window_days is None:
            browser.find_element_by_id('response-window-2').click()  # No
        else:
            browser.find_element_by_id('response-window-1').click()  # Yes
            browser.find_element_by_id('time-window').clear()
            browser.find_element_by_id('time-window').send_keys(response_window_days)
        expiring_element = browser.find_elements_by_class_name('populated')[-1]
        # Need to let JS load here, otherwise we get JSON in browser after the click
        click_button_with_text(browser, 'Save and continue')
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(ec.staleness_of(expiring_element))
        if response_window_days is not None:
            deadline = datetime.now() + timedelta(days=response_window_days)
            last_grey_box = browser.find_elements_by_class_name('populated')[-1]
            assert f'{response_window_days} days from request' in last_grey_box.text
            assert deadline.strftime(f'%-d{suffix(deadline.day)} %b %Y') in last_grey_box.text

        # Final confirm
        # Let event handler for confirm checkbox load
        sleep(10)
        browser.find_element_by_id('issue_confirm').click()
        # Let JS load here otherwise sometimes the overlay doesn't appear when we click issue button
        click_button_with_text(browser, 'Issue the')

        # Send notification overlay
        overlay = browser.find_element_by_class_name('overlay')
        send_button = click_button_with_text(overlay, 'Send')
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(ec.staleness_of(send_button))

        # Check submitted files appear in the 'original templates' box
        # Let JS load, clicking the expander doesn't work right away
        sleep(3)
        original_templates_box = browser.find_element_by_class_name('compact-section')
        original_templates_box.find_element_by_class_name('expander').click()
        for file in files:
            file_name = file['file_path'].split('/')[-1]
            WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
                ec.text_to_be_present_in_element((By.CLASS_NAME, 'compact-section'), file_name))
