from time import sleep

from caseworker.submissions.base import SubmissionCategory
from error_handling import error_handler


class DomesticProducer(SubmissionCategory):

    def _go_to(self, browser, case):
        super()._go_to(browser=browser, case=case)
        domestic_producer_heading = [h for h in browser.find_elements_by_class_name('heading-medium') if
                                     h.text == 'Domestic Producer'].pop()
        domestic_producer_table = domestic_producer_heading.find_element_by_xpath('./following::table')
        return domestic_producer_table

    @error_handler
    def reject(self, browser, case, party, submission_name, deficiency_documents, deficient_documents):
        self._reject(
            browser=browser,
            case=case,
            party=party,
            submission_name=submission_name,
            deficiency_documents=deficiency_documents,
            deficient_documents=deficient_documents)

    @error_handler
    def request_information(self, browser, case, party, submission_type, files, name, description, response_window_days=None):
        """
        :param files: [{'file_path': '...', 'confidential': True}, ...]
        """
        domestic_producer_table = self._go_to(browser=browser, case=case)
        link = domestic_producer_table.find_element_by_xpath('./following::div/a')
        assert 'Request information' in link.text
        link.click()

        # JS sometimes doesn't load fast enough, so clicking 'save and continue' shows raw json in the browser
        # Also if JS is not fully loaded when we start clicking, it might be the cause of 'unable to locate' url-type-1
        sleep(1)

        self._add_a_submission(
            browser=browser,
            party=party,
            submission_type=submission_type,
            files=files,
            name=name,
            description=description,
            response_window_days=response_window_days
        )
        return name
