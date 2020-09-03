from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class Investigation(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and _expand the investigation tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Investigation').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Post authentication analysis')
        )

    @error_handler
    def issue_questionnaires(
            self, browser, case,
            sample_companies_selected=None,
            sample_notification_issued_to_the_case_record=None,
            non_sampled_parties_notified=None,
            producer_questionnaires_issued=None,
            importer_questionnaires_issued=None,
            exporter_questionnaires_issued=None,
            government_questionnaires_issued=None,
            economic_interest_questionnaires_issued=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Issue questionnaires'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Sample companies selected': sample_companies_selected,
            'Sample notification issued to the case record': sample_notification_issued_to_the_case_record,
            'Non-sampled parties notified': non_sampled_parties_notified,
            'Producer questionnaires issued': producer_questionnaires_issued,
            'Importer questionnaires issued': importer_questionnaires_issued,
            'Exporter questionnaires issued': exporter_questionnaires_issued,
            'Government questionnaires issued (not anti dumping)': government_questionnaires_issued,
            'Economic interest questionnaires issued': economic_interest_questionnaires_issued
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def process_questionnaires(
            self, browser, case,
            non_confidential_producer_questionnaires_issued_to_case_record=None,
            non_confidential_importer_questionnaires_issued_to_case_record=None,
            non_confidential_economic_interest_questionnaires_issued_to_case_record=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Process questionnaires'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Non-confidential questionnaires issued to the case record - producers': non_confidential_producer_questionnaires_issued_to_case_record,
            'Non-confidential questionnaires issued to the case record - importers':  non_confidential_importer_questionnaires_issued_to_case_record,
            'Non-confidential questionnaires issued to case record - economic interest': non_confidential_economic_interest_questionnaires_issued_to_case_record
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def pre_authentication_data_analysis(
            self, browser, case,
            deficiency_responses_received=None,
            preliminary_injury_analysis_completed=None,
            preliminary_economic_interest_tests_completed=None,
            causation_and_non_attribution_analysis_completed=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Pre-authentication data analysis'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Deficiency responses received': deficiency_responses_received,
            'Preliminary injury analysis completed': preliminary_injury_analysis_completed,
            'Preliminary economic interest tests completed': preliminary_economic_interest_tests_completed,
            'Causation and non-attribution analysis completed': causation_and_non_attribution_analysis_completed
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def authentication(
            self, browser, case,
            authentication_visit_plan_and_tracker_created=None,
            travel_completed=None,
            authentications_finalised=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Authentication'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Authentication visit plan and tracker created': authentication_visit_plan_and_tracker_created,
            'Travel completed': travel_completed,
            'Authentications finalised': authentications_finalised
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def post_authentication_analysis(
            self, browser, case,
            injury_assessment_updated_with_authenticated_data=None,
            economic_interest_assessments_updated_with_authenticated_data=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Post authentication analysis'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Injury assessment updated with authenticated data': injury_assessment_updated_with_authenticated_data,
            'Economic interest assessments updated with authenticated data': economic_interest_assessments_updated_with_authenticated_data
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)
