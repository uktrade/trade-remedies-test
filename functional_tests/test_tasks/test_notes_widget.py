import os

import pytest
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from caseworker import Caseworker
from configuration import EXPLICIT_WAIT_SECONDS
from document import Document
from helpers import wait_for_download
from fixtures import browser, factory_reset_before_each_test


def test_notes(browser):
    """Test you can add notes to a task"""

    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type='Anti-dumping investigation', auto=True, browser=browser)
    notes = ['An important note', 'Another important note']

    caseworker.tasks.anti_dumping_investigation.initiation.initiation_decision(
        notes=notes,
        case=case,
        browser=browser
    )

    # Check that the notes are there when you navigate away from the page, then come back later
    caseworker.tasks.go_to_tasks(browser, case)
    browser.find_element_by_link_text('Initiation').click()
    browser.find_element_by_link_text('Initiation decision').click()
    for note in notes:
        WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(ec.text_to_be_present_in_element((By.CLASS_NAME, 'note-list'), note))


def test_documents(browser):
    """Test you can add documents to a task"""

    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type='Anti-dumping investigation', auto=True, browser=browser)

    documents = [
        Document(
            file_path=os.getcwd() + '/dummy_files/document 1.docx',
            confidential=True,
            friendly_name='My confidential file'),
        Document(
            file_path=os.getcwd() + '/dummy_files/document 2.docx',
            confidential=False,
            friendly_name='My non-confidential file')
    ]

    caseworker.tasks.anti_dumping_investigation.initiation.initiation_decision(
        documents=documents,
        case=case,
        browser=browser
    )

    # Check that the documents are there and downloadable after you navigate away and return
    for document in documents:
        caseworker.tasks.go_to_tasks(browser, case)
        browser.find_element_by_link_text('Initiation').click()
        browser.find_element_by_link_text('Initiation decision').click()
        browser.find_element_by_link_text(document.file_name).click()
        wait_for_download(document.file_name)


