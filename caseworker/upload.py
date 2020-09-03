from time import sleep

from selenium.webdriver.support.ui import Select, WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from error_handling import error_handler
from helpers import click_button_with_text
from configuration import EXPLICIT_WAIT_SECONDS


class Upload:

    def __init__(self, caseworker):
        self.caseworker = caseworker

    @error_handler
    def upload_case_documents(self, browser, case, submission_type, files, description):

        # Navigate to registration of case documents upload_files page
        self.caseworker.sign_in(browser=browser)
        browser.find_element_by_partial_link_text(case).click()
        browser.find_element_by_link_text('Case documents').click()

        # Upload files
        browser.find_element_by_partial_link_text('Add new').click()
        Select(browser.find_element_by_id('submissionType')).select_by_visible_text(submission_type)
        browser.find_element_by_name('save').click()
        upload_files(browser, files)

        if description:
            browser.find_element_by_id('submission_description').send_keys(description)

        click_button_with_text(browser, 'Save and continue')

        sleep(5)  # Let event handler load
        browser.find_element_by_id('issue_confirm').click()

        click_button_with_text(browser, 'Finalise the bundle')

        # Check for successful upload_files
        highlight_box = browser.find_element_by_class_name('govuk-box-highlight')
        assert 'Your bundle has been finalised' in highlight_box.text
        for file in files:
            file_name = file['file_path'].split('/')[-1]
            assert file_name in browser.page_source


def upload_files(browser, files):
    """Upload files using 'bundle builder' widget"""
    sleep(15)  # TR-1784
    for file in files:
        browser.find_element_by_class_name('test-file').send_keys(file['file_path'])
        file_name = file['file_path'].split('/')[-1]
        file_list = browser.find_element_by_class_name('file-list')
        for row in file_list.find_elements_by_tag_name('tr'):
            if file_name in row.text:
                confidential_dropdown_for_file = Select(row.find_element_by_name('confidential'))
                if file['confidential']:
                    confidential_dropdown_for_file.select_by_visible_text('Confidential')
                else:
                    confidential_dropdown_for_file.select_by_visible_text('Non-confidential')
                break
        else:
            raise ValueError("Expected to see {} in bundle file list".format(file_name))
    button = click_button_with_text(browser, 'Save and continue')
    WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(ec.staleness_of(button))
