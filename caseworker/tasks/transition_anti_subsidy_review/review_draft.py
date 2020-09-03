from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class ReviewDraft(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and _expand the review draft tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Review Draft').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Draft review outcomes')
        )

    @error_handler
    def begin_draft_review(
            self, browser, case,
            draft_received=None, draft_review_in_progress=None, hmrc_confirmations_requested=None):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Begin draft review'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Draft received': draft_received,
            'Draft review in progress': draft_review_in_progress,
            'HMRC confirmations requested': hmrc_confirmations_requested
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field)

    @error_handler
    def draft_review_outcomes(
            self, browser, case,
            hmrc_confirmations_received=None,
            draft_requires_review_and_applicant_has_been_informed=None,
            qa_review_of_draft_application_completed=None,
            draft_meets_minimum_pre_requisites_to_trigger_an_investigation=None,
            draft_is_sufficient_to_proceed_and_applicant_has_been_informed=None,
            documents=None,  # TODO
            notes=None,
    ):

        # Navigate to task
        task_name = 'Draft review outcomes'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()
    
        # Fill form
        value_for_form_field = {
            'HMRC confirmations received': hmrc_confirmations_received,
            'Draft requires review and applicant has been informed': draft_requires_review_and_applicant_has_been_informed,
            'QA review of draft application completed': qa_review_of_draft_application_completed,
            'Draft meets minimum pre-requisites to trigger an investigation': draft_meets_minimum_pre_requisites_to_trigger_an_investigation,
            'Draft is sufficient to proceed and applicant has been informed': draft_is_sufficient_to_proceed_and_applicant_has_been_informed
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)
