import requests
import sys
import re
import logging
from dataclasses import dataclass
from src.config import (
    COUNTRY_CODE,
    BASE_URL,
    ZIP_PATH,
    DIRECT_PATH,
    API_KEY,
    CONNECTION_TIMEOUT,
    READ_TIMEOUT,
)
from typing import Union, Optional

LOG_LEVEL = logging.CRITICAL


class GeoLocationError(Exception):
    """Base exception for GeoLocation errors"""


class ConnectionError(GeoLocationError):
    """Raised when connection fails"""


class RateLimitError(GeoLocationError):
    """Raised when API rate limit is exceeded"""


class UnauthorizedError(GeoLocationError):
    """Raised when API key is invalid"""


@dataclass
class LocationResult:
    name: str
    lat: float
    lon: float

    def __getitem__(self, item):
        return self.__dict__[item]


@dataclass
class GeoResult(LocationResult):
    search_term: str


ERROR_MESSAGES = {
    "invalid_format": "[SKIPPED] - INVALID FORMAT for `{}`. Please use `City, ST` or `5 DIGIT ZIP` format.",
    "not_found": "[NOTFOUND] - `{}` is not valid or yields no results.",
    "connection_error": "[CONNECTION ERROR] - Unable to connect to {} within {} second{}.",
    "rate_limit": "[RATE LIMIT ERROR]: Unable to get {} due to rate limit - {} - {}",
}


@dataclass
class LogMessage:
    message: str
    level: int
    should_exit: bool = False


class GeoLocationData:

    def __init__(self) -> None:
        self._errors: list[str] = []
        self._current_location: str = ""
        self._logger = self._setup_logger()

    @property
    def errors(self) -> list[str]:
        return self._errors

    def __call__(
        self, locations: Union[tuple[str, ...], list[str], str]
    ) -> list[GeoResult]:
        self._log(LogMessage("class called as a function", logging.DEBUG))
        return self.get_geoloc_data(locations)

    @staticmethod
    def _setup_logger() -> logging.Logger:
        logger = logging.getLogger(__name__)
        logger.setLevel(LOG_LEVEL)
        formatter = logging.Formatter("%(asctime)s - %(levelname)s - %(message)s")
        handler = logging.StreamHandler(sys.stdout)
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        return logger

    def _log(self, log_message: LogMessage) -> None:
        self._logger.log(log_message.level, log_message.message)

        if log_message.level in (logging.CRITICAL, logging.ERROR):
            self._errors.append(log_message.message)

        if log_message.should_exit:
            sys.exit(log_message.message)

    def _requests_handler(
        self, path: str, _params: dict, max_retries: int = 3
    ) -> Optional[LocationResult]:
        url = f"{BASE_URL + path}"
        params = {**_params, "appid": API_KEY, "limit": 1}

        try:
            response = requests.get(
                url, params=params, timeout=(CONNECTION_TIMEOUT, READ_TIMEOUT)
            )
            return self._handle_response(response)

        except requests.ConnectionError as e:
            raise ConnectionError(
                ERROR_MESSAGES["connection_error"].format(
                    url, CONNECTION_TIMEOUT, "" if CONNECTION_TIMEOUT == 1 else "s"
                )
            ) from e

        except requests.ReadTimeout as e:
            if max_retries > 0:
                self._log(
                    LogMessage(
                        f"Read timeout. Retrying {max_retries} more time(s)...",
                        logging.WARNING,
                    )
                )
                return self._requests_handler(path, _params, max_retries - 1)
            raise TimeoutError(f"Read timeout after {3 - max_retries} attempts") from e

        except (RateLimitError, UnauthorizedError) as e:
            raise e

        except Exception as e:
            self._log(
                LogMessage(
                    f"[UNHANDLED EXCEPTION] - ({type(e).__name__}) - {str(e)}",
                    logging.CRITICAL,
                    should_exit=True,
                )
            )
            return None

    def _handle_response(self, response: requests.Response) -> Optional[LocationResult]:
        match response.status_code:
            case 200:
                data = response.json()
                if data:
                    if isinstance(data, list):
                        data = data[0]
                    return LocationResult(data["name"], data["lat"], data["lon"])
                self._handle_not_found()

            case 404:
                self._handle_not_found()

            case 401:
                message = self._get_error_message(response)
                raise UnauthorizedError(
                    f"[UNAUTHORIZED ERROR]: {response.status_code} - {message}"
                )

            case 429:
                message = self._get_error_message(response)
                raise RateLimitError(
                    ERROR_MESSAGES["rate_limit"].format(
                        self._current_location, response.status_code, message
                    )
                )

            case _:
                message = self._get_error_message(response)
                self._log(
                    LogMessage(
                        f"[ERROR] - {response.status_code} - {response.url} - {message} {self._current_location}",
                        logging.CRITICAL,
                    )
                )
                return None

        return None

    @staticmethod
    def _get_error_message(response: requests.Response) -> str:
        """Extract error message from response"""
        try:
            return response.json().get("message", response.json())
        except requests.JSONDecodeError:
            return response.text

    def get_geoloc_data(
        self, locations: Union[tuple[str, ...], list[str], str]
    ) -> list[GeoResult]:
        """
        Get geolocation data for one or more locations.

        Args:
            locations: Single location string or collection of location strings

        Returns:
            List of GeoResult objects containing location data
        """

        self._log(LogMessage(f"Processing locations: {locations}", logging.DEBUG))

        if isinstance(locations, str):
            locations = self._parse_locations(locations)

        return [
            GeoResult(
                search_term=location,
                name=result["name"],
                lat=result["lat"],
                lon=result["lon"],
            )
            for location in locations
            if (result := self._get_geoloc_data(location)) is not None
        ]

    @staticmethod
    def _parse_locations(location_str: str) -> list[str]:
        """Parse quoted locations from a string"""
        locations = re.findall(r"[\"\'](.*?)[\"\']", location_str)
        return locations if locations else [location_str]

    def _get_geoloc_data(self, location: str) -> Optional[LocationResult]:
        self._log(LogMessage(f"getting geoloc data for `{location}`...", logging.DEBUG))
        self._current_location = location
        if location.isdigit() and len(location) == 5:
            return self._get_data_by_zip_code(location)
        else:
            return self._get_data_by_city_state(location)

    def _get_data_by_city_state(self, city_state: str) -> Optional[LocationResult]:
        self._log(
            LogMessage("checking if {city_state} is in valid format...", logging.DEBUG)
        )
        is_valid_format, city_name, state_code = (
            self._get_city_and_state_if_valid_pattern(city_state)
        )

        if is_valid_format:
            params = {"q": f"{city_name},{state_code},{COUNTRY_CODE}"}
            self._log(LogMessage(f"using DIRECT for {city_state}...", logging.DEBUG))
            return self._requests_handler(DIRECT_PATH, params)

        message = ERROR_MESSAGES["invalid_format"].format(city_state)
        self._log(LogMessage(message, logging.ERROR))
        return None

    def _get_data_by_zip_code(self, zip_code) -> Optional[LocationResult]:
        params = {"zip": f"{zip_code},{COUNTRY_CODE}"}
        self._log(LogMessage(f"using ZIP for {zip_code}...", logging.DEBUG))
        return self._requests_handler(ZIP_PATH, params)

    @staticmethod
    def _get_city_and_state_if_valid_pattern(
        city_state,
    ) -> tuple[bool, str | None, str | None]:
        city_state_pattern = re.compile(
            r"^([a-z\s-]+),? ([a-z]{2})$", flags=re.IGNORECASE
        )
        _match = city_state_pattern.match(city_state)
        is_match = bool(_match)
        city_name = _match.group(1) if _match else None
        state_code = _match.group(2) if _match else None
        return is_match, city_name, state_code

    def _handle_not_found(self) -> None:
        err_message = ERROR_MESSAGES["not_found"].format(
            self._current_location
            + ". Please double check the location and submit it as `City, ST` or `5 DIGIT ZIP` format"
        )
        self._log(LogMessage(err_message, logging.ERROR))
