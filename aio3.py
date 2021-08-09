import aiohttp
import asyncio
import time


async def false_asyncio():
    async with aiohttp.ClientSession() as session:
        for number in range(1, 105):
            url = f'https://deckofcardsapi.com/api/deck/new/draw/'
            async with session.get(url) as response:
                card = await response.json()
                card_value = card["cards"][0]["value"]
                card_suit = card["cards"][0]["suit"]
                print(f"{card_value} of {card_suit} in deck {number}")


async def get_card(deck_number):
    async with aiohttp.ClientSession() as session:
        url = f'https://deckofcardsapi.com/api/deck/new/draw/'
        async with session.get(url) as response:
            card = await response.json()
            card_value = card["cards"][0]["value"]
            card_suit = card["cards"][0]["suit"]
            print(f"{card_value} of {card_suit} in deck {deck_number}")


async def true_asyncio():
    await asyncio.gather(*(get_card(number) for number in range(1, 105)))

if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    try:
        start_time = time.time()
        loop.run_until_complete(false_asyncio())
        loop.run_until_complete(asyncio.sleep(1))
        print("---- seconds ---- {}".format(time.time() - start_time))
        start_time = time.time()
        loop.run_until_complete(true_asyncio())
        loop.run_until_complete(asyncio.sleep(1))
        print("---- seconds ---- {}".format(time.time() - start_time))
    except RuntimeError:
        pass
    finally:
        loop.close()
