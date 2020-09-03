from time import sleep

import pytest
from selenium.common.exceptions import NoSuchElementException

from error_handling import error_handler
from customer.base import Flow
from helpers import fail_fast, parse_table, wait_for_download, click_button_with_text


class RespondToSubmission(Flow):

    def _go_to_submission(self, browser, case, submission):
        super()._go_to_case(browser=browser, case=case)
        try:
            # Normally we should be on the my case page, with a table of submissions for the case
            table = parse_table(browser, browser.find_element_by_class_name('my-case'), preserve_links=True)
        except NoSuchElementException:
            # Registrations of interest bypass the my case page because we haven't joined the case yet
            if submission != 'Registration of Interest':
                raise
            else:
                # In that case we should be on the ROI task list for the case
                assert case in browser.find_element_by_class_name('heading-medium').text
        else:
            # If we're on the my case page, navigate to the submission
            try:
                [r for r in table if r['name'] == submission][0]['type'].click()
            except IndexError:
                pytest.xfail('TR-1730 - Information request disappears from dashboard')

    @error_handler
    def download_submission(self, browser, case, submission, file_names):
        self._go_to_submission(browser, case, submission)
        browser.find_element_by_partial_link_text('Download').click()
        self._download_documents(
            browser=browser,
            file_names=file_names
        )

    @error_handler
    def upload_response(self, browser, case, submission, files):
        self._go_to_submission(
            case=case,
            submission=submission,
            browser=browser
        )
        browser.find_element_by_link_text('Upload your documents').click()
        self._upload_documents_all_together(
            browser=browser,
            files=files
        )

    @error_handler
    def upload_non_confidential_response(self, browser, case, submission, files):
        self._go_to_submission(
            case=case,
            submission=submission,
            browser=browser
        )
        browser.find_element_by_link_text('Upload your documents for the public file').click()
        self._upload_documents_all_together(
            browser=browser,
            files=files
        )

    @error_handler
    def final_check(self, browser, case, submission):
        self._go_to_submission(
            case=case,
            browser=browser,
            submission=submission
        )
        # Check all upload indicators are green
        indicators = browser.find_elements_by_class_name('number-circle')
        for indicator in indicators:
            indicator_container_class = indicator.find_element_by_xpath('..').get_attribute('class').strip()
            # 'task-upload' is styled green by JS, 'task-upload in-progress' is yellow
            assert 'task-upload' in indicator_container_class

        browser.find_element_by_partial_link_text('Check').click()

        # Tick box and submit
        browser.find_element_by_name('documents_reviewed').click()
        click_button_with_text(browser, 'Save and continue')

        # Check for completed indicator
        browser.find_element_by_class_name('task-completed')

    @error_handler
    def submit(self, browser, case, submission):
        self._go_to_submission(
            case=case,
            submission=submission,
            browser=browser
        )
        with fail_fast(browser):
            try:
                browser.find_element_by_partial_link_text('Submit your').click()  # 'questionnaire response' / 'application'
            except NoSuchElementException:
                browser.find_element_by_link_text('Send your submission').click()

        browser.find_element_by_id('field-1051-1').click()
        browser.find_elements_by_class_name('multiple-choice')[-1].find_element_by_name('confirm').click()
        click_button_with_text(browser, 'Submit')

        assert 'Submission made' in browser.find_element_by_class_name('lede').text

    @error_handler
    def download_deficiency_notices(self, browser, case, submission, file_names):
        self._go_to_submission(
            case=case,
            submission=submission,
            browser=browser
        )

        # Check for presence of warning message
        warning_div = browser.find_element_by_class_name('warning')
        assert 'Your last submission was insufficient to proceed' in warning_div.text

        browser.find_element_by_partial_link_text('Download deficiency').click()  # notices / documents
        for file_name in file_names:
            browser.find_element_by_link_text(file_name).click()
            # Check file is actually downloaded
            wait_for_download(file_name)
        click_button_with_text(browser, 'Continue')

    @error_handler
    def replace_deficient_documents(self, browser, case, submission, replacement_file_for_deficient_file_name):
        """
        :param replacement_file_for_deficient_file_name: eg {'document1.docx': './folder/document1version2.docx'}
        """
        self._go_to_submission(browser, case, submission)
        browser.find_element_by_partial_link_text('Upload').click()
        # Let JS load
        sleep(3)
        self._replace_deficient_documents(
            browser=browser,
            replacement_file_for_deficient_file_name=replacement_file_for_deficient_file_name
        )
