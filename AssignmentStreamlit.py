# -*- coding: utf-8 -*-
"""
Created on Sat Feb 20 19:00:11 2021

@author: keven
"""

import pandas as pd
import numpy as np
from PIL import Image
import plotly.express as px
import streamlit as st
import pybase64

#putting the image on a variable
image = Image.open('capture.png')


#Displaying the image
st.image(image, use_column_width=True)


#Loading the video game dataset
@st.cache(allow_output_mutation=True)
def load_data(path):
    df=pd.read_csv(path)
    return df

df=load_data(r"C:\Users\keven\Desktop\Personal Project\DATA VIZ COURSE\vgsales.csv")
#Dropping NAs
df.dropna(inplace=True)

#Checking how many platform there are. We want to only keep playstation, nintendo and xbox consoles
df.Platform.unique()

#Dropping not so relevant platform
df.drop(df[df['Platform'] == 'DC'].index, inplace = True) 
df.drop(df[df['Platform'] == 'SAT'].index, inplace = True) 
df.drop(df[df['Platform'] == 'SCD'].index, inplace = True) 
df.drop(df[df['Platform'] == 'WS'].index, inplace = True) 
df.drop(df[df['Platform'] == 'NG'].index, inplace = True) 
df.drop(df[df['Platform'] == 'TG16'].index, inplace = True) 
df.drop(df[df['Platform'] == '3DO'].index, inplace = True) 
df.drop(df[df['Platform'] == 'GG'].index, inplace = True) 
df.drop(df[df['Platform'] == '2600'].index, inplace = True) 
df.drop(df[df['Platform'] == 'GEN'].index, inplace = True) 
df.drop(df[df['Platform'] == 'GC'].index, inplace = True) 
df.drop(df[df['Platform'] == 'PCFX'].index, inplace = True) 
#Checking agains



#Creating a dataframe that group every platform and the global sales next to it.
df1=df[['Platform','Global_Sales']].groupby(['Platform']).sum().sort_values(by=['Global_Sales']).reset_index()
df1.head()

#Creating a new colum that has the value of Nintendo if the platform is from nintent, Playstation if the platform is
#from Playstation etc.
Nintendo=['Wii','NES','GB','DS','SNES','GBA','3DS','N64','Wiiu']
Playstation=['PS','PS2','PS3','PS4','PSP','PSV']
XBOX=['XB','X360','XOne']
PC=['PC']

New_column=[]

for index, row in df.iterrows():
    if row['Platform'] in Nintendo:
        New_column.append('Nintendo')
    elif row['Platform'] in Playstation:
        New_column.append('Playstation')
    elif row['Platform'] in XBOX:
        New_column.append('XBOX')
    else:
        New_column.append('PC')

#The list created will be a new column inn the data frame
df['Company']=New_column

st.title("Video Games Sale: A Legendary Battle between Nintendo, PS and XBOX.")

st.markdown("""
This app is Segmented into two parts. **Part I**, will allow the user to 
chose many options. For instance, one might want to check the sales on a 
specific year or for a specific Video Game Genre. 
**Part II** will be us displaying some charts on the whole Data. 
Here are some topics that you can tackle using this application alone!
* **What are the most sold video games?**
* **Nintendo Vs PlayStation Vs XBOX**: Who is doing better?
* **Difference between Japanese Market, NA Market and EU Market**
* **Who are the best publishers?**  """)

 
#Creating the sidebar that will only be used for the first Part    
st.sidebar.header("User Input Features for Part I")
#Option for the years
selected_year=st.sidebar.selectbox("Year",list(reversed(range(1983,2018))))

#Defining a function that will create the a data frame for a specific year
def load_data(df,year):
    return df[df['Year']==year]
df_selected=load_data(df,selected_year)

#Function that allows the user to download the data
@st.cache
def filedownload(df):
    csv = df.to_csv(index=False)
    b64 = pybase64.b64encode(csv.encode()).decode()  # strings <-> bytes conversions
    href = f'<a href="data:file/csv;base64,{b64}" download="vgsales.csv">Download CSV File</a>'
    return href

#Here we are adding the differe boxes that will allow the user to chose what data he wants to download/find the analysis on it
sorted_unique_company = sorted(['Nintendo', 'XBOX', 'Playstation', 'PC'])
selected_Company = st.sidebar.multiselect('Team', sorted_unique_company, sorted_unique_company)

unique_plat =['Wii', 'NES', 'GB', 'DS', 'X360', 'PS3' ,'PS2', 'SNES', 'GBA', '3DS', 'PS4', 'N64',
 'PS', 'XB', 'PC', 'PSP', 'XOne', 'WiiU', 'PSV']
selected_plat = st.sidebar.multiselect('Company', unique_plat, unique_plat)

unique_genre =['Action', 'Adventure', 'Fighting', 'Misc', 'Platform', 'Puzzle', 'Racing', 'Role-Playing', 'Shooter', 'Simulation', 'Sports', 'Strategy']
selected_genre= st.sidebar.multiselect('Genre', unique_genre, unique_genre)

#In this part, we did the filtering
df_selected_final = df_selected[(df_selected.Company.isin(selected_Company)) & (df_selected.Platform.isin(selected_plat)) &(df_selected.Genre.isin(selected_genre))]



#Displaying the dataframe that the user can manipulate. This will allow the user to download the things the 
#he only need, instead of downloading the whole data. Perhaps he only desires a 1 year data
st.header('Part I: Play with the options in the sidebar and discover meaningful insights!')
st.subheader('Displaying Video Game Sales: This Data Changes According to Your Input')
st.write('Data Dimension: ' + str(df_selected_final.shape[0]) + ' rows and ' + str(df_selected_final.shape[1]) + ' columns.')
st.dataframe(df_selected_final)
st.markdown(filedownload(df_selected_final), unsafe_allow_html=True)

#Here, we are just plotting Charts. We introduced also a button that the user should click in order
#for the chart to be revealed

st.subheader('**Click** the below button for a comparison of Global Sales across Companies:')
if st.button('Total Sales for each Company'):
    fig = px.bar(df_selected_final , x="Company", y="Global_Sales", hover_name="Name",
                 title="Global Sales of Games for different company",labels=dict(Company="Company", Global_Sales="Total Game Sold in M"))
    st.plotly_chart(fig)


df1=df_selected_final[['Platform','Global_Sales']].groupby(['Platform']).sum().sort_values(by=['Global_Sales']).reset_index()


st.subheader('**Click** the below button to Check which Platform sold the most Video Game:')
if st.button('Best Platform'):
    fig = px.bar(df1,x='Platform',
            y='Global_Sales',title="Global Sales of Games in Different Platform",labels=dict(Platform="Platform", Global_Sales="Total Game Sold in M"))
    st.plotly_chart(fig)


## Created a histogram to check for the distribution of Globa Sales for the 4 different companies
st.subheader('**Click** the below button to check the sales distribution:')
if st.button('Distribution of Sales For each Company'):
    fig = px.histogram(df_selected_final, x="Global_Sales", color="Company"
                  ,labels=dict(Global_Sales="Total Game Sold in M"), title='Distribution of the Global Sales across platforms')
    st.plotly_chart(fig)


#This shows the genre across platform. It shows for instance that nintendo is home for platform, whereas playstation and 
#xbox is home for shooter
st.subheader('**Click** the below button to check all the games and their genre:')
if st.button('All the Games and the Genre'):
    fig = px.histogram(df_selected_final, x="Genre", color="Company",title="Genre Across Different Platform")
    st.plotly_chart(fig)

st.subheader('The top sold video game genre:')
num_vg=st.slider('Display the top N Genres:')
fig = px.histogram(df_selected_final.head(num_vg), x="Genre", color="Company",title='Displaying the Top Games in Terms of Global Sales and Their genre/platform')
st.plotly_chart(fig)


st.subheader('The top publishers:')  
num_vg=st.slider('Display the top N Publishers : 1,100,100')
df_N=df_selected_final.sort_values(by=['Global_Sales'],ascending=False)
df_N=df_N[:num_vg]
fig = px.histogram(df_selected_final.head(num_vg), x="Genre", color="Publisher",title='Displaying the Top Games in Terms of Global Sales and Their Publisher')
st.plotly_chart(fig)
 
st.subheader('Best video games:')
num_vg=st.slider('Display the top N Video Games : 1,100,100')
df_N=df_selected_final.sort_values(by=['Global_Sales'],ascending=False)
df_N=df_N[:num_vg]
fig = px.bar(df_N,x='Name',
            y='Global_Sales',title="Global Sales of Games in Different Platform",labels=dict(Name="Name", Global_Sales="Total Game Sold in M"), hover_name='Company')
st.plotly_chart(fig)
    
    
st.header('Part II: Analyzing all the data')
st.subheader('Display all the Data')
st.write('Data Dimension: ' + str(df.shape[0]) + ' rows and ' + str(df.shape[1]) + ' columns.')
st.dataframe(df)
st.markdown(filedownload(df), unsafe_allow_html=True)


df_agg1 = df.groupby(['Year','Company']).agg({'NA_Sales':np.sum,'EU_Sales':np.sum,'JP_Sales':np.sum,'Other_Sales':np.sum}).reset_index()
st.subheader('Nintendo Vs Xbox Vs Playstation Vs PC Sales over the years:')
fig = px.line(df_agg1 , x="Year", y=["Other_Sales","JP_Sales","EU_Sales","NA_Sales"],title= "Game Sales in different regions over the Years for each Platform",
  animation_frame="Company") 
st.plotly_chart(fig)
#Creating a table that groups every company with the global sale that year
df_agg = df.groupby(['Year','Company']).agg({'Global_Sales':np.sum}).reset_index()

#I have also noticed that since ps and Xbox did not start pre 2000, when I start with the animation, it only shows 
#Nintendo and forgets that there are competitors afterward. If however, we start w ps and xbox, the animation will take
# them into consideration for every year. That is why I created artificial line in the begining
df2 = pd.DataFrame({"Year":[1982.0,1982.0,1982.0,1982.0], 
                    "Company":["Nintendo","PC", "Playstation", "XBOX"],
                   "Global_Sales":[0,0,0,0]}) 
final=df2.append(df_agg) 

final["Cumulative_Sales"]=final.groupby('Company')['Global_Sales'].cumsum()

#Creating the animation. This show each year, how many Cumulative sales there was in each platform
st.subheader('Nintendo Vs Xbox Vs Playstation Vs PC cumulative Sales over the year:') 
fig = px.bar(final[final["Year"]<2017] , x="Company", y="Cumulative_Sales", color="Company",
  animation_frame="Year",labels=dict(Cumulative_Sales="Cumulative Total Game Sold in M"), title="Cumulative Sales as the Time Passes for Every Platform") 
st.plotly_chart(fig)


#Creating a dataframe that group every platform and the global sales next to it.
df1=df[['Platform','Global_Sales']].groupby(['Platform']).sum().sort_values(by=['Global_Sales']).reset_index()
#Plotting a barchart. x axis is the platform (Categorical) y axis is the Global_Sales of games (Numerical)
st.subheader('Top Platform in terms of Selling video games.') 
fig = px.bar(df1,x='Platform',
            y='Global_Sales',title="Global Sales of Games in Different Platform",labels=dict(Platform="Platform", Global_Sales="Total Game Sold in M"))
st.plotly_chart(fig)   

st.subheader('Which genres occupied the top spots?') 
num_vg=st.slider('Display the top Game of All time:')
fig = px.histogram(df.head(num_vg), x="Genre",color="Company")
st.plotly_chart(fig) 



#Again, here we are creating artificial rows for the same reason mentioned before
df2 = pd.DataFrame({"Rank":[100000001,100000002,100000003],
                    "Name":["Name2","Name3",'Name4'],
                    "Platform":["Unknown2","Unknown3","Unknown4"],
                    'Year':[1983.0,1983.0,1983.0],
                    'Genre':["Unknown2","Unknown3","Unknown4"],
                    'Publisher':["Unknown2","Unknown3","Unknown4"],
                    'NA_Sales':[0.1,0.1,0.00001],
                    'EU_Sales':[0.00001,0.00001,0.00001],
                    'JP_Sales':[0.00001,0.00001,0.00001],
                    'Other_Sales':[0.00001,0.00001,0.00001],
                    'Global_Sales':[0.00001,0.00001,0.00001],
                    'Company':['PC','Playstation','XBOX']})
    
#Here, we trying to find if there is a linear relation between Japan and Na sales. This will allow us to see if
#These two regions have the same tastes, if for instance we got a linear relation.
st.subheader("""Is there a difference between NA and JP Sales? It looks like yes since the the sales does not show a relationship:""") 
fig=px.scatter(df2.append(df).sort_values(by=['Year']), x="NA_Sales", y="JP_Sales", color="Company",size="Global_Sales", size_max=60, hover_name="Platform",
           animation_frame="Year",
           labels=dict(NA_Sales="North America Sales in M", JP_Sales="Japan Salesn in M"),
          title="Relation of Sales Between Japan and North America, Across Different Years")
st.plotly_chart(fig) 

#We did the same thing but this time we are comparing NA wit Eu
st.subheader("""Is there a difference between NA and EU Sales? It looks like no since the the sales does show a relationship:""") 
fig=px.scatter(df2.append(df).sort_values(by=['Year']), x="NA_Sales", y="EU_Sales", color="Company",size="Global_Sales", size_max=60, hover_name="Platform",
           animation_frame="Year",
           labels=dict(NA_Sales="North America Sales in M", EU_Sales="Europe Sales in M"),
          title='Relation of Sales Between Europe and North America, Across Different Years')
st.plotly_chart(fig) 


#This is not the case in japan vs Na where we can hardly see any relation. Perhaps in the nintendo platform, there is a relation
st.subheader('Another look at the relation between NA and JP:')
fig=px.scatter(df.sort_values(by=['Year']), x="NA_Sales", y="JP_Sales", color="Company",size="Global_Sales", size_max=60, hover_name="Platform",
             facet_col="Company", labels=dict(NA_Sales="NA Sales in M",JP_Sales="Japan Sales in M"),
          title="Relation between Japan Sales and NA Sales")
st.plotly_chart(fig)
#This is a better way to look at the relation between in this example NA and eu. We can see that they almost are linear in
# every platform except in PC.
#We can try a increase pop size
st.subheader('Another look at the relation between NA and EU:')
fig=px.scatter(df.sort_values(by=['Year']), x="NA_Sales", y="EU_Sales", color="Company",size="Global_Sales", size_max=60, hover_name="Platform",
             facet_col="Company", labels=dict(NA_Sales="NA Sales in M",EU_Sales="Europe Sales in M"),
          title="Relation between European Sales and NA Sales")
st.plotly_chart(fig)

#What does Japan like? Here is the top genre in terms of japan sales
st.subheader('Japan favorite Genre. We are displaying these just to show that different regions = different tastes:')
fig = px.histogram(df.sort_values(by=['JP_Sales']).head(100), x="Genre", color="Company",title="Top Games and their Genre in Japan")
st.plotly_chart(fig)

#What does Japan like? Here is the top genre in terms of NA sales
st.subheader('NA favorite Genre. We are displaying these just to show that different regions = different tastes:')
fig = px.histogram(df.sort_values(by=['NA_Sales']).head(100), x="Genre", color="Company", title="Top Games and their Genre in North America")
st.plotly_chart(fig)

#What does EU like? Here is the top genre in terms of EU sales
st.subheader('EU favorite Genre. We are displaying these just to show that different regions = different tastes:')
fig = px.histogram(df.sort_values(by=['EU_Sales']).head(100), x="Genre", color='Company',title='Top Games and their Genre in Europe')
st.plotly_chart(fig)

st.subheader('The all time best sellers:')
num_vg=st.slider('Display All time best seller: 1,100,100')
fig = px.bar(df.head(num_vg),x='Name',
            y='Global_Sales',title="Global Sales of Games in Different Platform",labels=dict(Name="Name", Global_Sales="Total Game Sold in M"), hover_name='Company')
st.plotly_chart(fig)
    


st.header('Conclusion:')
st.markdown(""" 
            It looks like there is a close competition between Nintendo and Playstaion, while Xbox seems to
            be trailing behind. PC is for hardcore gaming and so it represents a niche market. That is why
            it is in the last place. 
            We also found out that there is a difference between the Japanese market, and the western market.
            Developer targeting a specific region should look into what genres the region is into before developping
            the game.
            """)


