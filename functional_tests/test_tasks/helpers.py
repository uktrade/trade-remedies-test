import pytest


# TODO: Set fail_on_error = True by default
def check_case_summary(browser, caseworker, case, expected_case_summary, fail_on_error=False):
    case_summary = caseworker.tasks.parse_case_summary(
        browser=browser,
        case=case
    )
    for key, expected_value in expected_case_summary.items():
        if case_summary[key].lower() != expected_value.lower():
            error_message = f"Case summary was {case_summary}, expected {expected_case_summary}"
            if fail_on_error:
                pytest.fail(error_message)
            else:
                return error_message


def check_task_statuses(browser, caseworker, case, statuses_to_check):
    task_statuses = caseworker.tasks.parse_task_statuses(
        browser=browser,
        case=case
    )
    for task_name, expected_status in statuses_to_check.items():
        actual_status = task_statuses[task_name]
        if not actual_status == expected_status:
            pytest.fail(f"Expected task '{task_name}' to have status '{expected_status}', saw '{actual_status}'")


def check_case_is_archived(browser, case_name, caseworker, customer=None):
    # TODO: Check case is archived on the customer side as well
    cases = caseworker.get_cases(browser=browser)
    for case in cases['current']:
        if case['case name'] == case_name:
            pytest.fail("Case was visible in current cases after close")
    for case in cases['archived']:
        if case['case name'] == case_name:
            break
    else:
        pytest.fail("Case was not visible in archived cases after close")


def get_case_number_for_case_name(browser, caseworker, case_name):
    cases = caseworker.get_cases(browser=browser)
    for case in cases['current']:
        if case['case name'] == case_name:
            return case['no.']
    raise ValueError("No case found with name {}".format(case_name))
