# GeoLocation Data Service

A Python service that provides geolocation data using the OpenWeatherMap Geocoding API. This service supports looking up coordinates by ZIP code or City/State combinations for US locations.

## Prerequisites

- Python 3.10 or higher
- OpenWeatherMap API key ([Get one here](https://openweathermap.org/api))

## Installation

1. Clone the repository:
    ```bash
    $ git clone <repository-url>
    $ cd geolocutil_sample_code
    ```
2. Install pipenv and install dependencies (recommended):
    ```bash 
   $ pip install pipenv --user
   $ pipenv --python 3.12
   $ pipenv install
   $ pipenv shell
    ```
   or you can skip pipenv and do 
   ```bash
   $ pip install -r requirements.txt
   ```
   
3. Set up environment variables: <br />Create a `.env` file in the root directory with your API key:
    ```bash
    GEOLOC_API_KEY=your_api_key_here
   ```

## Usage

The service can be used in two ways:
1. In Python
   1. As a function call:
       ```python
       from GeoLocationData import GeoLocationData
       geo = GeoLocationData()
       ```
       Single location
       ```python
       result = geo("New York, NY")
       ```
       Multiple locations
       ```python
       results = geo(["90210", "Miami, FL", "Seattle, WA"])
       ```

   2. Using the get_geoloc_data method:
       ```python
       from GeoLocationData import GeoLocationData
       geo = GeoLocationData()
       results = geo.get_geoloc_data("Portland, OR")
       ```
      
2. Command Line Utility

   note: you may need ot use `python3` on some macs/linux machines instead of `python`
   ```bash
   $ python geolocutil.py [flags] locations
   ```
   Flags include:
   ```bash
   -h, --help    show this help message and exit
   -p, --print   Outputs pretty print to stdout instead of json string
   -j, --json    Converts all strings to ascii in json output
   -e, --errors  Prints out Error messages to stdout
   ```
   locations must be separated by quotes (single or double), example: `"New York, NY" "90210"`
   
   to pretty print to stdout:
   ```bash
   $ python geolocutil.py -p '90201' 'New York, NY'
   
   |-------------------------------------------------------------------------------------|
   | Search Term               | City/Town Name            | Latitude     | Longitude    |
   |-------------------------------------------------------------------------------------|
   | 90210                     | Beverly Hills             | 34.0901      | -118.4065    |
   | New York, NY              | New York                  | 40.7127281   | -74.0060152  |
   |-------------------------------------------------------------------------------------|
   ```
   To output in json
   ```bash
   $ python geolocutil.py -j '90210' 'New York, NY'
   
   [
    {
        "search_term": "90210",
        "name": "Beverly Hills",
        "lat": 34.0901,
        "lon": -118.4065
    },
    {
        "search_term": "New York, NY",
        "name": "New York",
        "lat": 40.7127281,
        "lon": -74.0060152
    }
   ]
   ```
   
3. Running tests  
To run tests you will need to use the unittest module in python as follows:
   ```bash
   $ python -m unittest discover -s ./tests -t ./tests
   ```
   

### Input Formats

The service accepts two formats:
- ZIP codes: 5-digit US ZIP codes (e.g., "90210")
- City, State: Format must be "City, ST" (e.g., "Miami, FL")

### Response Format

-
    ``` json
    {
        "search_term": "Miami, FL",
        "name": "Miami",
        "lat": 25.7742658,
        "lon": -80.1936589
    }
    ```


