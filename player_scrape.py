#first attempt at a web scraper which should
#be used to get stats about various basketball
#players

import urllib
import urllib.request
from bs4 import BeautifulSoup
import re
import json
import os
import shutil

    
#team class team contains all the players and later stats
class Team:

    def __init__(self, name, region, link,load=False, path = ""):
        self.name = name
        self.region = region
        self.link = link
        self.players = {}
        if load == False:
            self.get_players(region)
        else:
            self.load_team(path)
        #print(self.name + "\n\n")
        #self.print_team()


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

    def save_team(self, path):

        try:
            path = path + '\\' +self.name.replace(" ", "_")+"_"+self.region
            os.makedirs(path)
            for p in self.players.values():
                p.save_player(path)
        except FileExistsError:
            pass

    def load_team(self, path):
        print(path)


        
        

class Player:

    def __init__(self, player_info, team_name, link):
        p = player_info
        p[0] = "".join([x for x in p[1] if not x.isalpha() and x != ' ']) #sets p[0] to number =BUG= fix this
        p[1] = "".join([x for x in p[1] if x.isalpha() or x == " "]) #removes number from name =Bug=
        info = ["number", "name", "position", "age", "height", "weight", "college"
                ,"sal"]
        self.info_dict = {}
        for i in range(len(info)):
            self.info_dict[info[i]] =  p[i]
        self.info_dict["link"] = link
        

    def print_player(self):

        print("\tname:{} \n\tnumber:{}\n\tposition:{}".format(self.info_dict["name"],self.info_dict["number"],self.info_dict["position"]))
        print("\t" + self.info_dict['link'])

    #save function saves each player as a json in their teams folder
    def save_player(self, path):
        path = path+"\\"+self.info_dict['name'].replace(" ","_")
        with open(path, "w") as outfile:
            json.dump(self.info_dict, outfile)

    
#class which contains all teams
#lot to add maybe overall stats and at the least
# a team lookup system
class League:

    def __init__(self,path):
        self.path = path
        self.teams = []
        print("getting teams")
        if os.path.exists(path):
            self.load_state()
        else:
            self.get_teams()

    def get_teams(self, url="http://www.espn.com/nba/players"):
        page = urllib.request.urlopen(url)
        soup = BeautifulSoup(page, "html.parser")

        #iterates through all links on page
        for p in soup.select('a'):
            link = p.get("href")

            #checks to see if the link is a team
            if 'name' in link:
                region, name = link[36:].split('/')
                name = " ".join([x for x in name.split("-")])
                self.teams.append(Team(name, region, link,False))

    def save_state(self):
        path = self.path
        #f = open("League.dat", "w+")
        #json.dump(f,self.teams)
        try:
            os.makedirs(path)
            for t in self.teams:
                t.save_team(path)

        except FileExistsError:
            try:
                shutil.rmtree(path)
                self.save_state()
            except OSError:
                print("gone?")

    def load_state(self):
        for direct in os.listdir(self.path):
            dsplit = direct.split("_")
            region= dsplit.pop()
            name = "-".join([x for x in dsplit])
            link = "http://www.espn.com/nba/team/roster/_/name/" + region + name
            print("name: {}\nregion: {}\nlink: {}".format(name,region,link))
            self.teams.append(Team(name.replace("-", " "), region , link,True, self.path+ "\\"+direct))
            

        



#get_teams()
#t = Team("boston celtics", "bos", "http://www.espn.com/nba/team/roster/_/name/bos/boston-celtics")
#enter your path in path
l = League("path")
l.save_state()
