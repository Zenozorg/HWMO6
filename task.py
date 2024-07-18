import os
import requests
import aiohttp
import asyncio
import json

URL = "https://jsonplaceholder.typicode.com/posts"

FOLDER_PATH = "json_files"

os.makedirs(FOLDER_PATH, exist_ok=True)

def save_json_to_file(data, index, folder_path):
    file_path = os.path.join(folder_path, f"post_{index}.json")
    with open(file_path, 'w') as f:
        json.dump(data, f, indent=4)

def download_and_save_sequential():
    response = requests.get(URL)
    data = response.json()
    for index, item in enumerate(data):
        save_json_to_file(item, index, FOLDER_PATH)

async def download_and_save_async():
    async with aiohttp.ClientSession() as session:
        async with session.get(URL) as response:
            data = await response.json()
            tasks = []
            for index, item in enumerate(data):
                tasks.append(asyncio.create_task(save_json_to_file_async(item, index, FOLDER_PATH)))
            await asyncio.gather(*tasks)

async def save_json_to_file_async(data, index, folder_path):
    file_path = os.path.join(folder_path, f"post_{index}.json")
    async with aiofiles.open(file_path, 'w') as f:
        await f.write(json.dumps(data, indent=4))

import aiofiles
async def main():
    download_and_save_sequential()
    await download_and_save_async()

if __name__ == "__main__":
    asyncio.run(main())