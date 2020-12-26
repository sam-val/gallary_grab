import requests
from requests_html import HTMLSession
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

    session = HTMLSession()
    r = session.get(url)
    r.html.render()
    # find all the imgs tags
    urls = []
    soup = bs(r.html.html, "html.parser")
    divs = soup.find_all("div", {"class": "carousel-item"})
    
    imgs = [div.find("img") for div in divs]
    for img in  imgs:
        img_url = img.attrs.get("src")
        # select the ones with src attribute, grabs it
        if img_url:
            # check if it's already absolute, it not...
            if not is_valid(img_url):
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

    # close session:
    session.close()
    return urls


def download(url, folder_path):
    """
    folder_path should be a realpath when passed in
    """
    # if folder path doesn't exist, make one:
    if not os.path.isdir(folder_path):
        os.mkdir(folder_path)

    # download the content in chunks:
    r = requests.get(url, stream=True, timeout=10)

    # make the file name, aka grabbing it:
    file_path = os.path.join(folder_path, url.split("/")[-1])

    # optional: get file size:
    file_size = r.headers.get("content-length", 0)
    print(file_size)

    # exact the reponse content to a file
    with open(file_path, "wb") as f:
        for data_chunk in r.iter_content(1024):
            f.write(data_chunk)

def grab_gallary_img():
    pass

def main():
    # url = sys.argv[1]
    url = "https://mobirise.com/bootstrap-gallery/htmlimagegallery.html"
    url2 = ""
    download_path = os.path.join(os.path.dirname(os.path.realpath(__file__)), "img_folder")
    img_urls = grab_all(url)
    for i in img_urls:
        print(i)
    for img_url in img_urls:
        download(img_url, download_path)
    

if __name__ == "__main__":
    main()