from copy import deepcopy

from workflows.base import ASSIGN_TEAM, DRAFT_APPLICATION, STATEMENT_OF_INTENDED_FINAL_DETERMINATION
from workflows.base import FINAL_DETERMINATION, CLOSE_CASE, INITIATION, HEARINGS_AND_RESPONSES, RECONSIDERATION

final_determination = deepcopy(FINAL_DETERMINATION)
final_determination[1]['Final analysis'].remove('Subsidy calculations finalised')

initiation = deepcopy(INITIATION)
initiation[1]['Assessment of the application'].remove('Exporters’ foreign government(s) informed')
initiation[1]['Assessment of the application'].remove('Application checklist completed')
initiation[1]['Publish initiation notices'].remove('Foreign governments notified of initiation')

hearings_and_responses = deepcopy(HEARINGS_AND_RESPONSES)
del hearings_and_responses[1]['Assess undertakings']
hearings_and_responses[1]['Process responses to the Statement of Intended Final Determination'] = hearings_and_responses[1]['Process responses to the provisional determination']
del hearings_and_responses[1]['Process responses to the provisional determination']
hearings_and_responses[1]['Process responses to the Statement of Intended Final Determination'].remove('Responses to the provisional determination assessed')
hearings_and_responses[1]['Process responses to the Statement of Intended Final Determination'].remove('Non-confidential responses to the provisional determination published')
hearings_and_responses[1]['Process responses to the Statement of Intended Final Determination'].append('Responses to the Statement of Intended Final Determination assessed')
hearings_and_responses[1]['Process responses to the Statement of Intended Final Determination'].append('Non-confidential responses to the Statement of Intended Final Determination published')

EXPECTED_WORKFLOW = dict((
    ASSIGN_TEAM,
    DRAFT_APPLICATION,
    initiation,
    ('Investigation', {
        'Issue questionnaires': [
            'Sample companies selected',
            'Sample notification issued to case record',
            'Non-sampled parties notified',
            'Producer questionnaires issued',
            'Importer questionnaires issued',
            'Economic interest questionnaires issued'
            ],
        'Process questionnaires': [
            'Non-confidential questionnaires issued to case record - producers',
            'Non-confidential questionnaires issued to case record - importers',
            'Non-confidential questionnaires issued to case record - economic interest'
            ],
        'Pre-authentication analysis': [
            'Deficiency responses received',
            'Preliminary injury analysis completed',
            'Preliminary economic interest tests completed',
            'Causation and non-attribution analysis completed'
            ],
        'Authentication': [
            'Authentication visit plan and tracker created',
            'Travel completed',
            'Authentication reports finalised'
            ],
        'Post-authentication analysis': [
            'Injury / causation assessment updated with authenticated data',
            'Economic interest assessments updated with authenticated data',
            'Causation and non-attribution analysis updated with authenticated data',
            'Non-confidential authentication reports issued to the public file'
            ]
        }
     ),
    STATEMENT_OF_INTENDED_FINAL_DETERMINATION,
    hearings_and_responses,
    final_determination,
    RECONSIDERATION,
    CLOSE_CASE
))
