from caseworker.parties.awaiting_approval import AwaitingApproval


class Parties:

    def __init__(self, caseworker):
        self.caseworker = caseworker
        self.awaiting_approval = AwaitingApproval(caseworker=caseworker)
