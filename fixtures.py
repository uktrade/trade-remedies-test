import os
import shutil

import pytest
from retry import retry
from selenium import webdriver
from selenium.webdriver.chrome.options import Options

from configuration import DOWNLOADS_DIRECTORY, IMPLICIT_WAIT_SECONDS
from helpers import connect_to_docker_container as connect_to_docker_container
from pexpect.exceptions import TIMEOUT as PexpectTimeout


@pytest.fixture(scope='function', autouse=True)
@retry(PexpectTimeout, tries=3)
def factory_reset_before_each_test(request):
    """Reset everything to a clean state before each test function runs"""
    with connect_to_docker_container() as console:
        _reset_db(console)
        _flush_redis(console)


def validate_email_address(email_address):
    with connect_to_docker_container() as console:
        _validate_email_address(console, email_address)


@pytest.fixture(scope='function', autouse=True)
@retry(PexpectTimeout, tries=3)
def flush_redis_before_each_test(request):
    """Flush redis before each test function runs (redis is used to store session data, ie. logins + login attempts)"""
    with connect_to_docker_container() as console:
        _flush_redis(console)


@pytest.fixture(scope='module', autouse=True)
@retry(PexpectTimeout, tries=3)
def factory_reset_before_test_module(request):
    """Reset everything to a clean state only once at the start of the test module"""
    with connect_to_docker_container() as console:
        _reset_db(console)
        _flush_redis(console)


@pytest.fixture(scope='module', autouse=True)
@retry(PexpectTimeout, tries=3)
def reset_db_before_test_module(request):
    """Reset database to a clean state only once at the start of the test module"""
    with connect_to_docker_container() as console:
        _reset_db(console)


@pytest.fixture
def browser(request):
    if not os.path.exists(DOWNLOADS_DIRECTORY):
        os.makedirs(DOWNLOADS_DIRECTORY)
    options = Options()
    if request.config.getoption("--headless"):
        # Run Chrome headlessly
        options.add_argument("--headless")
        options.add_argument("--window-size=1920x1080")
        options.add_argument("--disable-dev-shm-usage")  # Overcome limited resource problems in Docker containers
        options.add_argument("--no-sandbox")  # Bypass OS security model
    driver = webdriver.Chrome(options=options)
    # Enable file downloads
    driver.command_executor._commands["send_command"] = ("POST", '/session/$sessionId/chromium/send_command')
    params = {'cmd': 'Page.setDownloadBehavior', 'params': {'behavior': 'allow', 'downloadPath': DOWNLOADS_DIRECTORY}}
    driver.execute("send_command", params)
    driver.implicitly_wait(IMPLICIT_WAIT_SECONDS)
    try:
        yield driver
    finally:
        driver.close()
        shutil.rmtree(DOWNLOADS_DIRECTORY)


def _validate_email_address(console, email_address):
    print(f"\n|Validating email {email_address}|")
    console.sendline(f'python /opt/traderemedies/api/trade_remedies_api/manage.py validate_email {email_address}')
    console.expect(email_address)
    print("|OK|")


def _reset_db(console):
    print("\n|Resetting database|")
    # Flush DB
    console.sendline('cd trade_remedies_api')
    console.expect('/opt/traderemedies/api/trade_remedies_api')

    print("flush")
    console.sendline('python manage.py flush --no-input')
    console.expect('/opt/traderemedies/api/trade_remedies_api')
    # Bootstrap
    print("resetsecurity")
    console.sendline('python manage.py resetsecurity')
    console.expect('/opt/traderemedies/api/trade_remedies_api')

    print("adminuser")
    console.sendline('python manage.py adminuser')
    console.expect('/opt/traderemedies/api/trade_remedies_api')

    # console.sendline('python manage.py loaddata core/fixtures/system_parameters.json')
    # console.expect('Installed')
    print("load_sysparams")
    console.sendline('python manage.py load_sysparams')
    console.expect("Created")

    print("notify_env")
    console.sendline('python manage.py notify_env')
    console.expect('TR_PUBLIC_2FA_CODE_EMAIL -> PUBLIC_2FA_CODE_EMAIL')
    console.sendline('cd ..')
    console.expect('/opt/traderemedies/api')

    print("fixtures")
    console.sendline('./fixtures.sh')
    console.expect('Fixtures loaded')
    print("database reset complete")


def _flush_redis(console):
    print("|Flushing redis|")
    # Flush redis
    console.sendline('python')
    console.expect('>>>')
    console.sendline('import redis')
    console.expect('>>>')
    console.sendline('redis.StrictRedis(host="localhost", port=6379, db=0).flushall()')
    console.expect('True')
    # Detach from python interpreter
    console.sendcontrol('d')
