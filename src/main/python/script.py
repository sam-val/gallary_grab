import requests
from tqdm import tqdm
from bs4 import BeautifulSoup as bs
from urllib.parse import urljoin, urlparse
import sys
import os

def is_valid(url):
    # check if url is valid:
    parsed = urlparse(url)
    return bool(parsed.scheme) and bool(parsed.netloc)

def grab_all(url):
    """
    Get all imgs from a URL
    """

    # find all the imgs tags
    urls = []
    soup = bs(requests.get(url).content, "html.parser")
    for img in soup.find_all("img"):
        img_url = img.attrs.get("src")
        # select the ones with src attribute, grabs it
        if img_url:
            # append it with the domain to get the absolute path

            img_url = urljoin(url, img_url)

            # remove query strings, e.g. "google.com/seach?sam=True"
            try:
                query_pos = img_url.index("?")

                img_url = img_url[:query_pos]
            except ValueError:
                pass

            # check if it's an valid url
            if is_valid(img_url):
                urls.append(img_url)


    return urls


def download(urls, folder_path):
    pass

def grab_gallary_img():
    pass

def main():
    url = sys.argv[1]
    download_path = os.path.realpath(".")
    img_urls = grab_all(url)
    
    for i in img_urls:
        print(i)

if __name__ == "__main__":
    main()