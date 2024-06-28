import scrapy
import random
from scrapy import Request
from urllib.parse import urljoin
# from urllib3.parse import urljoin


class PlayersSpider(scrapy.Spider):
    name = "Teams"
    allowed_domains = ["www.nba.com"]
    start_urls = ["https://www.nba.com/teams"]
    
    
    user_agent_list = [
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/93.0.4577.82 Safari/537.36',
    'Mozilla/5.0 (iPhone; CPU iPhone OS 14_4_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/14.0.3 Mobile/15E148 Safari/604.1',
    'Mozilla/4.0 (compatible; MSIE 9.0; Windows NT 6.1)',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/87.0.4280.141 Safari/537.36 Edg/87.0.664.75',
    'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/70.0.3538.102 Safari/537.36 Edge/18.18363',
    ]

    def parse(self, response):
        teams_resources = response.css("div.TeamDivisions_wrapper__5_SVo div.TeamDivisions_division__u3KUS div.TeamFigure_tf__jA5HW div.TeamFigure_tfContent__Vxiyh")
        base_url = "https://www.nba.com"
        # print (teams_resources)
        for team in teams_resources: 
            team_name = team.css("a::text").get() 
            # print (team_name)
            team_official_sideurl = team.css("a::attr(href)").get()
            team_other_resources = team.css("div.TeamFigure_tfLinks__gwWFj")
            
            team_official_fullurl = str(base_url) + str(team_official_sideurl)
            # Retrieve list of team links from team_other_resources
            team_links = team_other_resources.css("a::attr(href)").getall() 
            team_profile_sideurl = team_links[0]
            # print (type(team_profile_sideurl))
            team_stats_sideurl = team_links[1]
            team_schedule_sideurl = team_links[2]
                
            team_profile_fullurl = str(base_url) + str(team_profile_sideurl)
            team_stats_fullurl = str(base_url) + str(team_stats_sideurl)
            team_schedule_fullurl = str(base_url) + str(team_schedule_sideurl)
            
            Team_Details = {
                "Team Name" : str(team_name),
                "Team Offical URL" : str(team_official_fullurl),
                "Team Profile URL" : team_profile_fullurl,
                "Team Statistics URL" : team_stats_fullurl,
                "Team Schedule URL" : team_schedule_fullurl,
            }
            yield Team_Details
            # yield response.follow(team_official_fullurl, callback=self.parse_officialSite, headers={"User-Agent": random.choice(self.user_agent_list)})
            yield response.follow(team_profile_fullurl, callback=self.parse_team_profile, headers={"User-Agent": random.choice(self.user_agent_list)})
            # yield response.follow(team_stats_fullurl, callback=self.parse_team_statistics, headers={"User-Agent": random.choice(self.user_agent_list)})
            # yield response.follow(team_schedule_fullurl, callback=self.parse_team_schedule, headers={"User-Agent": random.choice(self.user_agent_list)})
    
    # Nothing much to scrape from here
    # def parse_officialSite(self, response): 
    #     url = response.url
    
    def parse_team_profile(self, response):
        url = response.url 
        current_team_roster = response.css("div.TeamRoster_tableContainer__CUtM0 table tbody tr")
        for players in current_team_roster: 
            player_link_information_sideurl = players.css("td a::attr(href)").get()
            player_name = players.css("td a::text").get()
            try: 
                player_number = players.css("td.text TeamRoster_extraPadding__4BsqP ::text").get()
            except: 
                player_number = "N/A"
            player_position = players.css("td ")
        

    # def parse_team_statistics(self, response): 
    #     pass
    
    # def parse_team_schedule(self, response):
    #     pass
        
        