# Trade Remedies Performance Tests

## Installation

pip install -r requirements.txt

## Configuration

The performance tests assume you have a live deployment already set up to test with.

Details about the deployment under test and some existing database objects are defined inside test_performance.py

## Running tests

To test the Caseworker app, run:

```
locust -f test_performance.py Caseworker
```

Or to test the Customer app, run:
```
locust -f test_performance.py Customer
```

You may then initiate a test run via the web interface at http://localhost:8089/

For further documentation see https://docs.locust.io/en/stable/
