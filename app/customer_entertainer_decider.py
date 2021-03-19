from math import radians, acos, sin, cos
from pathlib import Path
import json
import logging

RADIUS_OF_EARTH = 6378  # in km

logger = logging.getLogger('')


class CustomerEntertainerDecider:
    def __init__(self,
                 destination_latitude,
                 destination_longitude,
                 max_travel_distance,
                 customer_data_file,
                 customer_output_file=Path(__file__).parent.parent / 'output.txt'):
        self.destination_latitude_in_radians = radians(destination_latitude)
        self.destination_longitude_in_radians = radians(destination_longitude)
        self.customer_file = customer_data_file
        if not Path(self.customer_file).exists():
            raise FileNotFoundError(f'{self.customer_file} does not exist')
        self.max_travel_distance = max_travel_distance
        self.customer_output_file = customer_output_file
        if not Path(self.customer_output_file).parent.exists():
            self.customer_output_file = Path(__file__).parent.parent / 'output.txt'
            logger.warning(f'Given output file path: {customer_output_file} does not exist. '
                           f'Defaulting to: {self.customer_output_file}')
        self.customers_to_entertain = []

    def load_customer_data(self):
        with open(self.customer_file, 'r') as fi:
            while True:
                single_customer_data = fi.readline()
                if not single_customer_data:
                    break
                yield json.loads(single_customer_data.rstrip())

    def calculate_dist_to_dest(self, origin_latitude, origin_longitude):
        latitude_in_radians = radians(origin_latitude)
        longitude_in_radians = radians(origin_longitude)
        diff_longitude = abs(abs(self.destination_longitude_in_radians) - abs(longitude_in_radians))
        delta = acos(sin(latitude_in_radians) * sin(self.destination_latitude_in_radians) +
                     cos(latitude_in_radians) * cos(self.destination_latitude_in_radians) * cos(diff_longitude))
        distance = delta * RADIUS_OF_EARTH
        return distance

    def decide_customers_to_be_entertained(self):
        for customer_data in self.load_customer_data():
            distance = self.calculate_dist_to_dest(float(customer_data['latitude']), float(customer_data['longitude']))
            if distance <= 100:
                tmp_dict = {'user_id': customer_data['user_id'], 'name': customer_data['name']}
                self.customers_to_entertain.append(tmp_dict)
        self.customers_to_entertain.sort(key=lambda k: k['user_id'])
        self.render_results()

    def render_results(self):
        self.display_customers_to_entertain()
        self.save_customers_to_entertain_to_file()

    def display_customers_to_entertain(self):  # TO DO: format printing to console
        for customer in self.customers_to_entertain:
            print(customer)

    def save_customers_to_entertain_to_file(self):
        with open(self.customer_output_file, 'w') as fo:
            for customer in self.customers_to_entertain:
                fo.write(f'{json.dumps(customer)}\n')
