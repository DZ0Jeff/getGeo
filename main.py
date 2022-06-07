from src.models import getCoordinates
import logging

logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s', datefmt='%d-%b-%y %H:%M:%S', filename='coords.log', filemode='a')


def main():
    crawler = getCoordinates('data/mx-full.csv')
    crawler.start()


if __name__ == "__main__":
    main()
