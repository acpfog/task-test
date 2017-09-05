#!/usr/bin/env python

# This script will clean the events table!
# Run it only in a testing environment!

import json
import requests
import unittest
import psycopg2
from unittest import TestCase

# Make a connection to the db and clean the events table
class Test1(TestCase):
    def setUp(self):
        global db_conn
        db_conn = psycopg2.connect("dbname='db' user='postgres' host='localhost' password='master'")
    def tearDown(self):
        db_conn.close()
    def test_clean_all_events(self):
        with db_conn.cursor() as cur:
            cur.execute('DELETE FROM EVENTS')
        db_conn.commit()

# Check if reader is up and running
class Test2(TestCase):
    def test_reader_is_up_and_running(self):
        resp = requests.get('http://localhost:8000/stats')
        self.assertEqual(resp.status_code, 200)

# Check if writer is up and running
class Test3(TestCase):
    def test_writer_is_up_and_running(self):
        resp = requests.get('http://localhost:9000/log')
        self.assertEqual(resp.status_code, 405)

# Write a log message #1
class Test4(TestCase):
    def test_write_log_message_attempt_1(self):
        resp = requests.post('http://localhost:9000/log',data=json.dumps(dict(type='log',payload='System rebooted for hard disk upgrade')))
        self.assertEqual(resp.status_code, 200)

# Check if log message #1 was successfully stored
class Test5(TestCase):
    def test_reader_get_request_1(self):
        resp = requests.get('http://localhost:8000/stats')
        self.assertEqual(resp.json(), {'log             ':1})

# Write a log message #2
class Test6(TestCase):
    def test_write_log_message_attempt_2(self):
        resp = requests.post('http://localhost:9000/log',data=json.dumps(dict(type='warning',payload='Unable to open /dev/sr1 read-write')))
        self.assertEqual(resp.status_code, 200)

# Check if log message #2 was successfully stored
class Test7(TestCase):
    def test_reader_get_request_2(self):
        resp = requests.get('http://localhost:8000/stats')
        self.assertEqual(resp.json(), {'log             ':1, 'warning         ': 1})

# Write a log message #3
class Test8(TestCase):
    def test_write_log_message_attempt_3(self):
        resp = requests.post('http://localhost:9000/log',data=json.dumps(dict(type='error',payload='/dev/sr1: unrecognised disk label')))
        self.assertEqual(resp.status_code, 200)

# Check if log message #3 was successfully stored
class Test9(TestCase):
    def test_reader_get_request_3(self):
        resp = requests.get('http://localhost:8000/stats')
        self.assertEqual(resp.json(), {'log             ':1, 'warning         ': 1, 'error           ': 1})

# Run tests
if __name__ == '__main__':
    unittest.main(verbosity=2)
