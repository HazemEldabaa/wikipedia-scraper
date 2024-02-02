import requests
import json
from bs4 import BeautifulSoup
import re

class WikipediaScraper:
    """
    A class for the Wikipedia scraper with methods for retrieving data about country leaders.
    ----------
    Attributes:
        - base_url (str): The base URL for the country leaders API.
        - country_endpoint (str): The endpoint for retrieving countries.
        - leaders_endpoint (str): The endpoint for retrieving leaders data.
        - cookies_endpoint (str): The endpoint for refreshing cookies.
        - leaders_data (dict): A dictionary to store leaders' data.
        - cookie (Response): The cookie response obtained after refreshing.
    """

    def __init__(self) -> None:
        self.base_url = "https://country-leaders.onrender.com"
        self.country_endpoint = "/countries"
        self.leaders_endpoint = "/leaders"
        self.cookies_endpoint = "/cookie"
        self.leaders_data = {}
        self.cookie = self.refresh_cookie()
        
        self.progress_counter = 0

    def refresh_cookie(self) -> requests.Response:
        """
        Refreshes the cookie by making a request to the cookies endpoint.
        ----------
        Output:
        - Response: The cookie response after refreshing.
        """
        return requests.get(f"{self.base_url}{self.cookies_endpoint}")

    def get_countries(self) -> list:
        """
        Retrieves the list of countries from the API.
        ----------
        Output:
        - List: A list containing supported countries by the API.
        Raises:
        - ValueError: If the request to fetch countries data fails.
        """
        response = requests.get(f"{self.base_url}{self.country_endpoint}", cookies=self.refresh_cookie().cookies)
        if response.status_code == 200:
            return response.json()
            
        else:
            raise ValueError(f"Failed to fetch countries data. Status Code: {response.status_code}")

    def get_leaders(self, country:str) -> None:
        """
        Retrieves leaders data for a specific country.
        ----------
        Parameters:
        - country (str): The country for which leaders data is requested.
        ----------
        Output:
        Iterates over the leaders and runs the get_first_paragraph method on each
        ----------
        Raises:
        - ValueError: If the request to fetch leaders data fails.
        """
        params = {'country': country}
        self.leader_key = 0
        response = requests.get(f"{self.base_url}{self.leaders_endpoint}", cookies=self.refresh_cookie().cookies, params=params)
        if response.status_code == 200:
            leaders = response.json()
            self.leader_info = {}
            self.leaders_data[country] = {}
            

            for leader in leaders:
                self.leader_key += 1
                wikipedia_url = leader.get("wikipedia_url")
                birth_date = leader.get("birth_date")
                first_name = leader.get("first_name")
                last_name = leader.get("last_name")
                leader_id = leader.get("id")
                start_mandate = leader.get("start_mandate")
                end_mandate = leader.get("end_mandate")
                place_of_birth = leader.get("place_of_birth")
               
                if wikipedia_url:
                    first_paragraph = self.get_first_paragraph(wikipedia_url)
                    self.leader_info[self.leader_key] = {
                        "leader_id" : leader_id,
                        "wikipedia_url": wikipedia_url,
                        "first_name": first_name,
                        "last_name": last_name,
                        "birth_date": birth_date,
                        "place_of_birth": place_of_birth,
                        "start_mandate": start_mandate,
                        "end_mandate": end_mandate,
                        "first_paragraph": (re.sub(r"\[.*?\]|\n|\/[^\/]+\/", "", first_paragraph))
                    }
                    self.leaders_data[country][self.leader_key]=(self.leader_info[self.leader_key])
        elif response.status_code != 200:
            self.refresh_cookie
            print("Cookies refreshed")

        else:
            raise ValueError(f"Failed to fetch leaders data for {country}. Status Code: {response.status_code}")


    def get_first_paragraph(self, wikipedia_url: str) -> str:
        """
        Retrieves the first paragraph of a Wikipedia page.
        ----------
        Parameters:
        - wikipedia_url (str): The URL of the Wikipedia page.
        ----------
        Output:
        - str: The first paragraph of the Wikipedia page.
        """
        first_paragraph = ""
        
        try:
            r = requests.get(f"{wikipedia_url}").text
            soup = BeautifulSoup(r, "html.parser")
            paragraphs = soup.find_all('p')
            self.progress_counter += 1
            for p in paragraphs:
                if p.find('b') and len(p.text)>15:
                    first_paragraph = p.text
                    break
            print(f"Progress: {self.progress_counter}/136")         
            return first_paragraph
           
        except Exception as error:
            print(f"Error: {error}")
                
            
         

            
      
    def to_json_file(self, filepath: str) -> None:
        """
        Writes the leaders_data to a JSON file.
        ----------
        Parameters:
        - filepath (str): The path to the JSON file.
        ----------
        Output: a JSON file with the output of the dictionaries created
        """
        with open(filepath, 'w', encoding= "utf-8") as json_file:
            json.dump(self.leaders_data, json_file, indent = 4, separators=(',', ': '), ensure_ascii=False)
            