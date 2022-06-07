from scrapper_boilerplate.parser_handler import init_crawler, init_parser
from scrapper_boilerplate.output import log
from scrapper_boilerplate import dataToCSV, remove_duplicates, remove_duplicates_on_list
import logging
import concurrent.futures


class getCoordinates:
    def __init__(self, filename) -> None:
        self.filename = filename

    def start(self):
        cities = []
        for links in self.get_cities_coordinates("https://latitude.to/map/mx/mexico/cities/alphabetically/page/1"):
            cities.append(links)

        log(f"Total cities: {len(cities)}")
        with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
            executor.map(self.get_page_coordinates, cities)


    def get_cities_coordinates(self, url):
        soap = init_crawler(url)
        container = soap.find("div", class_="b-cities-listing cols-3")
        for li in container.find_all("li"):
            city = li.find("a").get_text()
            city_url = "https://latitude.to" + li.find("a")["href"]
            logging.debug(f"{city}: {city_url}")
            yield city_url

        next_page = soap.find("a", class_="next")
        if next_page:
            next_page_url = next_page["href"]
            log(f"Next page: {next_page_url}")
            yield from self.get_cities_coordinates("https://latitude.to" + next_page_url)

    def get_page_coordinates(self, page):
        log(f"Getting coordinates for {page}")
        try:
            soap = init_crawler(page)
            coords = soap.find("input", {"id": "DD"})['value']
            # coords = strip_ponctuation(coords)
            data = {}
            data["lat"] = coords.split(' ')[0]
            data["lgn"] = coords.split(' ')[1]
            data["city"] = soap.find("h2").find_all("span")[-1].text
            # [ print(f"{key}: {value}") for key, value in data.items() ]
            dataToCSV(data, self.filename)

        except Exception as e:
            logging.error(e)
            return
