from splinter import Browser
from splinter.browser import Browser
import pandas as pd
from bs4 import BeautifulSoup
import requests
import pymongo


def init_browser():
    executable_path = {'executable_path': 'chromedriver.exe'}
    return(Browser('chrome', **executable_path))
# NASA MArs News
# using splinter


def marsNewsSplinter():
    browser=init_browser()
    url = 'https://mars.nasa.gov/news/'
    browser.visit(url)
    news = {}
    content_title = browser.find_by_css('div[class="content_title"] ')
    content_desc = browser.find_by_css('div[class="article_teaser_body"] ')
    news_title = content_title[0].text
    news_p = content_desc[0].text
    news["news_title"] = news_title
    news["news_p"] = news_p
    return news
#JPL Mars Space Images - Featured Image
def jplImages():
    browser=init_browser()
    images={}
    url="https://www.jpl.nasa.gov/spaceimages/?search=&category=Mars"
    browser.visit(url)
    img_tag=browser.find_by_css('div[class="carousel_items"] article  ')
    imgurl=img_tag["style"].split('url("/')[1].split(")")[0]

    ur="\"https://www.jpl.nasa.gov/"
    featured_image_url=ur+imgurl
    images["image_url"]=featured_image_url
    return images
#Mars Weather Tweets
def marsWeather():
    browser=init_browser()
    weather_tweets={}
    url = 'https://twitter.com/marswxreport?lang=en'
    browser = init_browser()
    browser.visit(url)
    mars_weather = browser.find_by_css(' div[class="js-tweet-text-container"] ').text
    weather_tweets["mars_weather"]=mars_weather
    return weather_tweets
#Mars Facts
def marsFacts():
    browser=init_browser()
    url="https://space-facts.com/mars/"
    marsfacts={}
    marsdf=pd.read_html(url)
    df=marsdf[0]
    df.columns = [''] * len(df.columns)
    df2=df.transpose()
    df2.columns = [''] * len(df2.columns)
    df3=df2.transpose()
    df3.to_html("MarsFacts.html")
    filepath = "MarsFacts.html"
    with open(filepath) as file:
        html = file.read()
    marsfacts["Mars_Facts"]=html
    return marsfacts


# Mars Hemispheres
# refer https://www.w3schools.com/cssref/css_selectors.asp
# https://stackoverflow.com/questions/46468030/how-select-class-div-tag-in-splinter

def marsHemispheres():

    desc = []
    href1 = []
    MarsHemdict = {}
    MarsHemList = []
    browser = init_browser()
    url = "https://astrogeology.usgs.gov/search/results?q=hemisphere+enhanced&k1=target&v1=Mars"
    browser.visit(url)
    find_text = browser.find_by_css('div[class="description"] a h3')

    for i in find_text:
        desc.append(i.text)
    if(len(desc)<=0):
        browser = init_browser()
        url = "https://astrogeology.usgs.gov/maps/mars-viking-hemisphere-point-perspectives"
        browser.visit(url)

        find_text = browser.find_by_css('div[class="widget block products"] div[class="description"]  h3')
        for i in find_text:
            desc.append(i.text)

    # print(i.text)
    for bro in desc:
        browser.click_link_by_partial_text(bro)
        MarsHemdict["title"] = bro
        hr = browser.find_by_css('img[class="wide-image"]')
        MarsHemdict["image_url"] = hr["src"]

        MarsHemList.append(MarsHemdict)
        MarsHemdict = {}
        browser.quit()
        browser = init_browser()
        browser.visit(url)
    return MarsHemList
def finalresult():
    finallist=[]
    marshemi = {}
    marsNews=marsNewsSplinter()
    jplimage=jplImages()
    marsweather=marsWeather()
    marsfacts=marsFacts()
    marsHemispheres1 = marsHemispheres()
    finallist.append(marsNews)
    finallist.append(jplimage)
    finallist.append(marsweather)
    finallist.append(marsfacts)
    marshemi["HemispheresURLS"] = marsHemispheres1
    finallist.append(marshemi)

    return finallist

'''finallist = []
marsNews = marsNewsSplinter()
jplimage = jplImages()
marsweather = marsWeather()
marsfacts = marsFacts()
marsHemispheres1 = marsHemispheres()
finallist.append(marsNews)
finallist.append(jplimage)
finallist.append(marsweather)
finallist.append(marsfacts)
marshemi={}

marshemi["HemispheresURLS"] = marsHemispheres1
finallist.append(marshemi)
print(finallist)'''

