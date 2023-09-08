import asyncio
import aiohttp

from bs4 import BeautifulSoup
from .parsing import parser_service


class SearchService:
    async def grab_links(self, pageUrl: str) -> list[str]:
        async with aiohttp.ClientSession() as session:
            async with session.get(pageUrl) as response:
                text = await response.text()
                soup = BeautifulSoup(text, features="html.parser")
                content_area = soup.find("section", {"class": "content"})
                links = content_area.find_all("a")
                href_list: list[str] = [link.get("href") for link in links]
                return [href for href in href_list if href.startswith(pageUrl)]

    async def grab_groups(self, pageUrl: str) -> list[str]:
        courses = await self.grab_links(pageUrl)
        tasks = []
        for course in courses:
            tasks.append(asyncio.ensure_future(self.grab_links(course)))
        groups = await asyncio.gather(*tasks)
        return [item for sublist in groups for item in sublist]

    async def grab_schedule(self, pageLinks: list[str]):
        tasks = []
        for link in pageLinks:
            tasks.append(asyncio.ensure_future(
                parser_service.parse_lessons(link)))
        schedules = await asyncio.gather(*tasks)
        return [item for sublist in schedules for item in sublist]
    

search_service = SearchService()