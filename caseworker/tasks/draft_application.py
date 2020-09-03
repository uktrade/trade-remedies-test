from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class DraftApplication(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and _expand the draft application tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Draft application').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Draft review outcomes')
        )

    @error_handler
    def review_draft(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Review draft')
        else:
            raise NotImplementedError()

    @error_handler
    def draft_review_outcomes(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Draft review outcomes')
        else:
            raise NotImplementedError()
