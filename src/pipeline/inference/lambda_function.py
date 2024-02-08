import os
import json
from src.scripts.inference.inference import Inference

is_local_dst = True if 'IS_LOCAL_DST' in os.environ and os.environ['IS_LOCAL_DST'] == 'True' else False

def lambda_handler(event, context):
    chat_inference = Inference(event)
    result = chat_inference.response_main()
    print(result)

    response = {
        "status_code": 200    
    }
    
    print(f"response: {response}")    
    return response

if is_local_dst:
    with open("./src/pipeline/inference/local_event.json", "r") as json_file:
        event = json.load(json_file)
    response = lambda_handler(event, context=None)
