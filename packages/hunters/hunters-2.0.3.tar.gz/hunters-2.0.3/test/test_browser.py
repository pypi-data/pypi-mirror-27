# -*- coding:utf-8 -*-
# Created by qinwei on 2017/8/8
import unittest

from hunters.browser import ChromeTab, BaseChrome
from hunters.chrome import ChromeTabDevToolFactory
from hunters.config import BrowserConfig


class TestBrowser(unittest.TestCase):
    def setUp(self):
        canary = r"C:\Users\ADMIN\AppData\Local\Google\Chrome SxS\Application\chrome.exe"
        chrome = r"C:\Program Files (x86)\Google\Chrome\Application\chrome.exe"
        self.config = BrowserConfig(
            execute_bin=chrome,
            headless=False)

    def test_factory(self):
        factory = ChromeTabDevToolFactory(browser_config=self.config)
        chrome = BaseChrome(factory=factory)
        for i in range(2):
            r = chrome.get("https://news.qq.com/a/20171124/000144.htm")
            # r = chrome.get("https://baidu.com")
            r.window_size(1000, 1000)
            r.scroll_by(0, 10000)
            print(r.execute_js("document.title"))
            print(r.text)
            print(r.cookies(urls=["baidu.com"]))
            print(r.get_all_cookies())
            print(i)

    def test_multi_chrometab(self):
        cc = ChromeTab(browser_config=self.config)
        cc2 = ChromeTab(browser_config=self.config)
        r = cc.get("http://baidu.com")
        r2 = cc2.get("http://qq.com")
        print(r.text)


if __name__ == '__main__':
    TestBrowser.main()
