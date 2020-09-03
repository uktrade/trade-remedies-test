import os

import pytest
from selenium.common.exceptions import NoSuchElementException

from caseworker import Caseworker
from customer import Customer
from error_handling import UIErrorMessage
from fixtures import factory_reset_before_each_test, browser


def test_multiple_users_from_same_company_can_register_interest_in_a_case(browser):
    """Multiple users from the same company should be allowed to register interest in a case"""

    # Create two customers from the same company
    customer_1 = Customer(
        auto=True,
        browser=browser
    )
    customer_2 = Customer(
        company_name=customer_1.company_name,
        company_address=customer_1.company_address,
        company_number=customer_1.company_number,
        auto=True,
        browser=browser
    )

    # Caseworker creates an ex-officio case and initiates it
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type='Anti-dumping investigation', auto=True, browser=browser)
    caseworker.tasks.initiation.publish_initiation_notices(
        auto=True,
        case=case,
        browser=browser)

    # Both customers register interest in the case
    for customer in [customer_1, customer_2]:
        customer.register_interest.start_registration(case=case, browser=browser)
        customer.register_interest.upload_registration_documents(
            case=case,
            files=[os.getcwd() + '/dummy_files/document 1.docx'],
            browser=browser
        )
        customer.register_interest.submit_registration(case=case, browser=browser)


def test_register_interest_in_own_case_on_behalf_of_own_company_fails(browser):
    """Check for error message when registering interest in own case on behalf of own company"""

    caseworker = Caseworker()
    customer = Customer(auto=True, browser=browser)

    # Customer creates a case
    case = customer.apply_for_trade_remedy.create_case(case_type='Anti-dumping investigation', auto=True, browser=browser)

    # Caseworker initiates the case
    caseworker.tasks.initiation.publish_initiation_notices(
        auto=True,
        case=case,
        browser=browser)

    # Same customer tries to register interest
    try:
        customer.register_interest.start_registration(case=case, browser=browser)
    except UIErrorMessage as error:
        assert error.summary == [f'You have already registered interest in this case on behalf of: {customer.company_name}. View your registration']
    else:
        pytest.fail('Customer was able to register interest in their own case, expected an error.')


def test_register_interest_in_own_case_on_behalf_of_other_company_succeeds(browser):
    """It should be possible to register interest in own case on behalf of a different company"""

    caseworker = Caseworker()
    customer = Customer(auto=True, browser=browser)

    # Customer creates a case
    case = customer.apply_for_trade_remedy.create_case(case_type='Anti-dumping investigation', auto=True, browser=browser)

    # Caseworker initiates the case
    caseworker.tasks.initiation.publish_initiation_notices(
        auto=True,
        case=case,
        browser=browser)

    # Same customer tries to register interest
    customer.register_interest.start_registration(case=case, own_company=False, browser=browser)


def test_same_user_cant_register_interest_in_case_twice(browser):

    # Caseworker creates a case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type='Anti-dumping investigation', auto=True, browser=browser)
    caseworker.tasks.initiation.publish_initiation_notices(
        auto=True,
        case=case,
        browser=browser)

    # Customer tries registers interest in the same case twice
    customer = Customer(auto=True, browser=browser)
    customer.register_interest.start_registration(case=case, browser=browser)
    try:
        customer.register_interest.start_registration(case=case, browser=browser)
    except UIErrorMessage as error:
        assert error.summary == ['You have already registered interest in this case on behalf of: {}. View your registration'.format(customer.company_name)]
    else:
        pytest.fail("It was possible to register interest in the same case twice")


def test_different_users_from_same_organisation_can_register_interest_in_same_case(browser):
    """Allow multiple registrations of interest because companies don't want others to be able to find out whether they
       have registered interest by registering a new account for the company and checking if they are able to register
       interest"""

    # Caseworker creates a case
    caseworker = Caseworker()
    case = caseworker.new_ex_officio_case(case_type='Anti-dumping investigation', auto=True, browser=browser)
    caseworker.tasks.initiation.publish_initiation_notices(
        auto=True,
        case=case,
        browser=browser)

    # Two accounts for the same organisation register interest in the same case
    customer_1 = Customer(auto=True, browser=browser)
    customer_2 = Customer(
        uk_company=customer_1.uk_company,
        company_country=customer_1.company_country,
        company_name=customer_1.company_name,
        company_number=customer_1.company_number,
        company_address=customer_1.company_address,
        auto=True,
        browser=browser)
    customer_1.register_interest.start_registration(case=case, browser=browser)
    customer_2.register_interest.start_registration(case=case, browser=browser)
