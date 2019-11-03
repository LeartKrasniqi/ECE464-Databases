# -*- coding: utf-8 -*-
import scrapy
from ..items import BundesligaScraperItem

class BundesligaSpider(scrapy.Spider):
    name = 'bundesliga'
    allowed_domains = ['foxsports.com']
    start_urls = ['https://www.foxsports.com/soccer/stats?competition=4&season=20190&category=standard&sort=3']
    page_number = 2

    def parse(self, response):
    	items = BundesligaScraperItem()

    	player_name = response.css('.wisbb_fullPlayer span').css('::text').extract()
    	team_name = response.css('.wisbb_tableAbbrevLink a').css('::text').extract()
    	games_played = response.css('.wisbb_fixedColumn+ td').css('::text').extract()
    	goals = response.css('td.wisbb_selected').css('::text').extract()
    	assists = response.css('.wisbb_selected+ td').css('::text').extract()
    	yellow_cards = response.css('td:nth-child(9)').css('::text').extract()
    	red_cards = response.css('td:nth-child(10)').css('::text').extract()
    	player_name = player_name[0::2]

    	for player, team, games, g, a, yc, rc in zip(player_name, team_name, games_played, goals, assists, yellow_cards, red_cards):
    		items['player_name'] = player
    		items['team_name'] = team
    		items['games_played'] = games
    		items['goals'] = g
    		items['assists'] = a
    		items['yellow_cards'] = yc
    		items['red_cards'] = rc

    		yield items


        next_page = 'https://www.foxsports.com/soccer/stats?competition=4&season=20190&category=STANDARD&pos=0&team=0&isOpp=0&sort=3&sortOrder=0&page=' + str(BundesligaSpider.page_number)
        if BundesligaSpider.page_number <= 8:
        	BundesligaSpider.page_number += 1
        	yield response.follow(next_page, callback = self.parse)
