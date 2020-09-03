from datetime import date
import os

from dateutil.relativedelta import relativedelta
import pytest

from admin import Admin
from caseworker import Caseworker
from customer import Customer
from constants import CASE_TYPES, CUSTOMER_CREATEABLE_CASE_TYPES
from functional_tests.test_tasks.helpers import check_case_summary
from workflows import EXPECTED_WORKFLOWS
from fixtures import browser, factory_reset_before_test_module

# TODO: Check the task statuses (check_task_statuses) ie COMPLETED / IN PROGRESS


# Create case

def search_workflow(search_term, workflow):
    if isinstance(workflow, str):
        if search_term.lower() in workflow.lower():
            return True
        else:
            return False
    if isinstance(workflow, list):
        for item in workflow:
            if search_workflow(search_term, item):
                return True
        return False
    elif isinstance(workflow, dict):
        for k, v in workflow.items():
            if search_workflow(search_term, k):
                return True
            elif search_workflow(search_term, v):
                return True
    return False


@pytest.mark.parametrize('case_type', CUSTOMER_CREATEABLE_CASE_TYPES)
def test_customer_created_case_initial_status(browser, case_type):
    """
    Before the full application has been submitted, there should be no 'next notice due' date, since the 40 day
    decision deadline only applies once the application is received.
    """
    # Customer creates a new case
    caseworker = Caseworker()
    customer = Customer(auto=True, browser=browser)

    # Customer creates the shell of a case
    case = customer.apply_for_trade_remedy.create_case(
        case_type=case_type,
        auto=True,
        browser=browser
    )

    # Check initial case status
    check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Created',
            'Next action': 'Assign manager',
            'Next notice due': 'n/a'
        },
        fail_on_error=True
    )


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_ex_officio_case_initial_status(browser, case_type):
    """
    If TRA creates a case ex-officio, the 40 day decision deadline that applies to customer applications does not apply
    so 'next notice due' should be n/a.
    """
    # Create a new ex-officio case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Check initial case status
    check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Created',
            'Next action': 'Assign manager',
            'Next notice due': 'n/a'
        },
        fail_on_error=True
    )


# Assign manager

@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_assign_manager(browser, case_type):

    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Assign manager
    caseworker.tasks.assign_team(
        assign_manager=True,
        case=case,
        browser=browser
    )
    try:
        check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Manager assigned',
                'Next action': 'Assign team members',
                'Next notice due': 'n/a'
            },
            fail_on_error=True
        )
    except:
        if 'transition' in case_type.lower():
            pytest.xfail('TR-1780')


# Assign team

@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_ex_officio_case_assign_team_members(browser, case_type):
    """
    Next action should be 'assessment of the case' because we don't have applications or draft applications for
    ex-officio cases.
    TODO: Why do those sections exist on workflows for ex-officio cases then, they should be removed right?
    """
    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Assign team members
    caseworker.tasks.assign_team(
        assign_team_members=True,
        case=case,
        browser=browser
    )
    try:
        check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Team assigned',
                'Next action': 'Assessment of the case',
                'Next notice due': 'n/a'
            },
            fail_on_error=True
        )
    except:
        pytest.xfail("TR-1781")


@pytest.mark.parametrize('case_type', CUSTOMER_CREATEABLE_CASE_TYPES)
def test_customer_created_case_assign_team_members(browser, case_type):
    """
    Next action should be 'n/a' because we haven't received a draft or full application yet
    """
    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Assign team members
    caseworker.tasks.assign_team(
        assign_team_members=True,
        case=case,
        browser=browser
    )
    check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Team assigned',
            'Next action': 'n/a',
            'Next notice due': 'n/a'
        },
        fail_on_error=True
    )


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_ex_officio_case_assign_team(browser, case_type):
    """
    Next action should be 'assessment of the case' because we don't have applications or draft applications for
    ex-officio cases.
    TODO: Why do those sections exist on workflows for ex-officio cases then, they should be removed right?
    """
    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Assign manager
    caseworker.tasks.assign_team(
        auto=True,
        case=case,
        browser=browser
    )
    try:
        check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Team assigned',
                'Next action': 'Assessment of the case',
                'Next notice due': 'n/a'
            },
            fail_on_error=True
        )
    except:
        pytest.xfail("TR-1781")


@pytest.mark.parametrize('case_type', CUSTOMER_CREATEABLE_CASE_TYPES)
def test_customer_created_case_assign_team(browser, case_type):
    """
    Next action should be 'n/a' because we haven't received a draft or full application yet
    """
    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)

    # Assign manager
    caseworker.tasks.assign_team(
        auto=True,
        case=case,
        browser=browser
    )

    check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Team assigned',
            'Next action': 'n/a',
            'Next notice due': 'n/a'
        },
        fail_on_error=True
    )


# Draft application

@pytest.mark.parametrize('case_type', CUSTOMER_CREATEABLE_CASE_TYPES)
def test_draft_application(browser, case_type):

    # Customer creates a new case
    caseworker = Caseworker()
    customer = Customer(auto=True, browser=browser)

    # Customer submits draft application for review
    case = customer.apply_for_trade_remedy.create_case(
        case_type=case_type,
        auto=True,
        browser=browser
    )
    customer.apply_for_trade_remedy.upload_documents(
        browser=browser,
        case=case,
        files=[os.getcwd() + '/dummy_files/document 1.docx']
    )
    customer.apply_for_trade_remedy.request_review_of_draft_application(
        browser=browser,
        case=case
    )

    check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Draft received',
            'Next action': 'Review draft',
            'Next notice due': 'n/a'
        },
        fail_on_error=True
    )

    caseworker.tasks.draft_application.review_draft(
        browser=browser,
        case=case,
        auto=True
    )

    check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Draft reviewed',
            'Next action': 'n/a',
            'Next notice due': 'n/a'
        },
        fail_on_error=True
    )

    caseworker.tasks.draft_application.draft_review_outcomes(
        browser=browser,
        case=case,
        auto=True
    )

    try:
        check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Awaiting full application',
                'Next action': 'n/a',
                'Next notice due': 'n/a'
            },
            fail_on_error=True
        )
    except:
        pytest.xfail("TR-1776")


# Full application

@pytest.mark.parametrize('case_type', CUSTOMER_CREATEABLE_CASE_TYPES)
def test_full_application(browser, case_type):

    # Customer creates a new case
    caseworker = Caseworker()
    customer = Customer(auto=True, browser=browser)

    # Customer submits full application
    case = customer.apply_for_trade_remedy.create_case(
        case_type=case_type,
        auto=True,
        browser=browser
    )
    customer.apply_for_trade_remedy.upload_documents(
        browser=browser,
        case=case,
        files=[os.getcwd() + '/dummy_files/document 1.docx']
    )
    customer.apply_for_trade_remedy.upload_documents_for_public_file(
        browser=browser,
        case=case,
        files={'document 1.docx': os.getcwd() + '/dummy_files/document 2.docx'}
    )
    customer.apply_for_trade_remedy.check_application(
        browser=browser,
        case=case
    )
    customer.apply_for_trade_remedy.submit_application(
        browser=browser,
        case=case
    )

    check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Application received',
            'Next action': 'Initiation',
            'Next notice due': (date.today() + relativedelta(days=40)).strftime('%d %b %Y')
        },
        fail_on_error=True
    )

    return case  # Allow this test to be used as setup for other tests


# Initiation


@pytest.mark.parametrize('case_type', CUSTOMER_CREATEABLE_CASE_TYPES)
def test_customer_created_case_initiation(browser, case_type):

    # Customer submits a full application
    caseworker = Caseworker()
    case = test_full_application(browser, case_type)
    next_notice_due_days = 40

    # 5 days pass with nobody looking at the case
    admin = Admin()
    days_gone_by = 5
    admin.simulate_passage_of_time(browser, case, days_gone_by)
    next_notice_due_days -= days_gone_by

    # Assessment of the case/application
    if search_workflow('Assessment of the case', EXPECTED_WORKFLOWS[case_type]):
        caseworker.tasks.initiation.assessment_of_the_case(
            auto=True,
            case=case,
            browser=browser
        )
    elif search_workflow('Assessment of the application', EXPECTED_WORKFLOWS[case_type]):
        caseworker.tasks.initiation.assessment_of_the_application(
            auto=True,
            case=case,
            browser=browser
        )
    else:
        raise ValueError()

    # Next notice due date should still be the one set by receipt of the full application, we shouldn't reset it to 40 days
    try:
        check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Case assessed',
                'Next action': 'Initiation preparation',
                'Next notice due': (date.today() + relativedelta(days=next_notice_due_days)).strftime('%d %b %Y')  # To notice of initiation
            },
            fail_on_error=True
        )
    except:
        pytest.xfail('TR-1791 - NoI due date being reset to 40 days')

    days_gone_by = 1
    admin.simulate_passage_of_time(browser, case, days_gone_by)
    next_notice_due_days -= days_gone_by

    # Initiation preparation
    caseworker.tasks.initiation.initiation_preparation(
        auto=True,
        case=case,
        browser=browser
    )
    check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Initiation prepared',
            'Next action': 'Initiation decision',
            'Next notice due': (date.today() + relativedelta(days=next_notice_due_days)).strftime('%d %b %Y')  # To notice of initiation
        },
        fail_on_error=True
    )


@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_ex_officio_case_initiation(browser, case_type):

    # Calculate due date for notice of initiation
    if 'transition' in case_type.lower():
        next_notice_due_days = None
        next_notice_due_date = 'n/a'
    elif 'safeguard' in case_type.lower():
        next_notice_due_days = 30
        next_notice_due_date = (date.today() + relativedelta(days=next_notice_due_days)).strftime('%d %b %Y')
    else:
        next_notice_due_days = 40
        next_notice_due_date = (date.today() + relativedelta(days=next_notice_due_days)).strftime('%d %b %Y')

    # Caseworker creates an ex-officio case
    admin = Admin()
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(browser, case_type, auto=True)

    # Assessment of the case/application
    if search_workflow('Assessment of the case', EXPECTED_WORKFLOWS[case_type]):
        caseworker.tasks.initiation.assessment_of_the_case(
            auto=True,
            case=case,
            browser=browser
        )
    elif search_workflow('Assessment of the application', EXPECTED_WORKFLOWS[case_type]):
        caseworker.tasks.initiation.assessment_of_the_application(
            auto=True,
            case=case,
            browser=browser
        )
    else:
        raise ValueError()

    check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Case assessed',
            'Next action': 'Initiation preparation',
            'Next notice due': next_notice_due_date
        },
        fail_on_error=True
    )

    # A day passes
    days_gone_by = 1
    admin.simulate_passage_of_time(browser, case, days_gone_by)
    if next_notice_due_days is not None:
        next_notice_due_days -= days_gone_by
        next_notice_due_date = (date.today() + relativedelta(days=next_notice_due_days)).strftime('%d %b %Y')

    # Initiation preparation
    caseworker.tasks.initiation.initiation_preparation(
        auto=True,
        case=case,
        browser=browser
    )
    check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Initiation prepared',
            'Next action': 'Initiation decision',
            'Next notice due': next_notice_due_date
        },
        fail_on_error=True
    )
