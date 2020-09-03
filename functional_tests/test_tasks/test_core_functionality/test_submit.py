from time import sleep

import pytest
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec

from configuration import EXPLICIT_WAIT_SECONDS
from caseworker import Caseworker
from constants import CASE_TYPES
from workflows import EXPECTED_WORKFLOWS
from fixtures import browser, factory_reset_before_test_module


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_submit(browser, case_type, yes_no_na=True):
    """Mark every individual task as done, fill all text fields and submit every form. Check the app doesn't crash."""

    expected_workflow = EXPECTED_WORKFLOWS[case_type]
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    caseworker.tasks.go_to_tasks(case=case, browser=browser)

    for top_level_key, top_level_value in expected_workflow.items():
        # TODO: Remove this hack (skipping reconsiderations)
        if top_level_key == 'Reconsideration':
            continue
        if isinstance(top_level_value, list):
            # Top level section is a link (not an expander)
            caseworker.tasks.go_to_tasks(case=case, browser=browser)
            browser.find_element_by_link_text(top_level_key).click()
            form = caseworker.tasks.parse_form(browser=browser)
            save_and_exit_button = browser.find_elements_by_class_name('button-blue')[-1]
            for task in form.values():
                if task['type'] == 'checkboxes':
                    task[yes_no_na].click()
                elif task['type'] == 'text_field':
                    task['field'].send_keys('https://bogus.com')
                else:
                    raise ValueError
            save_and_exit_button.click()
            WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
                ec.staleness_of(save_and_exit_button)
            )
            # Check we're back at the task list (not on an error page)
            browser.find_element_by_partial_link_text(case)
        elif isinstance(top_level_value, dict):
            # Top level section is an expander
            for second_level_key, second_level_value in top_level_value.items():
                if not isinstance(second_level_value, list):
                    raise TypeError(f"Expected a list, saw {type(second_level_value)}")
                caseworker.tasks.go_to_tasks(case=case, browser=browser)
                _expand(expander_text=top_level_key, browser=browser)
                try:
                    browser.find_elements_by_link_text(second_level_key)[-1].click()
                except IndexError:
                    # Section link is disabled, skip for now (TODO)
                    continue
                form = caseworker.tasks.parse_form(browser=browser)
                save_and_exit_button = browser.find_elements_by_class_name('button-blue')[-1]
                for task in form.values():
                    if task['type'] == 'checkboxes':
                        task[yes_no_na].click()
                    elif task['type'] == 'text_field':
                        task['field'].send_keys('https://bogus.com')
                    else:
                        raise ValueError
                save_and_exit_button.click()
                WebDriverWait(browser, EXPLICIT_WAIT_SECONDS).until(
                    ec.staleness_of(save_and_exit_button)
                )
                # Check we're back at the task list (not on an error page)
                # TODO: Probably want to refactor this into some functions that can be decorated with error handler
                browser.find_element_by_partial_link_text(case)


def _expand(expander_text, browser):
    browser.find_element_by_link_text(expander_text).click()
    sleep(1)
