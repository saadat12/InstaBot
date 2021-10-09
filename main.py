from selenium import webdriver
import os
import time
import sys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
import urllib.request


class InstagramBot:
    def __init__(self, username, password, category):
        self.username = username
        self.password = password
        self.category = category
        self.driver = webdriver.Chrome("./chromedriver.exe")

    data_list = []

    def login(self):
        # time.sleep(5)
        self.driver.get('https://www.instagram.com/')
        time.sleep(5)
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, 'username')))
        WebDriverWait(self.driver, 20).until(EC.presence_of_element_located((By.NAME, 'password')))

        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.XPATH, '//*[contains(text(),"Log In")]')))
        # finding elements by name now and entering the username and password
        self.driver.find_element_by_name('username').send_keys(self.username)
        self.driver.find_element_by_name('password').send_keys(self.password)
        time.sleep(3)
        self.driver.find_element_by_xpath('//*[contains(text(),"Log In")]').click()

    def search_influencers(self):
        data_dict = {}
        # complete_data = ['Post', 'Followers', 'Following', 'contact_info']
        complete_data = ['Post', 'Followers', 'Following']
        link_data = []
        time.sleep(7)
        WebDriverWait(self.driver, 20).until(
            EC.presence_of_element_located((By.XPATH, '//input[@placeholder="Search"]'))).send_keys(self.category)
        # self.driver.find_element_by_xpath('//input[@placeholder="Search"]').send_keys(self.category)
        time.sleep(5)
        links = self.driver.find_elements_by_xpath('//div[@class="fuqBx "]/div/a')
        links = [i.get_attribute('href') for i in links]
        for link in links:
            l = link.split('/')
            if len(l) > 5:
                links.remove(link)
        print(self.category.capitalize() + " contains " + str(len(links)) + " influencers ")
        for link in links:
            self.driver.get(link)
            data = self.driver.find_elements_by_xpath('//span[@class="g47SY "]')
            all_data = [i.get_attribute("innerHTML") for i in data]
            if all_data:
                for value in all_data:
                    keys = complete_data[all_data.index(value)]
                    data_dict.update({keys: value})
                    # i = i + 1
            else:
                continue
            data_dict.update({'link': link, 'Name': link.split('/')[-2]})
            link_data.append(data_dict)
            print(data_dict)
            time.sleep(5)

        print('Influencers of category ' + self.category + str({self.category: link_data}))


category = input("Please Enter the category you want to search\n")
insta = InstagramBot('syedaliat97@gmail.com', 'Intelcorei5', category)
insta.login()
insta.search_influencers()
