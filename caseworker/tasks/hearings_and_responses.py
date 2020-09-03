from time import sleep

from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class HearingsAndResponses(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and expand the hearings and responses tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Hearings and responses').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Assess undertakings')
        )

    @error_handler
    def complete_hearings(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Complete hearings')
        else:
            raise NotImplementedError()

    @error_handler
    def process_responses_to_the_provisional_determination(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Process responses to the provisional determination')
        else:
            raise NotImplementedError()

    @error_handler
    def assess_undertakings(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Assess undertakings')
        else:
            raise NotImplementedError()
