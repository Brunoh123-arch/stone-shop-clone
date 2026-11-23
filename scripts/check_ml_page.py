# -*- coding: utf-8 -*-
import asyncio
from playwright.async_api import async_playwright

url = "https://www.mercadolivre.com.br/mochila-escolar-rebecca-bonbon-preto-com-ziper-compartimento-notebook/p/MLB63115237"

async def check_ml():
    user_data_dir = r"C:\Users\Dell\AppData\Local\Google\Chrome\User Data Max"
    async with async_playwright() as p:
        ctx = await p.chromium.launch_persistent_context(
            user_data_dir,
            channel="chrome",
            headless=False,
            args=["--profile-directory=Profile 42", "--no-sandbox"]
        )
        page = await ctx.new_page()
        await page.goto(url, wait_until="domcontentloaded", timeout=40000)
        await page.wait_for_timeout(3000)
        print("URL FINAL:", page.url)
        print("TITULO:", await page.title())
        content = await page.content()
        print("Tamanho do HTML retornado:", len(content))
        await ctx.close()

if __name__ == '__main__':
    asyncio.run(check_ml())
