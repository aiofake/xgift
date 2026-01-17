from .raw import GiftRaw
from typing import *
import asyncio, httpx, logging

logger = logging.getLogger(__name__)

class Gift:
    def __init__(self):
        self.client = httpx.AsyncClient(http2=True)  

    async def floorPrice(self, name: Union[str, List[str]]):
        try:
            api = GiftRaw()
            data = await api.CollectionInfo(name)
            
            if isinstance(name, list):
                results = []
                for item in data:
                    if isinstance(item, dict):
                        results.append(item.get("floorPrice", False))
                    else:
                        results.append(False)
                return results
            else:
                if isinstance(data, dict):
                    return data.get("floorPrice", False)
                return False
        except Exception as e:
            logger.error(f"[Gift]: Error in method floorPrice(). Error: {e}")
            return [] if isinstance(name, list) else False
        

    async def estimatedPrice(self, slug: Union[str, List[str]], asset: Literal["Ton", "Usd"]="Ton"):
        try:
            api = GiftRaw()
            data = await api.GiftInfo(slug)
            
            if isinstance(slug, list):
                results = []
                for item in data:
                    if isinstance(item, dict):
                        results.append(item.get(f"estimatedPrice{asset}", False))
                    else:
                        results.append(False)
                return results
            else:
                if isinstance(data, dict):
                    return data.get(f"estimatedPrice{asset}", False)
                return False
        except Exception as e:
            logger.error(f"[Gift]: Error in method estimatedPrice(). Error: {e}")
            return [] if isinstance(slug, list) else False
    

    async def models_floor(self, name: Union[str, List[str]]):
        try:
            if isinstance(name, list):
                tasks = []
                for item in name:
                    tasks.append(self._one_item(item, "Model"))
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                return {
                    item: result if not isinstance(result, Exception) else {}
                    for item, result in zip(name, results)
                }
            else:
                return await self._one_item(name, "Model")
        except Exception as e:
            logger.error(f"[Gift]: Error in method models_floor(). Error: {e}")
            return {} if isinstance(name, str) else {}
        

    async def backdrops_floor(self, name: Union[str, List[str]]):
        try:
            if isinstance(name, list):
                tasks = []
                for item in name:
                    tasks.append(self._one_item(item, "Backdrop"))
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                return {
                    item: result if not isinstance(result, Exception) else {}
                    for item, result in zip(name, results)
                }
            else:
                return await self._one_item(name, "Backdrop")
        except Exception as e:
            logger.error(f"[Gift]: Error in method backdrops_floor(). Error: {e}")
            return {} if isinstance(name, str) else {}
    

    async def symbols_floor(self, name: Union[str, List[str]]):
        try:
            if isinstance(name, list):
                tasks = []
                for item in name:
                    tasks.append(self._one_item(item, "Symbol"))
                
                results = await asyncio.gather(*tasks, return_exceptions=True)
                
                return {
                    item: result if not isinstance(result, Exception) else {}
                    for item, result in zip(name, results)
                }
            else:
                return await self._one_item(name, "Symbol")
        except Exception as e:
            logger.error(f"[Gift]: Error in method symbols_floor(). Error: {e}")
            return {} if isinstance(name, str) else {}
        

    async def _one_item(self, name: str, type: Literal["Model", "Backdrop", "Symbol"]):
        try:
            formatted = name.replace(" ", "").replace("'", "").replace("-", "")
            url = f"https://app-api.xgift.tg/gifts/filters/{formatted}"
            
            api = GiftRaw()
            response = await api._make_request(url=url, params={"collectionType": "upgradable"})
            
            if response is None:
                return {}
            
            result = {}
            try:
                data = response.json()
                f_name = "pattern" if type == "Symbol" else type.lower()
                for m in data.get(f"gift{type}", []):
                    if (n := m.get(f_name)) and (p := m.get("floorPriceTon")):
                        try:
                            result[n] = float(p)
                        except ValueError as e:
                            logger.error(f"[Gift]: ValueError in method _one_item(). Failed to convert price to float: {p}, Error: {e}")
                            result[n] = p
            except Exception as e:
                logger.error(f"[Gift]: Error in method _one_item(). Failed to parse JSON, Error: {e}")
                return {}
            
            return result
        except Exception as e:
            logger.error(f"[Gift]: Error in method _one_item(). Error: {e}")
            return {}
    

    async def getFloorGraph(self, slug: Union[str, List[str]]):
        try:
            api = GiftRaw()
            data = await api.CollectionInfo(slug)
            
            if isinstance(slug, list):
                results = []
                for item in data:
                    if isinstance(item, dict):
                        results.append(item.get("floor"))
                    else:
                        results.append(False)
                return results
            else:
                if isinstance(data, dict):
                    return data.get("floor")
                return False
        except Exception as e:
            logger.error(f"[Gift]: Error in method getFloorGraph(). Error: {e}")
            return [] if isinstance(slug, list) else False
        

    async def isMonochrome(self, slug: Union[str, List[str]]):
        try:
            api = GiftRaw()
            data = await api.GiftInfo(slug)
            
            if isinstance(slug, list):
                results = []
                for item in data:
                    if isinstance(item, dict):
                        results.append(item.get("isMonochrome", False))
                    else:
                        results.append(False)
                return results
            else:
                if isinstance(data, dict):
                    return data.get("isMonochrome", False)
                return False
        except Exception as e:
            logger.error(f"[Gift]: Error in method isMonochrome(). Error: {e}")
            return [] if isinstance(slug, list) else False
    
    async def close(self):
        try:
            await self.client.aclose()
        except Exception as e:
            logger.error(f"[Gift]: Error in method close(). Error: {e}")
