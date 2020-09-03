from caseworker.tasks.base import Task
from caseworker.tasks.transition_safeguard_review.initiation import Initiation
from caseworker.tasks.transition_safeguard_review.investigation import Investigation
from caseworker.tasks.transition_safeguard_review.decisions_and_reasons import DecisionsAndReasons
from caseworker.tasks.transition_safeguard_review.final_determination import FinalDetermination
from caseworker.tasks.transition_safeguard_review.reconsideration import Reconsideration
from caseworker.tasks.transition_safeguard_review.close_case import CloseCase


class TransitionSafeguardingReview(Task):
    """Task page for Transition Safeguarding Review"""

    def __init__(self, caseworker):
        super().__init__(caseworker=caseworker)
        self.initiation = Initiation(caseworker=caseworker)
        self.investigation = Investigation(caseworker=caseworker)
        self.decisions_and_reasons = DecisionsAndReasons(caseworker=caseworker)
        self.final_determination = FinalDetermination(caseworker=caseworker)
        self.reconsideration = Reconsideration(caseworker=caseworker)
        self.close_case = CloseCase(caseworker=caseworker)
