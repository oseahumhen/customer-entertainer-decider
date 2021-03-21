import argparse
from pathlib import Path

from app.customer_entertainer_decider import CustomerEntertainerDecider

DESTINATION_LATITUDE = 53.339428
DESTINATION_LONGITUDE = -6.257664
MAX_TRAVEL_DISTANCE = 100.0  # in km


def main():
    """
    App entry point function
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--customer_data_file',
                        type=Path,
                        default=Path(__file__).parent / 'customers.txt',
                        help='Full file path to customer data file',
                        required=False)
    parser.add_argument('--destination_latitude',
                        type=float,
                        default=DESTINATION_LATITUDE,
                        help='Latitude of customer destination in degrees',
                        required=False)
    parser.add_argument('--destination_longitude',
                        type=float,
                        default=DESTINATION_LONGITUDE,
                        help='Longitude of customer destination in degrees',
                        required=False)
    parser.add_argument('--max_travel_distance',
                        type=float,
                        default=MAX_TRAVEL_DISTANCE,
                        help='Maximum travel distance for customers',
                        required=False)
    parser.add_argument('--customer_output_file',
                        type=Path,
                        default=Path(__file__).parent / 'output.txt',
                        help='Full file path to output file where validated customers are stored',
                        required=False)
    args = parser.parse_args()
    customer_decider = CustomerEntertainerDecider(args.destination_latitude,
                                                  args.destination_longitude,
                                                  args.max_travel_distance,
                                                  args.customer_data_file,
                                                  args.customer_output_file,
                                                  )
    customer_decider.decide_customers_to_be_entertained()


if __name__ == '__main__':
    main()

