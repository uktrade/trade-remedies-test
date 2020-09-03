from datetime import datetime, timezone

import pytest

from configuration import EMAIL_ACCOUNT, EMAIL_PASSWORD
from customer import Customer
from email_client import check_for_email, get_emails
from fixtures import factory_reset_before_each_test, browser


@pytest.mark.skip(reason='Unwritten test / maybe not needed')
def test_customer_cancels_registration_of_interest(browser):
    """Not sure if there's meant to be an email for this?"""


def test_customer_cancels_application(browser):
    # TODO: Test creating a safeguarding case, and see that safeguarding appears in the email, not anti-dumping

    customer = Customer(email=EMAIL_ACCOUNT, auto=True, browser=browser)

    # Customer starts an application
    case_type = 'Anti-dumping investigation'
    start_time = datetime.now(timezone.utc)
    case = customer.apply_for_trade_remedy.create_case(
        case_type=case_type,
        auto=True,
        browser=browser
    )

    # Check no unexpected emails
    emails = get_emails(
        later_than=start_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD,
        delay=5
    )
    if emails:
        pytest.fail(f"Unexpected email(s) received before application cancellation: {emails}")

    # Customer cancels application
    cancellation_time = datetime.now(timezone.utc)
    customer.apply_for_trade_remedy.cancel_application(
        browser=browser,
        case=case
    )

    # Customer gets an email to confirm the cancellation
    check_for_email(
        with_subject='Application cancelled'.format(case),
        later_than=cancellation_time,
        addressed_to=customer.name,
        account=EMAIL_ACCOUNT,
        password=EMAIL_PASSWORD
    )


@pytest.mark.skip(reason="Unwritten test")
def test_customer_cancels_application_with_multi_user_account(browser):
    pass



