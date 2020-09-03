from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class DecisionsAndReasons(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and expand the decisions and reasons tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Decisions and Reasons').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Hearings and responses')
        )

    @error_handler
    def measure_type_decision_and_calculations(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Measure type decision and calculations')
        else:
            raise NotImplementedError()

    @error_handler
    def statement_of_intended_final_determination(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Statement of Intended Final Determination')
        else:
            raise NotImplementedError()

    @error_handler
    def hearings_and_responses(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Hearings and responses')
        else:
            raise NotImplementedError()
