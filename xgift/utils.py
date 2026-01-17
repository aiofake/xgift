from .raw import GiftRaw
from typing import *
import logging

logger = logging.getLogger(__name__)

api = GiftRaw()

async def tonRate():
    try:
        response = await api._make_request("https://app-api.xgift.tg/utils/ton-rate")
        return response.json()
    except Exception as e:
        logger.error(f"[utils]: Error in method tonRate(). Error: {e}")
        return None

async def nfts(type: Literal["names", "ids"]):
    try:
        if type not in ["names", "ids"]:
            error_msg = f"Unsupported type: {type}. Use 'names' or 'ids'"
            raise ValueError(error_msg)
            
        response = await api._make_request(f"https://api.changes.tg/{type}")
        return response.json()
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
