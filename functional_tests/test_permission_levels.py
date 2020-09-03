import os

import pytest

from caseworker import Caseworker
from fixtures import factory_reset_before_each_test, browser


@pytest.mark.parametrize(
    ['security_group', 'action_allowed'], [
        ('TRA Investigator', False),
        ('Lead Investigator', True),
        ('Head of Investigation', True),
        ('TRA Administrator', True)
    ]
)
def test_publish_to_public_file(browser, security_group, action_allowed):
    super_user = Caseworker()
    case = super_user.new_ex_officio_case(case_type='Anti-dumping investigation', browser=browser, auto=True)

    caseworker = super_user.users.new_investigator(browser, 'a@a.com', 'a', 'Abc123$$$', security_group)

    super_user.assign_team_members(browser, case, caseworker)

    try:
        caseworker.submissions.publish_documents(
            submission_type="Notice of Initiation",
            files=[{'file_path': os.getcwd() + '/dummy_files/document 1.docx', 'confidential': True}],  # TODO: If you mark conf on a file for the public file, what should happen?
            name='My Public Submission',
            description='for automated testing',
            case=case,
            browser=browser
        )
    except PermissionError:
        if action_allowed:
            pytest.fail(f"Investigators in security group '{security_group}' can't publish to the public file")
    else:
        if not action_allowed:
            pytest.fail(f"Investigators in security group '{security_group}' can publish to the public file")
