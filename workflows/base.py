from copy import deepcopy


ASSIGN_TEAM = (
    'Assign team', [
        'Assign manager',
        'Assign team members'
    ]
)

DRAFT_APPLICATION = (
    'Draft application', {
        'Review draft': [
            'Draft review in progress',
            'HMRC confirmations requested'
        ],
        'Draft review outcomes': [
            'HMRC confirmations received',
            'Draft requires review and applicant has been informed',
            'QA review of draft application completed',
            'Draft is sufficient to proceed and applicant has been informed',
            'Draft meets pre-requisite requirements to trigger an investigation'
        ]
    }
)

INITIATION = (
    'Initiation', {
        'Assessment of the application': [
            'Exporters’ foreign government(s) informed',
            'Notification filed to case',
            'Goods description finalised',
            'In scope HS codes finalised',
            'Period for the investigation finalised',
            'Import data assessed',
            'Familiarisation visits completed',
            'Application checklist completed'
        ],
        'Initiation preparation': [
            'Contact details for interested parties identified',
            'Case timeline prepared',
            'Notice of initiation prepared',
            'Notice of initiation correspondence prepared',
            'QA review of preparations completed',
            'PCN (product classification numbers) created',
            'Case title finalised',
            'Case type finalised',
            'Documents available in the system'
        ],
        'Initiation decision': [
            'Decide to initiate'
        ],
        'Publish initiation notices': [
            'Registration of interest documents issued to case',
            'Notice of initiation published',
            'Interested parties notified of initiation',
            'Foreign governments notified of initiation',
            'Notice of initiation URL:'
        ]
    }
)

TRANSITIONAL_INITIATION = deepcopy(INITIATION)
TRANSITIONAL_INITIATION[1]['Publish initiation notices'].remove('Foreign governments notified of initiation')
del TRANSITIONAL_INITIATION[1]['Assessment of the application']
TRANSITIONAL_INITIATION[1]['Assessment of the case'] = [
    'EU cases researched',
    'Goods description finalised',
    'In scope HS codes finalised',
    'Period for the investigation finalised',
    'Import data assessed',
    'Familiarisation visits completed'
]

INVESTIGATION = (
    'Investigation', {
        'Issue questionnaires': [
            'Sample companies selected',
            'Sample notification issued to case record',
            'Non-sampled parties notified',
            'Producer questionnaires issued',
            'Importer questionnaires issued',
            'Exporter questionnaires issued',
            'Government questionnaires issued',
            'Economic interest questionnaires issued'
        ],
        'Process questionnaires': [
            'Non-confidential questionnaires issued to case record - producers',
            'Non-confidential questionnaires issued to case record - importers',
            'Non-confidential questionnaires issued to case record - exporters',
            'Non-confidential questionnaires issued to case record - government',
            'Non-confidential questionnaires issued to case record - economic interest'
        ],
        'Pre-verification analysis': [
            'Deficiency responses received',
            'Preliminary dumping margins calculated',
            'Preliminary injury / causation analysis completed',
            'Preliminary economic interest tests completed'
        ],
        'Verification': [
            'Verification visit plan and tracker created',
            'Travel completed',
            'Verification reports finalised'
        ],
        'Post-verification analysis': [
            'Injury / causation assessment updated with verified data',
            'Economic interest assessments updated with verified data',
            'Causation and non-attribution analysis updated with verified data',
            'Non-confidential verification reports issued to the public file'
        ]
    }
)

PROVISIONAL_DETERMINATION = (
    'Provisional determination', {
        'Prepare the provisional determination': [
            'Provisional determination prepared',
            'Correspondence for SoS prepared',
            'Public notices prepared',
            'QA review of analysis and decision completed',
            'Interested party notification prepared',
            'HMRC notification prepared'
        ],
        'Approve the provisional determination': [
            'Provisional determination approved',
            'Provisional determination sent to SoS',
            'SoS approval of provisional determination granted'
        ],
        'Publish the provisional determination': [
            'Provisional determination published',
            'Section 6p6 notice published',
            'HMRC informed of provisional determination',
            'Governments of exporting countries notified of provisional determination',
            'Interested parties notified',
            'Provisional determination notice URL:'
        ]
    }
)

FINAL_DETERMINATION = (
  'Final determination', {
        'Final analysis': [
            'Subsidy calculations finalised',
            'Injury / causation calculations finalised',
            'Economic interest tests finalised'
        ],
        'Prepare final determination': [
            'Final determination prepared',
            'Documents for DIT tariff team prepared',
            'Correspondence for SoS prepared',
            'Interested party notification prepared',
            'Public notices prepared',
            'QA of final determination decision and documents completed',
            'Relevant documents filed'
        ],
        'Final determination approval': [
            'Final determination approved',
            'SoS office notified of final determination',
            'SoS approval of final determination granted'
        ],
        'Publish final determination': [
            'Final determination and SoS decision published',
            'Interested parties informed',
            'DIT tariff team informed',
            'Foreign government notified',
            'WTO notified',
            'Final determination notice URL:',
            'Relevant documents filed'
        ]
    }
)

HEARINGS_AND_RESPONSES = (
    'Hearings and responses', {
        'Complete hearings': [
            'Hearings completed',
            'Hearing summaries issued to case record'
        ],
        'Process responses to the provisional determination': [
            'Responses to the provisional determination assessed',
            'Non-confidential responses to the provisional determination published',
            'Calculations updated where appropriate'
        ],
        'Assess undertakings': [
            'Undertakings received',
            'Undertakings assessed',
            'Non-confidential undertakings issued to the public file',
            'Measures amended to incorporate undertakings'
        ]
    }
)

DECISIONS_AND_REASONS = (
    'Decisions and Reasons', {
        'Measure type decision and calculations': [
            'Tariff rate quotas will be used',
            'Provisional tariff or tariff rate quotas calculated',
            'Justification for tariff rate quotas uploaded to the system',
            'QA review of analysis and decision completed',
            'SoS informed of intention to use tariff rate quotas',
            'SoS response on tariff rate quotas received'
        ],
        'Statement of Intended Final Determination': [
            'Statement of Intended Final Determination prepared',
            'Statement of Intended Final Determination approved',
            'Statement of Intended Final Determination published',
            'Statement of Intended Final Determination notice URL:'
        ],
        'Hearings and responses': [
            'Hearing summaries issued to case record',
            'Non-confidential responses to Statement of Intended Final Determination published',
            'Responses to Statement of Intended Final Determination analysed'
        ]
    }
)

STATEMENT_OF_ESSENTIAL_FACTS_TRANSITION_CASES = (
    'The Statement of Essential Facts', {
        'The Statement of Essential Facts': [
            'Statement of Essential Facts prepared',
            'Statement of Essential Facts approved',
            'Statement of Essential Facts published',
            'Statement of Essential Facts notice URL:'
        ],
        'Hearings and responses': [
            'Hearings completed',
            'Hearing summaries issued to case record',
            'Non-confidential response to the Statement of Essential Facts published',
            'Responses to the Statement of Essential Facts assessed'
        ]
    }
)

STATEMENT_OF_ESSENTIAL_FACTS_NON_TRANSITION_CASES = (
    'The Statement of Essential Facts', {
        'The Statement of Essential Facts': [
            'Statement of Essential Facts prepared',
            'Statement of Essential Facts approved',
            'Statement of Essential Facts published',
            'Statement of Essential Facts notice URL:'
        ],
        'Process responses to the Statement of Essential Facts': [
            'Responses to the Statement of Essential Facts assessed',
            'Non-confidential responses to the Statement of Essential Facts published'
        ]
    }
)

STATEMENT_OF_INTENDED_FINAL_DETERMINATION = (
    'Statement of Intended Final Determination', {
        'Measure type decision and calculations': [
            'Tariff rate quotas will be used',
            'Provisional tariff or tariff rate quotas calculated',
            'Justification for tariff rate quotas uploaded to the system',
            'QA review of analysis and decision completed',
            'SoS informed of intention to use tariff rate quotas',
            'SoS response on tariff rate quotas received'
        ],
        'Prepare the Statement of Intended Final Determination': [
            'Statement of Intended Final Determination prepared',
            'Correspondence for SoS prepared',
            'Public notices prepared',
            'QA review of analysis and decision completed',
            'Interested party notification prepared',
            'HMRC notification prepared'
        ],
        'Approve the Statement of Intended Final Determination': [
            'Statement of Intended Final Determination approved',
            'Statement of Intended Final Determination sent to SoS',
            'SoS approval of Statement of Intended Final Determination granted'
        ],
        'Publish the Statement of Intended Final Determination': [
            'Statement of Intended Final Determination published',
            'Section 6p6 notice published',
            'HMRC informed of Statement of Intended Final Determination',
            'Governments of exporting countries notified of Statement of Intended Final Determination',
            'Interested parties notified',
            'Statement of Intended Final Determination notice URL:'
        ]
    }
)

RECONSIDERATION = (
    'Reconsideration', {
        'Assessment of the reconsideration': [
            'Reconsideration request received',
            'Assign reconsideration team',
            'Assessment of the request completed',
            'Documents prepared and in the system',
            'QA of documents approved'
        ],
        'Reconsideration initiation decision': [
            'Reconsideration will be initiated',
            'TRID approval of the decision'
        ],
        'Publish reconsideration initiation': [
            'Reconsideration initiation notice published',
            'Interested parties notified of reconsideration',
            'Foreign government notified of reconsideration',
            'Final versions of the reconsideration notices uploaded to the system',
            'Notice of initiation URL'
        ],
        'Reconsideration analysis': [
            'Data reviewed',
            'Economic interest assessments reconsidered',
            'Report on reconsideration outcomes prepared',
            'Amendments to final determination prepared',
            'QA of reconsideration decision and documents completed',
            'Relevant documents filed'
        ],
        'Reconsideration decision': [
            'Reconsideration approved',
            'SoS office notified of reconsideration',
            'SoS approval of final determination granted'
        ],
        'Publish amended final determination': [
            'Amended final determination published',
            'Reconsideration report published',
            'Interested parties informed',
            'DIT tariff team informed',
            'Foreign government notified',
            'WTO notified',
            'Reconsidered final determination notice URL:'
        ],
        'Appeals': [
            'Appeal request received'
        ]
    }
)

CLOSE_CASE = (
    'Close case', {
        'Dismiss case': [
            'Dismissal approved',
            'Relevant documents filed',
            'SoS informed'
        ],
        'Close case': [
            'Investigation completed',
            'Final determination active',
            'Reconsideration complete (where requested)',
            'All necessary files saved to case',
            'Notice reference no:',
            'Case close approved'
        ],
        'Case in appeal': [
            'Request for appeal granted',
            'Appeal outcomes filed to case',
            'Notice amendments filed to case',
            'Case close approved',
            'Notice reference no:'
        ]
    }
)
