import csv
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def extract_filename_from_url(url):
    parsed_url = urlparse(url)
    netloc_parts = parsed_url.netloc.split(".")
    return netloc_parts[-2] if len(netloc_parts) >= 2 else netloc_parts[-1]


def create_csv_file_with_header(file_name):
    try:
        with open(f"{file_name}.csv", mode="w", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(["SL No", "Links", "Title Tag", "Meta Description"])
        file.close()
    except Exception as e:
        print(f"An error occurred: {e}")


def get_soup(url):
    response = requests.get(url)
    return BeautifulSoup(response.text, "html.parser")


def get_website_description(soup):
    # Safely get the meta tag with name="description"
    description_tag = soup.find("meta", attrs={"name": "description"})
    return description_tag.get("content") if description_tag else "No description given"


def get_website_title(soup):
    # Safely get the title tag value
    title_tag = soup.find("title")
    return title_tag.string if title_tag else "No title found"


def write_to_csv(data):
    try:
        with open(f'{data["file_name"]}.csv', mode="a", newline="", encoding="utf-8") as file:
            writer = csv.writer(file)
            writer.writerow(
                [
                    data["serial_number"],
                    data["website_link"],
                    data["website_title"],
                    data["website_description"],
                ]
            )
        file.close()
    except Exception as e:
        print(f"An error occurred: {e}")


def add_homepage_to_csv(soup, file_name, url):
    website_title = get_website_title(soup)
    website_description = get_website_description(soup)
    data = {
        "file_name": file_name,
        "serial_number": 1,
        "website_link": url,
        "website_title": website_title,
        "website_description": website_description,
    }
    write_to_csv(data)


def add_all_webpages_to_csv(file_name, links):
    serial_number = 2
    for link in links:
        soup = get_soup(link)
        website_title = get_website_title(soup)
        website_description = get_website_description(soup)
        data = {
            "file_name": file_name,
            "serial_number": serial_number,
            "website_link": link,
            "website_title": website_title,
            "website_description": website_description,
        }
        write_to_csv(data)
        serial_number += 1


def get_href_value(anchor_tags):
    return [anchor_tag["href"] for anchor_tag in anchor_tags]


def remove_hash(hrefs):
    """Internal links with '#' in the links
    * '#service' not '/services'
    * '/blogs#blog-1' not '/blogs'
    """
    return [href for href in hrefs if "#" not in href]


def remove_external(hrefs, url):
    return [href for href in hrefs if href.startswith(url) or href.startswith("/")]


def get_full_links(hrefs, url):
    return [f"{url}{href}" if not href.startswith("http") else href for href in hrefs]


def main(url):
    print("The program is running...")
    soup = get_soup(url)
    anchor_tags = soup.find_all("a", href=True)
    # Extract and the filtered href values
    hrefs = remove_external(remove_hash(get_href_value(anchor_tags)), url)
    full_links = get_full_links(hrefs, url)
    file_name = extract_filename_from_url(url)
    create_csv_file_with_header(file_name)
    add_homepage_to_csv(soup, file_name, url)
    add_all_webpages_to_csv(file_name, full_links)
    print("CSV file has been created with the filtered links.")


# if __name__ == '__main__':
#     main()
