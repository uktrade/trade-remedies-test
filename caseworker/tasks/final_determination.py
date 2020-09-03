from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class FinalDetermination(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and expand the final determination tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Final determination').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Publish final determination')
        )

    @error_handler
    def final_analysis(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Final analysis')
        else:
            raise NotImplementedError()

    @error_handler
    def prepare_final_determination(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Prepare final determination')
        else:
            raise NotImplementedError()

    @error_handler
    def final_determination_approval(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Final determination approval')
        else:
            raise NotImplementedError()

    @error_handler
    def publish_final_determination(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Publish final determination')
        else:
            raise NotImplementedError()
