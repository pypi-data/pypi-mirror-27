import unittest
from mock import patch
from blink.blink import get_delay_in_sec
from blink.blink import get_delay_arg_from_console

class TestBlink(unittest.TestCase):
    
    def test_set_correct_delay_param(self):
        # given
        given_delay = 0.5
        expected_delay = 0.5
        
        # when
        result = get_delay_in_sec(given_delay)
        
        # then
        self.assertEquals(result, expected_delay)
        
    def test_set_to_default_if_empty(self):
        # given
        expected_delay = 1
        
        # when
        result = get_delay_in_sec(None)
        
        # then
        self.assertEquals(result, expected_delay)
        
    def test_set_to_default_if_not_float(self):
        # given
        expected_delay = 1
        
        # when
        result = get_delay_in_sec('delay')
        
        # then
        self.assertEquals(result, expected_delay)
        
    def test_return_empty_string_when_no_args_passed(self):
        # given
        expected_arg = ''
        test_args = ['path']
        
        # when
        with patch('sys.argv', test_args):
            result = get_delay_arg_from_console()
        
        # then
        self.assertEquals(result, expected_arg)
        
    def test_return_value_when_args_passed(self):
        # given
        expected_arg = 'test'
        test_args = ['path', expected_arg]
        
        # when
        with patch('sys.argv', test_args):
            result = get_delay_arg_from_console()
            
        # then
        self.assertEquals(result, expected_arg)
        
    if __name__ == '__main__':
        unittest.main()


