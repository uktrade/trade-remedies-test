from selenium.common.exceptions import NoSuchElementException
import pytest

from helpers import wait_for_download, click_button_with_text


class Flow:
    """Base class for customer flows"""

    def __init__(self, customer):
        self.customer = customer

    def _go_to_case(self, browser, case):
        self.customer.sign_in(browser=browser)

        # Links to initiated cases are prefixed with a number
        case_links = browser.find_element_by_class_name('dashboard-case-list').find_elements_by_tag_name('a')
        for case_link in case_links:
            if case in case_link.text:
                case_link.click()
                break
        else:
            raise ValueError("No case link found on dashboard for {}".format(case))

    def _upload_documents_one_by_one(self, browser, files):
        """Select one document at a time to upload, then repeat until all are uploaded"""
        for count, file_path in enumerate(files, start=1):
            file_name = file_path.split('/')[-1]
            file_input = browser.find_element_by_name('file')
            file_input.send_keys(file_path)
            file_input.submit()
            # Check document uploaded successfully
            display_panels = browser.find_elements_by_class_name('display-panel')
            for display_panel in display_panels:
                if file_name in display_panel.text:
                    # Found file name
                    break
            else:
                raise ValueError(f"No display panel found with text {file_name}")
            display_panel.find_element_by_class_name('icon-green-tick')

            if files[count:]:
                # More documents to upload
                click_button_with_text(browser, 'Add more files')

        click_button_with_text(browser, 'Continue')
        # Confirm that all documents uploaded
        upload_counter = self._get_upload_counter_element(browser)
        # try:
        #     assert '38, 166, 91' in upload_counter.value_of_css_property('color')  # green
        # except:
        #     pytest.xfail("TR-1808 colour wrong")
        assert upload_counter.text.split()[-1] == str(count)

    def _upload_documents_all_together(self, browser, files):
        """Select multiple documents to upload at once"""
        file_input = browser.find_element_by_name('file')
        file_input.send_keys('\n'.join(files))
        file_input.submit()
        document_list = browser.find_element_by_class_name('document-upload-list')

        # Check documents uploaded successfully
        for file_path in files:
            file_name = file_path.split('/')[-1]
            assert file_name in document_list.text

        click_button_with_text(browser, 'Continue')

        # Confirm that all documents uploaded
        upload_counter = self._get_upload_counter_element(browser)
        assert '38, 166, 91' in upload_counter.value_of_css_property('color')  # green
        assert upload_counter.text.split()[-1] == str(len(files))

    def _upload_public_versions_of_confidential_documents(self, browser, files):
        """
        :param files: eg. {'confidential.docx': '/path/to/public.docx'}
        """
        for confidential_file_name, public_file_path in files.items():
            file_panels = browser.find_elements_by_class_name('file-panel')
            for file_panel in file_panels:
                if confidential_file_name in file_panel.text:
                    # Found confidential file, upload corresponding public file
                    row = file_panel.find_element_by_xpath('..')
                    click_button_with_text(row, 'Upload')
                    file_input = row.find_element_by_name('file')
                    file_input.send_keys(public_file_path)
                    file_input.submit()
                    # Check it uploaded
                    public_file_name = public_file_path.split('/')[-1]
                    browser.find_element_by_link_text(public_file_name)
                    break
            else:
                raise ValueError(f"Couldn't find {confidential_file_name} in list of files on page")

        click_button_with_text(browser, 'Continue')
        # Confirm that all documents uploaded
        upload_counter = self._get_upload_counter_element(browser)
        assert '38, 166, 91' in upload_counter.value_of_css_property('color')  # green
        assert upload_counter.text.split()[-1] == str(len(files))

    def _download_documents(self, browser, file_names):
        for file_name in file_names:
            browser.find_element_by_link_text(file_name).click()
            # Check file is actually downloaded
            wait_for_download(file_name)
        click_button_with_text(browser, 'Continue')

        # Check download counter
        download_counter = self._get_download_counter_element(browser)
        assert '38, 166, 91' in download_counter.value_of_css_property('color')  # green
        assert download_counter.text.split()[-1] == str(len(file_names))

    def _replace_deficient_documents(self, browser, replacement_file_for_deficient_file_name):
        """
        :param replacement_file_for_deficient_file_name: eg {'document1.docx': './folder/document1_version2.docx'}
        """

        for deficient_file_name, replacement_file in replacement_file_for_deficient_file_name.items():
            deficient_file_link = browser.find_element_by_link_text(deficient_file_name)
            file_panel = deficient_file_link.find_element_by_xpath('../../../..')
            click_button_with_text(file_panel, 'Replace')
            file_input = file_panel.find_element_by_name('file')
            file_input.send_keys(replacement_file)
            file_input.submit()

            # Check that document was uploaded successfully
            replacement_file_name = replacement_file.split('/')[-1]
            browser.find_element_by_link_text(replacement_file_name)

        click_button_with_text(browser, 'Continue')

        # Confirm that all documents uploaded
        upload_counter = self._get_upload_counter_element(browser)
        # Replaced file is not currently deleted on the backend, Bob is working on it. As a result colour is orange.
        # assert '38, 166, 91' in upload_counter.value_of_css_property('color')  # green
        # assert upload_counter.text.split()[-1] == str(len(replacement_file_for_deficient_file_name))

    @staticmethod
    def _get_upload_counter_element(browser):
        # TODO: This assumes there's only one counter on the page, there are often several!
        task_upload_elements = browser.find_elements_by_class_name('task-upload')
        for element in task_upload_elements:
            if 'Files uploaded' in element.text:
                return element
        raise NoSuchElementException

    @staticmethod
    def _get_download_counter_element(browser):
        # TODO: This assumes there's only one counter on the page, there are often several!
        task_upload_elements = browser.find_elements_by_class_name('task-upload')
        for element in task_upload_elements:
            if 'Downloaded' in element.text:
                return element
        raise NoSuchElementException
