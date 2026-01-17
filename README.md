# xgift - Python библиотека для работы с xGift API

Простая и удобная библиотека для получения информации о NFT-гифтах на платформе xGift.

PyPI: https://pypi.org/project/xgift/

GitHub: https://github.com/aiofake/xgift
## Установка

```bash
pip install xgift
```

## Быстрое начало

### Простой пример

```python
import asyncio
from xgift import Gift

async def main():
    client = Gift()
    
    # Получаем цену гифта
    price = await client.floorPrice("PlushPepe")
    print(f"floor PlushPepe: {price} TON")
    
    await client.close()

asyncio.run(main())
```

### Класс Gift - основной клиент

```python
# Создание клиента
client = Gift()

# Получение floor price
price = await client.floorPrice("PlushPepe")  # Один гифт
prices = await client.floorPrice(["PlushPepe", "AstralShard"])  # Несколько гифтов

# Оценочная цена
estimated_ton = await client.estimatedPrice("PlushPepe-1", asset="Ton")
estimated_usd = await client.estimatedPrice("PlushPepe-1", asset="Usd")

# Получение floor элементов коллекции
models = await client.models_floor("PlushPepe")  # модели
backdrops = await client.backdrops_floor("PlushPepe")  # фоны
symbols = await client.symbols_floor("PlushPepe")  # символы

# floor + график
graph_data = await client.getFloorGraph("PlushPepe")

# Проверка на монохром
is_monochrome = await client.isMonochrome("PlushPepe-1")

# Закрытие соединения
await client.close()
```

### Класс GiftRaw - низкоуровневый доступ

```python
from xgift import GiftRaw

raw = GiftRaw()

# Прямые запросы к API
gift_info = await raw.GiftInfo("PlushPepe-1")
collection_info = await raw.CollectionInfo("PlushPepe")
gifts_in_collection = await raw.CollectionGifts("PlushPepe")

await raw.close()
```

### Утилиты

```python
from xgift import tonRate, nfts, lottie

# Курс TON
ton_rate = await tonRate()

# Список NFT
nft_names = await nfts("names")  # names-to-ids
nft_ids = await nfts("ids") # ids-to-names

# Lottie-анимация гифта
animation = await lottie("plushpepe-1")
```
