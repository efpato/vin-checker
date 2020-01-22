#!/usr/bin/env python
# -*- coding: utf-8 -*-

import logging
import sys
from datetime import date
from io import BytesIO
from time import sleep

from page_object import PageObject
from page_object.ui.jquery import Textbox, Link
from PIL import Image
from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait


def fullpage_screenshot(driver, filename):
    total_width = driver.execute_script("return document.body.offsetWidth")
    total_height = driver.execute_script("return document.body.parentNode.scrollHeight")
    viewport_width = driver.execute_script("return document.body.clientWidth")
    viewport_height = driver.execute_script("return window.innerHeight")
    rectangles = []

    y = 0
    while y < total_height:
        x = 0

        top_height = y + viewport_height
        if top_height > total_height:
            top_height = total_height

        while x < total_width:
            top_width = x + viewport_width
            if top_width > total_width:
                top_width = total_width

            rectangles.append((x, y, top_width, top_height))

            x += viewport_width

        y += viewport_height

    image = Image.new('RGB', (total_width, total_height))
    for rectangle in rectangles:
        driver.execute_script("window.scrollTo({0}, {1})".format(rectangle[0], rectangle[1]))
        sleep(0.2)

        screenshot = Image.open(BytesIO(driver.get_screenshot_as_png()))

        if rectangle[1] + viewport_height > total_height:
            offset = (rectangle[0], total_height - viewport_height)
        else:
            offset = (rectangle[0], rectangle[1])

        image.paste(screenshot, offset)

    image.save(filename)


class Page(PageObject):
    URL = 'https://гибдд.рф/check/auto'
    PAGE_LOAD_TIMEOUT = 300

    vin = Textbox(css="input#checkAutoVIN")
    history = Link(css="a[data-type='history']")
    dtp = Link(css="a[data-type='aiusdtp']")
    wanted = Link(css="a[data-type='wanted']")
    restricted = Link(css="a[data-type='restricted']")

    def dtp_count(self):
        results = self.webdriver.find_elements_by_css_selector(
            "div#checkAutoAiusdtp > div.checkResult > ul.aiusdtp-list > li")
        return len(results)

    def wanted_count(self):
        results = self.webdriver.find_elements_by_css_selector(
            "div#checkAutoWanted > div.checkResult > ul.wanted-list > li")
        return len(results)

    def restricted_count(self):
        results = self.webdriver.find_elements_by_css_selector(
            "div#checkAutoRestricted > div.checkResult > ul.restricted-list > li")
        return len(results)

    def wait_for_history(self, timeout=60):
        logging.debug('Waiting for history...')
        WebDriverWait(self.webdriver, timeout).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "div#checkAutoHistory > div.checkResult")
            ), 'History timeout is expired!')

    def wait_for_dtp(self, timeout=60):
        logging.debug('Waiting for dtp...')
        WebDriverWait(self.webdriver, timeout).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "div#checkAutoAiusdtp > div.checkResult")
            ), 'DTP timeout is expired!')

    def wait_for_wanted(self, timeout=60):
        logging.debug('Waiting for wanted...')
        WebDriverWait(self.webdriver, timeout).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "div#checkAutoWanted > div.checkResult")
            ), 'Wanted timeout is expired!')

    def wait_for_restricted(self, timeout=60):
        logging.debug('Waiting for restricted...')
        WebDriverWait(self.webdriver, timeout).until(
            expected_conditions.visibility_of_element_located(
                (By.CSS_SELECTOR, "div#checkAutoRestricted > div.checkResult")
            ), 'Restricted timeout is expired!')


def main(vin):
    filename = f'{date.today().isoformat()}_{vin}.png'
    driver = None
    options = ChromeOptions()
    # options.add_argument('headless')
    options.add_argument('--start-maximized')
    # options.add_argument('--proxy-server=https://fr-75-4-200.friproxy.biz:443')

    try:
        driver = Chrome(chrome_options=options)
        driver.maximize_window()
        logging.debug('Chrome started')

        driver.set_page_load_timeout(Page.PAGE_LOAD_TIMEOUT)
        logging.debug('Set page_load_timeout=%d', Page.PAGE_LOAD_TIMEOUT)

        logging.debug('Opening "%s"', Page.URL)
        driver.get(Page.URL)

        page = Page(driver)
        page.vin = vin
        sleep(1)

        page.dtp.click()
        page.wait_for_dtp()

        page.wanted.click()
        page.wait_for_wanted()

        page.restricted.click()
        page.wait_for_restricted()

        if page.dtp_count() >= 3:
            filename = f'3ДТП_{filename}'

        if page.wanted_count() > 0:
            filename = f'розыск_{filename}'

        if page.restricted_count() > 0:
            filename = f'ограничения_{filename}'

    except KeyboardInterrupt:
        pass
    finally:
        if driver is not None:
            fullpage_screenshot(driver, filename)
            driver.quit()


if __name__ == '__main__':
    logging.basicConfig(format="%(asctime)s  %(levelname)-8s %(module)-15s %(message)s", level=logging.DEBUG)
    logging.getLogger("selenium.webdriver.remote.remote_connection").setLevel(logging.WARNING)

    for arg in sys.argv[1:]:
        main(arg)
