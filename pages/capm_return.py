##importing libraries

import streamlit as st
import pandas as pd
import yfinance as yf  # Removed because it is not used
import datetime
from pages import capm_functions


st.set_page_config(page_title="CAPM", page_icon="chart_with_upwards_trend", layout="wide") ##setting page configuration

st.title("Capital Asset Pricing Model (CAPM) Calculator") ##setting title of the page

#getting  user input
col1,col2=st.columns([1,1])
with col1:
    stock_list=st.multiselect("Choose 4 stocks", ('TSLA', 'AAPL','NFLX','MSFT','GOOGL','AMZN','META','NVDA'), default=['TSLA', 'AAPL','NFLX','MSFT'])
with col2:
    year=st.number_input("Number of years",1,10)
    
#downloading data for SP500
try:
    end=datetime.date.today()
    start = datetime.date(datetime.date.today().year-year,datetime.date.today().month,datetime.date.today().day)
    SP500 = yf.download('^GSPC', start=start, end=end) #Yahoo Finance shut down their old API that pandas_datareader tries to use.
    stocks_df=pd.DataFrame()

    # print(f"Start date: {start}")
    # print(f"End date: {end}")  


    for stock in stock_list:
        data=yf.download(stock,period=f'{year}y') ##kitne year ke liye chahiye
        stocks_df[f'{stock}']= data['Close']
        
    stocks_df.reset_index(inplace=True)
    SP500=SP500[['Close']].reset_index()
    SP500.columns=['Date','sp500']

    stocks_df['Date']= stocks_df['Date'].astype('datetime64[ns]')
    stocks_df['Date']= stocks_df['Date'].apply(lambda x:str(x)[:10])
    stocks_df['Date']=pd.to_datetime(stocks_df['Date'])

    # Merge on the 'Date' column
    stocks_df = pd.merge(stocks_df, SP500, on='Date', how='inner')

    col1,col2=st.columns([1,1])
    with col1:
        st.markdown(["##Dataframe head"])
        st.dataframe(stocks_df.head(),use_container_width=True)
    with col2:
        st.markdown(["##Dataframe tail"])
        st.dataframe(stocks_df.tail(),use_container_width=True)

    col1,col2=st.columns([1,1])
    with col1:
        st.markdown('Price of all the Stocks')
        st.plotly_chart(capm_functions.interactive_plot(stocks_df))
    with col2:
        st.markdown('Price of all the Stocks after normalization')
        st.plotly_chart(capm_functions.interactive_plot(capm_functions.normalize(stocks_df)))

    stocks_daily_return = capm_functions.daily_return(stocks_df)
    print(stocks_daily_return.head())  

    beta={}
    alpha={}

    for i in stocks_daily_return.columns:
        if i !='Date' and i!= 'sp500':
            b,a = capm_functions.calculate_beta(stocks_daily_return,i)

            beta[i]=b
            alpha[i]=a
    print(beta,alpha)

    beta_df=pd.DataFrame(columns= ['Stock','Beta Value'])
    beta_df['Stock']=beta.keys()
    beta_df['Beta Value']= [str(round(i,2)) for i in beta.values()]

    with col1:
        st.markdown('Calculate Beta Value')
        st.dataframe(beta_df,use_container_width=True)

    rf=0
    rm=stocks_daily_return['sp500'].mean()*252

    return_df=pd.DataFrame()
    return_value=[]
    for stock,value in beta.items():
        return_value.append(str(round(rf+(value*(rm-rf)),2)))
    return_df['Stock']= stock_list

    return_df['Return Value'] = return_value

    with col2:
        st.markdown('Calculate Return using CAPM')
        st.dataframe(return_df,use_container_width=True )
except:
    st.write("Please select valid input")
