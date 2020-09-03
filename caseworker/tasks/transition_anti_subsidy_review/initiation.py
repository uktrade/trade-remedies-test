from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from error_handling import error_handler
from caseworker.tasks.base import Task


class Initiation(Task):

    def _go_to(self, browser, case):
        """Go to the tasks page and _expand the initiation tasks"""
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text('Initiation').click()
        # Wait until sub tasks list is expanded
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
            ec.text_to_be_present_in_element(
                (By.CLASS_NAME, 'action-list-user'), 'Publish initiation notices')
        )

    @error_handler
    def assessment_of_the_case(
        self, browser, case,
        eu_cases_researched=None,
        goods_description_finalised=None,
        in_scope_hs_codes_finalised=None,
        period_for_the_investigation_finalised=None,
        import_data_assessed=None,
        familiarisation_visits_completed=None,
        documents=None,  # TODO
        notes=None
    ):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Assessment of the case'
        self._go_to(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'EU cases researched': eu_cases_researched,
            'Goods description finalised': goods_description_finalised,
            'In scope HS codes finalised': in_scope_hs_codes_finalised,
            'Period for the investigation finalised': period_for_the_investigation_finalised,
            'Import data assessed': import_data_assessed,
            'Familiarisation visits completed': familiarisation_visits_completed
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def initiation_preparation(
            self, browser, case,
            contact_details_for_interested_parties_identified=None,
            case_timeline_prepared=None,
            notice_of_initiation_prepared=None,
            notice_of_initiation_correspondence_prepared=None,
            qa_review_of_preparations_completed=None,
            product_classification_numbers_created=None,
            case_title_finalised=None,
            case_type_finalised=None,
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
            'Case timeline prepared': case_timeline_prepared,
            'Notice of initiation prepared': notice_of_initiation_prepared,
            'Notice of initiation correspondence prepared': notice_of_initiation_correspondence_prepared,
            'QA review of preparations completed': qa_review_of_preparations_completed,
            'PCN (product classification numbers) created': product_classification_numbers_created,
            'Case title finalised': case_title_finalised,
            'Case type finalised': case_type_finalised,
            'Documents available in the system': documents_available_in_the_system
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)

    @error_handler
    def initiation_decision(
            self, browser, case,
            decide_to_initiate=None,
            documents=None,  # TODO
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
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)


    @error_handler
    def publish_initiation_notices(
            self, browser, case,
            roi_documents_issued_to_case=None,
            notice_of_initiation_published=None,
            interested_parties_notified_of_initiation=None,
            notice_of_initiation_url=None,
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
            'Registration of interest documents issued to case': roi_documents_issued_to_case,
            'Notice of initiation published': notice_of_initiation_published,
            'Interested parties notified of initiation': interested_parties_notified_of_initiation,
            'Notice of initiation URL:': notice_of_initiation_url
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field, notes=notes)
