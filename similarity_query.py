from feature_extractor import FeatureExtractor
from typing import List
from milvus_wrapper import MilvusWrapper
from pymilvus import Collection

extractor = FeatureExtractor()

class SimilarityQuery:
    def __init__(self, uri, token):
        self.uri = uri
        self.token = token
        self.db = MilvusWrapper(uri=self.uri, token=self.token)
        self.collection = Collection("retina")

    def query(self, image_data: str) -> List:
        self.collection.load()
        search_params = {"metric_type": "COSINE", "params": {"nprobe": 10}}

        results = self.collection.search(
            data=[extractor(image_data)],
            anns_field="embedding",
            output_fields=["product_url", "product_img"],
            param=search_params,
            limit=6,
            consistency_level="Strong"
        )

        items = []
        for result in results:
            for hit in result[:6]:
                items.append(hit)
        return items
    

if __name__ == "__main__":
    inst = SimilarityQuery()