from time import sleep

from selenium.common.exceptions import NoSuchElementException

from error_handling import error_handler
from caseworker.tasks.base import Task


class StatementOfEssentialFacts(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and expand the statement of essential facts tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('The Statement of Essential Facts').click()
        # Wait until sub tasks list is expanded. Sub task names differ by case type.
        sleep(2)

    @error_handler
    def statement_of_essential_facts(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        # Click the statement of essential facts link, not the statement of essential facts expander
        try:
            [e for e in browser.find_elements_by_link_text('The Statement of Essential Facts') if
             'task-name' in e.get_attribute('class')][0].click()
        except IndexError:
            # Statement of essential facts link doesn't exist
            raise NoSuchElementException from None
        if auto:
            form = self.parse_form(browser)
            value_for_form_field = self._auto_generate_form_values(form)
            self._submit_form(browser=browser, form_values_to_set=value_for_form_field)
        else:
            raise NotImplementedError()

    def process_responses_to_the_statement_of_essential_facts(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Process responses to the Statement of Essential Facts')
        else:
            raise NotImplementedError()

    @error_handler
    def hearings_and_responses(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Hearings and responses')
        else:
            raise NotImplementedError()
