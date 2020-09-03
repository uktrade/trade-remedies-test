from copy import deepcopy

from workflows.base import ASSIGN_TEAM, DRAFT_APPLICATION, INITIATION, INVESTIGATION, PROVISIONAL_DETERMINATION
from workflows.base import FINAL_DETERMINATION, HEARINGS_AND_RESPONSES, RECONSIDERATION, CLOSE_CASE
from workflows.base import STATEMENT_OF_ESSENTIAL_FACTS_NON_TRANSITION_CASES

investigation = deepcopy(INVESTIGATION)
investigation[1]['Pre-verification analysis'].remove('Preliminary dumping margins calculated')
investigation[1]['Pre-verification analysis'].append('Preliminary subsidy margins calculated')

EXPECTED_WORKFLOW = dict((
    ASSIGN_TEAM,
    DRAFT_APPLICATION,
    INITIATION,
    investigation,
    PROVISIONAL_DETERMINATION,
    HEARINGS_AND_RESPONSES,
    STATEMENT_OF_ESSENTIAL_FACTS_NON_TRANSITION_CASES,
    FINAL_DETERMINATION,
    RECONSIDERATION,
    CLOSE_CASE
))
