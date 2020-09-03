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
                (By.CLASS_NAME, 'action-list-user'), 'Appeals')
        )

    @error_handler
    def assessment_of_the_reconsideration(
            self, browser, case,
            reconsideration_request_received=None,
            assign_reconsideration_team=None,
            assessment_of_request_completed=None,
            documents_prepared_and_in_system=None,
            qa_of_documents_approved=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Assessment of the Reconsideration'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Reconsideration request received': reconsideration_request_received,
            'Assign reconsideration team': assign_reconsideration_team,
            'Assessment of the request completed': assessment_of_request_completed,
            'Documents prepared and in the system': documents_prepared_and_in_system,
            'QA of documents approved': qa_of_documents_approved
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def reconsideration_initiation_decision(
            self, browser, case,
            reconsideration_will_be_initiated=None,
            tra_approval_of_decision=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Reconsideration initiation decision'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Reconsideration will be initiated': reconsideration_will_be_initiated,
            'TRID approval of the decision': tra_approval_of_decision
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def publish_reconsideration_initiation(
            self, browser, case,
            reconsideration_initiation_notice_published=None,
            interested_parties_notified=None,
            foreign_government_notified=None,
            reconsideration_notices_uploaded=None,
            notice_of_initiation_url=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Publish reconsideration initiation'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Reconsideration initiation notice published': reconsideration_initiation_notice_published,
            'Interested parties notified of the reconsideration': interested_parties_notified,
            'Foreign government notified of the reconsideration': foreign_government_notified,
            'Final versions of the reconsideration notices uploaded to the system': reconsideration_notices_uploaded,
            'Notice of initiation URL': notice_of_initiation_url,
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def reconsideration_analysis(
            self, browser, case,
            data_reviewed=None,
            economic_interest_assessments_reconsidered=None,
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
            'Economic interest assessments reconsidered': economic_interest_assessments_reconsidered,
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
            sos_decision_on_final_determination_provided=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Reconsideration decision'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Reconsideration approved by TRID': reconsideration_approved_by_tra,
            'SoS office notified of the reconsideration': sos_office_notified_of_reconsideration,
            'SoS decision on final determination provided': sos_decision_on_final_determination_provided
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def amended_final_determination_published(
            self, browser, case,
            amended_final_determination_published=None,
            reconsideration_report_published=None,
            interested_parties_informed=None,
            dit_tariff_team_informed=None,
            foreign_government_notified=None,
            wto_notified=None,
            reconsidered_final_determination_notice_url=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Amended final determination published'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Amended final determination published': amended_final_determination_published,
            'Reconsideration report published': reconsideration_report_published,
            'Interested parties informed': interested_parties_informed,
            'DIT tariff team informed': dit_tariff_team_informed,
            'Foreign government notified': foreign_government_notified,
            'WTO notified': wto_notified,
            'Reconsidered final determination notice url': reconsidered_final_determination_notice_url,
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def appeals(
            self, browser, case,
            appeal_request_received=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Appeals'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Appeal request received': appeal_request_received
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)
