# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


class BundesligaScraperItem(scrapy.Item):
    # define the fields for your item here like:
    # name = scrapy.Field()
    player_name = scrapy.Field()
    team_name = scrapy.Field()
    games_played = scrapy.Field()
    goals = scrapy.Field()
    assists = scrapy.Field()
    yellow_cards = scrapy.Field()
    red_cards = scrapy.Field()
    
