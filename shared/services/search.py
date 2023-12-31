import asyncio
import aiohttp

from bs4 import BeautifulSoup
import requests
from .parsing import parser_service
from ..types.lesson import Lesson


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
            
    def grab_links_sync(self, pageUrl: str) -> list[str]:
        response = requests.get(pageUrl)
        text = response.text
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
    
    def grab_schedule_sync(self, page_links: list[str]) -> list[Lesson]:
        items = []
        for link in page_links:
            items += parser_service.parse_lessons_sync(link)
        return items
    

search_service = SearchService()