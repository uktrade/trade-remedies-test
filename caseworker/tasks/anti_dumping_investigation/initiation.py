from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class Initiation(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and expand the initiation tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Initiation').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Publish initiation notices')
        )

    @error_handler
    def assessment_of_the_application(
        self, browser, case,
        exporters_foreign_government_informed=None,
        notification_filed_to_the_case=None,
        import_data_received_from_hmrc=None,
        goods_description_finalised=None,
        in_scope_hs_codes_finalised=None,
        application_checklist_completed=None,
        documents=None,  # TODO
        notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Assessment of the application'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Exporters’ foreign government(s) informed': exporters_foreign_government_informed,
            'Notification filed to the case': notification_filed_to_the_case,
            'Import data received from HMRC': import_data_received_from_hmrc,
            'Goods description finalised': goods_description_finalised,
            'In scope HS codes finalised': in_scope_hs_codes_finalised,
            'Application checklist completed': application_checklist_completed
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def initiation_preparation(
            self, browser, case,
            contact_details_for_interested_parties_identified=None,
            notice_of_initiation_prepared=None,
            prepare_notice_of_initiation_correspondence=None,
            application_assessment_report_completed=None,
            case_timeline_prepared=None,
            qa_review_of_assessment_completed=None,
            product_classification_numbers_created=None,
            case_title_finalised=None,
            documents_available_in_the_system=None,
            documents=None,  # TODO
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Initiation preparation'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Contact details for interested parties identified': contact_details_for_interested_parties_identified,
            'Notice of initiation prepared': notice_of_initiation_prepared,
            'Notice of initiation correspondence prepared': prepare_notice_of_initiation_correspondence,
            'Application assessment report completed': application_assessment_report_completed,
            'Case timeline prepared': case_timeline_prepared,
            'QA review of assessment completed': qa_review_of_assessment_completed,
            'PCN (product classification numbers) created': product_classification_numbers_created,
            'Case title finalised': case_title_finalised,
            'Documents available in the system': documents_available_in_the_system
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def initiation_decision(
            self, browser, case,
            decide_to_initiate=None,
            documents=None,
            notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Initiation decision'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Decide to initiate': decide_to_initiate
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes, documents=documents)


    @error_handler
    def publish_initiation_notices(
            self, browser, case,
            notice_of_initiation_published=None,
            non_confidential_initiation_report_issued_to_case_record=None,
            non_confidential_application_issued_to_case_record=None,
            notify_foreign_government_of_initiation=None,
            interested_parties_notified_of_initiation=None,
            documents=None,  # TODO
            notes=None):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Publish initiation notices'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Notice of initiation published': notice_of_initiation_published,
            'Non-confidential initiation report issued to case record': non_confidential_initiation_report_issued_to_case_record,
            'Non-confidential application issued to case record': non_confidential_application_issued_to_case_record,
            'Notify foreign government of initiation': notify_foreign_government_of_initiation,
            'Interested parties notified of initiation': interested_parties_notified_of_initiation
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)
