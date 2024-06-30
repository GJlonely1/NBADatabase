# Define here the models for your scraped items
#
# See documentation in:
# https://docs.scrapy.org/en/latest/topics/items.html

import scrapy


# class PlayerscrapeItem(scrapy.Item):
#     # define the fields for your item here like:
#     # name = scrapy.Field()
#     pass


class TeamRoster(scrapy.Item):
    Team = scrapy.Field()
    player_link_information_url = scrapy.Field()
    name = scrapy.Field()
    jersey_number = scrapy.Field()
    position = scrapy.Field()
    height = scrapy.Field()
    weight = scrapy.Field()
    birthdate = scrapy.Field()
    age = scrapy.Field()
    years_of_experience = scrapy.Field()
    college = scrapy.Field()
    method_of_acquisition = scrapy.Field()

class RetiredPlayers(scrapy.Item):
    team = scrapy.Field()
    player_profile_link = scrapy.Field()
    jersey_number = scrapy.Field()
    name = scrapy.Field()
    position = scrapy.Field()
    seasons_with_team = scrapy.Field() 
    year_of_induction = scrapy.Field()

class HOF(scrapy.Item): 
    team = scrapy.Field()
    player_profile_link = scrapy.Field()
    name = scrapy.Field()
    position = scrapy.Field()
    seasons_with_team = scrapy.Field() 
    year_of_induction = scrapy.Field()


