import streamlit as st
import snscrape.modules.twitter as sntwitter
import pandas as pd
import datetime
import pymongo as py
from PIL import Image


# reference for database
Client=py.MongoClient('mongodb://127.0.0.1:27017/')
mydb=Client["twitter"]
info=mydb.twitter_info

# header image

image = Image.open('E:\Scrape.PNG')
new_image = image.resize((1700, 300))
st.image(new_image)


# title
st.markdown("<h1 style='text-align: center; color: black;'>Twitter Scrapping </h1>", unsafe_allow_html=True)

#Sidebar

with st.sidebar:
   st.info("Twitter Sctapping")
   st.markdown("""This application uses the Python library Snscrape and Streamlit to create a web-based Twitter scraping utility. 
   It enables users to look for tweets within a certain time period that contain a particular hashtag or keyword.""")
      
   image = Image.open('E:\Capture1.PNG')
   st.image(image,width=300)

   st.info("Uses")
   st.markdown("""Popular uses of data scraping include: Research for web content/business intelligence. Pricing for travel booker sites/price comparison sites.
   Finding sales leads/conducting market research by crawling public data sources (e.g. Yell and Twitter)""")



# reference for main function
df = pd.DataFrame()
search= st.radio('How do you expect the data to be retrived', ('Keyword', 'Hashtag'))
word = st.text_input('Please enter a '+search, 'Please enter the word',)
start_date = st.date_input("Select the start date", datetime.date(2020, 1, 1),key='d1')
end_date = st.date_input("Select the end date", datetime.date(2023, 4, 6),key='d2')
date= f'{start_date} to {end_date}'
tweet_numbers = st.slider('How many tweets to scrape', 0, 1000, 5)
tweets= []


# scrapped details

if word:
   if search=='Keyword':
       for i,tweet in enumerate(sntwitter.TwitterSearchScraper(f'{word} lang:en since:{start_date} until:{end_date}').get_items()):
           if i>tweet_numbers-1:
               break
           tweets.append([tweet.user.username,tweet.date,tweet.id,tweet.url,tweet.source,tweet.content, tweet.replyCount, tweet.retweetCount,tweet.likeCount,tweet.lang ])
       df = pd.DataFrame(tweets, columns=[ 'Username','Date','ID','URL','Source','Content', 'ReplyCount', 'RetweetCount', 'LikeCount','Language'])
   else:
       for i,tweet in enumerate(sntwitter.TwitterHashtagScraper(f'{word} lang:en since:{start_date} until:{end_date}').get_items()):
           if i>tweet_numbers-1:
               break            
           tweets.append([ tweet.user.username,tweet.date,tweet.id,tweet.url,tweet.source,tweet.content, tweet.replyCount, tweet.retweetCount,tweet.likeCount,tweet.lang ])
       df = pd.DataFrame(tweets, columns=[ 'Username','Date','ID','URL','Source','Content', 'ReplyCount', 'RetweetCount', 'LikeCount','Language' ])
else:
    st.warning( 'KEYWORD NOT BE EMPTY')






#show Scrappped tweets

def show(df):
   return df
a=show(df)

sh=st.button('Show Scrapped Tweets')
if sh:
   st.snow()
   df["Date"]=pd.to_datetime(df["Date"]).dt.date
   st.write(a) 
   st.success("Data Scrapped Successfully",icon="✅")


# download the data as csv
def csv(df):
   return df.to_csv(index=False) 

file1=csv(df)
cs=st.download_button(label="Download data as CSV",data=file1,file_name='Twitter_scrappped_data.csv',mime='text/csv',)        
if cs:
   st.success("Data downloaded in csv",icon="✅")


#download the data as json

def json(df):
   return df.to_json(orient ='records')

file2 = json(df)
js=st.download_button(label="Download data as JSON",file_name="Twitter_scrapped_data.json",mime="application/json",data=file2)
if js:
   st.success("Data downloaded in json",icon="✅")




# reference for db

dict=df.to_dict("records")
data={"Scrapped Word":word,"Scrapped date":date,"Scrapped data":dict}
def show(data):
   return data
z=show(data)


# uploaded in database
up=st.button("Upload to database")
if up:
   st.balloons()
   df["Date"]=pd.to_datetime(df["Date"]).dt.date
   info.insert_one(z) 
   st.success('Successfully uploaded in Database',icon="✅")


# show database

db=st.button("Show Database")
if db:
   st.snow()
   st.success("Uploaded Details",icon="✅")
   st.write(z)






  
