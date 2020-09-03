from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class ProvisionalDetermination(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and _expand the provisional determination tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Provisional determination').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Publish the provisional determination')
        )

    @error_handler
    def prepare_the_provisional_determination(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Prepare the provisional determination')
        else:
            raise NotImplementedError()

    @error_handler
    def approve_the_provisional_determination(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Approve the provisional determination')
        else:
            raise NotImplementedError()

    @error_handler
    def publish_the_provisional_determination(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Publish the provisional determination')
        else:
            raise NotImplementedError()
