from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class CloseCase(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and _expand the close case tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Close case').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Case in appeal')
        )

    @error_handler
    def reject_application(
            self, browser, case,
            applicant_informed=None,
            file_relevant_documents=None,
            termination_approved_by_tra=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Reject application'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Applicant informed': applicant_informed,
            'File relevant documents': file_relevant_documents,
            'Termination approved by TRID': termination_approved_by_tra
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

        # Check for success
        assert 'Rejected' in browser.page_source

    @error_handler
    def close_case(
            self, browser, case,
            no_reconsideration_requested=None,
            investigation_completed=None,
            final_determination_active=None,
            tracking_or_surveillance_requested=None,
            reconsideration_complete=None,
            all_necessary_files_saved_to_case=None,
            regulation_reference_no=None,
            case_close_approved_by_tra=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Close case'
        self._go_to(browser=browser, case=case)
        # Click the close case link, not the close case expander
        [e for e in browser.find_elements_by_link_text(task_name) if 'task-name' in e.get_attribute('class')][0].click()

        # Fill form
        value_for_form_field = {
            'No reconsideration requested': no_reconsideration_requested,
            'Investigation completed': investigation_completed,
            'Final determination active': final_determination_active,
            'Tracking/surveillance requested (where appropriate)': tracking_or_surveillance_requested,
            'Reconsideration complete (where requested)': reconsideration_complete,
            'All necessary files saved to case': all_necessary_files_saved_to_case,
            'Regulation reference no:': regulation_reference_no,
            'Case close approved by TRID': case_close_approved_by_tra
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def case_in_appeal(
            self, browser, case,
            regulation_reference_no=None,
            request_for_appeal_granted=None,
            appeal_outcomes_filed_to_case=None,
            regulation_amendments_filed_to_case=None,
            case_close_approved_by_tra=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Case in appeal'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Regulation reference no:': regulation_reference_no,
            'Request for appeal granted': request_for_appeal_granted,
            'Appeal outcomes filed to the case': appeal_outcomes_filed_to_case,
            'Regulation amendments filed to the case': regulation_amendments_filed_to_case,
            'Case close approved by TRID': case_close_approved_by_tra
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)
