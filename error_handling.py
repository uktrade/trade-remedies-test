import json
from functools import wraps

import pytest
from selenium.common.exceptions import NoSuchElementException, NoAlertPresentException, UnexpectedAlertPresentException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS


class DjangoDebugError(Exception):
    """Django debug error on the web UI"""
    def __init__(self, original_exception, summary):
        super().__init__(summary)
        self.summary = summary
        self.original_exception = original_exception


class UIErrorMessage(Exception):
    """Error message displayed on the web UI"""
    def __init__(self, original_exception, summary=None, messages=None):
        super().__init__(f"summary={summary}, messages={messages}")
        self.summary = summary
        self.messages = messages
        self.original_exception = original_exception


class UnhandledJSONResponse(Exception):
    """JSON response displayed in the browser, not handled by JS"""
    def __init__(self, original_exception, summary):
        super().__init__(summary)
        self.summary = summary
        self.original_exception = original_exception


def error_handler(func):
    """If the wrapped function fails, raise any error messages shown in the browser"""

    @wraps(func)
    def wrapped(self, browser, *args, **kwargs):
        try:
            return func(self, browser, *args, **kwargs)
        except Exception as original_exception:

            # Catch alerts
            try:
                alert = browser.switch_to.alert
            except NoAlertPresentException:
                pass
            else:
                raise UnexpectedAlertPresentException(alert_text=alert.text) from None

            # Catch Django debug pages
            if "You're seeing this error because" in browser.page_source:
                # Normal Django debug page
                summary = browser.find_element_by_id('summary').text
                raise DjangoDebugError(
                    original_exception=original_exception,
                    summary='\n' + summary) from None
            elif "The debugger caught an exception" in browser.page_source:
                # Werkzeug debugger page
                browser.find_element_by_class_name('traceback').click()  # Toggle copy/paste friendly traceback
                WebDriverWait(
                    browser, EXPLICIT_WAIT_SECONDS).until(
                    ec.text_to_be_present_in_element(
                        (By.CLASS_NAME, 'plain'),
                        "Traceback"
                    )
                )
                traceback = browser.find_element_by_class_name('plain').find_element_by_tag_name('pre').text
                raise DjangoDebugError(
                    original_exception=original_exception,
                    summary='\n' + traceback) from None

            # Detect JSON responses shown in browser (can happen when a form is submitted before JS has loaded)
            try:
                json.loads(browser.find_element_by_tag_name('html').text)
            except json.decoder.JSONDecodeError:
                pass
            else:
                raise UnhandledJSONResponse(
                    original_exception=original_exception,
                    summary=browser.find_element_by_tag_name('html').text)

            # Capture error summary (shown at top of page)
            error_summary = []
            try:
                error_summary_list_element = browser.find_element_by_class_name('error-summary-list')
            except NoSuchElementException:
                pass
            else:
                error_summary_list_items = error_summary_list_element.find_elements_by_tag_name('li')
                for item in error_summary_list_items:
                    errors = item.text.split('\n')
                    for error in errors:
                        error_summary.append(error)

            # Capture individual error messages (shown near specific fields)
            error_messages = []
            try:
                error_message_elements = browser.find_elements_by_class_name('error-message')
            except NoSuchElementException:
                pass
            else:
                for element in error_message_elements:
                    if element.text:
                        error_messages.append(element.text)

            # Catch error popups
            try:
                pop_up = browser.find_element_by_class_name('pop-up')
            except NoSuchElementException:
                pass
            else:
                # Get the error message from the popup
                error_summary = pop_up.text.split('\n')
                if 'Error' in error_summary:
                    error_summary.remove('Error')
                if 'OK' in error_summary:
                    error_summary.remove('OK')

            if error_summary or error_messages:
                # Saw one or more error messages
                raise UIErrorMessage(
                    original_exception=original_exception,
                    summary=error_summary,
                    messages=error_messages) from None
            else:
                # No error messages detected
                raise

    return wrapped
