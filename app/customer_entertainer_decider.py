from math import radians, acos, sin, cos
from pathlib import Path
import json
import mpmath as mp

RADIUS_OF_EARTH = 6378  # in km


class CustomerEntertainerDecider:
    def __init__(self,
                 destination_latitude,
                 destination_longitude,
                 max_travel_distance,
                 customer_data_file,
                 customer_output_file=Path(__file__).parent.parent / 'output.txt'):
        self.destination_latitude_in_radians = mp.radians(destination_latitude)
        self.destination_longitude_in_radians = mp.radians(destination_longitude)
        self.customer_file = customer_data_file
        if not Path(self.customer_file).exists():
            raise FileNotFoundError(f'{self.customer_file} does not exist')  # test
        self.max_travel_distance = max_travel_distance
        self.customer_output_file = customer_output_file
        if not Path(self.customer_output_file).parent.exists():
            self.customer_output_file = Path(__file__).parent.parent / 'output.txt'
            print(f'Given output file path: {customer_output_file} does not exist. '
                           f'Defaulting to: {self.customer_output_file}')
        self.customers_to_entertain = []

    def load_customer_data(self):
        with open(self.customer_file, 'r') as fi:
            while True:
                single_customer_data = fi.readline()
                if not single_customer_data:
                    break
                try:
                    yield json.loads(single_customer_data.rstrip())  # what happens with empty line???
                except json.decoder.JSONDecodeError:
                    print('Encountered invalid JSON input. Rendering as "{}"')
                    yield json.loads('{}')

    def calculate_travel_distance(self, origin_latitude, origin_longitude):
        latitude_in_radians = radians(origin_latitude)
        longitude_in_radians = radians(origin_longitude)
        diff_longitude = abs(abs(self.destination_longitude_in_radians) - abs(longitude_in_radians))
        delta_angle = acos(sin(latitude_in_radians) * sin(self.destination_latitude_in_radians) +
                      cos(latitude_in_radians) * cos(self.destination_latitude_in_radians) * cos(diff_longitude))
        travel_distance = delta_angle * RADIUS_OF_EARTH
        print(travel_distance)
        return travel_distance

    def decide_customers_to_be_entertained(self):
        for customer_data in self.load_customer_data():
            if self.validate_customer_data(customer_data):
                distance = self.calculate_travel_distance(float(customer_data['latitude']), float(customer_data['longitude']))
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

    @staticmethod
    def validate_customer_data(customer_data):
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


