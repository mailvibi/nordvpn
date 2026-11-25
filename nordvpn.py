from dataclasses import dataclass
from typing import List, Optional, Callable
import subprocess

@dataclass
class Result:
    success: bool
    error_info: Optional[str]
    success_info: List[str]


def execute_command(command: str, args: List[str]) -> Result:
    """
    Execute a command with given arguments.

    Args:
        command (str): The name of the command to execute.
        args (list): List of arguments to pass to the command.

    Returns:
        result: Dataclass containing execution outcome.
    """
    try:
        completed = subprocess.run([command] + args, capture_output=True, text=True)
        stdout = completed.stdout
        stderr = completed.stderr
        success = completed.returncode == 0
        return Result(success=success, error_info=None, success_info=[stdout, stderr])
    except Exception as e:
        return Result(success=False, error_info=str(e), success_info=[stdout, stderr])


def split_string_by_newlines_and_spaces(s: str) -> List[str]:
    """
    Split a string based on newlines and spaces, and return a list of entries
    that are not empty strings or spaces.

    Args:
        s (str): The input string to split.

    Returns:
        List[str]: List of non-empty, non-space entries.
    """
    # Split on any whitespace (spaces, tabs, newlines)
    parts = s.split()
    # Filter out any remaining empty or whitespace-only strings (though split() usually handles this)
    return [part for part in parts if part.strip()]


class NordVPN:
    """
    Class to interact with NordVPN CLI.
    """

    def get_supported_countries(self):
        """
        Get the list of supported countries by NordVPN.

        Returns:
            Result: Dataclass containing execution outcome.
        """
        res = execute_command("nordvpn", ["countries"])
        if res.success:
            countries = split_string_by_newlines_and_spaces(res.success_info[0])
            res.success_info = countries
        return res

    def get_supported_cities(self, country: str):
        """
        Get the list of supported cities for a given country by NordVPN.

        Args:
            country (str): The name of the country to get cities for.
        Returns:
            Result: Dataclass containing execution outcome.
        """
        res = execute_command("nordvpn", ["cities", country])
        if res.success:
            cities = split_string_by_newlines_and_spaces(res.success_info[0])
            res.success_info = cities
        return res

    def get_all_countries_and_cities(self):
        """
        Get a dictionary of all supported countries and their corresponding cities by NordVPN.

        Returns:
            Result: Dataclass containing execution outcome.
        """
        countries_result = self.get_supported_countries()
        if not countries_result.success:
            return countries_result

        country_city_map = {}
        for country in countries_result.success_info:
            cities_result = self.get_supported_cities(country)
            if cities_result.success:
                country_city_map[country] = cities_result.success_info
            else:
                country_city_map[country] = []
        return Result(success=True, error_info=None, success_info=country_city_map)


    def connect_to_country(self, country: str) -> Result:
        """
        Connect to a NordVPN server in the specified country.

        Args:
            country (str): The name of the country to connect to.

        Returns:
            Result: Dataclass containing execution outcome.
        """
        return execute_command("nordvpn", ["connect", country])


    def connect_to_city(self, country: str, city: str) -> Result:
        """
        Connect to a NordVPN server in the specified city and country.

        Args:
            country (str): The name of the country to connect to.
            city (str): The name of the city to connect to.
        Returns:
            Result: Dataclass containing execution outcome.
        """        
        return execute_command("nordvpn", ["connect", country, city])
    

    def disconnect(self):
        """
        Disconnect from the current NordVPN server.

        Returns:
            Result: Dataclass containing execution outcome.
        """
        return execute_command("nordvpn", ["disconnect"])

    def get_connection_status(self):
        """
        Get the current connection status of NordVPN.

        Returns:
            Result: Dataclass containing execution outcome.
        """
        return execute_command("nordvpn", ["status"])


