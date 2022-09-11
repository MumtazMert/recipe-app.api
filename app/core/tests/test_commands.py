from unittest.mock import patch
from psycopg2 import OperationalError as Psycopg2Error
#It provides to call a command by name
from django.core.management import call_command
from django.db.utils import OperationalError
from django.test import SimpleTestCase

#We are gonna mocking a check method to simulate
@patch('core.management.commands.wait_for_db.Command.check')
class CommandTests(SimpleTestCase):
    #Test commands 
    def test_wait_for_db_ready(self, patched_check):
        #Test waiting database if database is ready
        patched_check.return_value = True
        call_command('wait_for_db')
        patched_check.assert_called_once_with(databases=['default'])
    @patch('time.sleep')
    def test_wait_for_db_delay(self,patched_sleep, patched_check):
        #Test waiting for database getting operational error
        #We are saying for first 2 times we call the mocked method and raise psycopg2 eroor
        #next 3 times we raise operational error 
        patched_check.side_effect = [Psycopg2Error] * 2 + \
            [OperationalError] * 3 + [True]    
        call_command('wait_for_db')
        self.assertEqual(patched_check.call_count, 6)
        #Making sure patch check matches default
        patched_check.assert_called_with(databases=['default'])