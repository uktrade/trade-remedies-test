from caseworker.submissions.base import SubmissionCategory
from error_handling import error_handler


class Applicant(SubmissionCategory):

    def __init__(self, caseworker):
        self.caseworker = caseworker

    def _go_to(self, browser, case):
        super()._go_to(browser=browser, case=case)

        tabs = browser.find_elements_by_class_name('tab')
        sampled_tab = [tab for tab in tabs if tab.text.startswith('Sampled')][0]
        sampled_tab.click()
        applicant_table = browser.find_element_by_class_name('compact-table')
        return applicant_table

    @error_handler
    def reject(self, browser, case, party, submission_name, deficiency_documents, deficient_documents):
        self._reject(
            browser=browser,
            case=case,
            party=party,
            submission_name=submission_name,
            deficiency_documents=deficiency_documents,
            deficient_documents=deficient_documents,
            expected_status='Awaiting information')
