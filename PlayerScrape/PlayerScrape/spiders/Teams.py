import scrapy
import time
import random
from scrapy import Request
from urllib.parse import urljoin
from PlayerScrape.items import TeamRoster, RetiredPlayers, HOF, ALLFantasyNewsDetails, TeamSpecificNewsDetails, AllTimeRecords, TeamAchievementDetails, TeamBackgroundDetails, PlayerProfile, PlayerBoxScoreLast5Games
# from urllib3.parse import urljoin
from scrapy_selenium import SeleniumRequest
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver import ActionChains



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
        
        # fantasy_news_url = "https://www.nba.com/stats/fantasynews"
        
    # Nothing much to scrape from here
    # def parse_officialSite(self, response): 
    #     url = response.url
    
    def parse_team_profile(self, response):
        url = response.url 
        baseurl = "https://www.nba.com"
        current_team_roster = response.css("div.TeamRoster_tableContainer__CUtM0 table tbody tr")
        team_name = response.xpath('//*[@id="__next"]/div[2]/div[2]/main/section/div/div/div[3]/div[1]/div[1]/div[2]/text()').get()
        team_roster_details = TeamRoster()
        for players in current_team_roster: 
            team_roster_details['Team'] = team_name
            full_player_url = baseurl + players.css("td a::attr(href)").get()
            team_roster_details['player_link_information_url'] = full_player_url
            player_information = players.css("td.text ::text").getall()
            team_roster_details['name'] = player_information[0]
            if player_information[1].isnumeric(): 
                team_roster_details['jersey_number'] = player_information[1]
                team_roster_details['position'] = player_information[2]
                team_roster_details['height'] = player_information[3]
                team_roster_details['weight'] = player_information[4] + player_information[5]
                team_roster_details['birthdate'] = player_information[6]
                team_roster_details['age'] = player_information[7]
                team_roster_details['years_of_experience'] = player_information[8]
                team_roster_details['college'] = player_information[9]
                team_roster_details['method_of_acquisition'] = player_information[10]
            else: 
                team_roster_details['jersey_number'] = "NA"
                team_roster_details['position'] = player_information[1]
                team_roster_details['height'] = player_information[2]
                team_roster_details['weight'] = player_information[3] + player_information[4]
                team_roster_details['birthdate'] = player_information[5]
                team_roster_details['age'] = player_information[6]
                team_roster_details['years_of_experience'] = player_information[7]
                team_roster_details['college'] = player_information[8]
                team_roster_details['method_of_acquisition'] = player_information[9]
            yield team_roster_details
            
            yield response.follow(full_player_url, callback=self.player_information, headers={"User-Agent": random.choice(self.user_agent_list)})

    # # Retrieve Retired Numbers of Players
        retired_players_table = response.xpath('//*[@id="__next"]/div[2]/div[2]/main/div[3]/div[4]/div/div[1]/section/div/div[2]/div')
        retired_players_info = retired_players_table.css("table tbody tr")
        retired_player_details = RetiredPlayers() 
        for player in retired_players_info: 
            retired_player_details['team'] = team_name
            rp_sideurl = player.css("td.text a::attr(href)").get()
            if rp_sideurl is not None: 
                retired_player_details['player_profile_link'] = baseurl + rp_sideurl
            else: 
                retired_player_details['player_profile_link'] = "N/A"
            retired_player_stats = player.css("td ::text").getall()
            if retired_player_stats[0].isnumeric(): 
                retired_player_details['jersey_number'] = retired_player_stats[0]
                retired_player_details['name'] = retired_player_stats[1]
                retired_player_details['position'] = retired_player_stats[2]
                retired_player_details['seasons_with_team'] = retired_player_stats[-2]
                retired_player_details['year_of_induction'] = retired_player_stats[-1]
            else: 
                retired_player_details['jersey_number'] = "NA"
                retired_player_details['name'] = retired_player_stats[0]
                retired_player_details['position'] = retired_player_stats[1]
                retired_player_details['seasons_with_team'] = retired_player_stats[-2]
                retired_player_details['year_of_induction'] = retired_player_stats[-1]
            yield retired_player_details

    # Retrieve Hall of Fame Players
        HOF_table = response.xpath('//*[@id="__next"]/div[2]/div[2]/main/div[3]/div[4]/div/div[2]/section/div/div[2]/div')
        HOF_players = HOF_table.css("table tbody tr")
        HOF_player_details = HOF()
        for player in HOF_players:
            HOF_player_details['team'] = team_name
            hof_sideurl = player.css("td.primary a::attr(href)").get()
            if hof_sideurl is not None: 
                HOF_player_details['player_profile_link'] = baseurl + hof_sideurl
            else: 
                HOF_player_details['player_profile_link'] = 'N/A'
            
            hof_player_stats = player.css("td ::text").getall()
            HOF_player_details['name'] = hof_player_stats[0]
            HOF_player_details['position'] = hof_player_stats[1]
            HOF_player_details['seasons_with_team'] = hof_player_stats[2]
            HOF_player_details['year_of_induction'] = hof_player_stats[-1]

            yield HOF_player_details
            
    
    # # Access Team Specific Fantasy News
        team_specific_news = response.css("div article")
        team_news = TeamSpecificNewsDetails()
        for news in team_specific_news: 
            team_news['team'] = team_name
            team_news['date_time'] = news.css("p.TeamFantasyNews_articleDate__SrBm7 ::text").get()
            team_news['headline'] = news.css("p.TeamFantasyNews_articleHeadline__02sbs ::text").get()
            team_news['content'] = news.css("p.TeamFantasyNews_articleContent__x7vps ::text").get()
            yield team_news
            
    # # Retrieve All Time Records
        all_time_records_table = response.css("table.TeamRecords_table__0iapO tbody tr")
        all_time_records = AllTimeRecords()
        for indiv_stat in all_time_records_table:
            all_time_records['team'] = team_name
            all_time_records['statline'] = indiv_stat.css("td.TeamRecords_text__sr_pn ::text").get()
            all_time_records['name'] = indiv_stat.css("td.TeamRecords_player__1qlhr a::text").get()
            all_time_records['number'] = indiv_stat.css("td.TeamRecords_stat__R8MJw ::text").get()
            yield all_time_records

    # # Retrieve Team Achievements
        years_title_list = []
        team_achievement_table = response.css("div div.TeamAwards_group__XU0o9")
        team_achievement = TeamAchievementDetails() 
        team_achievement['team'] = team_name
        for ta in team_achievement_table:
            try:
                team_achievement['title'] = ta.css("h3.TeamAwards_heading__BvLNE ::text").get()
            except: 
                team_achievement['title'] = "N/A"
            try:     
                years_list = ta.css("ul.TeamAwards_list__EvaDJ li")
                for year in years_list:
                    years_title_list.append(year.css("li.TeamAwards_listItem__rb4hz ::text").get())
                team_achievement['years'] = years_title_list
            except: 
                team_achievement['years'] = "N/A"
    
            yield team_achievement
    
    # # Retrieve Team Background Information
        team_background_info = TeamBackgroundDetails() 
        tb_table = response.css('dl.TeamBackground_list__y1CMX')
        all_fields = tb_table.css('dt ::text').getall() 
        all_details = tb_table.css('dd ::text').getall()
        
        team_background_info['team'] = team_name
        for i in range(0, len(all_fields) - 1):
            team_background_info['field'] = all_fields[i]
            team_background_info['details'] = all_details[i]
            yield team_background_info 
    
    # # Get link to access fantasy news site to retrieve all news
    #     protocol = "https:"
    #     fantasy_news_path = response.xpath('//*[@id="__next"]/div[2]/div[2]/main/div[3]/div[3]/div/div[2]/section/div/div[1]/div')
    #     fantasy_news_sideurl = fantasy_news_path.css("a ::attr(href)").get()
    #     fantasy_news_url = protocol + str(fantasy_news_sideurl) 
        
    #     yield response.follow(fantasy_news_url, callback=self.parse_fantasy_news_all, headers={"User-Agent": random.choice(self.user_agent_list)})

    # # Retrieve Fantasy News - Only need to retrieve once because all fantasy news are the same. Checking has to be done at the start. 
    # def parse_fantasy_news_all(self, response): 
    #     fantasy_news_list = response.css("div.flex article")
    #     fantasy_news_details = ALLFantasyNewsDetails() 
    #     for indiv_news in fantasy_news_list: 
    #         fantasy_news_details['name'] = indiv_news.css("h2.StatsFantasyNewsItem_header__BTj_m a ::text").get()
    #         fantasy_news_details['date_time'] = indiv_news.css("time.StatsFantasyNewsItem_time__Y804k ::text").get()
    #         fantasy_news_details['content'] = indiv_news.css("section.StatsFantasyNewsItem_content__XZs6Q p ::text").get() 
    #         yield fantasy_news_details


    # def parse_team_statistics(self, response): 
    #     base_url = "https://www.nba.com"
    #     statisticalChoicesDropdown = response.xpath('//*[@id="__next"]/div[2]/div[2]/main/div[3]/section[1]/div/nav/div[2]/ul')
    #     statisticalChoicesOptionsDropdown = statisticalChoicesDropdown.css("li")
    #     for row in statisticalChoicesOptionsDropdown: 
    #         stats_sideURL = row.css("li a ::attr(href)").get()
    #         stats_officialURL = str(base_url) + str(stats_sideURL)
    #         yield SeleniumRequest(url=stats_officialURL, callback=self.parse_individual_statistical_table)
    #         # yield response.follow(stats_officialURL, callback=self.parse_individual_statistical_table, headers={"User-Agent": random.choice(self.user_agent_list)})
            
    # def parse_individual_statistical_table(self, response):
    #     target_url = response.url
    #     path = "C:/Users/guojiefoo/OneDrive/Documents/GitHub/NBADatabase/Chromedriver-win64/chromedriver.exe"
    #     # service = Service(executable_path=path) 
    #     options = Options()
    #     options.add_argument("start-maximized")
    #     options.headless = True
    #     options.add_experimental_option("excludeSwitches", ["enable-automation"])
    #     options.add_experimental_option("detach", True)
    #     options.add_experimental_option("useAutomationExtension", False)
        
    #     driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    #     driver.get(target_url)
    #     # year_choice_list = response.css("div.DropDown_content__Bsm3h SplitSelect_select__L8_El nba-stats-primary-split div.DropDown_dropdown__TMlAR select option").getall()
    #     # for year in year_choice_list: 
    #     #     print (year)
        
    #     # driver = response.request.meta["driver"]
    #       # scroll to the end of the page 10 times
    #     # for x in range(0, 10):
    #     #     # scroll down by 10000 pixels
    #     #     ActionChains(driver) \
    #     #         .scroll_by_amount(0, 10000) \
    #     #         .perform()
        
    #     #     # waiting 2 seconds for the products to load
    #     #     time.sleep(2)
    #     year_choice_dropdown = driver.find_element(By.XPATH,'//*[@id="__next"]/div[2]/div[2]/main/div[3]/section[2]/div/div[1]/div/label/div/select')
    #     years = year_choice_dropdown.find_elements(By.TAG_NAME, "option")
        
    #     for year in years: 
    #         yield {
    #             "Year" : year.text
    #         }
        
        # yield SeleniumRequest(url=url, headers={"User-Agent": random.choice(self.user_agent_list)}, callback=self.parse_individual_statistical_table, wait_time=10, wait_until=EC.presence_of_element_located((By.XPATH, '//*[@id="__next"]/div[2]/div[2]/main/div[3]/section[2]/div/div[1]/div/label/div')))
    
    # def parse_team_schedule(self, response):
    #     pass
        
    def player_information(self, response): 
        player_stat = response.css("div.PlayerSummary_playerStat__rmEOP p.PlayerSummary_playerStatValue___EDg_ ::text").getall()
        player_block_name = response.css("p.PlayerSummary_playerNameText___MhqC ::text").getall() 
        player_news_list = response.css('div.PlayerProfile_ppNews__t9sDh div.PlayerNews_item__10b5O')
        player_profile = PlayerProfile()
        player_name = ' '.join(player_block_name)
        player_profile['player_name'] = player_name
        player_profile['pts_per_game'] = player_stat[0]
        player_profile['rebounds_per_game'] = player_stat[1]
        player_profile['assists_per_game'] = player_stat[2]
        player_profile['player_impact_estimate'] = player_stat[-1]
        player_news_compiled = []
        for item in player_news_list: 
            news = {
                'Date Time' : item.css('p.PlayerNews_date___Te0H ::text').get(),
                "Headlines" : item.css('p.PlayerNews_headline__w4cFW ::text').get(),
                "Content" : item.css('p.PlayerNews_update__ntYMq ::text').get(),
            }
            player_news_compiled.append(news)
        player_profile['player_news'] = player_news_compiled
        yield player_profile
        
        
        base_url = "https://www.nba.com"
        player_box_score_last5games = PlayerBoxScoreLast5Games() 
        box_score_table  = response.css('div.MockStatsTable_statsTable__V_Skx div table tbody tr td')
        player_box_score_last5games['player_name'] = player_name
        game_sideurl = box_score_table[0].css("a ::attr(href)").get()
        player_box_score_last5games['game_date'] = box_score_table[0].css("a ::text").get() 
        player_box_score_last5games['game_url'] = base_url + game_sideurl
        player_box_score_last5games['matchup'] = box_score_table[1].css("td.text ::text").get()
        player_box_score_last5games['win_lose'] = box_score_table[2].css("td ::text").get()
        player_box_score_last5games['minutes_played'] = box_score_table[3].css("td ::text").get()
        player_box_score_last5games['points'] = box_score_table[4].css("td ::text").get()
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        player_box_score_last5games['field_goals_attempted'] = box_score_table[6].css("a ::text").get()
        player_box_score_last5games['field_goals_percentage'] = box_score_table[7].css("td ::text").get()
        player_box_score_last5games['three_pt_made'] = box_score_table[8].css("a ::text").get()
        
        
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        player_box_score_last5games['field_goals_made'] = box_score_table[5].css("a ::text").get()
        
        
