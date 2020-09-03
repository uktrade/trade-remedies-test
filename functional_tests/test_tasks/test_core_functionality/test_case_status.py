from datetime import date

import pytest
from dateutil.relativedelta import relativedelta

from caseworker import Caseworker
from constants import CASE_TYPES
from workflows import EXPECTED_WORKFLOWS
from functional_tests.test_tasks.helpers import check_case_summary, check_task_statuses, check_case_is_archived
from fixtures import browser, factory_reset_before_test_module


@pytest.mark.skip("These tests are being migrated to a new style in test_status_widget")
@pytest.mark.parametrize('case_type', CASE_TYPES)
def test_status_changes(browser, case_type):

    expected_workflow = EXPECTED_WORKFLOWS[case_type]

    skipped_tasks = [
        # Reconsideration (TODO: Need to test these separately)
        'Reconsideration',
        'Assessment of the Reconsideration',
        'Reconsideration initiation decision',
        'Publish reconsideration initiation',
        'Reconsideration analysis',
        'Reconsideration decision',
        'Amended final determination published',
        'Appeals',
        # Close case tasks (can't close it all three ways)
        'Dismiss case',
        'Case in appeal'
    ]

    errors = []

    # Create a new case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type=case_type, auto=True, browser=browser)
    errors.append(check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Created',
            'Next action': 'Assign manager',
            'Next notice due': 'n/a'
        }
    ))

    # Assign manager
    caseworker.tasks.assign_team(
        assign_manager=True,
        case=case,
        browser=browser
    )
    check_task_statuses(
        browser=browser,
        caseworker=caseworker,
        case=case,
        statuses_to_check={
            'Assign team': 'in progress',
        }
    )
    errors.append(check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Manager assigned',
            'Next action': 'Assign investigation team',
            'Next notice due': (date.today() + relativedelta(days=40)).strftime('%d %b %Y')  # To initiation
        }
    ))

    # Assign team
    caseworker.tasks.assign_team(
        assign_investigation_team=True,
        case=case,
        browser=browser
    )
    check_task_statuses(
        browser=browser,
        caseworker=caseworker,
        case=case,
        statuses_to_check={
            'Assign team': 'completed',
        }
    )
    errors.append(check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Team assigned',
            'Next action': 'Assessment of the case',
            'Next notice due': (date.today() + relativedelta(days=40)).strftime('%d %b %Y')  # To initiation
        }
    ))

    # Draft application
    if 'Draft application' in expected_workflow:
        caseworker.tasks.draft_application.review_draft(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Draft reviewed',
                'Next action': 'n/a',
                'Next notice due': 'n/a'
            }
        ))
        caseworker.tasks.draft_application.draft_review_outcomes(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Application received',
                'Next action': 'Assessment of the application',
                'Next notice due': 'n/a'
            }
        ))

    # Initiation
    if 'Assessment of the case' in expected_workflow['Initiation']:
        caseworker.tasks.initiation.assessment_of_the_case(
            auto=True,
            case=case,
            browser=browser
        )
        check_task_statuses(
            browser=browser,
            caseworker=caseworker,
            case=case,
            statuses_to_check={
                'Assessment of the case': 'completed'
            }
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Case assessed',
                'Next action': 'Initiation preparation',
                'Next notice due': (date.today() + relativedelta(days=40)).strftime('%d %b %Y')  # To initiation
            }
        ))
    elif 'Assessment of the application' in expected_workflow['Initiation']:
        caseworker.tasks.initiation.assessment_of_the_application(
            auto=True,
            case=case,
            browser=browser
        )
        check_task_statuses(
            browser=browser,
            caseworker=caseworker,
            case=case,
            statuses_to_check={
                'Assessment of the application': 'completed'
            }
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Application assessed',
                'Next action': 'Initiation preparation',
                'Next notice due': (date.today() + relativedelta(days=40)).strftime('%d %b %Y')  # To initiation
            }
        ))
    else:
        raise ValueError()
    caseworker.tasks.initiation.initiation_preparation(
        auto=True,
        case=case,
        browser=browser
    )
    errors.append(check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Initiation prepared',
            'Next action': 'Initiation decision',
            'Next notice due': (date.today() + relativedelta(days=40)).strftime('%d %b %Y')  # To initiation
        }
    ))
    caseworker.tasks.initiation.initiation_decision(
        auto=True,
        case=case,
        browser=browser
    )
    errors.append(check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'To be initiated',
            'Next action': 'Publish initiation notices',
            'Next notice due': (date.today() + relativedelta(days=40)).strftime('%d %b %Y')  # To initiation
        }
    ))
    caseworker.tasks.initiation.publish_initiation_notices(
        auto=True,
        case=case,
        browser=browser
    )

    if 'Decisions and Reasons' in expected_workflow:
        next_notice_due = (date.today() + relativedelta(days=191)).strftime('%d %b %Y')  # To SoIFD
    elif 'The Statement of Essential Facts' in expected_workflow:
        next_notice_due = (date.today() + relativedelta(days=227)).strftime('%d %b %Y')  # To SoEF
    else:
        raise ValueError("Expected 'Decisions and Reasons' or 'The Statement of Essential Facts'")

    errors.append(check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Case initiated',
            'Next action': 'Issue questionnaires',
            'Next notice due': next_notice_due
        }
    ))

    # Investigation
    caseworker.tasks.investigation.issue_questionnaires(
        auto=True,
        case=case,
        browser=browser
    )
    errors.append(check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Questionnaires issued',
            'Next action': 'Process questionnaires',
            'Next notice due': next_notice_due
        }
    ))

    if 'Verification' in expected_workflow['Investigation']:
        caseworker.tasks.investigation.process_questionnaires(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Questionnaires processed',
                'Next action': 'Pre-verification data analysis',
                'Next notice due': next_notice_due
            }
        ))
        caseworker.tasks.investigation.pre_verification_data_analysis(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Data analysed',
                'Next action': 'Verification',
                'Next notice due': next_notice_due
            }
        ))
        caseworker.tasks.investigation.verification(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Verifications complete',
                'Next action': 'Post-verification analysis',
                'Next notice due': next_notice_due
            }
        ))
        caseworker.tasks.investigation.post_verification_data_analysis(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Verifications analysed',
                'Next action': 'Decide measure type' if 'Decisions and Reasons' in expected_workflow else 'The Statement of Essential Facts',
                'Next notice due': next_notice_due
            }
        ))
    elif 'Authentication' in expected_workflow['Investigation']:
        caseworker.tasks.investigation.process_questionnaires(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Questionnaires processed',
                'Next action': 'Pre-authentication data analysis',
                'Next notice due': next_notice_due
            }
        ))
        caseworker.tasks.investigation.pre_authentication_data_analysis(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Data analysed',
                'Next action': 'Authentication',
                'Next notice due': next_notice_due
            }
        ))
        caseworker.tasks.investigation.authentication(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Authentications complete',
                'Next action': 'Post authentication analysis',
                'Next notice due': next_notice_due
            }
        ))
        caseworker.tasks.investigation.post_authentication_analysis(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Authentications analysed',
                'Next action': 'Decide measure type',
                'Next notice due': next_notice_due
            }
        ))
    else:
        raise ValueError("Expected either 'Verification' or 'Authentication'")

    if 'Provisional determination' in expected_workflow:
        # Provisional determination
        caseworker.tasks.provisional_determination.prepare_the_provisional_determination(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Provisional determination prepared',
                'Next action': 'Approve the provisional determination',
                'Next notice due': (date.today() + relativedelta(days=182)).strftime('%d %b %Y')  # TODO: Check against spreadsheet
            }
        ))
        caseworker.tasks.provisional_determination.approve_the_provisional_determination(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Provisional determination approved',
                'Next action': 'Publish the provisional determination',
                'Next notice due': (date.today() + relativedelta(days=14)).strftime('%d %b %Y')  # TODO: Check against spreadsheet
            }
        ))
        caseworker.tasks.provisional_determination.publish_the_provisional_determination(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Provisional determination approved',  # TODO: Bug? Should be published! Is the status change being triggered by the actual publication? Is that how we want it?!
                'Next action': 'Complete hearings',
                'Next notice due': (date.today() + relativedelta(days=14)).strftime('%d %b %Y')  # TODO: Check against spreadsheet
            }
        ))

    if 'Hearings and responses' in expected_workflow:
        # Hearings and responses
        caseworker.tasks.hearings_and_responses.complete_hearings(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Hearings completed',
                'Next action': 'Process responses to the provisional determination',
                'Next notice due': (date.today() + relativedelta(days=14)).strftime('%d %b %Y')  # TODO: Check against spreadsheet
            }
        ))
        caseworker.tasks.hearings_and_responses.process_responses_to_the_provisional_determination(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Provisional determination responses processed',
                'Next action': 'Assess undertakings',
                'Next notice due': (date.today() + relativedelta(days=14)).strftime('%d %b %Y')  # TODO: Check against spreadsheet
            }
        ))
        caseworker.tasks.hearings_and_responses.assess_undertakings(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Undertakings assessed',
                'Next action': 'The Statement of Essential Facts',
                'Next notice due': (date.today() + relativedelta(days=14)).strftime('%d %b %Y')  # TODO: Check against spreadsheet
            }
        ))

    if 'Decisions and Reasons' in expected_workflow:
        # Decisions and Reasons
        caseworker.tasks.decisions_and_reasons.measure_type_decision_and_calculations(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Measure type decided',
                'Next action': 'Statement of Intended Final Determination',
                'Next notice due': next_notice_due
            }
        ))
        caseworker.tasks.decisions_and_reasons.statement_of_intended_final_determination(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Statement of Intended Final Determination - response window open',
                'Next action': 'Hearings and responses',
                'Next notice due': (date.today() + relativedelta(days=87)).strftime('%d %b %Y')  # To FD
            }
        ))
        caseworker.tasks.decisions_and_reasons.hearings_and_responses(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Hearings and responses complete',
                'Next action': 'Final analysis',
                'Next notice due': (date.today() + relativedelta(days=87)).strftime('%d %b %Y')  # To FD
            }
        ))

    # Anti dumping, anti subsidy: separate hearings and responses
    # Safeguard: seperate hearings and responses (no SoEF section at all)
    # ONLY trans reviews will have H&R as a subsection of SoEF

    elif 'The Statement of Essential Facts' in expected_workflow:
        caseworker.tasks.statement_of_essential_facts.statement_of_essential_facts(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Statement of Essential Facts - response window open',
                'Next action': 'Hearings and responses',
                'Next notice due': (date.today() + relativedelta(days=87)).strftime('%d %b %Y')  # To FD
            }
        ))
        if 'Process responses to the Statement of Essential Facts' in expected_workflow['The Statement of Essential Facts']:
            caseworker.tasks.statement_of_essential_facts.process_responses_to_the_statement_of_essential_facts(
                auto=True,
                case=case,
                browser=browser
            )
            errors.append(check_case_summary(
                browser=browser,
                caseworker=caseworker,
                case=case,
                expected_case_summary={
                    'Current stage': 'Responses to Statement of Essential Facts completed',
                    'Next action': 'Final analysis',
                    'Next notice due': (date.today() + relativedelta(days=21)).strftime('%d %b %Y')  # TODO: Check against spreadsheet
                }
            ))
        elif 'Hearings and responses' in expected_workflow['The Statement of Essential Facts']:
            caseworker.tasks.statement_of_essential_facts.hearings_and_responses(
                auto=True,
                case=case,
                browser=browser
            )
            errors.append(check_case_summary(
                browser=browser,
                caseworker=caseworker,
                case=case,
                expected_case_summary={
                    'Current stage': 'Hearings and responses complete',
                    'Next action': 'Final analysis',
                    'Next notice due': (date.today() + relativedelta(days=87)).strftime('%d %b %Y')  # To FD
                }
            ))
        else:
            raise ValueError(
                "Expected 'Process responses to the Statement of Essential Facts' or 'Hearings and responses'")
    else:
        raise ValueError("Expected either 'Decisions and Reasons' or 'The Statement of Essential Facts'")

    # Final determination
    caseworker.tasks.final_determination.final_analysis(
        auto=True,
        case=case,
        browser=browser
    )
    errors.append(check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Final analysis complete',
            'Next action': 'Prepare final determination',
            'Next notice due': (date.today() + relativedelta(days=87)).strftime('%d %b %Y')  # To FD
        }
    ))
    caseworker.tasks.final_determination.prepare_final_determination(
        auto=True,
        case=case,
        browser=browser
    )
    errors.append(check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Final determination prepared',
            'Next action': 'Final determination approval',
            'Next notice due': (date.today() + relativedelta(days=87)).strftime('%d %b %Y')  # To FD
        }
    ))
    caseworker.tasks.final_determination.final_determination_approval(
        auto=True,
        case=case,
        browser=browser
    )
    errors.append(check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Final determination approved',
            'Next action': 'Publish final determination',
            'Next notice due': (date.today() + relativedelta(days=87)).strftime('%d %b %Y')  # To FD
        }
    ))
    caseworker.tasks.final_determination.publish_final_determination(
        auto=True,
        case=case,
        browser=browser
    )
    errors.append(check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Current stage': 'Final determination published',
            'Next action': 'Check for reconsideration requests',
            'Next notice due': 'n/a'  # To reconsideration init OR case close
        }
    ))

    if 'Reconsideration' in expected_workflow:
        # Reconsideration
        caseworker.tasks.reconsideration.assessment_of_the_reconsideration(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Reconsideration assessed',
                'Next action': 'n/a',
                'Next notice due': (date.today() + relativedelta(days=25)).strftime('%d %b %Y')  # TODO: Check
            }
        ))
        caseworker.tasks.reconsideration.reconsideration_initiation_decision(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Reconsideration initiated',
                'Next action': 'n/a',
                'Next notice due': (date.today() + relativedelta(days=25)).strftime('%d %b %Y')  # TODO: Check
            }
        ))
        caseworker.tasks.reconsideration.publish_reconsideration_initiation(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Reconsideration initiation published',
                'Next action': 'n/a',
                'Next notice due': (date.today() + relativedelta(days=65)).strftime('%d %b %Y')  # TODO: Check
            }
        ))
        caseworker.tasks.reconsideration.reconsideration_analysis(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Reconsideration analysed',
                'Next action': 'n/a',
                'Next notice due': (date.today() + relativedelta(days=65)).strftime('%d %b %Y')  # TODO: Check
            }
        ))
        caseworker.tasks.reconsideration.reconsideration_decision(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Reconsideration decided',
                'Next action': 'n/a',
                'Next notice due': (date.today() + relativedelta(days=65)).strftime('%d %b %Y')  # TODO: Check
            }
        ))
        caseworker.tasks.reconsideration.publish_amended_final_determination(
            auto=True,
            case=case,
            browser=browser
        )
        errors.append(check_case_summary(
            browser=browser,
            caseworker=caseworker,
            case=case,
            expected_case_summary={
                'Current stage': 'Amended final determination published',
                'Next action': 'n/a',
                'Next notice due': (date.today() + relativedelta(days=30)).strftime('%d %b %Y')  # TODO: Check
            }
        ))
        # Completing this task disables close case task, which we want to test
        # caseworker.tasks.reconsideration.appeals(
        #     auto=True,
        #     case=case,
        #     browser=browser
        # )
        # errors.append(check_case_summary(
        #     browser=browser,
        #     caseworker=caseworker,
        #     case=case,
        #     expected_case_summary={
        #         'Current stage': 'Amended final determination published',  # BUG! No change
        #         'Next action': 'n/a',
        #         'Next notice due': (date.today() + relativedelta(days=30)).strftime('%d %b %Y')  # TODO: Check
        #     }
        # ))

    # Close the case
    caseworker.tasks.close_case.close_case(
        auto=True,
        case=case,
        browser=browser
    )
    errors.append(check_case_summary(
        browser=browser,
        caseworker=caseworker,
        case=case,
        expected_case_summary={
            'Archived': 'Case closed'
        }
    ))

    # TODO: After closing case, it's worth checking the status/next action on dashboard
    #     since I found a bug in this for trans AD, might exist elsewhere
    check_case_is_archived(caseworker=caseworker, case_name=case, browser=browser)

    # Check that we haven't missed any tasks / all expected tasks are marked completed
    # TODO: Write a separate test to check the in-progress status works for part-complete tasks and task groups
    task_statuses = caseworker.tasks.parse_task_statuses(browser=browser, case=case)
    for task_name, status in task_statuses.items():
        if task_name in skipped_tasks:
            continue
        if isinstance(status, list):
            for status_ in status:
                if status_ != 'completed':
                    errors.insert(0, f"Task '{task_name}' had status '{status_}', expected 'completed'")
        else:
            if status != 'completed':
                errors.insert(0, f"Task '{task_name}' had status '{status}', expected 'completed'")

    if any(errors):
        errors = [error for error in errors if error is not None]
        pytest.fail('\n'+'\n\n'.join(errors))



