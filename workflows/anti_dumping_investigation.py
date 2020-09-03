from copy import deepcopy

from workflows.base import ASSIGN_TEAM, DRAFT_APPLICATION, INITIATION, INVESTIGATION, PROVISIONAL_DETERMINATION
from workflows.base import FINAL_DETERMINATION, HEARINGS_AND_RESPONSES, RECONSIDERATION, CLOSE_CASE
from workflows.base import STATEMENT_OF_ESSENTIAL_FACTS_NON_TRANSITION_CASES

investigation = deepcopy(INVESTIGATION)
investigation[1]['Issue questionnaires'].remove('Government questionnaires issued')
investigation[1]['Process questionnaires'].remove('Non-confidential questionnaires issued to case record - government')

final_determination = deepcopy(FINAL_DETERMINATION)
final_determination[1]['Final analysis'].remove('Subsidy calculations finalised')
final_determination[1]['Final analysis'].append('Dumping calculations finalised')

EXPECTED_WORKFLOW = dict((
    ASSIGN_TEAM,
    DRAFT_APPLICATION,
    INITIATION,
    investigation,
    PROVISIONAL_DETERMINATION,
    HEARINGS_AND_RESPONSES,
    STATEMENT_OF_ESSENTIAL_FACTS_NON_TRANSITION_CASES,
    final_determination,
    RECONSIDERATION,
    CLOSE_CASE
))
