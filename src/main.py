import requests
from bs4 import BeautifulSoup, ResultSet
import os
import urllib.parse

from requests import Response

from logger import logger


def scrape_images_from_google(label: str, limit: int):
    # Create a directory to store downloaded images
    try:
        os.makedirs("downloads", exist_ok=True)
    except OSError:
        logger.debug("There is a problem creating the folder, it can be permissions, pathing or a file system error.")

    try:
        # Encode the search keyword for the URL
        encoded_keyword: str = urllib.parse.quote_plus(label)

        # Construct the Google Images search URL
        search_url: str = f"https://www.google.com/search?q={encoded_keyword}&tbm=isch"

        # Send a GET request to the search URL
        response: Response = requests.get(search_url)

        # Parse the HTML response using BeautifulSoup
        soup = BeautifulSoup(response.content, "html.parser")

        # Find all image tags in the parsed HTML
        image_tags: ResultSet = soup.find_all("img")

        # Download and save the images
        for i, img_tag in enumerate(image_tags[:limit]):
            # Extract the image source URL
            image_url = img_tag["src"]

            if 'https://' not in image_url:
                continue

            # Send a GET request to download the image
            image_response = requests.get(image_url)

            # Save the image to the 'downloads' directory
            with open(f"downloads/{label}_{i + 1}.jpg", "wb") as f:
                f.write(image_response.content)
    except AttributeError:
        logger.debug("The attribute that you are trying to access already exists.")
    except TypeError:
        logger.debug("An invalid argument has been typed in a method or function for BeautifulSoup.")
    except ValueError:
        logger.debug("An invalid argument has been passed.")


if __name__ == "__main__":
    # Specify the label and the number of images to download
    label: str = "cats"
    limit: int = 10  # Number of images to download

    # Call the function to scrape and download images
    scrape_images_from_google(label, limit)
