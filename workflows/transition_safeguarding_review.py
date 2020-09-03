from copy import deepcopy

from workflows.base import ASSIGN_TEAM, TRANSITIONAL_INITIATION, DECISIONS_AND_REASONS, FINAL_DETERMINATION, RECONSIDERATION
from workflows.base import CLOSE_CASE

# NB. Safeguarding cases don't have exporter questionnaires

final_determination = deepcopy(FINAL_DETERMINATION)
final_determination[1]['Final analysis'] = [
    'Injury calculations finalised',
    'Causation and non-attribution finalised',
    'Economic interest tests finalised',
    'Final tariff or tariff rate quota calculated'
]

EXPECTED_WORKFLOW = dict((
    ASSIGN_TEAM,
    TRANSITIONAL_INITIATION,
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
        'Pre-authentication analysis': [  # TODO: Spreadsheet says verification instead of authentication?
            'Deficiency responses received',
            'Preliminary injury analysis completed',
            'Preliminary economic interest tests completed',
            'Causation and non-attribution analysis completed'
        ],
        # TODO: Spreadsheet says verification instead of authentication?
        'Authentication': [
            'Authentication visit plan and tracker created',
            'Travel completed',
            'Authentications finalised'
        ],
        # TODO: Spreadsheet says verification instead of authentication
        'Post-authentication analysis': [
            'Injury / causation assessment updated with authenticated data',
            'Economic interest assessments updated with authenticated data',
            'Causation and non-attribution analysis updated with verified data',  # TODO: Verified or authenticated?
            'Non-confidential authentication reports issued to the public file'
        ]
    }),
    DECISIONS_AND_REASONS,
    final_determination,
    RECONSIDERATION,
    CLOSE_CASE
))
