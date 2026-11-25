
import urllib.request
import os
from urllib.parse import urlparse
from nordvpn import NordVPN
from nordvpn import Result
import time
from typing import Callable, Tuple, Optional


def download_file(url: str) -> Tuple[bool, Optional[str]]:
    """
    Download a file from the given URL.

    Args:
        url (str): The URL of the file to download.

    Returns:
        Tuple[bool, Optional[str]]: (success, file_path) where file_path is the path to the downloaded file if successful, None otherwise.
    """
    try:
        # Parse the URL to get the filename
        parsed_url = urlparse(url)
        filename = os.path.basename(parsed_url.path)
        if not filename:
            filename = "downloaded_file"
        
        # Download the file
        with urllib.request.urlopen(url) as response:
            with open(filename, 'wb') as f:
                f.write(response.read())
        
        return True, filename
    except Exception as e:
        # Log the error if needed, but don't raise
        print(f"Error downloading file: {e}")
        return False, None


def delete_file(file_path: str) -> bool:
    """
    Delete the file at the given file path.

    Args:
        file_path (str): The path to the file to delete.

    Returns:
        bool: True if the file was deleted successfully, False otherwise.
    """
    try:
        if os.path.exists(file_path):
            os.remove(file_path)
            return True
        else:
            print(f"File does not exist: {file_path}")
            return False
    except Exception as e:
        print(f"Error deleting file: {e}")
        return False


def do_task_for_all_countries_and_cities(task_function, connection_count: int = 5):
    if not callable(task_function):
        print("Provided task_function is not callable.")
        return
    connected_count = 0
    vpn = NordVPN()
    result = vpn.get_all_countries_and_cities()
    if result.success:
        for country, cities in result.success_info.items():
            for city in cities:
                print(f"Connecting to NordVPN server in: {country}, {city}")
                if connected_count >= connection_count:
                    print(f"Reached the specified connection count of {connection_count}. Stopping further connections.")
                    return
                conn_result = vpn.connect_to_city(country, city)
                if conn_result.success:
                    print(f"Successfully connected to NordVPN server in {country}, {city}.")
                    connected_count += 1
                    status_result = vpn.get_connection_status()
                    if status_result.success:
                        print("Connection status:")
                        print(status_result.success_info[0])
                        print("*" * 40)
                        task_function()
                        print("*" * 40)
                    else:
                        print(f"Failed to retrieve connection status. Error: {status_result.error_info}")
                    disconnect_result = vpn.disconnect()
                    if disconnect_result.success:
                        print("Successfully disconnected from NordVPN.")
                    else:
                        print(f"Failed to disconnect from NordVPN. Error: {disconnect_result.error_info}")
                    time.sleep(5)  # Sleep for a short time before connecting to the next city
                else:
                    print(f"Failed to connect to NordVPN server in {country}, {city}. Error: {conn_result.error_info}:{conn_result.success_info[1]}")
    else:
        print(f"Error: {result.error_info}")


def test_function():
    print("This is a test function that runs after connecting to each country.")


def get_easy_cert():
    pass


if __name__ == "__main__":
    # Test the function
#    test_nordvpn_get_supported_countries()
    for _ in range(0,1000):
        do_task_for_all_countries_and_cities(get_easy_cert, connection_count=1000000)
#    test_nordvpn_get_all_countries_and_cities()
