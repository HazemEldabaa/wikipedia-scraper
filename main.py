from src.scraper import WikipediaScraper


def main() -> None:
    """Main function to run the WikipediaScraper and save leaders data to a JSON file."""
    scraper = WikipediaScraper()
    scraper.refresh_cookie()
    print("Cookies created")

    countries = scraper.get_countries()
    print("Countries:", countries)
    for country_code in countries:
        scraper.get_leaders(country_code) 
        print(f"Packing info for {country_code}...")
    scraper.to_json_file('leaders_data.json')
    print("Leaders data saved to leaders_data.json")

if __name__ == "__main__":
    main()
