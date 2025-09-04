from bs4 import BeautifulSoup
import requests
from urllib.parse import urlparse

class TrendyolXML:
    def __init__(self, number_of_page: int = 1):
        self.number_of_page = number_of_page

    def save_sitemaps(self) -> bool:
        try:
            for i in range(self.number_of_page):
                xml = requests.get(f"https://www.trendyol.com/sitemap_products{i + 1}.xml").content
                
                with open(f"sitemaps/map{i + 1}.xml", "wb") as f:
                    f.write(xml)
        except Exception as e:
            raise e
        finally:
                return True

    def parse_xml(self, file_number: int = 1) -> dict[str, list]:
        product_data = {}

        with open(f"sitemaps/map{file_number}.xml", "rb") as f:
            soup = BeautifulSoup(f)

            urls = soup.find_all(name= "url")

            for item in urls:
                url = item.find(name="loc").text
                image_node = item.find_all(name="image:image")

                imgs = []
                for url_imgs in image_node:
                    for url_img in url_imgs.find_all(name="image:loc"):
                        imgs.append(url_img.text)

                product_data[url] = imgs
            
        return product_data, len(urls)

                
if __name__ == "__main__":
    ob = TrendyolXML()

    data = ob.xml_parse()

    for number, (product_url, images) in enumerate(data.items()):
         print(f"Saved. {number} / {len(data)}")
    
    