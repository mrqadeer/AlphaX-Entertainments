from bs4 import BeautifulSoup
import requests
import pathlib

HEADERS = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
    'Accept-Language': 'en-US,en;q=0.9',
    'Accept-Encoding': 'gzip, deflate, br',
    'Connection': 'keep-alive',
    'Upgrade-Insecure-Requests': '1'
}

default_img = pathlib.Path('data/images/default.png')  # Corrected the path separator

def get_image_url(imdb_url):
    try:
        response = requests.get(imdb_url, headers=HEADERS, timeout=10)  # Added timeout
        soup = BeautifulSoup(response.content, 'html.parser')
        
        # Use CSS selector for more reliable and faster searching
        div = soup.select_one('div.ipc-media.ipc-media--poster-27x40.ipc-image-media-ratio--poster-27x40')

        if div:
            # Check for img tag
            img_tag = div.find('img')

            # Handle lazy-loading by checking data attributes
            if img_tag:
                img_url = img_tag.get('src') or img_tag.get('data-src') or img_tag.get('data-lazy')
                if img_url:
                    return img_url
                
        # If no image found, return default image
        return default_img

    except (requests.ConnectionError, requests.HTTPError, requests.Timeout) as e:
        return default_img

if __name__ == '__main__':
    imdb_url = 'https://www.imdb.com/title/tt5290382/'
    image_url = get_image_url(imdb_url)
    print(image_url)
