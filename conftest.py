import os

import pytest


@pytest.fixture(scope="session", autouse=True)
def dummy_files():
    if not os.path.exists(os.getcwd() + '/dummy_files'):
        os.mkdir(os.getcwd() + '/dummy_files')
    for i in range(1, 11):
        if not os.path.exists(os.getcwd() + f'/dummy_files/document {i}.docx'):
            open(os.getcwd() + f'/dummy_files/document {i}.docx', 'a').close()
    # TODO: Remove these files at end of test run (not a big deal though)


def pytest_addoption(parser):
    parser.addoption('--headless', action='store_true', help='Run Chrome in headless mode')
