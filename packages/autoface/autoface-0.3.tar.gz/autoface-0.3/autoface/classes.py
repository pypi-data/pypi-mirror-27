#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Thu Nov 30 21:12:48 2017

@author: ahmed
"""

from selenium import webdriver 
from selenium.webdriver.firefox.webdriver import FirefoxProfile
import random
import facebook
from datetime import datetime
import dateutil.parser
import time
import os
import json
import urllib.request


#--------------------------------------------------------
# Read important data and config variables


with open("config.json","r") as config:
    config = json.load(config)
    
dir = config["directory_of_videos_to_upload_as_posts_on_timeline"]
interval = config["interval_in_secs"]
likesCount = config["how_many_wall_likes"]
commentsCount = config["how_many_wall_comments"]
reactsCount = config["how_many_wall_reacts"]
postsCount = config["how_many_posts"]
videosCount = config["how_many_videos"]
postsInGroupCount = config["how_many_posts_in_groups"]

token = config["fb_access_token"]
graph = facebook.GraphAPI(access_token=token, version="2.11") #changed from 2.10
picsdir = config["picsdir"]
firefox_profile = config["firefox_profile"]  
profile = FirefoxProfile(firefox_profile)


with open("textfile_used_to_find_groups_for_example_from_wikipedia_of_the_city.txt","r") as textwiki:
    textwiki = textwiki.read()

text = textwiki.split(' ')

with open("selectedPosts.json","r") as selectedPosts:
    selectedPosts = json.load(selectedPosts)
with open("selectedComments.json","r") as selectedComments:
    selectedComments = json.load(selectedComments)
with open("selectedPages.json","r") as selectedPages:
    selectedPages = json.load(selectedPages)
        
with open("selectedPostsPics.json","r") as selectedPostsPics:
    selectedPostsPics = json.load(selectedPostsPics)

#--------------------------------------------------------
#define the classes and packages
class Trigger:
    link = ''
    message = ''
    def __init__(self,graph,firefoxProfile,picsdir):
        self.picsdir = picsdir
        self.graph = graph
        self.profile = firefoxProfile
        self.driver = webdriver.Firefox(self.profile)
    def postGroup(self,message):
        self.driver.get("https://m.facebook.com/groups/?seemore")
        ins = self.driver.find_elements_by_xpath('//a[@href]')
        groupsLinks = []
        for item in ins:
            s = item.get_attribute("href")
            for x in range(9):
                groupNumber= "groups/"+str(x)
                if groupNumber in s:
                    print(item.text)
                    groupsLinks.append(s)
        self.link = random.choice(groupsLinks)
        self.message = message
        self.driver.get(self.link)
        try:
            ins = self.driver.find_element_by_id('u_0_0')
            ins.send_keys(message)
            # submit input
            ins = self.driver.find_elements_by_tag_name('input')
            for x in ins:
                if 'Post' in x.get_attribute('value'):
                    x.click()
                    break
        except:
            print("exception happened")
            pass
    def postMe(self,message):
        self.link = "https://m.facebook.com/home.php"
        self.message = message
        self.driver.get(self.link) 
        try:
            ins = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
            ins.send_keys(self.message)
            # submit input
            ins = self.driver.find_elements_by_tag_name('input')
            for x in ins:
                if 'Post' in x.get_attribute('value'):
                    x.click()
                    break
        except:
            print("exception happened")
            pass

    def comment(self,link,message):
        self.link = link
        self.message = message
        self.driver.get(self.link)
        
        try:
            ins = self.driver.find_element_by_id('composerInput')
            ins.send_keys(self.message)
            # submit input
            ins = self.driver.find_elements_by_tag_name('input')
            for x in ins:
                if 'omment' in x.get_attribute('value'):
                    x.click()
                    break        
        except:
            print("exception happened")
            pass

    def likeHome(self):
        self.link = "https://m.facebook.com/"
        self.driver.get(self.link)    
        try:
            ins = self.driver.find_elements_by_tag_name("a")
            for x in range(30):
                x=random.choice(ins)
                print(x.text)
                if 'ike' in x.text:
                    x.click()
                    break
            
        except:
            print("exception happened")
            pass
        
        
    def reactHome(self):
        self.link = "https://m.facebook.com/"
        self.driver.get(self.link)  
        try:
            ins = self.driver.find_elements_by_xpath('//a[@href]')
            for i in range(len(ins)):
                x=random.choice(ins)
                if 'React' in x.text:
                    x.click()  
                    time.sleep(5)
                    reactIns = self.driver.find_elements_by_xpath('//a[@href]')
                    for j in range(len(reactIns)):
                        reactX = random.choice(reactIns)
                        if reactX.text in ["Angry", "Wow","Sad"]:
                            reactX.click()
                            break  
                    break 
        except:
            print("exception happened")
            pass  

    def commentHome(self):            
        self.link = "https://m.facebook.com/"
        self.driver.get(self.link)  
        try:
            ins = self.driver.find_elements_by_xpath('//a[@href]')
            for i in range(len(ins)):
                x=random.choice(ins)
                if 'Comment' in x.text:
                    x.click() 
                    time.sleep(5)
                    
                    oldLink = self.driver.current_url
                    if (oldLink.find("story_fbid=") > 10):
                        id = oldLink.rsplit('&id=')[1].rsplit('&')[0]
                        newLink = "https://m.facebook.com/profile.php?id="+id +"&v=timeline"
                        self.driver.get(newLink)     
                        ins = self.driver.find_elements_by_xpath('//a[@href]')
                        for i in range(len(ins)*2):
                            x=random.choice(ins)
                            if "omments" in x.text:
                                x.click()  
                                time.sleep(5)
                                a = self.driver.find_elements_by_xpath('.//div[4]')
                                a2 = a[0].find_elements_by_xpath('.//div')
                                h = [a2[x]  for x in range(len(a2)) if a2[x].get_attribute("style") == "text-align: right;"]
                                self.message = random.choice(h).text
                                break
                    else:
                        newLink = oldLink.rsplit('?')[0]
                        self.driver.get(newLink)     
                        ins = self.driver.find_elements_by_xpath('//a[@href]')
                        for i in range(len(ins)*2):
                            x=random.choice(ins)
                            if "omments" in x.text:
                                x.click()  
                                time.sleep(5)
                                a = self.driver.find_elements_by_xpath('.//div')
                                h = [a[x]  for x in range(len(a)) if a[x].get_attribute("style") == "text-align: right;"]
                                self.message = random.choice(h).text
                                break

                        
                    
                    self.driver.get(oldLink)    
                    ins = self.driver.find_element_by_id('composerInput')
                    ins.send_keys(self.message)
                    # submit input
                    ins = self.driver.find_elements_by_tag_name('input')
                    for x in ins:
                        if 'omment' in x.get_attribute('value'):
                            x.click()
                            break    
                    break
        except:
            print("exception happened")
            pass                 
    def postVideo(self, dir):
        filename = random.choice(os.listdir(dir))
        path = os.path.join(dir, filename)
        self.link = "https://www.facebook.com/ahmed.gkae.7"
        self.driver.get(self.link)
        time.sleep(5)
        ins1 = self.driver.find_elements_by_tag_name('a')
        a = []
        i = 0
        for x1 in ins1:
            print(i)
            i = i + 1
            try:
                ins2 = x1.find_elements_by_tag_name('input')
                for x2 in ins2:
                    if "video/*" in x2.get_attribute("accept"):
                        print("succeeded")
                        a.append(x1)
            except:
                print("exception")
                pass
    
        time.sleep(5)
        a[0].find_element_by_css_selector("input[type=\"file\"]").send_keys(path)
        time.sleep(60)
        ins = self.driver.find_elements_by_tag_name('button')
        i = 0
        for x in ins:
            if 'Post' in x.text:
                try:
                    x.click()
                    break
                except:
                    print("waiting file to upload ..")
                    time.sleep(30)

                       
    def postPic(self, selectedPostsPics):
        self.link = "https://m.facebook.com/home.php"
        messageAll = random.choice(selectedPostsPics)
        self.message = messageAll['message']
        dir = self.picsdir
        path = dir +"/"+ str(messageAll['id']) + ".jpg"
        self.driver.get(self.link) 
        try:
            ins = self.driver.find_element_by_xpath('//*[@id="u_0_0"]')
            ins.send_keys(self.message)
            ins = self.driver.find_element_by_name("view_photo")
            ins.click()
            time.sleep(3)
            ins = self.driver.find_element_by_name("file1")
            ins.send_keys(path)
            time.sleep(2)
            ins = self.driver.find_element_by_name("add_photo_done")
            ins.click()
            time.sleep(60)
            ins = self.driver.find_element_by_name("view_post")
            ins.click()
            time.sleep(60)
            try:
                ins = self.driver.find_element_by_name("done")
                ins.click()
            except:
                print("no done here")
                ins = self.driver.find_elements_by_tag_name("a")
                for x in ins:
                    if x.text in ["Skip"]:
                        x.click()
                        break
            
            
        except:
            print("exception happened")
            pass    
        
  
    def postGroupFromGroup(self):
        try:
            self.driver.get("https://m.facebook.com/groups/?seemore")
            ins = self.driver.find_elements_by_tag_name('table')
            insRef = []
            for item in ins:
                try:  
                    insRef.append(int(item.find_element_by_tag_name('span').text))
                except:
                    print("not a count")
                    insRef.append(0)
                    pass
            #by experimenting
            insRef = insRef[:-2]
            insRef.pop(0)
            insRef.pop(0)
            
            
            maxInsRef = [x for x,y in enumerate(insRef) if y == 25]
            ins = self.driver.find_elements_by_xpath('//a[@href]')
            groupsLinks = []
            for item in ins:
                s = item.get_attribute("href")
                for x in range(9):
                    groupNumber= "groups/"+str(x)
                    if groupNumber in s:
                        print(item.text)
                        groupsLinks.append(s)
            
            
            self.link = groupsLinks[random.choice(maxInsRef)]
            self.groupId = self.link.rsplit('?')[0].rsplit('groups/')[1]
            self.messages1 =  self.graph.get_object(self.groupId,fields = "feed")['feed']['data']
            self.message = self.messages1[len(self.messages1)-3]['message']
            self.driver.get(self.link)
            try:
                ins = self.driver.find_element_by_id('u_0_0')
                ins.send_keys(self.message)
                # submit input
                ins = self.driver.find_elements_by_tag_name('input')
                for x in ins:
                    if 'Post' in x.get_attribute('value'):
                        print("Post input found")
                        x.click()
                        break
            except:
                print("exception happened")
                pass
        except:
            print("exception from postGroupFromGroup")
            pass
        
    def markMessagesAsRead(self):
        self.link = "https://m.facebook.com/messages/?folder=unread"
        self.driver.get(self.link)
        ins = self.driver.find_elements_by_xpath('//a[@href]')
        chatsLinks = []
        for item in ins:
            s = item.get_attribute("href")
            if "/messages/read/?" in s:
                chatsLinks.append(s)
        for item in chatsLinks:
            self.driver.get(item)
            time.sleep(3)
        
        
      
                    
                    
def commentScanner(Trigger,graph, pagesIds,comments,timedif):
    print("commentScanner working ..")
    posts = graph.get_connections(id=random.choice(pagesIds), connection_name='posts')
    postTime = posts["data"][0]['created_time']
    postTimeFormatted= dateutil.parser.parse(postTime)
    now = datetime.utcnow()
    postTimeFormatted = postTimeFormatted.replace(tzinfo=None)
    timeDif = now - postTimeFormatted
    if (timeDif.seconds < timedif):
        post = posts["data"][0]['id']
        m = post.split(sep = '_')
        link = "https://m.facebook.com/story.php?story_fbid=" + str(m[1])+"&id=" + str(m[0])
        Trigger.comment(link,random.choice(comments))
        


           
        

def addFriends(Trigger, graph,numberOfFriends,groupsIdsUnique ):
    while numberOfFriends > 0:
        try:
            #a = graph.get_object(random.choice(membersIdsUnique), fields = "link")['link'].rsplit('www')
            #userLink = a[0]+'m'+a[1]
            #Trigger.driver.get(userLink)
            id = random.choice(groupsIdsUnique)
            groupLink = "https://m.facebook.com/browse/group/members/?id=" + str(id) +"&start=0&listType=list_nonfriend"
            Trigger.driver.get(groupLink)
            ins = Trigger.driver.find_elements_by_xpath('//a[@href]')
            newIns = [ins[x] for x in range(len(ins)) if "fref=pb" in ins[x].get_attribute("href")]
            random.choice(newIns).click()
            time.sleep(3)
            if any(word in Trigger.driver.page_source for word in ["Munich","München","munich","münchen","Neuherberg","neuherberg"]):
                ins = Trigger.driver.find_elements_by_tag_name("a")
                for x in ins:
                    if "See all friends" in x.text:
                        print(x.text)
                        a = int(x.text.rsplit('(')[1].rsplit(')')[0])
                        print(a)
                        if (a > 2000 and a < 4500):
                            ins = Trigger.driver.find_elements_by_xpath('//a[@href]')
                            for xx in ins:
                                print(xx.text)
                                if 'Add Friend' in xx.text:
                                    xx.click()
                                    time.sleep(5)
                                    numberOfFriends = numberOfFriends - 1
                                    break      
                        break
        except:
            print("exception happended ")
            pass
        

        

def groupsGen(graph,text):
    groupsIdsLarge = []
    for letter in random.sample(text,len(text)):
        print(letter)
        try:
            groupsList = graph.search('group',q =letter)
            groupsListIds = [groupsList['data'][x]['id'] for x in range(len(groupsList['data'])) if groupsList['data'][x]['privacy']=='OPEN']
            groupsIdsLarge.append(groupsListIds)
        except:
            print("exception")
            pass

    groupsIdsFlat = [val for sublist in groupsIdsLarge for val in sublist]
    groupsIdsUnique = list(set(groupsIdsFlat))
    with open("groupsIdsUnique.json","w") as outputfile:
        json.dump(groupsIdsUnique,outputfile)
    
    
def joinGroups(Trigger, groupsIdsUnique, numberOfGroupsToJoin):
    while numberOfGroupsToJoin > 0:
        try:
            link = 'https://m.facebook.com/groups/'+str(random.choice(groupsIdsUnique))
            Trigger.driver.get(link)
            insSpan = Trigger.driver.find_elements_by_tag_name("span")
            numbers = []
            print("checking group ...")
            for item in insSpan:
                if item.text.isdigit():
                    numbers.append(int(item.text))
            print("...................it has "+str(max(numbers))+"members ")
            if (max(numbers) > 40000 and max(numbers) < 1000000):    
                ins = Trigger.driver.find_elements_by_tag_name('input')
                for x in ins:
                    if 'oin' in x.get_attribute('value'):
                        x.click()
                        print("group selected.!!")
                        numberOfGroupsToJoin = numberOfGroupsToJoin - 1
                        break
        except:
            print("exception happened")
            pass                             
        

def genPostPics(graph,picsdir):
    pagesIdsLarge = []
    for letter in text:
        pagesList = graph.search('page',q =letter)
        pagesListIds = [pagesList['data'][x]['id'] for x in range(len(pagesList['data']))]
        pagesIdsLarge.append(pagesListIds)

    pagesIdsFlat = [val for sublist in pagesIdsLarge for val in sublist]
    pagesIdsUnique = list(set(pagesIdsFlat))  
    allPos = []
    for pageId in random.sample(pagesIdsUnique, len(pagesIdsUnique)):
        posts = graph.get_connections(id=pageId, connection_name='posts')
        postsIds = [posts["data"][x]["id"] for x in range(len(posts["data"]))]
        for postId in postsIds:
            postStory = graph.get_object(id=postId,field = 'message')
            postCount = graph.get_connections(postId,connection_name = "likes",summary='true')['summary']['total_count']
            allPos.append({"story":postStory, "count":postCount, "id":postId})
    fixedList = []
    for item in allPos:
        try:
            dic = {"count":item['count'],"message":item['story']['message'],"id":item["id"]}
        except:
            pass
        fixedList.append(dic)
    #sort them       
    longPosts = [{"message":fixedList[x]['message'],"count":fixedList[x]['count'],"id":fixedList[x]['id']} for x in range(len(fixedList)) if len(fixedList[x]['message']) > 2 and fixedList[x]['count'] > 400]
    i = len(longPosts)
    for x in longPosts:
        print(i)
        i = i -1
        try:
            pictureLink = graph.get_object(x['id'], fields = "full_picture")['full_picture']
            dir = picsdir
            path = dir +"/"+ str(x['id']) + ".jpg"
            urllib.request.urlretrieve(pictureLink,path )
        except:
            print("no photos for this post")
            pass
       
    with open("selectedPostsPics.json","w") as outputfile:
        json.dump(longPosts,outputfile)


#---------------------------------------------------------------
#begin the firefox and now listening
print("Opening firefox please wait ...")
t = Trigger(graph, profile)        



what_to_do = [[1] * likesCount,[2] * commentsCount, [3] * reactsCount, [4] * postsCount, [5] * videosCount , [6] * postsInGroupCount ]
what_to_do = [val for sublist in what_to_do for val in sublist]
x = len(what_to_do)
while x > 0:
    x = x - 1
    time.sleep(abs(int(random.gauss(interval,interval/ 10))))
    m = random.choice(what_to_do)
    try:
        if (m == 1):
            t.likeHome()
        elif (m == 2):
            t.commentHome()
        elif (m == 3):
            t.reactHome()
        elif (m == 4):
            t.postPic(selectedPostsPics)
        elif (m == 5):
            t.postVideo(dir)
        elif (m == 6):
            t.postGroupFromGroup()
    except:
        print("exception happen in modulus work")
        pass