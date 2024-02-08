import os
import json

from src.scripts.create_index.create_faiss_index import CreateFaissIndex

is_local_dst = True if 'IS_LOCAL_DST' in os.environ and os.environ['IS_LOCAL_DST'] == 'True' else False

def lambda_handler(event, context):
    # s = ScrapeData(event)
    # s.scrape_data()
    cfi = CreateFaissIndex(event)
    cfi.create_faiss_index()

    response = {
        "status_code": 200    
    }
    
    print(f"response: {response}")    
    return response

if is_local_dst:
    with open("./src/pipeline/scraping/local_event.json", "r") as json_file:
        event = json.load(json_file)
    response = lambda_handler(event, context=None)
