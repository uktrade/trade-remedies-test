from time import sleep

import pytest
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from helpers import fail_fast, click_button_with_text


def _pairwise(iterable):
    """s -> (s0, s1), (s2, s3), (s4, s5), ..."""
    a = iter(iterable)
    return zip(a, a)


class Task:
    """Base class for task pages"""

    def __init__(self, caseworker):
        self.caseworker = caseworker

    def go_to_tasks(self, browser, case):
        """Navigate to task list"""
        self.caseworker.sign_in(browser=browser)
        try:
            browser.find_element_by_partial_link_text(case).click()
        except NoSuchElementException:
            # Case not found in current tab, try looking under archived tab
            tabs = browser.find_elements_by_class_name('tab')
            archived_tab = [tab for tab in tabs if tab.text == 'Archived'][0]
            archived_tab.click()
            browser.find_element_by_partial_link_text(case).click()
        browser.find_element_by_link_text('Tasks').click()

        browser.find_element_by_class_name('task-list')
        sleep(1)  # Let JS load

    @error_handler
    def parse_task_statuses(self, browser, case):
        """Get the status of each task in the task list (eg None, 'in progress', 'completed')"""
        status_for_task = dict()

        # Navigate to task list for case
        self.go_to_tasks(browser=browser, case=case)

        # Fully expand the task list
        sections = browser.find_elements_by_class_name('task-list-item')
        for section in sections[::-1]:  # Expand bottom to top so that expander elements aren't moving as you click
            with fail_fast(browser):
                # Click expander if it exists
                try:
                    expander = section.find_element_by_class_name('expander')
                except NoSuchElementException:
                    pass
                else:
                    expander.click()
                    # Wait to finish expanding
                    sleep(1)

        # Parse statuses
        task_list = browser.find_element_by_class_name('task-list')
        sections = task_list.find_elements_by_class_name('task-list-item')
        for section in sections:

            single_element_section = False
            with fail_fast(browser):
                try:
                    section_heading = section.find_element_by_class_name('expander').text
                except NoSuchElementException:
                    # Single element section with no expander (eg 'Assign team')
                    single_element_section = True
                    section_heading = section.find_element_by_class_name('task-name').text

            task_names = [section_heading]
            task_statuses = [e.text for e in section.find_elements_by_class_name('pull-right')]

            if not single_element_section:
                task_names += [e.text for e in section.find_elements_by_class_name('task-name')]

            for task_name, status in zip(task_names, task_statuses):
                if task_name:
                    if task_name in status_for_task:
                        # Handle duplicate names (eg Close case is a task group AND a task)
                        status_for_task[task_name] = [status_for_task[task_name]]
                        status_for_task[task_name].append(status.lower() or None)
                    else:
                        status_for_task[task_name] = status.lower() or None

        return status_for_task

    def parse_case_summary(self, browser, case):
        """Get the case summary from the task list page"""

        # Navigate to task list for case
        self.go_to_tasks(browser=browser, case=case)

        # Parse the case summary box
        parsed = {}
        case_summary = browser.find_element_by_class_name('case-summary').text
        chunks = case_summary.split('\n')
        for key, value in _pairwise(chunks):
            parsed[key] = value
        return parsed

    @staticmethod
    def parse_form(browser):
        """
        Parse a task form. Return a dictionary for easy interaction eg.

        {'Assign manager': {True: yes_radio_button_element, False: no_radio_button_element, 'selected': None},
        'Draft review in progress': {True: yes_checkbox_element, False: na_checkbox_element, 'selected': None}}

        None = Nothing selected
        True = Yes
        False = No or N/A
        """
        parsed_form = dict()

        form_element = browser.find_element_by_class_name('action-form')
        heading = form_element.find_element_by_class_name('heading-large').text
        row_elements = form_element.find_elements_by_class_name('grid-row')
        with fail_fast(browser):
            for row_element in row_elements:
                try:
                    row_label = row_element.find_element_by_class_name('form-label').text
                except NoSuchElementException:
                    # Skip over information boxes and column heading row
                    continue
                if not row_label:
                    continue
                choice_elements = row_element.find_elements_by_class_name('multiple-choice')
                if len(choice_elements) == 2:
                    # Row with two checkbox options
                    parsed_form[row_label] = {'type': 'checkboxes', 'selected': None}
                    for choice_element in choice_elements:
                        input_element = choice_element.find_element_by_tag_name('input')
                        input_element_value = input_element.get_attribute('value')
                        if input_element_value == 'yes':
                            parsed_form[row_label][True] = input_element
                            if input_element.is_selected():
                                parsed_form[row_label]['selected'] = True
                        elif input_element_value in ['no', 'na']:
                            parsed_form[row_label][False] = input_element
                            if input_element.is_selected():
                                parsed_form[row_label]['selected'] = False
                        else:
                            raise ValueError("Failed to parse input element in '{}' form".format(heading))
                else:
                    # Row with text field (eg a reference number input)
                    try:
                        text_input = row_element.find_element_by_tag_name('input')
                        if not text_input.is_displayed():
                            # Not a real text input (eg. 'Upload your documents below:')
                            raise NoSuchElementException
                    except NoSuchElementException:
                        continue
                    parsed_form[row_label] = {'type': 'text_field', 'field': text_input, 'text': text_input.text}
        return parsed_form

    def _auto_fill_form(self, browser, task_name):
        browser.find_element_by_link_text(task_name).click()
        form = self.parse_form(browser)
        value_for_form_field = self._auto_generate_form_values(form)
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field)

    @staticmethod
    def _auto_generate_form_values(form):
        form_values = {}
        for field_name, field in form.items():
            if field['type'] == 'checkboxes':
                form_values[field_name] = True
            elif field['type'] == 'text_field':
                form_values[field_name] = 'autogenerated_text'
            else:
                raise ValueError(f"unexpected type: {field['type']}")
        return form_values

    def _submit_form(self, browser, form_values_to_set, notes=None, documents=None):
        # Fill form
        form = self.parse_form(browser)

        # TODO: This won't work if you try to set True when True is already set (it will uncheck the box) (+ similar cases)
        for page_text, value_to_set in form_values_to_set.items():
            if value_to_set is not None:
                if form[page_text]['type'] == 'checkboxes':
                    if value_to_set is True and form[page_text]['selected'] is False:
                        # If N/A is set, you must first un-set N/A before setting Yes (UI disables Yes)
                        form[page_text][False].click()
                    element_to_click = form[page_text][value_to_set]
                    if not element_to_click.is_enabled():
                        raise RuntimeError(f"Element with label '{page_text}' is disabled, value to set was '{value_to_set}'")
                    element_to_click.click()
                elif form[page_text]['type'] == 'text_field':
                    element = form[page_text]['field']
                    element.clear()
                    element.send_keys(value_to_set)
                else:
                    raise ValueError("Unexpected field type")

        # Add notes
        if notes is not None:
            for note in notes:
                sleep(5)  # Event handler for add note button needs to load
                add_note_link = WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(ec.element_to_be_clickable((By.CLASS_NAME, 'add-note')))
                add_note_link.click()
                note_list = browser.find_element_by_class_name('note-list')
                text_box = note_list.find_element_by_tag_name('textarea')
                text_box.send_keys(note)
                save_button = click_button_with_text(browser, 'Save')
                # Make sure the button goes away when you click it
                WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
                    ec.staleness_of(save_button)
                )
            for note in notes:
                assert note in note_list.text

        # Upload documents
        if documents is not None:
            for document in documents:
                sleep(5)  # Event handler for add note button needs to load
                add_note_link = WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(ec.element_to_be_clickable((By.CLASS_NAME, 'add-note')))
                add_note_link.click()
                note_list = browser.find_element_by_class_name('note-list')
                browser.find_element_by_id('file-selector').send_keys(document.file_path)
                file_list = browser.find_element_by_class_name('file-list')
                file_list_lines = file_list.find_elements_by_class_name('file-list-line')
                for line in file_list_lines:
                    if document.file_name in line.text:
                        Select(line.find_element_by_class_name('confidential')).select_by_visible_text('Confidential' if document.confidential else 'Non-confidential')
                        break
                else:
                    raise ValueError(f"Couldn't find {document.file_name}")
                if document.friendly_name:
                    text_box = note_list.find_element_by_tag_name('textarea')
                    text_box.send_keys(document.friendly_name)

                save_button = click_button_with_text(browser, 'Save')
                # Make sure the button goes away when you click it
                WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
                    ec.staleness_of(save_button)
                )
            for document in documents:
                notes = note_list.find_elements_by_class_name('note')
                for note in notes:
                    if document.file_name in note.text:
                        # Found matching document/note line
                        if document.friendly_name:
                            assert document.friendly_name in note.text
                        if document.confidential:
                            # Check for confidential flag
                            note.find_element_by_class_name('icon-flag')
                        else:
                            # Check no confidential flag
                            with fail_fast(browser):
                                try:
                                    note.find_element_by_class_name('icon-flag')
                                    pytest.fail("Saw confidential flag on non-confidential document")
                                except NoSuchElementException:
                                    pass
                        break
                else:
                    raise ValueError(f"Couldn't find {document.file_name}")

        # Submit
        browser.find_element_by_name('btnAction').click()

        # Check that we are redirected back to the tasks page
        browser.find_element_by_class_name('task-list')
