from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class FinalDetermination(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and _expand the final determination tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Final determination').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Publish final determination')
        )

    @error_handler
    def final_analysis(
            self, browser, case,
            non_confidential_responses_to_statement_of_essential_facts_published=None,
            responses_to_statement_of_essential_facts_analysed=None,
            dumping_or_subsidy_calculations_finalised=None,
            injury_or_causation_calculations_finalised=None,
            economic_interest_tests_finalised=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Final analysis'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Non-confidential responses to the Statement of Essential Facts published': non_confidential_responses_to_statement_of_essential_facts_published,
            'Responses to the Statement of Essential Facts analysed': responses_to_statement_of_essential_facts_analysed,
            'Dumping/Subsidy calculations finalised': dumping_or_subsidy_calculations_finalised,
            'Injury/Causation calculations finalised': injury_or_causation_calculations_finalised,
            'Economic interest tests finalised': economic_interest_tests_finalised
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def prepare_final_determination(
            self, browser, case,
            final_determination_prepared=None,
            documents_for_hmrc_prepared=None,
            correspondence_for_sos_prepared=None,
            interested_party_notification_prepared=None,
            public_notices_prepared=None,
            qa_of_final_determination_decision_and_documents_completed=None,
            relevant_documents_filed=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Prepare final determination'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Final determination prepared': final_determination_prepared,
            'Documents for HMRC prepared': documents_for_hmrc_prepared,
            'Correspondence for SoS prepared': correspondence_for_sos_prepared,
            'Interested party notification prepared': interested_party_notification_prepared,
            'Public notices prepared': public_notices_prepared,
            'QA of final determination decision and documents completed': qa_of_final_determination_decision_and_documents_completed,
            'Relevant documents filed': relevant_documents_filed
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def final_determination_approval(
            self, browser, case,
            final_determination_approved_by_tra=None,
            sos_office_notified_of_final_determination=None,
            sos_approval_of_final_determination_granted=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Final determination approval'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Final determination approved by TRID': final_determination_approved_by_tra,
            'SoS office notified of final determination': sos_office_notified_of_final_determination,
            'SoS approval of final determination granted': sos_approval_of_final_determination_granted
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def publish_final_determination(
            self, browser, case,
            publish_final_determination=None,
            interested_parties_informed=None,
            hmrc_informed=None,
            foreign_government_notified=None,
            wto_notified=None,
            relevant_documents_filed=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Publish final determination'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Publish final determination': publish_final_determination,
            'Interested parties informed': interested_parties_informed,
            'HMRC informed': hmrc_informed,
            'Foreign government notified': foreign_government_notified,
            'WTO notified': wto_notified,
            'Relevant documents filed': relevant_documents_filed
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)
