from datetime import datetime, timedelta
import sys

from pexpect.exceptions import TIMEOUT as PexpectTimeout
from retry import retry
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import ADMIN_BASE_URL, ADMIN_EMAIL, ADMIN_PASSWORD, EXPLICIT_WAIT_SECONDS
from helpers import connect_to_docker_container, fail_fast


@retry(PexpectTimeout, tries=3)
def process_timegate_actions():
    """Trigger processing of timegate actions"""
    with connect_to_docker_container() as console:
        console.sendline('cd trade_remedies_api')
        console.expect('/opt/traderemedies/api/trade_remedies_api')
        console.sendline('python manage.py process_timegate_actions')
        console.expect('Completed processing timegate actions')


class Admin:

    def __init__(self, email=ADMIN_EMAIL, password=ADMIN_PASSWORD):
        self.email = email
        self.password = password

    def sign_in(self, browser):
        browser.get(ADMIN_BASE_URL)

        # Log out if necessary
        try:
            browser.find_element_by_link_text('LOG OUT').click()
            browser.get(ADMIN_BASE_URL)
        except NoSuchElementException:
            pass

        # Log in
        email_field = browser.find_element_by_id('id_username')
        password_field = browser.find_element_by_id('id_password')
        log_in_button = browser.find_elements_by_tag_name('input')[-1]
        email_field.send_keys(self.email or '')
        password_field.send_keys(self.password or '')
        log_in_button.click()

    @staticmethod
    def _parse_table(browser):
        parsed_table = []
        table = browser.find_element_by_id('result_list')
        table_body = table.find_element_by_tag_name('tbody')
        rows = table_body.find_elements_by_tag_name('tr')
        for row in rows:
            link_element = row.find_element_by_tag_name('a')
            case = row.find_element_by_class_name('field-case').text
            key_ = row.find_element_by_class_name('field-key').text
            value = row.find_element_by_class_name('field-value').text
            due_date_ = row.find_element_by_class_name('field-due_date').text
            parsed_table.append(
                {
                    'link_element': link_element,
                    'case': case,
                    'key': key_,
                    'value': value,
                    'due_date': due_date_,
                }
            )
        return parsed_table

    def simulate_passage_of_time(self, browser, case, days):
        """Go through all case workflow states for case. If a due date exists, set it back by the specified no of days"""

        self.sign_in(browser=browser)

        browser.find_element_by_link_text('Case workflow states').click()

        # Filter by case to avoid sifting through multiple pages when lots of cases are present
        with fail_fast(browser):
            paginator = browser.find_element_by_class_name('paginator')
            try:
                filters = browser.find_element_by_id('changelist-filter')
            except NoSuchElementException:
                # Num cases <=1 so no case filter is present
                pass
            else:
                # Filter by case
                filters.find_element_by_partial_link_text(case).click()
                WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(ec.staleness_of(paginator))

        modified_row_keys = []
        start_time = datetime.now()
        timeout_minutes = 5
        while datetime.now() <= start_time + timedelta(minutes=timeout_minutes):
            parsed_table = self._parse_table(browser)
            for row in parsed_table:
                if case not in row['case']:
                    continue
                if row['key'] not in modified_row_keys and row['due_date'] != '-':
                    row['link_element'].click()
                    due_date_field = browser.find_element_by_id('id_due_date_0')
                    current_value = due_date_field.get_attribute('value')
                    new_value = (datetime.strptime(current_value, '%Y-%m-%d') - timedelta(days=days)).strftime('%Y-%m-%d')
                    due_date_field.clear()
                    due_date_field.send_keys(new_value)
                    browser.find_element_by_name('_save').click()
                    if 'changed successfully' not in browser.page_source:
                        raise Exception("Failed to modify due date")
                    else:
                        modified_row_keys.append(row['key'])
                        break
            else:
                # Reached end of table, no more rows need editing
                break
        else:
            raise TimeoutError("Timed out while modifying case workflow state due dates")

        process_timegate_actions()
