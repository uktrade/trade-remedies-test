"""
Helper functions used within multiple packages
"""
import os
from time import sleep
from datetime import datetime, timedelta
from contextlib import contextmanager

import pexpect
from selenium.common.exceptions import NoSuchElementException

from configuration import (EXPLICIT_WAIT_SECONDS,
                           IMPLICIT_WAIT_SECONDS,
                           PEXPECT_TIMEOUT_SECONDS,
                           DOWNLOADS_DIRECTORY,
                           DOCKER_API_CONTAINER_NAME,
                           )

@contextmanager
def fail_fast(browser):
    """Temporarily override the implicit wait in cases where you expect a failure and don't want a long delay"""
    browser.implicitly_wait(0.1)
    yield browser
    browser.implicitly_wait(IMPLICIT_WAIT_SECONDS)


def parse_table(browser, table_element, preserve_links=False):
    """
    :param preserve_links: If True, return link elements instead of cell text where links exist
    """
    parsed_table = []
    headings_container = table_element.find_element_by_tag_name('thead')
    heading_elements = headings_container.find_elements_by_tag_name('th')
    headings = [element.text.lower() for element in heading_elements]

    body_container = table_element.find_element_by_tag_name('tbody')
    row_elements = body_container.find_elements_by_tag_name('tr')

    last_value_seen_for_first_column = None
    for row in row_elements:
        parsed_row = {}
        columns = row.find_elements_by_tag_name('td')
        for index, (heading, column) in enumerate(zip(headings, columns)):
            if preserve_links:
                with fail_fast(browser):
                    try:
                        link_element = column.find_element_by_tag_name('a')
                        parsed_row[heading] = link_element
                    except NoSuchElementException:
                        parsed_row[heading] = column.text
            else:
                parsed_row[heading] = column.text
            # Each party is shown once, then each row below that with a blank party cell belongs to the party
            if index == 0:
                if not parsed_row[heading]:
                    parsed_row[heading] = last_value_seen_for_first_column
                else:
                    last_value_seen_for_first_column = parsed_row[heading]
        parsed_table.append(parsed_row)

    return parsed_table


@contextmanager
def connect_to_docker_container():
    # Connect to local docker container
    console = pexpect.spawn(f"docker exec -i -t {DOCKER_API_CONTAINER_NAME} /bin/bash")
    console.timeout = PEXPECT_TIMEOUT_SECONDS
    console.setwinsize(1000, 1000)
    console.expect('/opt/traderemedies/api#')

    try:
        yield console
    finally:
        # Detach from docker
        console.sendcontrol('d')
        # Detach from host
        console.sendcontrol('d')
        console.close()


def input_hs_codes(browser, hs_codes):
    expected_num_hs_code_fields = 1
    for product_classification_code in hs_codes or []:
        browser.find_elements_by_name('hs_code')[-1].send_keys(product_classification_code)
        sleep(1)
        add_link = [elem for elem in browser.find_elements_by_class_name('link') if 'Add' in elem.text][0]
        add_link.click()
        expected_num_hs_code_fields += 1
        start_time = datetime.now()
        while datetime.now() <= start_time + timedelta(seconds=IMPLICIT_WAIT_SECONDS):
            num_hs_code_fields = len(browser.find_elements_by_name('hs_code'))
            if num_hs_code_fields == expected_num_hs_code_fields:
                break
        else:
            raise ValueError(
                "Expected {} hs_code elements, saw {}".format(expected_num_hs_code_fields, num_hs_code_fields))


def click_button_with_text(browser, button_text):
    found_button = False
    find_button_start_time = datetime.now()
    while datetime.now() < find_button_start_time + timedelta(seconds=EXPLICIT_WAIT_SECONDS):
        buttons = browser.find_elements_by_class_name('button') + browser.find_elements_by_tag_name('button')
        for button in buttons:
            if button_text in button.text:
                found_button = True
                if not button.get_attribute('disabled'):
                    button.click()
                    return button
    if found_button:
        raise TimeoutError(f"Timed out waiting for button with text '{button_text}' to be enabled")
    else:
        raise TimeoutError(f"Timed out looking for button with text '{button_text}'")


def wait_for_download(file_name, timeout=10):
    start_time = datetime.now()
    while datetime.now() <= start_time + timedelta(seconds=timeout):
        downloaded_files = os.listdir(DOWNLOADS_DIRECTORY)
        if file_name in downloaded_files:
            return
    else:
        raise TimeoutError
