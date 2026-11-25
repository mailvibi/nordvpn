from nordvpn import NordVPN



def test_nordvpn_get_supported_countries():
    """
    Test the retrieval of supported countries by NordVPN.
    """
    vpn = NordVPN()
    result = vpn.get_supported_countries()
    if result.success:
        print("Supported countries:")
        for i, country in enumerate(result.success_info):
            print(f"{i+1}. {country}")
    else:
        raise Exception(f"Error retrieving supported countries: {result.error_info}")


def test_nordvpn_get_supported_cities(country: str):
    """
    Test the retrieval of supported cities for a given country by NordVPN.

    Args:
        country (str): The name of the country to get cities for.
    """
    vpn = NordVPN()
    result = vpn.get_supported_cities(country)
    if result.success:
        print(f"Supported cities in {country}:")
        for i, city in enumerate(result.success_info):
            print(f"{i+1}. {city}")
    else:
        raise Exception(f"Error retrieving supported cities for {country}: {result.error_info}")


def test_nordvpn_get_all_countries_and_cities():
    """
    Test the retrieval of all supported countries and their corresponding cities by NordVPN.
    """
    vpn = NordVPN()
    result = vpn.get_all_countries_and_cities()
    if result.success:
        print("Supported countries and their corresponding cities:")
        for country, cities in result.success_info.items():
            print(f"{country}:")
            for i, city in enumerate(cities):
                print(f"  {i+1}. {city}")
    else:
        raise Exception(f"Error retrieving all countries and cities: {result.error_info}")


def test_nordvpn_connect_to_country(country: str):
    """
    Test the connection to a NordVPN server in the specified country.

    Args:
        country (str): The name of the country to connect to.       
    """
    vpn = NordVPN()
    result = vpn.connect_to_country(country)
    if result.success:
        print(f"Successfully connected to NordVPN server in {country}.")
        status_result = vpn.get_connection_status()
        if status_result.success:
            print("Connection status:")
            print(status_result.success_info[0])
        else:
            raise Exception(f"Failed to retrieve connection status. Error: {status_result.error_info}")
    else:
        raise Exception(f"Failed to connect to NordVPN server in {country}. Error: {result.error_info}")


def test_nordvpn_connect_to_city(country: str, city: str):
    """
    Test the connection to a NordVPN server in the specified city and country.

    Args:
        country (str): The name of the country to connect to.
        city (str): The name of the city to connect to.       
    """
    vpn = NordVPN()
    result = vpn.connect_to_city(country, city)
    if result.success:
        print(f"Successfully connected to NordVPN server in {country}, {city}.")
        status_result = vpn.get_connection_status()
        if status_result.success:
            print("Connection status:")
            print(status_result.success_info[0])
        else:
            raise Exception(f"Failed to retrieve connection status. Error: {status_result.error_info}")
    else:
        raise Exception(f"Failed to connect to NordVPN server in {country}, {city}. Error: {result.error_info}")


def main():
    """
    Main function to run all tests one by one.
    """
    try:
        print("Running test_nordvpn_get_supported_countries...")
        test_nordvpn_get_supported_countries()
        print("Test passed.\n")

        print("Running test_nordvpn_get_supported_cities for United States...")
        test_nordvpn_get_supported_cities("United States")
        print("Test passed.\n")

        print("Running test_nordvpn_get_all_countries_and_cities...")
        test_nordvpn_get_all_countries_and_cities()
        print("Test passed.\n")

        print("Running test_nordvpn_connect_to_country for United States...")
        test_nordvpn_connect_to_country("United States")
        print("Test passed.\n")

        print("Running test_nordvpn_connect_to_city for United States, New York...")
        test_nordvpn_connect_to_city("United States", "New York")
        print("Test passed.\n")

        print("All tests passed!")

    except Exception as e:
        print(f"Test failed: {e}")


if __name__ == "__main__":
    main()
