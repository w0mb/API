from fastapi import FastAPI, HTTPException
import aiohttp
import os
from playwright.async_api import async_playwright

app = FastAPI()

# Функция для получения временной ссылки на видео
async def get_temporary_video_url(video_url: str) -> str:
    try:
        async with async_playwright() as p:
            browser = await p.chromium.launch(headless=True)
            page = await browser.new_page()
            await page.goto(video_url)

            # Найти элемент <video> и извлечь ссылку на потоковое видео
            video_element = await page.query_selector("video")
            if not video_element:
                raise Exception("Видео не найдено на странице")

            temporary_url = await video_element.get_attribute("src")
            await browser.close()

            if not temporary_url:
                raise Exception("Не удалось получить временную ссылку на видео")

            return temporary_url
    except Exception as e:
        raise Exception(f"Ошибка при получении временной ссылки: {e}")

# Функция для скачивания видео по временной ссылке
async def download_video(temporary_url: str, output_path: str):
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(temporary_url) as response:
                if response.status == 200:
                    with open(output_path, "wb") as file:
                        file.write(await response.read())
                else:
                    raise Exception(f"Не удалось скачать видео, статус: {response.status}")
    except Exception as e:
        raise Exception(f"Ошибка при скачивании видео: {e}")

@app.get("/download/{username}/{video_id}")
async def download_tiktok_video(username: str, video_id: str):
    video_url = f"https://www.tiktok.com/@{username}/video/{video_id}"
    output_file = f"{username}_{video_id}.mp4"

    try:
        # Получить временную ссылку
        temporary_url = await get_temporary_video_url(video_url)
        # Скачивать видео
        await download_video(temporary_url, output_file)
        return {"message": "Видео успешно скачано", "file_path": output_file}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
