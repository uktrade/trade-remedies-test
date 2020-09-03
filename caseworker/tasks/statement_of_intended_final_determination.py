from time import sleep

from selenium.common.exceptions import NoSuchElementException

from error_handling import error_handler
from caseworker.tasks.base import Task


class StatementOfIntendedFinalDetermination(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and expand the statement of essential facts tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Statement of Intended Final Determination').click()
        # Wait until sub tasks list is expanded. Sub task names differ by case type.
        sleep(2)

    def publish_soifd(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Publish the Statement of Intended Final Determination')
        else:
            raise NotImplementedError()

    @error_handler
    def hearings_and_responses(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Hearings and responses')
        else:
            raise NotImplementedError()
