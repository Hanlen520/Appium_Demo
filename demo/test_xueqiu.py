#!/usr/bin/env python
# -*- coding: utf-8 -*-

import pytest
import unittest
from appium import webdriver
from time import sleep

from appium.webdriver.common.touch_action import TouchAction
from selenium.webdriver.support.wait import WebDriverWait


class TestXueqiu(unittest.TestCase):
    loaded = False

    def setUp(self):
        print("setup")
        caps = {}
        caps["platformName"] = "android"
        caps["deviceName"] = "demo"
        caps["appPackage"] = "com.xueqiu.android"
        caps["appActivity"] = ".view.WelcomeActivityAlias"
        caps["autoGrantPermissions"] = "true"
        caps["automationName"] = "UiAutomator2"

        if TestXueqiu.loaded == True:
            caps["noReset"] = "true"

        self.driver = webdriver.Remote("http://localhost:4723/wd/hub", caps)
        self.driver.implicitly_wait(10)
        loaded = True

    def test_add_stock(self):
        self.driver.find_element_by_id("tv_search").click()
        self.driver.save_screenshot("screenshot/tv_search.png")
        self.driver.find_element_by_id("search_input_text").send_keys("pdd")
        self.driver.save_screenshot("screenshot/search_input_text.png")

        print(self.driver.find_element_by_id("add_attention") \
              .find_element_by_class_name("android.widget.TextView") \
              .get_attribute("resourceId"))

        if len(self.driver.find_elements_by_id("follow_btn")) > 0:
            self.driver.find_element_by_id("follow_btn").click()
            self.driver.find_element_by_xpath("//*[@text='下次再说']").click()

    def test_check_stock(self):
        for i in range(1, 5):
            element = self.driver.find_element_by_xpath(
                "//*[@text='自选' and contains(@resource-id, 'tab_name')]")
            print(element.location)
            element.get_attribute("text")
        self.driver.find_element_by_xpath(
            "//*[@text='自选' and contains(@resource-id, 'tab_name')]").click()
        assert 1 == len(self.driver.find_elements_by_xpath(
            "//*[contains(@resource-id, 'portfolio_stockName') and @text='拼多多']"))

    def test_mobile(self):
        # self.driver.start_activity("com.android.calculator2", ".Calculator")
        print(self.driver.is_locked())
        self.driver.lock(5)
        self.driver.unlock()
        # self.driver.shake()

    def test_touch(self):
        self.loaded()
        self.driver.find_element_by_xpath(
            "//*[@text='自选' and contains(@resource-id, 'tab_name')]").click()

        element = self.driver.find_element_by_xpath("//*[@text='拼多多']")
        TouchAction(self.driver).long_press(element).perform()
        self.driver.find_element_by_xpath("//*[@text='删除']").click()

    def test_main_swipe(self):
        self.loaded()
        for i in range(1, 10):
            sleep(1)
            self.driver.swipe(start_x=1340, start_y=2000, end_x=200, end_y=600, duration=1000)

    def find(self, by, locator):

        try:
            self.driver.find_element(by, locator)
        except:
            keywords=[]
            for key in keywords:
                elements=self.driver.find_elements(key)
                if len(elements)>0:
                    elements[0].click()


    def loaded(self):
        locations = ["x", "y"]
        while locations[-1] != locations[-2]:
            element = self.driver.find_element_by_xpath(
                "//*[@text='自选' and contains(@resource-id, 'tab_name')]")
            locations.append(element.location)
            print(locations)

    def test_battery(self):
        print(self.driver.execute_script("mobile:batteryInfo"))

    def test_shell(self):
        print(self.driver.execute_script("mobile:shell",
                                         {"command": "am",
                                          "args": ["start", "-n", "com.android.calculator2/.Calculator"]}))



