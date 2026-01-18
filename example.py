from xgift import *
import asyncio


api = Gift()
async def main():
    nft = await nfts("names")
    print(nft)
    data = await api.models_floor(nft)
    # data = await api.backdrops_floor(nft)
    # data = await api.symbols_floor(nft)
    print(data)

asyncio.run(main())