# customer-entertainer-decider

A console app used to determine customers to be entertained based on maximum allowed travel distance from a given destination latitude and longitude value.
Name and user id of customers within allowed travel distance(default is 100km) will be outputted in an output.txt file.

## Installation Steps
1. Install Python3.7 on your machine.
   
   Windows users can install from here: <https://www.python.org/ftp/python/3.7.9/python-3.7.9.exe>
   
   Linux users should follow instructions here: <https://linuxize.com/post/how-to-install-python-3-7-on-ubuntu-18-04/> or <https://tecadmin.net/install-python-3-7-on-ubuntu-linuxmint/>
   
   **NB:** Development was done in Python3.7 but new versions of Python3 or Python3.6 can be used as well.
   
2. Clone this repository by running:
   ```
   git clone https://github.com/oseahumhen/customer-entertainer-decider.git
   ```
   Alternatively, download source code zip here: <https://github.com/oseahumhen/customer-entertainer-decider/archive/refs/heads/main.zip> 
   and extract to known directory.

3. Navigate to project directory (customer-entertainer-decider) and run following command to create Python virtual environment
   ```
    # For Windows users
    py -3.7 -m venv venv
    
    # For Linux users
    python3.7 -m venv venv
   ```

## User Instruction

### How To Run Application
1. Navigate to project root (customer-entertainer-decider) and activate virtual environment by running following command below:
   ```
    # For Windows users
    venv\Scripts\activate.bat
    
    # For linux users
    source venv/bin/activate
   ```
2. Still in project root directory, run application with below command:
   ```
   python app.py
   ```
   Running without any parameters assumes that a customers.txt file exists in project root and uses default maximum travel distance and coordinates defined in source code.
   Output file will also be saved to project root.
   
   Application can be run with parameters. To see help menu, run `python app.py -h`. 
   See below for help menu console output:
   ```
   python app.py -h
   usage: app.py [-h] [--customer_data_file CUSTOMER_DATA_FILE]
              [--destination_latitude DESTINATION_LATITUDE]
              [--destination_longitude DESTINATION_LONGITUDE]
              [--max_travel_distance MAX_TRAVEL_DISTANCE]
              [--customer_output_file CUSTOMER_OUTPUT_FILE]

   optional arguments:
   -h, --help            show this help message and exit
   --customer_data_file CUSTOMER_DATA_FILE
                        Full file path to customer data file. If not
                        specified, application assumes a customers.txt file
                        exists in project root
   --destination_latitude DESTINATION_LATITUDE
                        Latitude of customer destination in degrees
   --destination_longitude DESTINATION_LONGITUDE
                        Longitude of customer destination in degrees
   --max_travel_distance MAX_TRAVEL_DISTANCE
                        Maximum travel distance for customers
   --customer_output_file CUSTOMER_OUTPUT_FILE
                        Full file path to output file where validated
                        customers are stored. Defaults to output.txt in
                        project root
   ```

### How To Run Tests
Ensure you are in the project root directory and run `python tests/test_customer_entertainer_decider.py`
   
Alternatively, from `customer-entertainer-decider/tests` directory, run `python test_customer_entertainer_decider.py`


