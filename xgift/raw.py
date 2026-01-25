import asyncio, logging
from typing import *
from curl_cffi.requests import AsyncSession, Response

logger = logging.getLogger(__name__)

class GiftRaw:
    def __init__(self, proxy: Optional[str] = None, batch_size: int = 1, delay: float = 0, impersonate: str = "safari_ios"):
        self.batch_size = batch_size
        self.delay = delay
        
        if proxy:
            self.client = AsyncSession(impersonate=impersonate, proxies={"http": proxy, "https": proxy})
        else:
            self.client = AsyncSession(impersonate=impersonate)
    

    async def _make_request(self, url: str, method: str = "GET", params: Optional[Dict] = None) -> Optional[Response]:
        try:
            response = await self.client.request(method=method, url=url, params=params, headers={'Accept': 'application/json, text/plain, */*', 'Accept-Language': 'en-US,en;q=0.9', 'Referer': 'https://xgift.tg/', 'Origin': 'https://xgift.tg', 'Sec-Fetch-Dest': 'empty', 'Sec-Fetch-Mode': 'cors', 'Sec-Fetch-Site': 'same-site'})
            response.raise_for_status()
            return response
        except Exception as e:
            logger.error(f"[GiftRaw]: Error in method _make_request(). URL: {url}, Error: {e}")
            return None
    

    async def GiftInfo(self, slug: Union[str, List[str]]):
        try:
            if isinstance(slug, list):
                results = []
                
                for i in range(0, len(slug), self.batch_size):
                    batch = slug[i:i + self.batch_size]
                    
                    tasks = []
                    for item in batch:
                        tasks.append(self._make_request(url=f"https://app-api.xgift.tg/gifts/{item}"))
                    
                    batch_responses = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    for response in batch_responses:
                        if isinstance(response, Exception) or response is None:
                            results.append({})
                        else:
                            try:
                                results.append(response.json())
                            except Exception as e:
                                logger.error(f"[GiftRaw]: Error in method GiftInfo(). Failed to parse JSON, Error: {e}")
                                results.append({})
                    
                    if i + self.batch_size < len(slug) and self.delay > 0:
                        await asyncio.sleep(self.delay)
                
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
                results = []
                
                for i in range(0, len(name), self.batch_size):
                    batch = name[i:i + self.batch_size]
                    
                    tasks = []
                    for item in batch:
                        item = item.replace(" ", "").replace("'", "").replace("-", "")
                        tasks.append(self._make_request(url=f"https://app-api.xgift.tg/collections/{item}"))
                    
                    batch_responses = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    for response in batch_responses:
                        if isinstance(response, Exception) or response is None:
                            results.append({})
                        else:
                            try:
                                results.append(response.json())
                            except Exception as e:
                                logger.error(f"[GiftRaw]: Error in method CollectionInfo(). Failed to parse JSON, Error: {e}")
                                results.append({})
                    
                    if i + self.batch_size < len(name) and self.delay > 0:
                        await asyncio.sleep(self.delay)
                
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
                results = []
                
                for i in range(0, len(name), self.batch_size):
                    batch = name[i:i + self.batch_size]
                    
                    tasks = []
                    for item in batch:
                        item = item.replace(" ", "").replace("'", "").replace("-", "")
                        tasks.append(self._make_request(url=f"https://app-api.xgift.tg/gifts/filters/{item}", params={"collectionType": "upgradable"}))
                    
                    batch_responses = await asyncio.gather(*tasks, return_exceptions=True)
                    
                    for response in batch_responses:
                        if isinstance(response, Exception) or response is None:
                            results.append({})
                        else:
                            try:
                                results.append(response.json())
                            except Exception as e:
                                logger.error(f"[GiftRaw]: Error in method CollectionGifts(). Failed to parse JSON, Error: {e}")
                                results.append({})
                    
                    if i + self.batch_size < len(name) and self.delay > 0:
                        await asyncio.sleep(self.delay)
                
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
            await self.client.close()
        except Exception as e:
            logger.error(f"[GiftRaw]: Error in method close(). Error: {e}")
