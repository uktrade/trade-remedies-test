from contextlib import contextmanager
from copy import copy
from time import sleep

import pytest
from selenium.common.exceptions import NoSuchElementException

from caseworker import Caseworker
from constants import CASE_TYPES
from workflows import EXPECTED_WORKFLOWS
from fixtures import browser, factory_reset_before_test_module


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_workflow_text(browser, case_type):
    """Check that the workflow text on the UI matches the workflow text defined in this test repository"""

    expected_workflow = EXPECTED_WORKFLOWS[case_type]

    errors = []

    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    caseworker.tasks.go_to_tasks(case=case, browser=browser)

    # Check top level sections
    expected_top_level_sections = expected_workflow.keys()
    top_level_sections = _get_task_list_visible_items(browser=browser)
    _compare(
        item_type='top level sections',
        expected=expected_top_level_sections,
        actual=top_level_sections,
        errors=errors
    )
    if errors:
        pytest.fail('\n'.join(errors))

    # Check subsections
    for top_level_key, top_level_value in expected_workflow.items():
        if isinstance(top_level_value, dict):
            # Top level section should be an expander
            visible_items_before_expansion = _get_task_list_visible_items(browser=browser)
            with _no_url_change_expected(browser):
                # Expand top level section
                _expand(expander_text=top_level_key, browser=browser)
                sleep(1)
            visible_items_after_expansion = _get_task_list_visible_items(browser=browser)
            expected_subsections = top_level_value.keys()
            subsections = _difference(visible_items_after_expansion, visible_items_before_expansion)
            _compare(
                item_type=f"subsections under '{top_level_key}' section",
                expected=expected_subsections,
                actual=subsections,
                errors=errors
            )

    if errors:
        pytest.fail('\n'.join(errors))

    # Check individual tasks
    for top_level_key, top_level_value in expected_workflow.items():
        # TODO: Remove this hack (skipping reconsiderations)
        if top_level_key == 'Reconsideration':
            continue
        if isinstance(top_level_value, list):
            # Top level section is a link (not an expander)
            caseworker.tasks.go_to_tasks(case=case, browser=browser)
            browser.find_element_by_link_text(top_level_key).click()
            form = caseworker.tasks.parse_form(browser=browser)
            expected_tasks = top_level_value
            actual_tasks = form.keys()
            _compare(
                item_type=f"tasks on '{top_level_key}' page",
                expected=expected_tasks,
                actual=actual_tasks,
                errors=errors
            )
        elif isinstance(top_level_value, dict):
            # Top level section is an expander
            for second_level_key, second_level_value in top_level_value.items():
                if not isinstance(second_level_value, list):
                    raise TypeError(f"Expected a list, saw {type(second_level_value)}")
                caseworker.tasks.go_to_tasks(case=case, browser=browser)
                expanded_section = _expand(expander_text=top_level_key, browser=browser)
                try:
                    expanded_section.find_element_by_link_text(second_level_key).click()
                except NoSuchElementException:
                    assert second_level_key in browser.page_source
                    # Section link is disabled, skip for now (TODO)
                    continue
                form = caseworker.tasks.parse_form(browser=browser)
                expected_tasks = second_level_value
                actual_tasks = form.keys()
                _compare(
                    item_type=f"tasks on '{second_level_key}' page",
                    expected=expected_tasks,
                    actual=actual_tasks,
                    errors=errors
                )

    if errors:
        pytest.fail('\n'.join(errors))


@contextmanager
def _no_url_change_expected(browser):
    url_before = browser.current_url
    yield
    url_after = browser.current_url
    if url_before != url_after:
        pytest.fail(f'Page URL unexpectedly changed from {url_before} to {url_after}')


def _get_task_list_visible_items(browser):
    task_list = browser.find_element_by_class_name('task-list')
    visible_items = []
    for item in task_list.find_elements_by_tag_name('li'):
        if item.text:
            if '\n' in item.text:
                # List item contains further list items (it's an expander)
                visible_items.append(item.text.split('\n')[0])  # Get the expander text ignoring the subsections
            else:
                visible_items.append(item.text)
    return visible_items


def _difference(l1, l2):
    """
    Return items in l1 that do not match a corresponding item in l2. Different to set operator ._difference
    because it handles multiple instances of the same item in l1 or l2, each item corresponds to exactly one other.
    eg l1 = [1,1,2], l2 = [1,2], _difference = [1]
    """
    difference_ = copy(list(l1))
    for item in l2:
        if item in difference_:
            difference_.remove(item)
    return difference_


def _compare(item_type, expected, actual, errors):

    expected_but_not_present = _difference(expected, actual)
    present_but_not_expected = _difference(actual, expected)
    if expected_but_not_present or present_but_not_expected:
        errors.append('\n')
    if expected_but_not_present:
        errors.append(f"Missing {item_type}: \n{expected_but_not_present}")
    if present_but_not_expected:
        errors.append(f"Unexpected {item_type}: \n{present_but_not_expected}")


def _expand(expander_text, browser):
    expander = browser.find_element_by_link_text(expander_text)
    expander.click()
    expanded_section = expander.find_element_by_xpath('../../..').find_element_by_class_name('expand-section')
    return expanded_section
