import json
from pathlib import Path
import unittest

from app.customer_entertainer_decider import CustomerEntertainerDecider


class CustomerEntertainerDeciderTest(unittest.TestCase):

    def test_non_existent_customer_data_file(self):
        with self.assertRaises(FileNotFoundError):
            CustomerEntertainerDecider(10, 20, 100, Path(__file__).parent / 'not_exist.txt')

    def test_non_existent_customer_output_file(self):
        customer_decider = CustomerEntertainerDecider(10, 20, 100,
                                                      Path(__file__).parent / 'test_customers.txt',
                                                      Path(__file__).parent / 'no_exist' / 'output.txt')
        self.assertEqual(customer_decider.customer_output_file, Path(__file__).parent.parent / 'output.txt')

    def test_all_customer_data_loaded(self):
        customer_decider = CustomerEntertainerDecider(10, 20, 100,
                                                      Path(__file__).parent / 'test_customers.txt')
        count = 0
        for __ in customer_decider.load_customer_data():
            count += 1
        self.assertEqual(count, 7)

    def test_customer_data_converted_to_dict(self):
        customer_decider = CustomerEntertainerDecider(10, 20, 100,
                                                      Path(__file__).parent / 'test_customers.txt',
                                                      Path(__file__).parent / 'test_output.txt')
        customer_data = next(customer_decider.load_customer_data())
        self.assertIsInstance(customer_data, dict)
        self.assertDictEqual(customer_data, {'latitude': '53.521111', 'user_id': 20, 'name': 'Enid Enright',
                                             'longitude': '-9.831111'})

    def test_validate_customer_data(self):
        customer_decider = CustomerEntertainerDecider(10, 20, 100,
                                                      Path(__file__).parent / 'test_customers_with_invalid_data.txt',
                                                      Path(__file__).parent / 'test_output.txt')

        count = 0
        for customer_data in customer_decider.load_customer_data():
            if customer_decider.validate_customer_data(customer_data):
                count += 1
        self.assertEqual(count, 2)

    def test_calculate_travel_distance(self):
        customer_decider = CustomerEntertainerDecider(53.339428,  -6.257664, 100,
                                                      Path(__file__).parent / 'test_customers.txt',
                                                      Path(__file__).parent / 'test_output.txt')
        self.assertEqual(round(customer_decider.calculate_travel_distance(60, -8), 2), 749.26)

    def test_output_sorted(self):
        customer_decider = CustomerEntertainerDecider(53.339428, -6.257664, 100,
                                                      Path(__file__).parent / 'test_customers.txt',
                                                      Path(__file__).parent / 'test_output.txt')
        customer_decider.decide_customers_to_be_entertained()
        user_ids = []
        for customer_data in customer_decider.customers_to_entertain:
            user_ids.append(customer_data['user_id'])
        self.assertTrue(user_ids == sorted(user_ids))

    def test_output_file_created(self):
        customer_decider = CustomerEntertainerDecider(53.339428, -6.257664, 100,
                                                      Path(__file__).parent / 'test_customers.txt',
                                                      Path(__file__).parent / 'test_output.txt')
        customer_decider.decide_customers_to_be_entertained()
        self.assertTrue(customer_decider.customer_output_file.exists())

    def test_output_data_format_json(self):
        customer_decider = CustomerEntertainerDecider(53.339428, -6.257664, 100,
                                                      Path(__file__).parent / 'test_customers.txt',
                                                      Path(__file__).parent / 'test_output.txt')
        customer_decider.decide_customers_to_be_entertained()
        invalid = False
        with open(customer_decider.customer_output_file, 'r') as fi:
            while True:
                single_customer_data = fi.readline()
                if not single_customer_data:
                    break
                try:
                    json.loads(single_customer_data)
                except ValueError:
                    invalid = True
        self.assertFalse(invalid)


if __name__ == '__main__':
    unittest.main()
