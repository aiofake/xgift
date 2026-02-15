# xgift

[![PyPI version](https://badge.fury.io/py/xgift.svg)](https://badge.fury.io/py/xgift)
[![Python Versions](https://img.shields.io/pypi/pyversions/xgift.svg)](https://pypi.org/project/xgift/)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](https://opensource.org/licenses/MIT)

**xgift** — это простая и асинхронная Python библиотека для взаимодействия с API платформы [xGift](https://xgift.tg/). Она позволяет легко получать информацию о коллекционных NFT-гифтах, их ценах, элементах и многом другом.

Библиотека предоставляет как высокоуровневый интерфейс (`Gift`) для удобного доступа к данным, так и низкоуровневый клиент (`GiftRaw`) для прямых запросов к API.

---

## Особенности

*   **Асинхронность**: Полностью асинхронная работа на базе `asyncio` и `curl_cffi`.
*   **Простота**: Интуитивно понятный API для быстрого старта.
*   **Гибкость**: Поддержка одиночных и пакетных запросов к нескольким гифтам/коллекциям одновременно.
*   **Низкоуровневый доступ**: Возможность использовать "сырые" ответы от API через класс `GiftRaw`.
*   **Эмуляция браузера**: Использование `curl_cffi` для имитации реального браузера и обхода простых блокировок.
*   **Утилиты**: Встроенные функции для получения курса TON, списка NFT и Lottie-анимаций.

---

## Установка

Установить библиотеку можно с помощью `pip`:

```bash
pip install xgift
```

---

## Быстрый старт

### Получение минимальной цены (Floor Price) гифта

```python
import asyncio
from xgift import Gift

async def main():
    # 1. Создаем клиент
    client = Gift()

    # 2. Получаем цену для одного гифта (по его названию)
    price = await client.floorPrice("PlushPepe")
    print(f"PlushPepe floor price: {price} TON")

    # 3. Всегда закрываем клиент после использования
    await client.close()

asyncio.run(main())
```

### Получение информации для нескольких гифтов

```python
import asyncio
from xgift import Gift

async def main():
    client = Gift()

    gifts = ["PlushPepe", "AstralShard", "FreshSocks"]
    prices = await client.floorPrice(gifts)

    for gift, price in zip(gifts, prices):
        print(f"{gift}: {price} TON")

    await client.close()

asyncio.run(main())
```

---

## Подробное руководство

### 1. Класс `Gift` (Высокоуровневый)

Это основной класс для взаимодействия с API. Он использует `GiftRaw` внутри себя и предоставляет удобные методы.

#### Инициализация

```python
from xgift import Gift

client = Gift(
    proxy="http://user:pass@host:port",  # Опционально: прокси-сервер
    batch_size=5,                         # Опционально: кол-во запросов в пачке (для списков)
    delay=0.5,                             # Опционально: задержка между пачками (в секундах)
    impersonate="chrome_120"               # Опционально: браузер для эмуляции
)
```

*   `proxy`: Адрес прокси-сервера (поддерживается http/https).
*   `batch_size`: При передаче списка названий, запросы будут выполняться пачками по `batch_size` штук для оптимизации.
*   `delay`: Задержка между отправкой пачек.
*   `impersonate`: Указывает, какой браузер имитировать. По умолчанию `safari_ios`. Список поддерживаемых значений можно найти в [документации curl_cffi](https://github.com/yifeikong/curl_cffi).

#### Основные методы `Gift`

*   **`async floorPrice(name: Union[str, List[str]])`**
    *   Возвращает текущую минимальную цену (`floorPrice`) для одного или нескольких **названий коллекций**.
    *   Если передан `str`, возвращает `float` или `False` в случае ошибки.
    *   Если передан `List[str]`, возвращает `List[float | bool]`.
    *   **Пример:** `await client.floorPrice("PlushPepe")`

*   **`async simpleEstimation(slug: Union[str, List[str]])`**
    *   Возвращает упрощенную оценочную цену (`simpleEstimation.price`) для одного или нескольких **конкретных гифтов (slug)**.
    *   `slug` — это уникальный идентификатор гифта, например `"plushpepe-1"`.
    *   **Пример:** `await client.simpleEstimation("plushpepe-1")`

*   **`async estimatedPrice(slug: Union[str, List[str]], asset: Literal["Ton", "Usd"]="Ton")`**
    *   Возвращает оценочную цену (`estimatedPriceTon` или `estimatedPriceUsd`) для гифта(ов).
    *   **Пример:** `await client.estimatedPrice("plushpepe-1", asset="Usd")`

*   **`async models_floor(name: Union[str, List[str]])`**
    *   Возвращает словарь, где ключи — это названия **моделей (модификаторов)** гифта из коллекции `name`, а значения — их минимальные цены (`floorPriceTon`).
    *   **Пример:** `await client.models_floor("PlushPepe")` вернет `{'Amalgam': 9999.0, 'Aqua Plush': 9999.0, 'Barcelona': 10500.0, ...}`

*   **`async backdrops_floor(name: Union[str, List[str]])`** (Аналогично `models_floor`, но для фонов)
*   **`async symbols_floor(name: Union[str, List[str]])`** (Аналогично `models_floor`, но для символов)

*   **`async getFloorGraph(slug: Union[str, List[str]])`**
    *   Возвращает данные для построения графика цены (`floor`) для гифта(ов). Обычно это список исторических значений.

*   **`async isMonochrome(slug: Union[str, List[str]])`**
    *   Проверяет, является ли гифт монохромным.

*   **`async close()`**
    *   **Важно!** Этот метод закрывает HTTP-сессию. Всегда вызывайте его после завершения работы с клиентом, чтобы освободить ресурсы.

---

### 2. Класс `GiftRaw` (Низкоуровневый)

Предоставляет "сырые" методы, которые напрямую соответствуют эндпоинтам API xGift и возвращают необработанные `dict` с ответом от сервера.

#### Методы `GiftRaw`

*   **`async GiftInfo(slug: Union[str, List[str]])`**
    *   Получает детальную информацию о конкретном гифте по его `slug`.
    *   **Эндпоинт:** `https://app-api.xgift.tg/gifts/{slug}`

*   **`async CollectionInfo(name: Union[str, List[str]])`**
    *   Получает информацию о коллекции по её названию (например, "PlushPepe").
    *   **Эндпоинт:** `https://app-api.xgift.tg/collections/{name}`

*   **`async CollectionGifts(name: Union[str, List[str]])`**
    *   Получает список всех гифтов в коллекции, включая их модели, бэкдропы и символы.
    *   **Эндпоинт:** `https://app-api.xgift.tg/gifts/filters/{name}`

*   **`async close()`**
    *   Закрывает HTTP-сессию.

```python
import asyncio
from xgift import GiftRaw

async def main():
    raw_client = GiftRaw()
    # Получаем "сырые" данные
    data = await raw_client.GiftInfo("plushpepe-1")
    print(data)  # Выведет полный JSON-ответ от API
    await raw_client.close()

asyncio.run(main())
```

---

### 3. Утилиты (`xgift.utils`)

Набор полезных функций для быстрого доступа к дополнительным данным.

*   **`async tonRate()`**
    *   Возвращает текущий курс TON к фиатным валютам (обычно USD).
    *   **Пример:** `rate = await tonRate()`

*   **`async nfts(type: Literal["names", "ids", "all"]="all")`**
    *   Возвращает список всех доступных NFT-гифтов.
    *   `type="names"` — вернет список названий.
    *   `type="ids"` — вернет список ID.
    *   `type="all"` — вернет словарь `{name: id}`.
    *   **Пример:** `all_nfts_dict = await nfts()`

*   **`async lottie(slug: str)`**
    *   Возвращает JSON с Lottie-анимацией для указанного гифта.
    *   **Пример:** `anim = await lottie("plushpepe-1")`

*   **`async emoji(collection_id="all")`**
    *   Загружает данные из локального файла `gift_data.json`, который содержит маппинг ID коллекций, названий и их моделей. Полезно для получения официальных emojiID телеграм подарков.
    *   **Пример:** `data = await emoji("6005564615793050414")` (Вернет данные для коллекции Instant Ramen)

*   **`async graph(collection_id)`**
    *   Возвращает URL до PNG-изображения графика цены для указанной коллекции.
    *   **Пример:** `graph_url = await graph("6005564615793050414")`

---

## Лицензия

Этот проект распространяется под лицензией MIT. Подробности смотрите в файле `LICENSE`.
