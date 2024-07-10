import streamlit as st
from streamlit_option_menu import option_menu
import pandas as pd
import plotly.express as px
import psycopg2
import requests
import json
from PIL import Image


# DATAFRAME CREATION:
mydb=psycopg2.connect(host="localhost",user="postgres",port="5432",database="phonepe_data",password="Podafool348")
cursor=mydb.cursor()

# Aggre_transaction_table:
cursor.execute("SELECT * FROM aggre_transaction")
mydb.commit()
table1=cursor.fetchall()

Aggre_transaction=pd.DataFrame(table1 ,columns=("States","Years","Quarter","Transaction_type","Transaction_count","Transaction_amount") )


# Aggre_USER_table:
cursor.execute("SELECT * FROM aggre_user")
mydb.commit()
table2=cursor.fetchall()

Aggre_USER=pd.DataFrame(table2 ,columns=("States","Years","Quarter","Brands","Transaction_count","Percentage") )


# Map_tran:
cursor.execute("SELECT * FROM map_tran")
mydb.commit()
table3=cursor.fetchall()

Map_tran=pd.DataFrame(table3 ,columns=("States","Years","Quarter","Districts","Transaction_count","Transaction_amount") )


# Map_user:
cursor.execute("SELECT * FROM map_user")
mydb.commit()
table4=cursor.fetchall()

Map_user=pd.DataFrame(table4 ,columns=("States","Years","Quarter","Districts","RegisteredUsers","AppOpens") )


# Top_tran:
cursor.execute("SELECT * FROM top_tran")
mydb.commit()
table5=cursor.fetchall()

Top_tran=pd.DataFrame(table5 ,columns=("States","Years","Quarter","Pincodes","Transaction_count","Transaction_amount") )

#Top user:
cursor.execute("SELECT * FROM top_user")
mydb.commit()
table6=cursor.fetchall()

Top_user=pd.DataFrame(table6 ,columns=("States","Years","Quarter","Pincodes","RegisteredUsers") )


def Transaction_amount_count_Y(df, year):
    
    tacy= df[df["Years"] == year]
    tacy.reset_index(drop=True, inplace=True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2 = st.columns(2)
    with col1:
        fig_amount= px.bar(tacyg, x="States" , y="Transaction_amount" , title=f"{year} TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl,height= 650,width= 600)
        st.plotly_chart(fig_amount)

    with col2:
        fig_count= px.bar(tacyg, x="States" , y="Transaction_count" , title=f"{year} TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered_r,height= 650,width= 600)
        st.plotly_chart(fig_count)

    col1,col2=st.columns(2)
    with col1:      
        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        response
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM", color= "Transaction_amount", color_continuous_scale= "rainbow", range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),hover_name= "States",title= f"{year} TRANSACTION AMOUNT", fitbounds= "locations", height= 600,width= 600)

        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)
    
    
    with col2:  
        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM", color= "Transaction_count", color_continuous_scale= "rainbow", range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),hover_name= "States",title= f"{year} TRANSACTION COUNT", fitbounds= "locations", height= 600,width= 600)

        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)  

    return tacy      

def Transaction_amount_count_Y_Q(df, quarter):
    tacy= df[df["Quarter"] == quarter]
    tacy.reset_index(drop=True, inplace=True)

    tacyg= tacy.groupby("States")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:
        
        fig_amount= px.bar(tacyg, x="States" , y="Transaction_amount" , title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT",color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    with col2:
    
        fig_count= px.bar(tacyg, x="States" , y="Transaction_count" , title=f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT",color_discrete_sequence=px.colors.sequential.Bluered_r, height= 650,width= 600)
        st.plotly_chart(fig_count)
    col1,col2=st.columns(2)
    with col1:

        url= "https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
        response=requests.get(url)
        response
        data1=json.loads(response.content)
        states_name=[]
        for feature in data1["features"]:
            states_name.append(feature["properties"]["ST_NM"])

        states_name.sort()

        fig_india_1=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM", color= "Transaction_amount", color_continuous_scale= "rainbow", range_color=(tacyg["Transaction_amount"].min(), tacyg["Transaction_amount"].max()),hover_name= "States",title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION AMOUNT", fitbounds= "locations", height= 600,width= 600)

        fig_india_1.update_geos(visible= False)
        st.plotly_chart(fig_india_1)

    with col2:

        fig_india_2=px.choropleth(tacyg, geojson=data1, locations="States", featureidkey= "properties.ST_NM", color= "Transaction_count", color_continuous_scale= "rainbow", range_color=(tacyg["Transaction_count"].min(), tacyg["Transaction_count"].max()),hover_name= "States",title= f"{tacy['Years'].min()} YEAR {quarter} QUARTER TRANSACTION COUNT", fitbounds= "locations", height= 600,width= 600)

        fig_india_2.update_geos(visible= False)
        st.plotly_chart(fig_india_2)

    return tacy

def Aggre_Tran_Transaction_Type(df, state):
    tacy= df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg= tacy.groupby("Transaction_type")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:

        fig_pie_1=px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_amount",width= 600, title= f"{state.upper()} TRANSACTION AMOUNT",hole= 0.5)
        st.plotly_chart(fig_pie_1)

    with col2:
        fig_pie_2=px.pie(data_frame= tacyg, names= "Transaction_type", values= "Transaction_count",width= 600, title= f"{state.upper()} TRANSACTION COUNT",hole= 0.5)
        st.plotly_chart(fig_pie_2)

#Aggre_User_Analysis_1
def Aggre_user_plot_1(df, year):
    aguy= df[df["Years"]== year]
    aguy.reset_index(drop= True, inplace= True)

    aguyg= pd.DataFrame(aguy.groupby("Brands")[["Transaction_count"]].sum())
    aguyg.reset_index(inplace= True)
    aguyg

    fig_bar_1= px.bar(aguy, x="Brands", y="Transaction_count", title= f"{year} BRANDS AND TRANSACTION COUNT",width=1000, color_discrete_sequence=px.colors.sequential.haline, hover_name="Brands")
    st.plotly_chart(fig_bar_1)
    
    return aguy

#Aggre_user_Analysis_2
def Aggre_user_plot_2(df, quarter):
    aguyq= df[df["Quarter"]== quarter]
    aguyq.reset_index(drop= True, inplace= True)

    aguyqg= pd.DataFrame(aguyq.groupby("Brands")["Transaction_count"].sum())
    aguyqg.reset_index(inplace= True)

    fig_bar_1= px.bar(aguyqg, x="Brands", y="Transaction_count", title= f"{quarter} QUARTER, BRANDS AND TRANSACTION COUNT",width=1000, color_discrete_sequence=px.colors.sequential.Greens_r, hover_name="Brands")
    st.plotly_chart(fig_bar_1)

    return aguyq

#Aggre_user_analysis_3
def Aggre_user_plot_3(df, state):
    auyqs= df[df["States"] == "state"]
    auyqs.reset_index(drop= True, inplace= True)

    fig_line_1=px.line(auyqs, x="Brands", y="Transaction_count", hover_data="Percentage", title=f"{state.upper()} BRANDS, TRANSACTION COUNT,PERCENTAGE", width= 1000, markers= True)
    st.plotly_chart(fig_line_1)

#Map_Transaction_Districts
def Map_Tran_Districts_Type(df, state):
    
    tacy= df[df["States"] == state]
    tacy.reset_index(drop=True, inplace=True)

    tacyg= tacy.groupby("Districts")[["Transaction_count","Transaction_amount"]].sum()
    tacyg.reset_index(inplace=True)

    col1,col2= st.columns(2)
    with col1:
        fig_bar_1= px.bar(tacyg, x= "Transaction_amount", y= "Districts", orientation= "h",height= 600, title= f"{state.upper()} DISTRICT AND TRANSACTION AMOUNT", color_discrete_sequence= px.colors.sequential.algae_r)
        st.plotly_chart(fig_bar_1)

    with col2:
        fig_bar_2=px.bar(tacyg, x= "Transaction_count", y= "Districts", orientation= "h",height= 600, title= f"{state.upper()} DISTRICT AND TRANSACTION count", color_discrete_sequence= px.colors.sequential.Peach_r)
        st.plotly_chart(fig_bar_2)

    return tacy

#map_user_plot_1:
def map_user_plot_1(df, year):
    muy= df[df["Years"]== year]
    muy.reset_index(drop= True, inplace= True)

    muyg= muy.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyg.reset_index(inplace= True)
    muyg

    fig_line_1=px.line(muyg, x="States", y= ["RegisteredUsers", "AppOpens"], title=f"{year} REGISTERED USERS,APPOPENS", width= 1000,height= 800, markers= True)
    st.plotly_chart(fig_line_1)

    return muy

#map_user_plot_2:
def map_user_plot_2(df, quarter):
    muyq= df[df["Quarter"]== quarter]
    muyq.reset_index(drop= True, inplace= True)

    muyqg= muyq.groupby("States")[["RegisteredUsers", "AppOpens"]].sum()
    muyqg.reset_index(inplace= True)

    fig_line_1=px.line(muyqg, x="States", y= ["RegisteredUsers", "AppOpens"], title=f"{df['Years'].min()} YEARS {quarter} QUARTER REGISTERED USERS,APPOPENS", width= 1000,height= 800, markers= True,color_discrete_sequence=px.colors.sequential.BuPu_r)
    fig_line_1.show()

    return muyq

#map_user_plot_3
def map_user_plot_3(df,states):
    muyqs= df[df["States"]== states]
    muyqs.reset_index(drop= True, inplace= True)

    col1,col2= st.columns(2)
    with col1:
        fig_map_user_bar_1= px.bar(muyqs, x="RegisteredUsers", y="Districts", orientation= "h", title= f"{states.upper()} REGISTERED USERS", height= 800, color_discrete_sequence=px.colors.sequential.Blackbody_r)
        st.plotly_chart(fig_map_user_bar_1)

    with col2:
        fig_map_user_bar_2= px.bar(muyqs, x="AppOpens", y="Districts", orientation= "h", title= f"{states.upper()} APPOPENS", height= 800, color_discrete_sequence=px.colors.sequential.Blackbody)
        st.plotly_chart(fig_map_user_bar_2 )

#top_transaction_plot_1:
def top_transaction_plot_1(df, state):
    tay= df[df["States"]== "state"]
    tay.reset_index(drop= True, inplace= True)

    col1,col2=st.columns(2)
    with col1:

        fig_top_user_bar_1= px.bar(tay, x="Quarter", y="Transaction_amount",hover_data= "Pincodes", title= "TRANSACTION AMOUNT", height= 800, color_discrete_sequence=px.colors.sequential.Cividis)
        st.plotly_chart(fig_top_user_bar_1)

    with col2:
    
        fig_top_user_bar_2= px.bar(tay, x="Quarter", y="Transaction_count",hover_data= "Pincodes", title= "TRANSACTION COUNT", height= 800, color_discrete_sequence=px.colors.sequential.Cividis_r)
        st.plotly_chart(fig_top_user_bar_2)

def top_user_plot_1(df, year):
    tuy= df[df["Years"]== year]
    tuy.reset_index(drop= True, inplace= True)
    
    tuyg= pd.DataFrame(tuy.groupby(["States", "Quarter"])["RegisteredUsers"].sum())
    tuyg.reset_index(inplace= True)

    fig_top_plot_1=px.bar(tuyg, x="States", y="RegisteredUsers", color="Quarter", width=1000, height=800, color_discrete_sequence=px.colors.sequential.Cividis_r, hover_name="States", title=f"{year} REGISTERED USERS")
    fig_top_plot_1.show()

    return tuy

#top_user_plot_2
def top_user_plot_2(df, state):
    tuys= df[df["States"]== "state"]
    tuys.reset_index(drop= True, inplace= True)
    tuys

    fig_top_plot_2=px.bar(tuys, x="Quarter", y="RegisteredUsers", title= "REGISTERED USERS, PINCODES, QUARTER", width=1000, height=800, color="RegisteredUsers", hover_data="Pincodes", color_continuous_scale= px.colors.sequential.Magenta_r)
    st.plotly_chart(fig_top_plot_2)

#sql connection
def top_chart_transaction_amount(table_name):
    mydb=psycopg2.connect(host="localhost",user="postgres",port="5432",database="phonepe_data",password="Podafool348")
    cursor=mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(transaction_amount) as transaction_amount 
                from {table_name}
                GROUP BY states
                ORDER BY transaction_amount desc
                limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("States", "transaction_amount"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x= "States", y= "transaction_amount", title= "Top 10 Of TRANSACTION AMOUNT", hover_name="States", color_discrete_sequence= px.colors.sequential.Emrld_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(transaction_amount) as transaction_amount 
                from {table_name}
                GROUP BY states
                ORDER BY transaction_amount
                limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("States", "transaction_amount"))

    with col2:
        fig_amount_2= px.bar(df_2, x= "States", y= "transaction_amount", title= "LAST 10 Of TRANSACTION AMOUNT", hover_name="States", color_discrete_sequence= px.colors.sequential.Emrld_r,height=650, width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''SELECT states, AVG(transaction_amount) as transaction_amount 
                from {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("States", "transaction_amount"))

    fig_amount_3= px.bar(df_3, y= "States", x= "transaction_amount", orientation= "h", title= "AVERAGE OF TRANSACTION AMOUNT", hover_name="States", color_discrete_sequence= px.colors.sequential.Viridis,height=800, width=1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_transaction_count(table_name):
    mydb=psycopg2.connect(host="localhost",user="postgres",port="5432",database="phonepe_data",password="Podafool348")
    cursor=mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(transaction_count) as transaction_count 
                from {table_name}
                GROUP BY states
                ORDER BY transaction_count desc
                limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("States", "transaction_count"))

    col1,col2=st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x= "States", y= "transaction_count", title= "Top 10 Of TRANSACTION COUNT", hover_name="States", color_discrete_sequence= px.colors.sequential.Oranges,height=650, width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(transaction_count) as transaction_count 
                from {table_name}
                GROUP BY states
                ORDER BY transaction_count
                limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("States", "transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x= "States", y= "transaction_count", title= "Last 10 Of TRANSACTION COUNT", hover_name="States", color_discrete_sequence= px.colors.sequential.Oranges_r,height=650, width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''SELECT states, AVG(transaction_count) as transaction_count 
                from {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("States", "transaction_count"))

    fig_amount_3= px.bar(df_3, y= "States", x= "transaction_count", orientation= "h", title= "Average Of TRANSACTION COUNT", hover_name="States", color_discrete_sequence= px.colors.sequential.Viridis,height=800, width=1000)
    st.plotly_chart(fig_amount_3)

def top_chart_registered_user(table_name, state):
    mydb=psycopg2.connect(host="localhost",user="postgres",port="5432",database="phonepe_data",password="Podafool348")
    cursor=mydb.cursor()

    #plot_1
    query1= f'''select districts,SUM(registeredusers) as registereduser
                from {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                order by registereduser desc
                limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("districts", "registereduser"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x= "districts", y= "registereduser", title= "TOP 10 OF REGISTERED USER", hover_name="districts", color_discrete_sequence= px.colors.sequential.Emrld_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select districts,SUM(registeredusers) as registereduser
                from {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                order by registereduser
                limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("districts", "registereduser"))

    with col2:
        fig_amount_2= px.bar(df_2, x= "districts", y= "registereduser", title= "LAST 10 Of REGISTERED USER", hover_name="districts", color_discrete_sequence= px.colors.sequential.Emrld_r,height=650, width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select districts,AVG(registeredusers) as registereduser
                from {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                order by registereduser;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("districts", "registereduser"))

    fig_amount_3= px.bar(df_3, y= "districts", x= "registereduser", orientation= "h", title= "AVERAGE OF REGISTERED USER", hover_name="districts", color_discrete_sequence= px.colors.sequential.Viridis,height=800, width=1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_appopens(table_name, state):
    mydb=psycopg2.connect(host="localhost",user="postgres",port="5432",database="phonepe_data",password="Podafool348")
    cursor=mydb.cursor()

    #plot_1
    query1= f'''select districts,SUM(appopens) as appopens
                from {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                order by appopens desc
                limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("districts", "appopens"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x= "districts", y= "appopens", title= "TOP 10 OF APP OPENS", hover_name="districts", color_discrete_sequence= px.colors.sequential.Emrld_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select districts,SUM(appopens) as appopens
                from {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                order by appopens
                limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("districts", "appopens"))

    with col2:
        fig_amount_2= px.bar(df_2, x= "districts", y= "appopens", title= "LAST 10 Of APP OPENS", hover_name="districts", color_discrete_sequence= px.colors.sequential.Emrld_r,height=650, width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select districts,AVG(appopens) as appopens
                from {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                order by appopens;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("districts", "appopens"))

    fig_amount_3= px.bar(df_3, y= "districts", x= "appopens", orientation= "h", title= "AVERAGE OF APP OPENS", hover_name="districts", color_discrete_sequence= px.colors.sequential.Viridis,height=800, width=1000)
    st.plotly_chart(fig_amount_3)

def top_chart_registered_users(table_name):
    mydb=psycopg2.connect(host="localhost",user="postgres",port="5432",database="phonepe_data",password="Podafool348")
    cursor=mydb.cursor()

    #plot_1
    query1= f'''select states, sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers desc
                limit 10;'''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()

    df_1=pd.DataFrame(table_1, columns=("states", "registeredusers"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x= "states", y= "registeredusers", title= "TOP 10 OF REGISTERED USERS", hover_name="states", color_discrete_sequence= px.colors.sequential.Emrld_r, height=650, width=600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''select states, sum(registeredusers) as registeredusers
                from {table_name}
                group by states
                order by registeredusers
                limit 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()

    df_2=pd.DataFrame(table_2, columns=("states", "registeredusers"))

    with col2:
        fig_amount_2= px.bar(df_2, x= "states", y= "registeredusers", title= "LAST 10 Of REGISTERED USERS", hover_name="states", color_discrete_sequence= px.colors.sequential.Emrld_r,height=650, width=600)
        st.plotly_chart(fig_amount_2)


    #plot_3
    query3= f'''select states, avg(registeredusers) as registeredusers
                from {table_name}
                group by states 
                order by registeredusers desc;'''

    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3=pd.DataFrame(table_3, columns=("states", "registeredusers"))

    fig_amount_3= px.bar(df_3, y= "states", x= "registeredusers", orientation= "h", title= "AVERAGE OF REGISTERED USERS", hover_name="states", color_discrete_sequence= px.colors.sequential.Viridis,height=800, width=1000)
    st.plotly_chart(fig_amount_3)


#streamlit part
st.set_page_config(layout= "wide")
st.title("PHONEPE DATA VISUALISATION AND EXPLORATION")

with st.sidebar:
    
    select=option_menu("Main Menu",["HOME","DATA EXPLORATION","TOP CHARTS"])

if select == "HOME":
    
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open("C:/Users/DIVYA/Downloads/phonepe.jpg"))

    col3,col4= st.columns(2)
    
    with col3:
        st.image(Image.open(r"C:\Users\DIVYA\Downloads\phonepe 2.png"))

    with col4:
        st.write("****Easy Transactions****")
        st.write("****One App For All Your Payments****")
        st.write("****Your Bank Account Is All You Need****")
        st.write("****Multiple Payment Modes****")
        st.write("****PhonePe Merchants****")
        st.write("****Multiple Ways To Pay****")
        st.write("****1.Direct Transfer & More****")
        st.write("****2.QR Code****")
        st.write("****Earn Great Rewards****")

    col5,col6= st.columns(2)

    with col5:
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.markdown(" ")
        st.write("****No Wallet Top-Up Required****")
        st.write("****Pay Directly From Any Bank To Any Bank A/C****")
        st.write("****Instantly & Free****")

    with col6:
        st.image(Image.open(r"C:\Users\DIVYA\Downloads\phonepe 3.jpg"))


elif select == "DATA EXPLORATION":

    tab1, tab2, tab3 = st.tabs(["Aggregated Analysis", "Map Analysis", "Top Analysis"])

    with tab1:

        method_1=st.radio("Select The Method",["Transaction Analysis","User Analysis"])
        
        if method_1 == "Transaction Analysis":
            
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select The Year",Aggre_transaction["Years"].min(),Aggre_transaction["Years"].max(),Aggre_transaction["Years"].min())
            tac_Y= Transaction_amount_count_Y(Aggre_transaction, years)

            col1,col2= st.columns(2)
            
            with col1:
                quarters= st.slider("Select The Quarter",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Transaction_amount_count_Y_Q(tac_Y, quarters)
            
            with col1:
                states= st.selectbox ("Selelct the State",tac_Y["States"].unique() )
            
            Aggre_Tran_Transaction_Type(tac_Y, states)

            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("Select The Quarter_ty",tac_Y["Quarter"].min(),tac_Y["Quarter"].max(),tac_Y["Quarter"].min())
            Aggre_tran_tac_Y_Q=Transaction_amount_count_Y_Q(tac_Y, quarters)
            
            col1,col2= st.columns(2)
            with col1:
                states=st.selectbox("Select The State_ty",Aggre_tran_tac_Y_Q["States"].unique())

            Aggre_Tran_Transaction_Type(Aggre_tran_tac_Y_Q, states)     
    

        elif method_1 == "User Analysis":
            
            col1,col2= st.columns(2)            
            with col1:
                years= st.slider("Select The Year",Aggre_USER["Years"].min(),Aggre_USER["Years"].max(),Aggre_USER["Years"].min())
            Aggre_USER_Y= Aggre_user_plot_1(Aggre_USER, years)
 
            col1,col2= st.columns(2)           
            with col1:
                
                quarters= st.slider("Select The Quarter",Aggre_USER_Y["Quarter"].min(),Aggre_USER_Y["Quarter"].max(),Aggre_USER_Y["Quarter"].min())
            Aggre_USER_Y_Q= Aggre_user_plot_2(Aggre_USER_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states=st.selectbox("Select The State_ty",Aggre_USER_Y_Q["States"].unique())

            Aggre_user_plot_3(Aggre_USER_Y_Q, states)     

        
    with tab2:

        method_2= st.radio("Select The Method",["Map Transaction","Map User "])

        if method_2 == "Map Transaction":
            
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select The Year_mt",Map_tran["Years"].min(),Map_tran["Years"].max(),Map_tran["Years"].min())
            Map_tran_tac_Y= Transaction_amount_count_Y(Map_tran, years)

            col1,col2= st.columns(2)           
            with col1:
                states= st.selectbox ("Selelct the State_mi",Map_tran_tac_Y["States"].unique() )
            
            Map_Tran_Districts_Type(Map_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("Select The Quarter_ti",Map_tran_tac_Y["Quarter"].min(),Map_tran_tac_Y["Quarter"].max(),Map_tran_tac_Y["Quarter"].min())
            Map_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Map_tran_tac_Y, quarters)

            col1,col2= st.columns(2)
            with col1:
                states=st.selectbox("Select The State_tt",Map_tran_tac_Y_Q["States"].unique())

            Map_Tran_Districts_Type(Map_tran_tac_Y_Q, states)   

        elif method_2 == "Map User":
            
            col1,col2= st.columns(2)
            
            with col1:
                
                years= st.slider("Select The Year_mu",Map_user["Years"].min(),Map_user["Years"].max(),Map_user["Years"].min())
            map_user_Y= map_user_plot_1(Map_user, years)

            col1,col2= st.columns(2)
            
            with col1:
                quarters= st.slider("Select The Quarter_mu",map_user_Y["Quarter"].min(),map_user_Y["Quarter"].max(),map_user_Y["Quarter"].min())
            Map_User_Y_Q= map_user_plot_2(map_user_Y, quarters)
            
            col1,col2= st.columns(2)
            with col1:
                states=st.selectbox("Select The State_mu",Map_User_Y_Q["States"].unique())

            map_user_plot_3(Map_User_Y_Q, states)

    with tab3:

        method_3= st.radio("Select The Method",["Top Transaction","Top User "])

        if method_3 == "Top Transaction":
            col1,col2= st.columns(2)
            with col1:
                years= st.slider("Select The Year",Top_tran["Years"].min(),Top_tran["Years"].max(),Top_tran["Years"].min())
            Top_tran_tac_Y= Transaction_amount_count_Y(Top_tran, years)

            col1,col2= st.columns(2)
            with col1:
                states=st.selectbox("Select The State_xu",Top_tran_tac_Y["States"].unique())

            top_transaction_plot_1(Top_tran_tac_Y, states)

            col1,col2= st.columns(2)
            with col1:
                quarters= st.slider("Select The Quarter_tz",Top_tran_tac_Y["Quarter"].min(),Top_tran_tac_Y["Quarter"].max(),Top_tran_tac_Y["Quarter"].min())
            Top_tran_tac_Y_Q=Transaction_amount_count_Y_Q(Top_tran_tac_Y, quarters)


        elif method_3 == "Top User":
            
            col1,col2= st.columns(2)
            with col1:
                
                years= st.slider("Select The Year_yh",Top_user["Years"].min(),Top_user["Years"].max(),Top_user["Years"].min())
            Top_user_Y= top_user_plot_1(Top_user, years)            

            col1,col2= st.columns(2)
            with col1:
                states=st.selectbox("Select The State_oj",Top_user["States"].unique())
                top_user_plot_2(Top_user, states)


elif select == "TOP CHARTS":
    
    question= st.selectbox("Select the Question",["1. Transaction Amount and Count of Transaction Analysis",
                                                  "2. Transaction Amount and Count of Map Transaction",
                                                  "3. Transaction Amount and Count of Top Transaction",
                                                  "4. Transaction Amount and Count of User Analyisis",
                                                  "5. Transaction Amount and Count of Map User",
                                                  "6. Transaction Amount and Count of Top User",
                                                  "7. Transaction Count of Aggregated User",
                                                  "8. Registered users of Map User",
                                                  "9. App Opens Of Map User",
                                                  "10. Registered users of Top User",
                                                  ])
    
    if question == "1. Transaction Amount and Count of Transaction Analysis":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount ("aggre_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count ("aggre_transaction")

    elif question == "2. Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount ("map_tran")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count ("map_tran")   

    elif question == "3. Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount ("top_tran")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count ("top_tran")   

    elif question == "4. Transaction Amount and Count of User Analyisis":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount ("aggre_transaction")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count ("aggre_transaction") 

    elif question == "5. Transaction Amount and Count of Map User":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount ("Map_tran")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count ("Map_user")

    elif question == "6. Transaction Amount and Count of Top User":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount ("Top_tran")
        
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count ("Top_user") 

    elif question == "7. Transaction Count of Aggregated User":
             
        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count ("Aggre_USER")     

    elif question == "8. Registered users of Map User":
             
        states =st.selectbox("Select The State",Map_user["States"].unique())
        st.subheader("REGISTERED USERS")
        top_chart_registered_user ("Map_user", states)
    
    elif question == "9. App Opens Of Map User":
             
        states =st.selectbox("Select The State",Map_user["States"].unique())
        st.subheader("APPOPENS")
        top_chart_appopens ("Map_user", states)

    elif question == "10. Registered users of Top User":
             
        st.subheader("REGISTERED USERS")
        top_chart_registered_users ("Top_user")
