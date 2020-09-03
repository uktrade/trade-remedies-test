from collections import defaultdict

import pytest
from selenium.common.exceptions import WebDriverException, StaleElementReferenceException

from caseworker import Caseworker
from fixtures import browser, factory_reset_before_each_test


def test_find_broken_links(browser):
    """
    Find and click as many links as possible, report any broken links.
    """
    # TODO: This test is quick and dirty - lots of room for improvement:
    #   1. click on buttons, not just links.
    #   2. when a link triggers a popup window, are we handling this correctly or
    #   just deciding that all links on the page are now unclickable?

    visited_addresses = []
    error_addresses = defaultdict(list)

    def explore(browser):

        current_url = browser.current_url
        print("Exploring page: {}".format(current_url))
        expanders = browser.find_elements_by_class_name('expander')
        for expander in expanders:
            try:
                expander.click()
            except WebDriverException as e:
                print("Clicking expander failed")
                if 'not clickable' in e.msg:
                    pass

        link_elements = browser.find_elements_by_tag_name('a')

        for link_element in link_elements:

            # Parse link
            try:
                link_text = link_element.text
                link_address = link_element.get_property('href')
            except StaleElementReferenceException:
                continue

            # Decide whether to click this link
            if link_element.is_displayed() and link_element.is_enabled() and link_text and link_address not in visited_addresses and 'logout' not in link_address:

                # Click the link
                try:
                    link_element.click()
                except WebDriverException as e:
                    print("Clicking link failed")
                    if 'not clickable' in e.msg:
                        pass
                    else:
                        raise RuntimeError("Failed to click link that should have been clickable: {}".format(e))
                else:
                    print("*** Clicked link: {} ***".format(link_text))
                    visited_addresses.append(link_address)

                    # Check for new tabs
                    if len(browser.window_handles) > 1:
                        print("A new tab opened")
                        # TODO: Need to check that the contents of the new tab is not an error page

                    # Check page for errors
                    if "You're seeing this error because" in browser.page_source or 'Traceback' in browser.page_source:
                        print("Error detected!")
                        error_addresses[current_url].append(link_address)

                    # Explore the new page
                    explore(browser)

                    # When you're done, go back
                    print("Navigating back")
                    browser.get(current_url)
                    explore(browser)

        print("Recursion branch terminated")

    caseworker = Caseworker()
    caseworker.sign_in(browser)
    caseworker.new_ex_officio_case(case_type='Anti-dumping investigation', auto=True, browser=browser)
    caseworker.sign_in(browser)
    explore(browser)

    if error_addresses:
        pytest.fail("The following pages failed to load: {}".format(error_addresses))
