import os
from azure.cosmos import CosmosClient


class CosmosRepo():
    def __init__(self,item = None):
        self.url = os.getenv("COSMOS_URL")
        self.key = os.getenv("COSMOS_KEY")
        self.database_name = os.getenv("COSMOS_DATABASE")
        self.container_name = os.getenv("COSMOS_CONTAINER")
        self.client = CosmosClient(self.url, credential=self.key)
        self.db = self.client.get_database_client(self.database_name)
        self.container = self.db.get_container_client(self.container_name)
        self.container2_name = os.getenv("COSMOS_CONTAINER2")
        self.container2 = self.db.get_container_client(self.container2_name)
        self.container_days_name = os.getenv("COSMOS_CONTAINER3")
        self.container_days = self.db.get_container_client(self.container_days_name)
        self.item = item


    def insert(self,item):
        self.container.create_item(item)

    def obtain_all(self) -> list:
        items = list(self.container.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True
        ))
        return items

    def write_to_state(self,item):
        self.container2.upsert_item(item)

    def write_to_state_days(self,item):
        self.container_days.upsert_item(item)

    def get_model_state(self):

        items = self.container2.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True
        )
        return list(items)

    def get_model_state_days(self):
        items = self.container_days.query_items(
            query="SELECT * FROM c",
            enable_cross_partition_query=True
        )
        return list(items)
