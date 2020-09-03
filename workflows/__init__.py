from workflows.anti_dumping_investigation import EXPECTED_WORKFLOW as ANTI_DUMPING_INVESTIGATION_WORKFLOW
from workflows.anti_subsidy_investigation import EXPECTED_WORKFLOW as ANTI_SUBSIDY_INVESTIGATION_WORKFLOW
from workflows.safeguarding import EXPECTED_WORKFLOW as SAFEGUARDING_WORKFLOW
from workflows.transition_anti_dumping_review import EXPECTED_WORKFLOW as TRANSITION_ANTI_DUMPING_REVIEW_WORKFLOW
from workflows.transition_anti_subsidy_review import EXPECTED_WORKFLOW as TRANSITION_ANTI_SUBSIDY_REVIEW_WORKFLOW
from workflows.transition_safeguarding_review import EXPECTED_WORKFLOW as TRANSITION_SAFEGUARDING_REVIEW_WORKFLOW

EXPECTED_WORKFLOWS = {
    'Anti-dumping investigation': ANTI_DUMPING_INVESTIGATION_WORKFLOW,
    'Anti-subsidy investigation': ANTI_SUBSIDY_INVESTIGATION_WORKFLOW,
    'Safeguarding': SAFEGUARDING_WORKFLOW,
    'Safeguard suspension review': SAFEGUARDING_WORKFLOW,
    'Safeguard extension review': SAFEGUARDING_WORKFLOW,
    'Safeguard mid-term review': SAFEGUARDING_WORKFLOW,
    'Safeguard discontinuation': SAFEGUARDING_WORKFLOW,
    'Transition anti-dumping review': TRANSITION_ANTI_DUMPING_REVIEW_WORKFLOW,
    'Transition anti-subsidy review': TRANSITION_ANTI_SUBSIDY_REVIEW_WORKFLOW,
    'Transition safeguarding review': TRANSITION_SAFEGUARDING_REVIEW_WORKFLOW,
    'Absorption review': ANTI_DUMPING_INVESTIGATION_WORKFLOW,
    'Scope review': ANTI_DUMPING_INVESTIGATION_WORKFLOW,
    'Circumvention review': ANTI_DUMPING_INVESTIGATION_WORKFLOW,
    'Undertaking review': ANTI_DUMPING_INVESTIGATION_WORKFLOW,
    'New exporter review': ANTI_DUMPING_INVESTIGATION_WORKFLOW,
    'Refund request': ANTI_DUMPING_INVESTIGATION_WORKFLOW,
    'Expiry review': ANTI_DUMPING_INVESTIGATION_WORKFLOW,
    'Interim review': ANTI_DUMPING_INVESTIGATION_WORKFLOW,
    'Suspension review': ANTI_DUMPING_INVESTIGATION_WORKFLOW,
    'Dispute ruling': ANTI_DUMPING_INVESTIGATION_WORKFLOW
}
