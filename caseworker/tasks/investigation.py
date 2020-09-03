from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class Investigation(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and expand the investigation tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Investigation').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                # 'Post authentication analysis' OR 'Post verification analysis'
                (By.CLASS_NAME, 'action-list-user'), 'Post')
        )

    @error_handler
    def issue_questionnaires(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Issue questionnaires')
        else:
            raise NotImplementedError()

    @error_handler
    def process_questionnaires(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Process questionnaires')
        else:
            raise NotImplementedError()
    
    # Some case types use the term 'authentication' instead of 'verification' 
    @error_handler
    def pre_authentication_data_analysis(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Pre-authentication data analysis')
        else:
            raise NotImplementedError()

    @error_handler
    def authentication(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Authentication')
        else:
            raise NotImplementedError()

    @error_handler
    def post_authentication_analysis(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Post authentication analysis')
        else:
            raise NotImplementedError()

    # Some case types use the term 'verification' instead of 'authentication'
    @error_handler
    def pre_verification_data_analysis(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Pre-verification analysis')
        else:
            raise NotImplementedError()

    @error_handler
    def verification(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Verification')
        else:
            raise NotImplementedError()

    @error_handler
    def post_verification_data_analysis(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Post-verification analysis')
        else:
            raise NotImplementedError()
