from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class Reconsideration(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and expand the reconsideration tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Reconsideration').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Publish Reconsiderations')
        )

    @error_handler
    def assign_reconsideration_team(
            self, browser, case,
            reconsideration_request_received=None,
            assign_manager=None,
            assign_team=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Assign reconsideration team'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Reconsideration request received': reconsideration_request_received,
            'Assign manager': assign_manager,
            'Assign team': assign_team
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def reconsideration_initiation(
            self, browser, case,
            reconsideration_initiation_documents_prepared=None,
            qa_of_decision_to_initiate_reconsideration=None,
            tra_approval_of_decision=None,
            publish_reconsideration_initiation_documents=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Reconsideration initiation'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Reconsideration initiation documents prepared': reconsideration_initiation_documents_prepared,
            'QA of decision to initiate a reconsideration': qa_of_decision_to_initiate_reconsideration,
            'TRID approval of decision': tra_approval_of_decision,
            'Publish reconsideration initiation documents': publish_reconsideration_initiation_documents,
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def reconsideration_analysis(
            self, browser, case,
            data_reviewed=True,
            dumping_or_subsidy_calculations_reconsidered=None,
            economic_interest_assessments_reconsidered=None,
            injury_or_causation_assessment_reconsidered=None,
            report_on_reconsideration_outcomes_prepared=None,
            amendments_to_final_determination_prepared=None,
            qa_of_reconsideration_decision_and_documents_completed=None,
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
        task_name = 'Reconsideration analysis'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Data reviewed': data_reviewed,
            'Dumping/Subsidy calculations reconsidered': dumping_or_subsidy_calculations_reconsidered,
            'Economic interest assessments reconsidered': economic_interest_assessments_reconsidered,
            'Injury/causation assessment reconsidered': injury_or_causation_assessment_reconsidered,
            'Report on reconsideration outcomes prepared': report_on_reconsideration_outcomes_prepared,
            'Amendments to final determination prepared': amendments_to_final_determination_prepared,
            'QA of reconsideration decision and documents completed': qa_of_reconsideration_decision_and_documents_completed,
            'Relevant documents filed': relevant_documents_filed
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def reconsideration_decision(
            self, browser, case,
            reconsideration_approved_by_tra=None,
            sos_office_notified_of_reconsideration=None,
            sos_approval_of_reconsideration_granted=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Reconsideration Decision'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Reconsideration approved by TRID': reconsideration_approved_by_tra,
            'SoS office notified of the reconsideration': sos_office_notified_of_reconsideration,
            'SoS approval of reconsideration granted': sos_approval_of_reconsideration_granted
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def publish_reconsiderations(
            self, browser, case,
            amended_final_determination_published=None,
            interested_parties_informed=None,
            hmrc_informed=None,
            foreign_government_notified=None,
            wto_notified=None,
            reconsideration_report_published=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Publish Reconsiderations'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Amended final determination published': amended_final_determination_published,
            'Interested parties informed': interested_parties_informed,
            'HMRC informed': hmrc_informed,
            'Foreign government notified': foreign_government_notified,
            'WTO notified': wto_notified,
            'Reconsideration report published': reconsideration_report_published
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)
