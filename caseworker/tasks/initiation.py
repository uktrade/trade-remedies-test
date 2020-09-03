from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class Initiation(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and _expand the initiation tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Initiation').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Publish initiation notices')
        )

    @error_handler
    def assessment_of_the_case(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Assessment of the case')
        else:
            raise NotImplementedError()

    @error_handler
    def assessment_of_the_application(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Assessment of the application')
        else:
            raise NotImplementedError()

    @error_handler
    def initiation_preparation(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Initiation preparation')
        else:
            raise NotImplementedError()

    @error_handler
    def initiation_decision(self, browser, case, decide_to_initiate=None, auto=False):
        task_name = 'Initiation decision'
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name=task_name)
        else:
            browser.find_element_by_link_text(task_name).click()
            # Fill form
            value_for_form_field = {
                'Decide to initiate': decide_to_initiate
            }
            self._submit_form(browser=browser, form_values_to_set=value_for_form_field)

    @error_handler
    def publish_initiation_notices(self, browser, case, notice_of_initiation_published=None, auto=False):
        task_name = 'Publish initiation notices'
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name=task_name)
        else:
            browser.find_element_by_link_text(task_name).click()
            value_for_form_field = {
                'Notice of initiation published': notice_of_initiation_published,
                # TODO: Are the others common to all case types?
            }
            self._submit_form(browser=browser, form_values_to_set=value_for_form_field)
