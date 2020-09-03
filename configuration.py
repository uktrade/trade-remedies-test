import os

IMPLICIT_WAIT_SECONDS = 5
EXPLICIT_WAIT_SECONDS = 5
PEXPECT_TIMEOUT_SECONDS = 120

CASEWORKER_BASE_URL = 'http://localhost:8001'
CUSTOMER_BASE_URL = 'http://localhost:8002'
ADMIN_BASE_URL = 'http://localhost:8000/admin'

ADMIN_EMAIL = 'masteradmin@test.com'
ADMIN_PASSWORD = 'M4$teradmin'

EMAIL_ACCOUNT = 'traderemediesautotest@outlook.com'
EMAIL_ACCOUNT_2 = 'traderemediesautotest2@outlook.com'
EMAIL_PASSWORD = os.environ.get('EMAIL_PASSWORD', 'Aut0t3$t')

DOCKER_API_CONTAINER_NAME = os.getenv('DOCKER_API_CONTAINER_NAME', 'trade-remedies-api-cli')

DOWNLOADS_DIRECTORY = '~/Downloads'
