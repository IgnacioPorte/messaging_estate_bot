import winsound
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.expected_conditions import presence_of_element_located
from webdriver_manager.chrome import ChromeDriverManager
from time import sleep
from random import uniform
from selenium.webdriver.common.action_chains import ActionChains

from fastapi import FastAPI, Depends
from typing import Optional
from pydantic import BaseModel
from scraper import Bot
from config import settings
from functools import lru_cache

app = FastAPI(title="API scraper",
              description="scraper bot that enable a real estate broker to message sellers of particular houses",
              version="1.0.1")


# @lru_cache()
# def get_settings():
#     return Settings()

class Search(BaseModel):
    name: str
    last_name: str
    place: str
    email: str
    phone: str

@app.get("/")
async def index():
    return {"message": "Hello World"}

@app.post("/")
async def index(search: Search):
    # initialize bot
    bot = Bot(**dict(search))

    # get index page
    bot.get_home_page()

    # login
    
    bot.login(settings.api_key)
    sleep(40)

    bot.search_place()

    bot.send_messages()


    print(type(search), dict(search).values())
    
    return search