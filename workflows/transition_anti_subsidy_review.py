from copy import deepcopy

from workflows.base import ASSIGN_TEAM, TRANSITIONAL_INITIATION, INVESTIGATION, FINAL_DETERMINATION, CLOSE_CASE
from workflows.base import STATEMENT_OF_ESSENTIAL_FACTS_TRANSITION_CASES, RECONSIDERATION

investigation = deepcopy(INVESTIGATION)
investigation[1]['Pre-verification analysis'].remove('Preliminary dumping margins calculated')
investigation[1]['Pre-verification analysis'].append('Preliminary subsidy margins calculated')

EXPECTED_WORKFLOW = dict((
    ASSIGN_TEAM,
    TRANSITIONAL_INITIATION,
    investigation,
    STATEMENT_OF_ESSENTIAL_FACTS_TRANSITION_CASES,
    FINAL_DETERMINATION,
    RECONSIDERATION,
    CLOSE_CASE
))

