from pymilvus import MilvusClient, Collection, CollectionSchema, DataType, FieldSchema
from pymilvus import connections
import os
from dotenv import load_dotenv

class MilvusWrapper:
    def __init__(self, uri:str, token:str):
        self.uri = uri
        self.token = token
        self.client = MilvusClient(uri=self.uri,token=self.token)
        self._conn = connections.connect(alias="default", host="localhost", port="19530", token=self.token)

    def add_index_save(self, collection_name="", field_name:str = "", metric_type:str = "", index_type:str = "", index_name:str = "", params:dict = {}, **kwargs):
        describe_index = self.client.describe_index(collection_name, index_name)

        if not isinstance(describe_index, dict):
            index_params = self.client.prepare_index_params()
            index_params.add_index(
                field_name=field_name,
                metric_type=metric_type,
                index_type=index_type,
                index_name=index_name,
                params=params
            )
            return self._save_index(collection_name, index_params)
        
        return describe_index
    
    def _save_index(self, collection_name, index_params, **kwargs) -> None:
        self.client.create_index(
            collection_name=collection_name,
            index_params=index_params,
            **kwargs
        )

        return None

    def drop_collection(self, collection_name:str):
        self.client.drop_collection(collection_name)

    def load_collection(self, collection_name:str):
        return Collection(collection_name)

    def create_collection(self, collection_name:str, schema:CollectionSchema) -> Collection:
        if not self.client.has_collection(collection_name):
            self.client.create_collection(
                collection_name = collection_name,
                schema = schema
            )   
        return Collection(collection_name)


if __name__ == "__main__":

    load_dotenv()

    URI = os.getenv("URI")
    TOKEN = os.getenv("TOKEN")

    db = MilvusWrapper(uri=URI, token=TOKEN)

    fields = [
        FieldSchema(name="id", dtype=DataType.INT64, is_primary=True, auto_id=True),
        FieldSchema(name="product_url", dtype=DataType.VARCHAR, max_length=2000),
        FieldSchema(name="product_img", dtype=DataType.VARCHAR, max_length=2000),
        FieldSchema(name="embedding", dtype=DataType.FLOAT_VECTOR, dim=768)  # DINOv2-B = 768 dim
    ]

    schema = CollectionSchema(fields=fields, description="Retina Collection")

    collection = db.create_collection(collection_name="retina", schema=schema)

    db.add_index_save(
        collection_name="retina",
        field_name="embedding",
        metric_type="COSINE",
        index_type="IVF_FLAT",
        index_name="embedding_index",
        params={ "nlist": 128 }
    )

    print(collection.num_entities)

