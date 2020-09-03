from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class ProvisionalDetermination(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and _expand the provisional determination tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Provisional determination').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'The Statement of Essential Facts')
        )

    @error_handler
    def prepare_the_provisional_determination(
            self, browser, case,
            provisional_determination_prepared=None,
            correspondence_for_sos_prepared=None,
            public_notices_prepared=None,
            qa_review_of_analysis_and_decision_completed=None,
            interested_party_notification_prepared=None,
            hmrc_notification_prepared=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Prepare the Provisional Determination'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Provisional Determination prepared': provisional_determination_prepared,
            'Correspondence for SoS prepared': correspondence_for_sos_prepared,
            'Public notices prepared': public_notices_prepared,
            'QA review of analysis and decision completed': qa_review_of_analysis_and_decision_completed,
            'Interested party notification prepared': interested_party_notification_prepared,
            'HMRC notification prepared': hmrc_notification_prepared
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def provisional_determination_approval(
            self, browser, case,
            provisional_determination_is_approved_by_tra=None,
            provisional_determination_sent_to_sos=None,
            approval_of_provisional_determination_granted=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Provisional Determination approval'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Provisional Determination is approved by TRID': provisional_determination_is_approved_by_tra,
            'Provisional Determination sent to SoS': provisional_determination_sent_to_sos,
            'Approval of Provisional Determination granted': approval_of_provisional_determination_granted
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def publish_the_provisional_determination(
            self, browser, case,
            provisional_determination_published=None,
            publish_section_6p6_notice=None,
            hmrc_informed_of_provisional_determination=None,
            government_of_exporting_country_notified_of_provisional_determination=None,
            interested_parties_notified=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Publish the Provisional Determination'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Provisional Determination published': provisional_determination_published,
            'Publish Section 6p6 notice.': publish_section_6p6_notice,
            'HMRC informed of Provisional Determination': hmrc_informed_of_provisional_determination,
            'Government of exporting country/countries notified of provisional determination': government_of_exporting_country_notified_of_provisional_determination,
            'Interested parties notified': interested_parties_notified
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def process_responses_to_the_provisional_determination(
            self, browser, case,
            responses_to_the_provisional_determination_assessed=None,
            hearings_held=None,
            hearing_summaries_issued_to_the_case_record=None,
            calculations_updated_where_appropriate=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Process responses to the provisional determination'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Responses to the Provisional Determination assessed': responses_to_the_provisional_determination_assessed,
            'Hearings held': hearings_held,
            'Hearing summaries issued to the case record': hearing_summaries_issued_to_the_case_record,
            'Calculations updated where appropriate': calculations_updated_where_appropriate
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def statement_of_essential_facts(
            self, browser, case,
            statement_of_essential_facts_prepared=None,
            statement_of_essential_facts_approved_by_tra=None,
            statement_of_essential_facts_published=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'The Statement of Essential Facts'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'The Statement of Essential Facts prepared': statement_of_essential_facts_prepared,
            'The Statement of Essential Facts is approved by TRID': statement_of_essential_facts_approved_by_tra,
            'The Statement of Essential Facts is published': statement_of_essential_facts_published
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

