import httpx, asyncio, logging
from typing import *
from httpx import Response

logger = logging.getLogger(__name__)

class GiftRaw:
    def __init__(self):
        self.client = httpx.AsyncClient(http2=True)
    
    async def _make_request(self, url: str, method: str = "GET", params: Optional[Dict] = None, headers: Optional[Dict] = None) -> Optional[Response]:
        try:
            response = await self.client.request(method=method, url=url, params=params, headers=headers)
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"[GiftRaw]: Error in method _make_request(). URL: {url}, Error: {e}")
            return None
    
    async def GiftInfo(self, slug: Union[str, List[str]]):
        try:
            if isinstance(slug, list):
                tasks = []
                for item in slug:
                    tasks.append(self._make_request(url=f"https://app-api.xgift.tg/gifts/{item}"))
                
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                
                results = []
                for response in responses:
                    if isinstance(response, Exception) or response is None:
                        results.append({})
                    else:
                        try:
                            results.append(response.json())
                        except Exception as e:
                            logger.error(f"[GiftRaw]: Error in method GiftInfo(). Failed to parse JSON, Error: {e}")
                            results.append({})
                
                return results

            else:
                response = await self._make_request(url=f"https://app-api.xgift.tg/gifts/{slug}")
                
                if response is None:
                    return {}
                
                try:
                    return response.json()
                except Exception as e:
                    logger.error(f"[GiftRaw]: Error in method GiftInfo(). Failed to parse JSON, Error: {e}")
                    return {}
        except Exception as e:
            logger.error(f"[GiftRaw]: Error in method GiftInfo(). Error: {e}")
            return {} if isinstance(slug, str) else []
    
    async def CollectionInfo(self, name: Union[str, List[str]]):
        try:
            if isinstance(name, list):
                tasks = []
                for item in name:
                    item = item.replace(" ", "").replace("'", "").replace("-", "")
                    tasks.append(self._make_request(url=f"https://app-api.xgift.tg/collections/{item}"))
                
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                
                results = []
                for response in responses:
                    if isinstance(response, Exception) or response is None:
                        results.append({})
                    else:
                        try:
                            results.append(response.json())
                        except Exception as e:
                            logger.error(f"[GiftRaw]: Error in method CollectionInfo(). Failed to parse JSON, Error: {e}")
                            results.append({})
                
                return results

            else:
                name = name.replace(" ", "").replace("'", "").replace("-", "")
                response = await self._make_request(url=f"https://app-api.xgift.tg/collections/{name}")
                
                if response is None:
                    return {}
                
                try:
                    return response.json()
                except Exception as e:
                    logger.error(f"[GiftRaw]: Error in method CollectionInfo(). Failed to parse JSON, Error: {e}")
                    return {}
        except Exception as e:
            logger.error(f"[GiftRaw]: Error in method CollectionInfo(). Error: {e}")
            return {} if isinstance(name, str) else []
            
    async def CollectionGifts(self, name: Union[str, List[str]]):
        try:
            if isinstance(name, list):
                tasks = []
                for item in name:
                    item = item.replace(" ", "").replace("'", "").replace("-", "")
                    tasks.append(self._make_request(url=f"https://app-api.xgift.tg/gifts/filters/{item}", params={"collectionType": "upgradable"}))
                
                responses = await asyncio.gather(*tasks, return_exceptions=True)
                
                results = []
                for response in responses:
                    if isinstance(response, Exception) or response is None:
                        results.append({})
                    else:
                        try:
                            results.append(response.json())
                        except Exception as e:
                            logger.error(f"[GiftRaw]: Error in method CollectionGifts(). Failed to parse JSON, Error: {e}")
                            results.append({})
                
                return results

            else:
                name = name.replace(" ", "").replace("'", "").replace("-", "")
                response = await self._make_request(url=f"https://app-api.xgift.tg/gifts/filters/{name}", params={"collectionType": "upgradable"})
                
                if response is None:
                    return {}
                
                try:
                    return response.json()
                except Exception as e:
                    logger.error(f"[GiftRaw]: Error in method CollectionGifts(). Failed to parse JSON, Error: {e}")
                    return {}
        except Exception as e:
            logger.error(f"[GiftRaw]: Error in method CollectionGifts(). Error: {e}")
            return {} if isinstance(name, str) else []
            

    async def close(self):
        try:
            await self.client.aclose()
        except Exception as e:
            logger.error(f"[GiftRaw]: Error in method close(). Error: {e}")