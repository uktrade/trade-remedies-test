from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class DecisionsAndReasons(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and expand the decisions and reasons tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Decisions and Reasons').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Hearings and responses')
        )

    @error_handler
    def measure_type_decision_and_calculations(
            self, browser, case,
            tariff_rate_quotas_will_be_used=None,
            provisional_tariff_rate_quotas_calculated=None,
            justification_for_tariff_rate_quotas_uploaded=None,
            qa_review_of_analysis_and_decision_completed=None,
            sos_informed_of_intention_to_use_tariff_rate_quotas=None,
            sos_response_on_tariff_rate_quotas_received=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Measure type decision and calculations'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Tariff rate quotas will be used': tariff_rate_quotas_will_be_used,
            'Provisional tariff or tariff rate quotas calculated': provisional_tariff_rate_quotas_calculated,
            'Justification for tariff rate quotas uploaded to the system': justification_for_tariff_rate_quotas_uploaded,
            'QA review of analysis and decision completed': qa_review_of_analysis_and_decision_completed,
            'SoS informed of intention to use tariff rate quotas': sos_informed_of_intention_to_use_tariff_rate_quotas,
            'SoS response on tariff rate quotas received': sos_response_on_tariff_rate_quotas_received
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def statement_of_intended_final_determination(
            self, browser, case,
            statement_of_intended_final_determination_prepared=None,
            statement_of_intended_final_determination_approved=None,
            statement_of_intended_final_determination_published=None,
            statement_of_intended_final_determination_notice_url=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Statement of Intended Final Determination'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Statement of Intended Final Determination prepared': statement_of_intended_final_determination_prepared,
            'Statement of Intended Final Determination approved by TRID': statement_of_intended_final_determination_approved,
            'Statement of Intended Final Determination published': statement_of_intended_final_determination_published,
            'Statement of Intended Final Determination notice URL:': statement_of_intended_final_determination_notice_url
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def hearings_and_responses(
            self, browser, case,
            hearing_summaries_issued_to_case_record=None,
            non_confidential_responses_to_soifd_published=None,
            responses_to_soifd_analysed=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Hearings and responses'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Hearing summaries issued to case record': hearing_summaries_issued_to_case_record,
            'Non-confidential responses to statement of intended final determination published': non_confidential_responses_to_soifd_published,
            'Responses to statement of intended final determination analysed': responses_to_soifd_analysed,
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)
