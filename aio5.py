import asyncio
import asyncio
import aiohttp
import aiofiles
import time
import platform

urls = [
    "https://images.unsplash.com/photo-this-image-does-not-exists",
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
 
def download_with_real_async():
    t1 = time.perf_counter()
    loop = asyncio.get_event_loop()
    tasks = asyncio.gather(*(adownload_file(url) for url in urls), return_exceptions=True) # NOTE the return_exceptions=True
    loop.run_until_complete(tasks)
    t2 = time.perf_counter()
    print(f"Finished in {t2 - t1} seconds")
    return tasks.result()
 
if __name__ == "__main__":
    if platform.system() == "Windows":
        asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())
    tasks_status = download_with_real_async()
    print(tasks_status)
