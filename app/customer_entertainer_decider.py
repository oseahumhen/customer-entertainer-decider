from math import radians, acos, sin, cos
from pathlib import Path
import json

RADIUS_OF_EARTH = 6378  # in km


class CustomerEntertainerDecider:
    """
    Customer Entertainer Decider class
    """
    def __init__(self,
                 destination_latitude,
                 destination_longitude,
                 max_travel_distance,
                 customer_data_file,
                 customer_output_file=Path(__file__).parent.parent / 'output.txt'):
        """
        Class constructor
        :param destination_latitude: (float) destination latitude
        :param destination_longitude: (float) destination longitude
        :param max_travel_distance: (float) maximum allowed travel distance
        :param customer_data_file: (Path) Full path to customer data file
        :param customer_output_file: (Path) Full path to customer output file
        """
        self.destination_latitude = destination_latitude
        self.destination_longitude = destination_longitude
        self.destination_latitude_in_radians = radians(self.destination_latitude)
        self.destination_longitude_in_radians = radians(self.destination_longitude)
        self.customer_file = customer_data_file
        if not Path(self.customer_file).exists():
            raise FileNotFoundError(f'{self.customer_file} does not exist')
        self.max_travel_distance = max_travel_distance
        self.customer_output_file = customer_output_file
        if not Path(self.customer_output_file).parent.exists():
            self.customer_output_file = Path(__file__).parent.parent / 'output.txt'
            print(f'Given output file path: {customer_output_file} does not exist. '
                  f'Defaulting to: {self.customer_output_file}')
        self.customers_to_entertain = []

    def load_customer_data(self):
        """
        A generator method which is able to load single customer data from memory one at a time
        :return: (generator object) customer data generator
        """
        with open(self.customer_file, 'r') as fi:
            while True:
                single_customer_data = fi.readline()
                if not single_customer_data:
                    break
                try:
                    yield json.loads(single_customer_data.rstrip())
                except json.decoder.JSONDecodeError:
                    print('Encountered invalid JSON input. Rendering as "{}"')
                    yield json.loads('{}')

    def calculate_travel_distance(self, origin_latitude, origin_longitude):
        """
        Method to calculate travel distance between given origin latitude and longitude with respect to
        destination latitude and longitude
        :param origin_latitude: (float) origin latitude
        :param origin_longitude: (float) origin longitude
        :return: (float) Calculated travel distance
        """
        latitude_in_radians = radians(origin_latitude)
        longitude_in_radians = radians(origin_longitude)
        diff_longitude = abs(abs(self.destination_longitude_in_radians) - abs(longitude_in_radians))
        delta_angle = acos(sin(latitude_in_radians) * sin(self.destination_latitude_in_radians) +
                      cos(latitude_in_radians) * cos(self.destination_latitude_in_radians) * cos(diff_longitude))
        travel_distance = delta_angle * RADIUS_OF_EARTH
        return travel_distance

    def decide_customers_to_be_entertained(self):
        """
        Method to generate customers which will be entertained based on max_travel_distance
        """
        for customer_data in self.load_customer_data():
            if self.validate_customer_data(customer_data):
                distance = self.calculate_travel_distance(float(customer_data['latitude']), float(customer_data['longitude']))
                if distance <= self.max_travel_distance:
                    tmp_dict = {'user_id': customer_data['user_id'], 'name': customer_data['name']}
                    self.customers_to_entertain.append(tmp_dict)
        self.customers_to_entertain.sort(key=lambda k: k['user_id'])
        self.display_customers_to_entertain()
        self.save_customers_to_entertain_to_file()

    def display_customers_to_entertain(self):
        """
        Method to display customers to be entertained to console
        """
        print(f'Customers within {self.max_travel_distance}km Distance of latitude: {self.destination_latitude} '
              f'and longitude: {self.destination_longitude}')
        print('{:<10} {:<10}'.format('USER_ID', 'NAME'))
        for customer in self.customers_to_entertain:
            print('{:<10} {:<10}'.format(customer['user_id'], customer['name']))

    def save_customers_to_entertain_to_file(self):
        """
        Method to save customers to entertain to output txt file
        """
        with open(self.customer_output_file, 'w') as fo:
            for customer in self.customers_to_entertain:
                fo.write(f'{json.dumps(customer)}\n')

    @staticmethod
    def validate_customer_data(customer_data):
        """
        Method to check customer data has needed fields in right formats
        :param customer_data: (dict) dictionary of individual customer data
        :return: (bool) True if customer data is valid. False for otherwise
        """
        return_value = False
        if all(key in customer_data for key in ('latitude', 'longitude', 'name', 'user_id')):
            try:
                float(customer_data['latitude'])
                float(customer_data['longitude'])
            except ValueError:
                pass
            else:
                return_value = True
        if not return_value:
            print(f'Omitting invalid customer record: {customer_data}')
        return return_value



