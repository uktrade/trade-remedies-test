from copy import copy

from bs4 import BeautifulSoup
from locust import HttpLocust, TaskSequence, seq_task
from locust.exception import StopLocust

# Caseworker host configuration
CASEWORKER_HOST = 'caseworker.traderemedies-uat.uktrade.io'
CASEWORKER_BASE_URL = 'https://' + CASEWORKER_HOST

# Caseworker account
CASEWORKER_EMAIL = 'minnie@mouse.com'
CASEWORKER_PASSWORD = 'aass12'
ALUMINIUM_CRATES_CASE_NAME = 'Diamond fabric from Belize'  # Case with many parties, submissions & files
ALUMININUM_CRATES_CASE_ID = 'fb757349-5895-49ef-909e-adcd92cbdf8d'
TRADE_LAW_MATTERS_ORGANISATION_ID = 'b837388e-2642-47f5-a6e9-b220eda0e933'  # Organisation with many contacts
TRADE_LAW_MATTERS_ORGANISATION_CONTACT_NAME = 'Fred Flintstone'

# Customer host configuration
CUSTOMER_HOST = 'trade-remedies-public-dev.london.cloudapps.digital'
CUSTOMER_BASE_URL = 'https://' + CUSTOMER_HOST

# Customer account
CUSTOMER_NAME = 'Fred Flintstone'
CUSTOMER_EMAIL = "fred@flintstone.com"
CUSTOMER_PASSWORD = 'Falafel1!'
BOX_LTD_ORGANISATION_NAME = 'TRADE CONSULTING SERVICE  LTD'
BOX_LTD_ORGANISATION_ID = 'b837388e-2642-47f5-a6e9-b220eda0e933'  # Organisation with many submissions in my case record
SUBMISSION_ID = 'aa86ebb6-2546-4b6c-893c-c587c4b64ac8'

# Global configuration
WAIT_BETWEEN_ACTIONS_MILLISECONDS = 2000  # How long a user should wait between actions
BASIC_AUTH = ('trade', 'injury')
COMMON_HEADERS = {
    "Connection": "keep-alive",
    "Upgrade-Insecure-Requests": "1",
    "Content-Type": "application/x-www-form-urlencoded",
    "User-Agent": "Chrome/70.0.3538.110",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8",
    "Accept-Encoding": "gzip, deflate, br",
    "Accept-Language": "en-US,en;q=0.9"
}


class TradeRemediesTaskSequence(TaskSequence):

    def get(self, url, expected_text_in_response=None):

        # Make request
        with self.client.get(url, catch_response=True, auth=BASIC_AUTH) as response:

            # Check response
            if 'Two factor authentication' in response.text:
                response.failure("Please disable 2FA in the Django admin before running these performance tests")
                return
            elif expected_text_in_response is not None and expected_text_in_response not in response.text:
                response.failure(f"Response text did not contain '{expected_text_in_response}' as expected")
                return

            # Update referer
            self.headers['Referer'] = f'{self.base_url}{url}'

            # Get CSRF token
            csrftoken = response.cookies.get('csrftoken')
            if csrftoken:
                self._set_cookie('csrftoken', csrftoken)
                self._set_cookie('seen_cookie_message', 'yes')

            # Get CSRF middleware token
            soup = BeautifulSoup(response.text, features="html.parser")
            csrfmiddlewaretoken = soup.find('input', {'name': 'csrfmiddlewaretoken'})
            if csrfmiddlewaretoken:
                self.csrfmiddlewaretoken = csrfmiddlewaretoken['value']

            # Get session cookie
            sessionid = response.cookies.get('sessionid')
            if sessionid:
                self._set_cookie('sessionid', sessionid)

            return response

    def post(self, url, data, expected_text_in_response=None):

        # Include CSRF middleware token with request data
        data['csrfmiddlewaretoken'] = self.csrfmiddlewaretoken

        # Make request
        with self.client.post(url, data, catch_response=True, auth=BASIC_AUTH, headers=self.headers) as response:

            # Check response
            if 'Two factor authentication' in response.text:
                response.failure("Please disable 2FA in the Django admin before running these performance tests")
                return
            if expected_text_in_response is not None and expected_text_in_response not in response.text:
                response.failure(f"Response text did not contain '{expected_text_in_response}' as expected")
                return
            return response

    def _set_cookie(self, key, value):

        # Parse existing cookies
        cookies_dict = {}
        cookies_header = self.headers.get('Cookie')
        if cookies_header:
            cookie_strings = cookies_header.split('; ')
            for cookie_string in cookie_strings:
                cookie_key, cookie_value = cookie_string.split('=')
                cookies_dict[cookie_key] = cookie_value

        # Set new cookie
        cookies_dict[key] = value
        cookie_strings = []
        for key, value in cookies_dict.items():
            cookie_strings.append(f'{key}={value}')
        cookies_string = '; '.join(cookie_strings)
        self.headers['Cookie'] = cookies_string


class CaseworkerTasks(TradeRemediesTaskSequence):
    """Define the sequence of actions taken by a caseworker"""

    base_url = CASEWORKER_BASE_URL

    headers = copy(COMMON_HEADERS)
    headers.update({
        "Host": CASEWORKER_HOST,
        "Origin": CASEWORKER_BASE_URL
    })

    def on_start(self):
        """Log in"""
        self.get(
            url="/accounts/login/",
            expected_text_in_response='Password')
        self.post(
            url="/accounts/login/",
            data={"email": CASEWORKER_EMAIL, "password": CASEWORKER_PASSWORD},
            expected_text_in_response=ALUMINIUM_CRATES_CASE_NAME  # User should be redirected to dashboard after login
        )

    @seq_task(1)
    def dashboard(self):
        """Refresh the dashboard"""
        self.get("/cases/", expected_text_in_response=ALUMINIUM_CRATES_CASE_NAME)

    @seq_task(2)
    def case(self):
        """Go to case page"""
        self.get(f"/case/{ALUMININUM_CRATES_CASE_ID}/", expected_text_in_response=ALUMINIUM_CRATES_CASE_NAME)

    @seq_task(3)
    def parties(self):
        """Go to parties tab for case"""
        self.get(f"/case/{ALUMININUM_CRATES_CASE_ID}/parties/", expected_text_in_response='Add Applicant')

    @seq_task(4)
    def submissions(self):
        """Go to submissions tab for case"""
        self.get(f"/case/{ALUMININUM_CRATES_CASE_ID}/submissions/", expected_text_in_response='Request information')

    @seq_task(5)
    def files(self):
        """Go to files tab for case"""
        self.get(f"/case/{ALUMININUM_CRATES_CASE_ID}/files/", expected_text_in_response='File name')

    @seq_task(6)
    def tasks_(self):
        """Go to tasks tab for case"""
        self.get(f"/case/{ALUMININUM_CRATES_CASE_ID}/actions/", expected_text_in_response='Close case')

    # This is now performed locally with JS, no further request is made, so response time is effectively 0
    # @seq_task(7)
    # def close_case_task(self):
    #     """Go to Close Case task for case"""
    #     self.get(f"/case/{ALUMININUM_CRATES_CASE_ID}/action/CLOSE_CASE", expected_text_in_response='Save and Exit')

    @seq_task(7)
    def organisation(self):
        """View an organisation"""
        self.get(
            f"/case/{ALUMININUM_CRATES_CASE_ID}/organisation/{TRADE_LAW_MATTERS_ORGANISATION_ID}",
            expected_text_in_response= TRADE_LAW_MATTERS_ORGANISATION_CONTACT_NAME
        )

    @seq_task(8)
    def stop(self):
        # Run each set of user actions once per locust, then stop the locust (don't loop forever)
        raise StopLocust

    def on_stop(self):
        """Log out"""
        self.get("/accounts/logout/", expected_text_in_response='Password')


class CustomerTasks(TradeRemediesTaskSequence):
    """Define the sequence of actions taken by a customer"""

    base_url = CUSTOMER_BASE_URL

    headers = copy(COMMON_HEADERS)
    headers.update({
        "Host": CUSTOMER_HOST,
        "Origin": CUSTOMER_BASE_URL
    })

    def on_start(self):
        """Log in"""
        self.get(
            url="/accounts/login/",
            expected_text_in_response='Password')
        self.post(
            url="/accounts/login/",
            data={"email": CUSTOMER_EMAIL, "password": CUSTOMER_PASSWORD},
            expected_text_in_response=f'Welcome {CUSTOMER_NAME}'  # User should be redirected to dashboard after login
        )

    @seq_task(1)
    def dashboard(self):
        """Refresh the dashboard"""
        self.get("/dashboard/", expected_text_in_response=f'Welcome {CUSTOMER_NAME}')

    @seq_task(2)
    def case(self):
        """Go to case page"""
        self.post(
            url="/organisation/set/",
            data={
                'next': f'/case/{ALUMININUM_CRATES_CASE_ID}/',
                'organisation_id': BOX_LTD_ORGANISATION_ID
            },
            expected_text_in_response=f"You are currently representing {BOX_LTD_ORGANISATION_NAME.replace(' ', '  ')}"
        )

    @seq_task(3)
    def public_file_tab(self):
        """Go to public file tab"""
        self.get(
            f'/case/{ALUMININUM_CRATES_CASE_ID}/?tab=case_record&organisation_id={BOX_LTD_ORGANISATION_ID}',
            expected_text_in_response='Party Type')

    @seq_task(4)
    def my_case_record_tab(self):
        """Go back to my case record tab"""
        self.get(
            f'/case/{ALUMININUM_CRATES_CASE_ID}/?tab=my_case_record&organisation_id={BOX_LTD_ORGANISATION_ID}',
            expected_text_in_response='Modified date')

    @seq_task(5)
    def view_submission(self):
        """View an existing submission"""
        self.get(
            f'/case/{ALUMININUM_CRATES_CASE_ID}/submission/{SUBMISSION_ID}/',
            expected_text_in_response='Registration submitted'
        )

    @seq_task(6)
    def start_submit_evidence(self):
        """Start the process of submitting evidence (but don't finish)"""
        self.get(
            f'/case/{ALUMININUM_CRATES_CASE_ID}/organisation/{BOX_LTD_ORGANISATION_ID}/submission/create/',
            expected_text_in_response='Submit evidence'
        )
        self.get(
            f'/case/{ALUMININUM_CRATES_CASE_ID}/submission/3/meta/',
            expected_text_in_response='About the submission'
        )
        self.post(
            url=f'/case/{ALUMININUM_CRATES_CASE_ID}/submission/3/meta/',
            data={
             'submission_name': 'test_submission',
             'submission_type_id': '3',
             'btn-action': 'savecontinue'
            },
            expected_text_in_response='Submit evidence'
        )

    @seq_task(7)
    def stop(self):
        # Run each set of user actions once per locust, then stop the locust (don't loop forever)
        raise StopLocust

    def on_stop(self):
        self.get("/accounts/logout/")


class Caseworker(HttpLocust):
    host = CASEWORKER_BASE_URL
    task_set = CaseworkerTasks
    min_wait = max_wait = WAIT_BETWEEN_ACTIONS_MILLISECONDS


class Customer(HttpLocust):
    host = CUSTOMER_BASE_URL
    task_set = CustomerTasks
    min_wait = max_wait = WAIT_BETWEEN_ACTIONS_MILLISECONDS
