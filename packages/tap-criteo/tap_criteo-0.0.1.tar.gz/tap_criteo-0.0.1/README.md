# tap-criteo

singer.io tap- Extracts data from the Criteo API, written in python 3.5.

Author: Ashwani Singh (ashwani.s@blueoceanmi.com)


1. Install

    >>python setup.py install 
    >>tap-criteo -h

2. Execution and configuration options:

    tap-criteo takes two inputs arguments
     
     I. --config:  It takes a configuration file as authentication parameters and parameters are "username", "password", "apptoken", "clientversion", "user_agent", "start_date" and "increment" parameters all are mandatory, if state file is not passed than start_date from config file used as filter option for data extraction and "increment" will be used to increment start_date to get end_date for filter. 

     II. --state: This is optional parameter define state where data extraction done last time, this parameter takes JSON file as input, format is based on same format which Criteo supports, for referenece about how Criteo filter works please refer https://support.criteo.com/hc/en-us/articles/209273149-How-do-I-call-the-reporting-information-using-the-Criteo-API-.
          

3. Running the application:
    >> tap-criteo --config config.json  [--state  state.json]

