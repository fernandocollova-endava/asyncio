import time
import asyncio
import asyncio
import aiohttp
import aiofiles

urls = [
    "https://images.unsplash.com/photo-1564135624576-c5c88640f235",
    "https://images.unsplash.com/photo-1541698444083-023c97d3f4b6",
    "https://images.unsplash.com/photo-1522364723953-452d3431c267",
    "https://images.unsplash.com/photo-1513938709626-033611b8cc03",
    "https://images.unsplash.com/photo-1507143550189-fed454f93097",
    "https://images.unsplash.com/photo-1493976040374-85c8e12f0c0e",
    "https://images.unsplash.com/photo-1504198453319-5ce911bafcde",
    "https://images.unsplash.com/photo-1530122037265-a5f1f91d3b99",
    "https://images.unsplash.com/photo-1516972810927-80185027ca84",
    "https://images.unsplash.com/photo-1550439062-609e1531270e",
    "https://images.unsplash.com/photo-1549692520-acc6669e2f0c",
]

RATE_LIMIT = 2

async def async_download_file(url):
    local_filename = url.split("/")[-1] + ".jpg"
    # NOTE the stream=True parameter below
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            async with aiofiles.open(local_filename, "wb") as f:
                async for chunk in response.content.iter_chunked(3000):
                    await f.write(chunk)
        return local_filename


async def async_with_semaphore(url, sem):
    async with sem:
        await async_download_file(url)


async def download_with_async_limited():
    t1 = time.perf_counter()
    sem = asyncio.Semaphore(RATE_LIMIT)
    await asyncio.gather(
        *[
            async_with_semaphore(url, sem)
            for url in urls
        ]
    )
    t2 = time.perf_counter()
    print(f"Finished in {t2 - t1} seconds")

if __name__ == "__main__":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    asyncio.run(download_with_async_limited())