#first attempt at a web scraper which should
#be used to get stats about various basketball
#players

import urllib
import urllib.request
from bs4 import BeautifulSoup
import re



def get_teams(url="http://www.espn.com/nba/players"):
    page = urllib.request.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    teams = []

    #iterates through all links on page
    for p in soup.select('a'):
        link = p.get("href")

        #checks to see if the link is a team
        if 'name' in link:
            region, name = link[36:].split('/')
            name = " ".join([x for x in name.split("-")])
            teams.append(Team(name, region, link))

    
#team class team contains all the players and later stats
class Team:

    def __init__(self, name, region, link):
        self.name = name
        self.region = region
        self.link = link
        self.players = {}
        self.get_players(region)
        print(self.name + "\n\n")
        self.print_team()


    #will have to go through the linked page and
    #scrape for players
    #currently working
    def get_players(self,region):
        page = urllib.request.urlopen("http://www.espn.com/nba/team/roster/_/name/"+region)
        soup = BeautifulSoup(page, 'html.parser')
        


        #sets player info to the values in all of the data colums
        #much cleaner implementation but doesn't get link for page
        #player_info = [[x.getText() for x in row] for row in soup.find_all("tr", {'class':re.compile('Table2__tr*')})]

        #used for the above way of doing things
        #for p in player_info:
            #self.players[p[1]] = Player(p, self.name, outlink[0])



        #ugly implementation but retrieves the link for each page
        for row in soup.find_all('tr', {'class':re.compile('Table2__tr*')})[1:]:
            player_info = []
            p_info,outlink  = [], []
            for x in row:
                link = x.select("a")
                link = [y.get('href') for y in link if(y!= None)]
                if len(link) >= 1:
                    outlink.append(link)
                p_info.append(x.getText())
            #print(outlink[0][0])
            self.players[p_info[1]] = Player(p_info, self.name,outlink[0][0])
            #player_info.append(p_info)

            
 
    def print_team(self):
        for play in self.players:
            self.players[play].print_player()
            print("\n")

        
        

class Player:

    def __init__(self, player_info, team_name, link):
        p = player_info
        self.name = p[1]
        self.number = p[0]
        self.position = p[2]
        self.age = p[3]
        self.height = p[4]
        self.weight = p[5]
        self.college = p[6]
        self.sal = p[6]
        self.team = team_name
        self.link = link
        

    def print_player(self):
        print("\tname:{} \n\tnumber:{}\n\tposition:{}".format(self.name, self.number, self.position)) 
        print("\t" + self.link)
    
get_teams()
#t = Team("boston celtics", "bos", "http://www.espn.com/nba/team/roster/_/name/bos/boston-celtics")
