# -*- coding: utf-8 -*-
"""
Created on Thu Apr 25 12:31:39 2019

@author: FaiHuntrakool
"""

def get_by_prefecture(prefecture):
    #### things to do in Tokyo
    page=requests.get("https://www.tripadvisor.com"+prefecture)
    contents = page.content
    soup=BeautifulSoup(contents,'html.parser')
    links=[]
    for link in soup.find_all('a'):
        if str(link).find('Attraction_Review')>=0:
            if str(link).find("#REVIEWS")<0:
                  links.append(link.get('href'))
    links=list(set(links))
    data=dict()
    i=0
    for link in links:
        page = requests.get('https://www.tripadvisor.com'+str(link))
        contents = page.content
        ###### Attraction page ####
        ####eg: https://www.tripadvisor.com/Attraction_Review-g1066443-d1987338-Reviews-Yurakucho_Itocia-Chiyoda_Tokyo_Tokyo_Prefecture_Kanto.html######
        def get_data(contents):
            soup=BeautifulSoup(contents,'html.parser')
        #    html=(soup.prettify())
            def get_place_name():    
                place=str(soup.title.string)
                place=place[:place.find('- 2019')]
                return place
            def get_time():
                soup.get_text()
                spans=soup.find_all('span',{'class':'time'})
                if len(spans)>0:
                    lines=list(set([span.get_text() for span in spans]))
                    
                    import datetime
                    for i in range(0,len(lines)):
                        lines[i]=str(datetime.datetime.strptime(lines[i].replace(' ',''),'%I:%M%p').time())    
                    lines.sort()
                    return str(lines[0])+'-'+str(lines[1])
                else:
                    return 'no data'
            def get_place_type():
                spans=soup.find_all('div',{'class':'detail'})
                place_type=spans[0].get_text()
                return place_type
            data=dict()
            data['name']=get_place_name()
            data['working hours']=get_time()
            data['type']=get_place_type()
            return data
        data[i]=get_data(contents)
        i+=1
    
    city=prefecture[prefecture.find('Activities-')+11:prefecture.find('_')]
    
    import pandas as pd    
    df=pd.DataFrame()
    for index,val in data.items():
        temp=pd.DataFrame.from_dict(val,'index').transpose()
        df=df.append(temp,ignore_index=True)
    df=df.drop_duplicates().reset_index(drop=True)
    df['city']=city
    return df

### things to do in Japan
import requests
from bs4 import BeautifulSoup
import pandas as pd
page=requests.get("https://www.tripadvisor.com/Attractions-g294232-Activities-Japan.html")
contents = page.content
soup=BeautifulSoup(contents,'html.parser')
links=[]
for link in soup.find_all('a'):
    if (str(link).find('Attractions-')>=0) & (str(link).find('Prefecture')>=0):
        links.append(link.get('href'))

data=pd.DataFrame()
i=0
for prefecture in links:
    data=data.append(get_by_prefecture(prefecture))
  
data.to_csv('trip_scrap.csv',index=False)











