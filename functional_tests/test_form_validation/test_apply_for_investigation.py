import pytest

from error_handling import UIErrorMessage
from customer import Customer
from fixtures import factory_reset_before_test_module, browser
from helpers import fail_fast


@pytest.mark.parametrize(
    ['hs_code', 'valid', 'description'],
    [('12345', False, '5 digits'),
     ('123456', True, ' 6 digits'),
     ('1234567', False, '7 digits'),
     ('12345678', True, '8 digits'),
     ('123456789', False, '9 digits'),
     ('1234567890', True, '10 digits'),
     ('12345678901', False, '11 digits'),
     ('12345a', False, 'non-numeric')]
)
def test_commodity_codes(browser, hs_code, valid, description):
    # TODO: Test multiple commodity codes
    customer = Customer(browser=browser, auto=True)

    with fail_fast(browser):
        try:
            customer.apply_for_trade_remedy.create_case(
                case_type='Anti-dumping investigation',
                commodity_codes=[hs_code],
                auto=True,
                browser=browser
            )
        except UIErrorMessage as error:
            # Error message
            if valid:
                pytest.fail(f"Saw error message {error}, for valid HS code {hs_code} ({description})")
            if not valid:
                assert error.messages == [f'Invalid HS Code: {hs_code}. You must enter 6, 8 or 10 digits']
        else:
            # No error message
            if valid:
                pass
            else:
                pytest.fail(f"Invalid HS code {hs_code} ({description}) was accepted with no error message")
