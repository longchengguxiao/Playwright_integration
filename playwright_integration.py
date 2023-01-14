from playwright.async_api import async_playwright
from playwright.sync_api import sync_playwright
import logging
import asyncio
from typing import Literal, Optional, List, Dict, Tuple

logging.basicConfig(level=logging.INFO,
                    format='%(asctime)s - %(levelname)s: %(message)s')

class SyncPlaywright():
    """
    同步的浏览器自动测试工具
    """
    def initization(self, browser: int = 0, device: str = "", headless: bool = False):
        self.p = sync_playwright().start()
        if device != "":
            try:
                self.p = self.p.devices[device]
            except:
                logging.error("Device name is illegal, for example 'iPhone 12 Pro Max' is legal. Param device will be ignore.")
        if browser == 0:
            self.b = self.p.chromium.launch(headless=headless)
        elif browser == 1:
            self.b = self.p.firefox.launch(headless=headless)
        elif browser == 2:
            self.b = self.p.webkit.launch(headless=headless)
        logging.info("Successfully created a new browser")
        self.context = self.b.new_context()
        logging.info("Successfully created a new context")
        self.page = self.context.new_page()
        logging.info("Successfully created a new page")

    def goto(self, url: str, timeout: int = 10000):
        """
        前往目标网址
        :param url: 目标网址
        :param timeout: 最大等待时间，默认为10000ms
        :return:
        """
        self.page.goto(url, timeout=timeout)
        logging.info("Successfully goto url %s", url)

    def click(self, selector: str,  delay: float = 300, click_count: int = 1):
        """
        采用选择器点击一个按钮
        :param selector:选择器
        :param delay: 延时（毫秒），默认为300ms
        :param click_count: 点击次数，默认为1次
        :return:
        """
        self.page.click(selector=selector, delay=delay, click_count=click_count)
        logging.info("Successfully clicked button '%s'", selector)

    def type(self, selector:str, text:str, timeout:int = 10000):
        """
        采用选择器填充文本
        :param selector:选择器
        :param text: 待填充文本
        :param timeout: 最大等待时间，默认10000ms
        :return:
        """
        self.page.fill(selector=selector, value=text, timeout=timeout)
        logging.info("Successfully filled %s with %s", selector, text)

    def get_attr(self, selector:str, name:str, timeout:int = 10000) -> List[str]:
        """
        采用选择器获取指定属性值
        :param selector: 选择器
        :param name: 属性
        :param timeout: 最大等待时间，默认10000ms
        :return: 返回一个包含所有符合条件的属性结果的列表
        """
        elements = self.page.query_selector_all(selector=selector)
        attr = [element.get_attribute(name) for element in elements]
        logging.info("Successfully obtained attribute named %s in %s", name, selector)
        return attr

    def cancel_request_picture(self):
        """
        在goto之前使用，目的是不显示图片，加快加载速度
        """
        self.page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
        logging.info("Successfully truncated picture loading")

    def capture_requests(self, on_response, url:str):
        """
        在goto之前使用，目的是监听某种类型的响应
        :param on_response: 回调函数
        :param url: 目标网址
        """
        self.page.on("response", on_response)
        self.goto(url)
        self.page.wait_for_load_state("networkidle")
        logging.info("Successfully intercepted target response")

    def close_all(self):
        self.page.close()
        self.b.close()
        self.p.stop()
        logging.info("Successfully closed all processes")

class AsyncPlaywright():
    """
    异步的浏览器测试工具
    """
    async def initization(self, browser: int = 0, device: str = "", headless: bool = False):
        self.p = await async_playwright().start()
        if device != "":
            try:
                self.p = self.p.devices[device]
            except:
                logging.error("Device name is illegal, for example 'iPhone 12 Pro Max' is legal. Param device will be ignore.")
        if browser == 0:
            self.b = await self.p.chromium.launch(headless=headless)
        elif browser == 1:
            self.b = await self.p.firefox.launch(headless=headless)
        elif browser == 2:
            self.b = await self.p.webkit.launch(headless=headless)
        logging.info("Successfully created a new browser")
        self.context = await self.b.new_context()
        logging.info("Successfully created a new context")
        self.page = await self.context.new_page()
        logging.info("Successfully created a new page")

    async def goto(self, url: str, timeout: int = 10000):
        """
        前往目标网址
        :param url: 目标网址
        :param timeout: 最大等待时间，默认为10000ms
        :return:
        """
        await self.page.goto(url, timeout=timeout)
        logging.info("Successfully goto url %s", url)

    async def click(self, selector: str,  delay: float = 300, click_count: int = 1):
        """
        采用选择器点击一个按钮
        :param selector:选择器
        :param delay: 延时（毫秒），默认为300ms
        :param click_count: 点击次数，默认为1次
        :return:
        """
        await self.page.click(selector=selector, delay=delay, click_count=click_count)
        logging.info("Successfully clicked button '%s'", selector)

    async def type(self, selector:str, text:str, timeout:int = 10000):
        """
        采用选择器填充文本
        :param selector:选择器
        :param text: 待填充文本
        :param timeout: 最大等待时间，默认10000ms
        :return:
        """
        await self.page.fill(selector=selector, value=text, timeout=timeout)
        logging.info("Successfully filled %s with %s", selector, text)

    async def get_attr(self, selector:str, name:str, timeout:int = 10000) -> List[str]:
        """
        采用选择器获取指定属性值
        :param selector: 选择器
        :param name: 属性
        :param timeout: 最大等待时间，默认10000ms
        :return: 返回一个包含所有符合条件的属性结果的列表
        """
        elements = await self.page.query_selector_all(selector=selector)
        attr = [await element.get_attribute(name) for element in elements]
        logging.info("Successfully obtained attribute named %s in %s", name, selector)
        return attr

    async def cancel_request_picture(self):
        """
        在goto之前使用，目的是不显示图片，加快加载速度
        """
        await self.page.route("**/*.{png,jpg,jpeg}", lambda route: route.abort())
        logging.info("Successfully truncated picture loading")

    def capture_requests(self, on_response, url:str):
        """
        在goto之前使用，目的是监听某种类型的响应
        :param on_response: 回调函数
        :param url: 目标网址
        """
        self.page.on("response", on_response)
        self.goto(url)
        self.page.wait_for_load_state("networkidle")
        logging.info("Successfully intercepted target response")

    async def close_all(self):
        await self.page.close()
        await self.b.close()
        await self.p.stop()
        logging.info("Successfully closed all processes")
# test for AsyncPlaywright
async def main():
    b = AsyncPlaywright()
    await b.initization()
    await b.goto("https://www.baidu.com")
    await b.click("input[name=\"wd\"]")
    await b.type("input[name=\"wd\"]", "nba")
    await b.click("text=百度一下")

    await b.close_all()

if __name__ == "__main__":
    # # test for SyncPlaywright
    # b = SyncPlaywright()
    # b.initization()
    # b.goto("https://www.baidu.com")
    # b.click("input[name=\"wd\"]")
    # b.type("input[name=\"wd\"]", "nba")
    # b.click("text=百度一下")
    # import time
    # time.sleep(2)
    # b.close_all()
    asyncio.get_event_loop().run_until_complete(main())

