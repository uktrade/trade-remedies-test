from caseworker.tasks.base import Task
from caseworker.tasks.draft_application import DraftApplication
from caseworker.tasks.initiation import Initiation
from caseworker.tasks.investigation import Investigation
from caseworker.tasks.provisional_determination import ProvisionalDetermination
from caseworker.tasks.hearings_and_responses import HearingsAndResponses
from caseworker.tasks.decisions_and_reasons import DecisionsAndReasons
from caseworker.tasks.statement_of_essential_facts import StatementOfEssentialFacts
from caseworker.tasks.statement_of_intended_final_determination import StatementOfIntendedFinalDetermination
from caseworker.tasks.final_determination import FinalDetermination
from caseworker.tasks.reconsideration import Reconsideration
from caseworker.tasks.close_case import CloseCase
from caseworker.tasks.anti_dumping_investigation import AntiDumpingInvestigation
from caseworker.tasks.transition_safeguard_review import TransitionSafeguardingReview
from caseworker.tasks.transition_anti_subsidy_review import TransitionAntiSubsidyReview

from error_handling import error_handler


class Tasks(Task):

    def __init__(self, caseworker):
        super().__init__(caseworker=caseworker)

        # Generic methods
        self.draft_application = DraftApplication(caseworker=caseworker)
        self.initiation = Initiation(caseworker=caseworker)
        self.investigation = Investigation(caseworker=caseworker)
        self.provisional_determination = ProvisionalDetermination(caseworker=caseworker)
        self.hearings_and_responses = HearingsAndResponses(caseworker=caseworker)
        self.decisions_and_reasons = DecisionsAndReasons(caseworker=caseworker)
        self.statement_of_essential_facts = StatementOfEssentialFacts(caseworker=caseworker)
        self.statement_of_intended_final_determination = StatementOfIntendedFinalDetermination(caseworker=caseworker)
        self.final_determination = FinalDetermination(caseworker=caseworker)
        self.reconsideration = Reconsideration(caseworker=caseworker)
        self.close_case = CloseCase(caseworker=caseworker)

        # Methods specific to case types
        self.anti_dumping_investigation = AntiDumpingInvestigation(caseworker=caseworker)
        self.transition_safeguarding_review = TransitionSafeguardingReview(caseworker=caseworker)
        self.transition_anti_subsidy_review = TransitionAntiSubsidyReview(caseworker=caseworker)

    @error_handler
    def assign_team(self, browser, case, assign_manager=None, assign_team_members=None, auto=False):
        """
        None -> Perform no action on this input
        True -> Set this input to Yes
        False -> Set this input to No or N/A
        """
        task_name = 'Assign team'
        self.go_to_tasks(browser=browser, case=case)
        if auto:
            self._auto_fill_form(browser=browser, task_name=task_name)
        else:
            browser.find_element_by_link_text(task_name).click()
            value_for_form_field = {
                'Assign manager': assign_manager,
                'Assign team members': assign_team_members
            }
            self._submit_form(browser=browser, form_values_to_set=value_for_form_field)

