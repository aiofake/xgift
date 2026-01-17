# xgift - Python библиотека для работы с xGift API

Простая и удобная библиотека для получения информации о NFT-гифтах с платформы xGift.

**PyPI:** https://pypi.org/project/xgift/  

**GitHub:** https://github.com/aiofake/xgift

## Установка

```bash
pip install xgift
```

## Быстрый старт

### Пример 1: Получить цену гифта

```python
import asyncio
from xgift import Gift

async def main():
    client = Gift()
    price = await client.floorPrice("PlushPepe")
    print(f"PlushPepe floor price: {price} TON")
    await client.close()

asyncio.run(main())
```

### Пример 2: Получить информацию о нескольких гифтах

```python
import asyncio
from xgift import Gift

async def main():
    client = Gift()
    
    gifts = ["PlushPepe", "AstralShard", "Bitcoin"]
    prices = await client.floorPrice(gifts)
    
    for gift, price in zip(gifts, prices):
        print(f"{gift}: {price} TON")
    
    await client.close()

asyncio.run(main())
```

## Основные методы

### Класс Gift

```python
import asyncio
from xgift import Gift

async def main():
    client = Gift()
    
    # Получить floor price
    price = await client.floorPrice("PlushPepe")
    
    # Получить оценочную цену
    estimated_ton = await client.estimatedPrice("PlushPepe-1", asset="Ton")
    estimated_usd = await client.estimatedPrice("PlushPepe-1", asset="Usd")
    
    # Получить элементы коллекции
    models = await client.models_floor("PlushPepe")
    backdrops = await client.backdrops_floor("PlushPepe")
    symbols = await client.symbols_floor("PlushPepe")
    
    # График цены
    graph = await client.getFloorGraph("PlushPepe")
    
    # Проверка монохромности
    is_mono = await client.isMonochrome("PlushPepe-1")
    
    print(f"Price: {price}")
    await client.close()

asyncio.run(main())
```

### Класс GiftRaw (низкоуровневый API)

```python
import asyncio
from xgift import GiftRaw

async def main():
    raw = GiftRaw()
    
    # Прямые запросы к API
    gift_info = await raw.GiftInfo("PlushPepe-1")
    collection_info = await raw.CollectionInfo("PlushPepe")
    gifts_in_collection = await raw.CollectionGifts("PlushPepe")
    
    print(gift_info)
    await raw.close()

asyncio.run(main())
```

### Утилиты

```python
import asyncio
from xgift import tonRate, nfts, lottie

async def main():
    # Курс TON
    rate = await tonRate()
    print(f"TON rate: {rate}")
    
    # NFT
    names = await nfts("names")  # names-to-ids
    ids = await nfts("ids")      # ids-to-names
    print(names)
    
    # Lottie анимация
    animation = await lottie("plushpepe-1")
    print(animation)

asyncio.run(main())
```
