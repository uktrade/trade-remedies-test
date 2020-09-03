from error_handling import error_handler


class Users:

    def __init__(self, caseworker):
        self.caseworker = caseworker

    def _go_to(self, browser):
        self.caseworker.sign_in(browser=browser)
        # TODO: Remove workaround (click link in footer)
        browser.get("http://localhost:8001/users")
        browser.find_element_by_partial_link_text("New investigator").click()

    @error_handler
    def new_investigator(self, browser, email, name, password, security_group):
        self._go_to(browser=browser)

        id_for_security_group = {
            'TRA Administrator': 'role_1',
            'TRA Investigator': 'role_2',
            'Lead Investigator': 'role_3',
            'Head of Investigation': 'role_4'
        }

        browser.find_element_by_id('email').send_keys(email)
        browser.find_element_by_id('name').send_keys(name)
        browser.find_element_by_id('password').send_keys(password)
        browser.find_element_by_id('password_confirm').send_keys(password)
        browser.find_element_by_id(id_for_security_group[security_group]).click()

        browser.find_element_by_class_name('button-blue').click()

        # Check we're back on the user list, with a new entry for the created user
        browser.find_element_by_link_text(email)

        Caseworker = type(self.caseworker)  # Avoid circular import
        return Caseworker(email=email, password=password)
