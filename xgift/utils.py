from .raw import GiftRaw
from typing import *
import logging, json, time
from pathlib import Path

logger = logging.getLogger(__name__)

api = GiftRaw()

async def tonRate():
    try:
        response = await api._make_request("https://app-api.xgift.tg/utils/ton-rate")
        return response.json()
    except Exception as e:
        logger.error(f"[utils]: Error in method tonRate(). Error: {e}")
        return None

async def nfts(type: Literal["names", "ids", "all"]="all"):
    try:
        if type not in ["names", "ids", "all"]:
            error_msg = f"Unsupported type: {type}. Use 'names', 'ids' or 'all'"
            raise ValueError(error_msg)
            
        response = await api._make_request(f"https://api.changes.tg/names")

        if type == "names":
            response = list(response.json().keys())
        elif type == "ids":
            response = list(response.json().values())
        elif type == "all":
            response = response.json()

        return response
    except Exception as e:
        logger.error(f"[utils]: Error in method nfts(). Error: {e}")
        return None

async def lottie(slug: str):
    try:
        response = await api._make_request(f"https://nft.fragment.com/gift/{slug}.lottie.json")
        return response.json()
    except Exception as e:
        logger.error(f"[utils]: Error in method lottie(). Error: {e}")
        return None
    
async def emoji(collection_id="all"):
    current_dir = Path(__file__).parent
    json_file = current_dir / "gift_data.json"
    
    with open(json_file, "r", encoding="utf-8") as f:
        data = json.load(f)

    if collection_id == "all":
        return data
    elif collection_id in data:
        result = data[collection_id]
        return result
    else:
        print("[utils]: Try different id")

async def graph(collection_id):
    return f"https://static-gift.xgift.tg/gifts/graphs/{collection_id}.png?timestamp={int(time.time() * 1000)}"