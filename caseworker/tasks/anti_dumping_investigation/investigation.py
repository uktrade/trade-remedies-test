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
                (By.CLASS_NAME, 'action-list-user'), 'Post-verification analysis')
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
            non_confidential_producer_questionnaires_issued_to_public_file=None,
            non_confidential_exporter_questionnaires_issued_to_public_file=None,
            non_confidential_importer_questionnaires_issued_to_public_file=None,
            non_confidential_producer_economic_interest_questionnaires_issued_to_public_file=None,
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
            'Non-confidential producer questionnaires issued to public file': non_confidential_producer_questionnaires_issued_to_public_file,
            'Non-confidential exporter questionnaires issued to public file': non_confidential_exporter_questionnaires_issued_to_public_file,
            'Non-confidential importer questionnaires issued to public file': non_confidential_importer_questionnaires_issued_to_public_file,
            'Non-confidential producer Economic interest questionnaires issued to public file': non_confidential_producer_economic_interest_questionnaires_issued_to_public_file,
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def pre_verification_data_analysis(
            self, browser, case,
            preliminary_dumping_or_subsidy_margins_calculated=None,
            preliminary_injury_or_causation_analysis_completed=None,
            preliminary_economic_interest_tests_completed=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Pre-verification data analysis'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Preliminary dumping/subsidy margins calculated': preliminary_dumping_or_subsidy_margins_calculated,
            'Preliminary injury / causation analysis completed': preliminary_injury_or_causation_analysis_completed,
            'Preliminary Economic interest tests completed': preliminary_economic_interest_tests_completed
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def verification(
            self, browser, case,
            verification_visit_plan_and_tracker_created=None,
            travel_completed=None,
            verifications_finalised=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Verification'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Verification visit plan and tracker created': verification_visit_plan_and_tracker_created,
            'Travel completed': travel_completed,
            'Verifications finalised': verifications_finalised
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def post_verification_data_analysis(
            self, browser, case,
            dumping_calculations_adjusted_to_contain_verified_data=None,
            economic_interest_assessments_updated_with_verified_data=None,
            injury_or_causation_assessment_updated_with_verified_data=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Post-verification analysis'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Dumping calculations adjusted to contain verified data': dumping_calculations_adjusted_to_contain_verified_data,
            'Economic interest assessments updated with verified data': economic_interest_assessments_updated_with_verified_data,
            'Injury/causation assessment updated with verified data': injury_or_causation_assessment_updated_with_verified_data
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)
