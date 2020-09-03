from selenium.webdriver.common.by import By
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class CloseCase(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and expand the close case tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Close case').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Case in appeal')
        )

    @error_handler
    def dismiss_case(
            self, browser, case,
            dismissal_approved_by_tra=None,
            file_relevant_documents=None,
            sos_informed=None,
            auto=False):

        task_name = 'Dismiss case'
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name=task_name)
        else:
            browser.find_element_by_link_text(task_name).click()
            value_for_form_field = {
                'Dismissal approved by TRID': dismissal_approved_by_tra,
                'File relevant documents': file_relevant_documents,
                'SoS informed': sos_informed
            }
            self._submit_form(browser=browser, form_values_to_set=value_for_form_field)

    @error_handler
    def reject_application(self, browser, case, auto=False):
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name='Reject application')
        else:
            raise NotImplementedError()

    @error_handler
    def close_case(
            self, browser, case,
            investigation_completed=None,
            final_determination_active=None,
            reconsideration_complete=None,
            all_necessary_files_saved_to_case=None,
            notice_reference_no=None,
            case_close_approved_by_tra=None,
            auto=False):

        self._go_to(browser=browser, case=case)
        # Click the close case link, not the close case expander
        try:
            [e for e in browser.find_elements_by_link_text('Close case') if
             'task-name' in e.get_attribute('class')][0].click()
        except IndexError:
            # Close case link doesn't exist
            raise NoSuchElementException from None
        if auto:
            form = self.parse_form(browser)
            value_for_form_field = self._auto_generate_form_values(form)
        else:
            # Fill form
            value_for_form_field = {
                'Investigation completed': investigation_completed,
                'Final determination active': final_determination_active,
                'Reconsideration complete (where requested)': reconsideration_complete,
                'All necessary files saved to case': all_necessary_files_saved_to_case,
                'Notice reference no:': notice_reference_no,
                'Case close approved by TRID': case_close_approved_by_tra
            }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field)

    @error_handler
    def case_in_appeal(
            self, browser, case,
            notice_reference_no=None,
            request_for_appeal_granted=None,
            appeal_outcomes_filed_to_case=None,
            regulation_amendments_filed_to_case=None,
            case_close_approved_by_tra=None,
            auto=False):

        task_name = 'Case in appeal'
        self._go_to(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name=task_name)
        else:
            browser.find_element_by_link_text(task_name).click()
            value_for_form_field = {
                'Notice reference no:': notice_reference_no,
                'Request for appeal granted': request_for_appeal_granted,
                'Appeal outcomes filed to the case': appeal_outcomes_filed_to_case,
                'Regulation amendments filed to the case': regulation_amendments_filed_to_case,
                'Case close approved by TRID': case_close_approved_by_tra
            }
            self._submit_form(browser=browser, form_values_to_set=value_for_form_field)
