import csv
import os
from dotenv import load_dotenv
from azure.cosmos import CosmosClient
import uuid

load_dotenv()


cosmos_url = os.getenv("COSMOS_URL")
cosmos_key = os.getenv("COSMOS_KEY")
cosmos_database = os.getenv("COSMOS_DATABASE")
cosmos_container = os.getenv("COSMOS_CONTAINER")
cosmos_container2 = os.getenv("COSMOS_CONTAINER2")
client = CosmosClient(url=cosmos_url, credential=cosmos_key)
database = client.get_database_client(cosmos_database)
container = database.get_container_client(cosmos_container)

csv_path = 'energy.csv'

all_items = []

def process(filename=csv_path):
    try:
        with open(filename,mode='r',encoding='utf-8') as infile:
            reader = csv.DictReader(infile)
            if 'Timestamp' not in reader.fieldnames or 'Load' not in reader.fieldnames:
                print('x and y vals invalid')

            print('reading started')
            for row in reader:
                random = uuid.uuid4()
                rstr = str(random)
                row_dict = {'Timestamp':row['Timestamp'],'Load':row['Load'],'id':rstr}
                print(row_dict)
                container.upsert_item(body=row_dict)
    except FileNotFoundError:
        print("file not found")


process()
