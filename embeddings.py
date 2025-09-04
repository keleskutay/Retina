from feature_extractor import FeatureExtractor
from milvus_wrapper import MilvusWrapper
from scrap import TrendyolXML
from urllib.parse import urlparse
import requests
import concurrent.futures
import os
from dotenv import load_dotenv

load_dotenv()

URI = os.getenv("URI")
TOKEN = os.getenv("TOKEN")

extractor = FeatureExtractor()

dbs = MilvusWrapper(uri=URI, token=TOKEN)

collection = dbs.load_collection("retina")

def insert_data(product_url, product_imgs, num_worker, length):
     if collection.num_entities > 0:
          res = collection.query(
                   expr= f"product_url == '{product_url}'",
                   output_fields=["product_url"]
                    )
          
          if res:
                 print("Skipping exists..")
                 return False
            
     for product_img in product_imgs:
                    img_data = requests.get(product_img).content
                    image_embedding = extractor(img_data)
                    collection.insert(
                             {"embedding": image_embedding, "product_url": product_url, "product_img": product_img},
                    )
     print(product_url)
     
     print(f"{num_worker} / {length}")


def insert_embeddings():   
    trendyol_scrapper = TrendyolXML(number_of_page = 1)

    trendyol_scrapper.save_sitemaps()

    for i in range(1):
          product_data, length = trendyol_scrapper.parse_xml(file_number = i + 1)
          with concurrent.futures.ThreadPoolExecutor(max_workers=10) as executor:
               for num_worker, (product_url, images) in enumerate(product_data.items()):
                    executor.submit(insert_data, product_url, images, num_worker, length)
                    


if __name__ == "__main__":
        insert_embeddings()