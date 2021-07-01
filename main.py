import discord
import pandas as pd
from selenium import webdriver
import re
from datetime import date

pattern = r'[0-9]'


def monthIndex(string):
    m = {
        'jan': 1,
        'feb': 2,
        'mar': 3,
        'apr': 4,
        'may': 5,
        'jun': 6,
        'jul': 7,
        'aug': 8,
        'sep': 9,
        'oct': 10,
        'nov': 11,
        'dec': 12
    }
    s = string.strip()[:3].lower()
    out = m[s]
    return out


def checkDate(startDate):
    sd = re.sub(pattern, '', startDate)
    sd = sd[:-4]
    sd = sd[:3]
    sd = sd.lower()
    month = (monthIndex(sd))
    if(month >= date.today().month):
        return True


client = discord.Client()

PATH = 'C:\Program Files (x86)\chromedriver.exe'
driver = webdriver.Chrome(PATH)

url = 'https://devfolio.co/hackathons'
driver.get(url)

cards = driver.find_elements_by_class_name('hskJsg')

hackathons = []

for element in cards:
    title = element.find_element_by_xpath(
        './/div/div/div/div[1]/a/span/span[1]').text
    start_date = element.find_element_by_xpath(
        './/div/div/div/div[2]/div[1]/span[2]').text
    end_date = element.find_element_by_xpath(
        './/div/div/div/div[2]/div[2]/span[2]').text

    if(checkDate(start_date)):
        hackathon = {
            'Title': title,
            'Start Date': start_date,
            'End Date': end_date
        }
        hackathons.append(hackathon)


@client.event
async def on_ready():
    print('We have logged in as {0.user}'.format(client))


@client.event
async def on_message(message):
    if message.author == client.user:
        return

    if message.content.startswith('~hack'):
        msg = ''
        for hacks in hackathons:
            msg += f"{hacks['Title']} \n Starts: {hacks['Start Date']} \n End Date: {hacks['End Date']} \n\n"

        await message.channel.send(msg)

#client.run(TOKEN)