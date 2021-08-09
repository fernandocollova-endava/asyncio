import requests
import time
import concurrent.futures
import asyncio
import aiohttp
import aiofiles

img_urls = [
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


def download_file(url):
    local_filename = url.split("/")[-1] + ".jpg"
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=3000):
                # If you have chunk encoded response uncomment if
                # and set chunk_size parameter to None.
                # if chunk:
                f.write(chunk)
    return local_filename


async def bogous_download_file(url):
    local_filename = url.split("/")[-1] + ".jpg"
    # NOTE the stream=True parameter below
    with requests.get(url, stream=True) as r:
        r.raise_for_status()
        with open(local_filename, "wb") as f:
            for chunk in r.iter_content(chunk_size=3000):
                f.write(chunk)
    return local_filename


async def adownload_file(url):
    local_filename = url.split("/")[-1] + ".jpg"
    # NOTE the stream=True parameter below
    async with aiohttp.ClientSession() as session:
        async with session.get(url) as response:
            response.raise_for_status()
            async with aiofiles.open(local_filename, "wb") as f:
                async for chunk in response.content.iter_chunked(3000):
                    f.write(chunk)
        return local_filename


def download_with_threads():
    t1 = time.perf_counter()
    with concurrent.futures.ThreadPoolExecutor(max_workers=8) as executor:
        executor.map(download_file, img_urls)
    t2 = time.perf_counter()
    print(f"Finished in {t2 - t1} seconds")


def download_serially():
    t1 = time.perf_counter()
    for url in img_urls:
        download_file(url)
    t2 = time.perf_counter()
    print(f"Finished in {t2 - t1} seconds")


async def download_with_bogous_async():
    t1 = time.perf_counter()
    await asyncio.gather(*(bogous_download_file(url) for url in img_urls))
    t2 = time.perf_counter()
    print(f"Finished in {t2 - t1} seconds")


async def download_with_real_async():
    t1 = time.perf_counter()
    await asyncio.gather(*(adownload_file(url) for url in img_urls))
    t2 = time.perf_counter()
    print(f"Finished in {t2 - t1} seconds")

if __name__ == "__main__":
    download_serially()
    print()
    download_with_threads()
    print()
    asyncio.run(download_with_bogous_async())
    print()
    asyncio.run(download_with_real_async())
