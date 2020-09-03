from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class Reconsideration(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and _expand the reconsideration tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Reconsideration').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Appeals')
        )

    @error_handler
    def assessment_of_the_reconsideration(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Assessment of the reconsideration')
        else:
            raise NotImplementedError()

    @error_handler
    def reconsideration_initiation_decision(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Reconsideration initiation decision')
        else:
            raise NotImplementedError()

    @error_handler
    def publish_reconsideration_initiation(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Publish reconsideration initiation')
        else:
            raise NotImplementedError()

    @error_handler
    def reconsideration_analysis(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Reconsideration analysis')
        else:
            raise NotImplementedError()

    @error_handler
    def reconsideration_decision(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Reconsideration decision')
        else:
            raise NotImplementedError()

    @error_handler
    def publish_amended_final_determination(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Publish amended final determination')
        else:
            raise NotImplementedError()

    @error_handler
    def appeals(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Appeals')
        else:
            raise NotImplementedError()
