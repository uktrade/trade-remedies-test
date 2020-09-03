from copy import deepcopy

from workflows.base import ASSIGN_TEAM, TRANSITIONAL_INITIATION, INVESTIGATION, FINAL_DETERMINATION, CLOSE_CASE
from workflows.base import STATEMENT_OF_ESSENTIAL_FACTS_TRANSITION_CASES, RECONSIDERATION

investigation = deepcopy(INVESTIGATION)
investigation[1]['Issue questionnaires'].remove('Government questionnaires issued')
investigation[1]['Process questionnaires'].remove('Non-confidential questionnaires issued to case record - government')

final_determination = deepcopy(FINAL_DETERMINATION)
final_determination[1]['Final analysis'].remove('Subsidy calculations finalised')
final_determination[1]['Final analysis'].append('Dumping calculations finalised')

EXPECTED_WORKFLOW = dict((
    ASSIGN_TEAM,
    TRANSITIONAL_INITIATION,
    investigation,
    STATEMENT_OF_ESSENTIAL_FACTS_TRANSITION_CASES,
    final_determination,
    # TODO: Need to check reconsideration tasks against the ticket (spreadsheet is a lie)
    RECONSIDERATION,
    CLOSE_CASE
))
