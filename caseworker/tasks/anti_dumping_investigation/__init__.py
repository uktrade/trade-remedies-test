from caseworker.tasks.base import Task
from caseworker.tasks.anti_dumping_investigation.review_draft import ReviewDraft
from caseworker.tasks.anti_dumping_investigation.initiation import Initiation
from caseworker.tasks.anti_dumping_investigation.investigation import Investigation
from caseworker.tasks.anti_dumping_investigation.provisional_determination import ProvisionalDetermination
from caseworker.tasks.anti_dumping_investigation.final_determination import FinalDetermination
from caseworker.tasks.anti_dumping_investigation.reconsideration import Reconsideration
from caseworker.tasks.anti_dumping_investigation.close_case import CloseCase
from error_handling import error_handler


class AntiDumpingInvestigation(Task):
    """Task page for Anti Dumping Investigation"""

    def __init__(self, caseworker):
        super().__init__(caseworker=caseworker)
        self.review_draft = ReviewDraft(caseworker=caseworker)
        self.initiation = Initiation(caseworker=caseworker)
        self.investigation = Investigation(caseworker=caseworker)
        self.provisional_determination = ProvisionalDetermination(caseworker=caseworker)
        self.final_determination = FinalDetermination(caseworker=caseworker)
        self.reconsideration = Reconsideration(caseworker=caseworker)
        self.close_case = CloseCase(caseworker=caseworker)


    @error_handler
    def assign_team(self, browser, case, assign_manager=None, assign_team_members=None):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """

        # Navigate to task
        task_name = 'Assign team'
        self.go_to_tasks(browser=browser, case=case)
        browser.find_element_by_link_text(task_name).click()

        # Fill form
        value_for_form_field = {
            'Assign manager': assign_manager,
            'Assign team members': assign_team_members
        }
        self._submit_form(browser=browser, form_values_to_set=value_for_form_field)
