# -*- coding: utf-8 -*-
"""
Created on Thu Sep  7 23:29:13 2023

@author: user
"""
import pandas as pd
import streamlit as st
import numpy as np
import yfinance as yf
import requests
from bs4 import BeautifulSoup
import plotly.graph_objects as go
from Gann import Gann
from tradingview_ta import TA_Handler, Interval

def underline_text(text):
    return f"<u>{text}</u>"

def format_dataframe_with_2_decimals(dataframe):
    return dataframe.style.format("{:.2f}")
# Set pandas display option to 2 decimals
pd.set_option('display.float_format', '{:.2f}'.format)

st. set_page_config(layout="wide")

st.header("Stocks - Analytics")

if 'clicked' not in st.session_state:
    st.session_state.clicked = False

def click_button():
    st.session_state.clicked = False
    
padding_top = 0
padding_bottom = 10
padding_left = 1
padding_right = 10

st.markdown(f'''
            <style>
                .reportview-container .sidebar-content {{
                    padding-top: {padding_top}rem;
                }}
                .reportview-container .main .block-container {{
                    padding-top: {padding_top}rem;
                    padding-right: {padding_right}rem;
                    padding-left: {padding_left}rem;
                    padding-bottom: {padding_bottom}rem;
                }}
                
            </style>
            ''', unsafe_allow_html=True,
)

st.markdown("""
<style>

	.stTabs [data-baseweb="tab-list"] {
		gap: 8px;
    }

	.stTabs [data-baseweb="tab"] {
		height: 50px;
		background-color: #F0F2F6;
		border-radius: 4px 4px 0px 0px;
		gap: 5px;
		padding-top: 10px;
		padding-bottom: 10px;
    }

	.stTabs [aria-selected="true"] {
  		background-color: #F0F2F6;
	}

</style>
<style>
    .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {
    font-size:26px;
    color:Blue;
    }
</style>
""", unsafe_allow_html=True)

listTabs = ["Nifty Indices", "Stocks based on Category","Stock Analysis"]
whitespace = 9
col1, col2, col3 = st.tabs([s.center(whitespace,"\u2001") for s in listTabs])

with col1:
 
    def main():
        
        Index_df = pd.read_excel("Nifty_Index_List_V1.xlsx",sheet_name = 'UniqueIndices',engine = 'openpyxl')
        
        st.title("Nifty Index Analysis")
    
        Indices = list(Index_df['Indices'].unique())
        selected_Index = st.selectbox("Select an Index ", Indices )
        Symbol = Index_df[Index_df.Indices == selected_Index]['YahooIndex'].unique().tolist()
        st.write("Selected option:", selected_Index)
        
        Symbol= '^CNX100'
        
        if st.button('Submit Index', on_click=click_button):
            symbol = Symbol
            ticker = yf.Ticker(symbol)
            todays_data = ticker.history(period='1d')
            Close = todays_data['Close'][0]
            st.write("Last close price is:", np.round(Close,2))
    
    
            st.write(underline_text("6 Months Graph:"), unsafe_allow_html=True)
            
            df = ticker.history(period='6mo')
            df['Date'] = pd.to_datetime( df.index)
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            df = df[['Open', 'High', 'Low', 'Close', 'Volume','Date']].reset_index(drop = True)
            df['direction'] = df[['Open', 'Close']].apply(lambda x: 'Decreasing' if x.Open>x.Close else 'Increasing',axis = 1 )
            
            if not df.empty:
                # Plot candlestick chart
                fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                                      open=df['Open'],
                                                      high=df['High'],
                                                      low=df['Low'],
                                                      close=df['Close'])])
                fig.update_layout(
                width=1000,
                height=1000            )
                    
                #st.plotly_chart(fig, use_container_width=True)
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.write("No data available for the selected period.")
                
            Buy_At,Sell_At,Buy_Target1, Buy_Target2, Buy_Target3, Buy_Target4,Sell_target1, Sell_target2, Sell_target3, Sell_target4,Resistance1, Resistance2, Resistance3, Resistance4, Resistance5,Support1, Support2, Support3, Support4,Support5 = Gann(Close)    
            
            buy_above = Buy_At
            buy_targets = [Buy_Target1, Buy_Target2, Buy_Target3, Buy_Target4]
            buy_stoploss = Sell_At
            
            sell_below = Sell_At
            sell_targets = [Sell_target1, Sell_target2, Sell_target3, Sell_target4]
            sell_stoploss = Buy_At
        
            st.write(underline_text("Recommendation:"), unsafe_allow_html=True)
            
            message = f"Buy at / above: {buy_above}\nTargets: {', '.join(map(str, buy_targets))} \n\n STOPLOSS: {buy_stoploss}\n\nSell at / below: {sell_below}\nTargets: {', '.join(map(str, sell_targets))} \n\n STOPLOSS: {sell_stoploss}\n\n"
            st.write(message)
        
            st.write(underline_text("Resistance/Support Levels:"), unsafe_allow_html=True)
            
            Resistance_targets = [Resistance1, Resistance2, Resistance3, Resistance4, Resistance5]
            Support_targets = [Support1, Support2, Support3, Support4,Support5]
            
            df = pd.DataFrame([Resistance_targets,Support_targets]).T
            df.columns = ['Resistance','Support'] 
            df.index = [1,2,3,4,5]
            df=df.round(decimals = 2)
        
            st.table(format_dataframe_with_2_decimals(df)) 
            #selected_Index = 'NIFTY 100'
            MC_Symbol = Index_df[Index_df.Indices == selected_Index]['MoneyControlIndices'].unique().tolist()[0]
            
            r = requests.get('https://www.moneycontrol.com/indian-indices/'+MC_Symbol+'.html')
            
    
            soup = BeautifulSoup(r.content, 'html.parser')
            s = soup.find('div', id ='indi_contribute')
            s1 = s.find('div', class_='contribut_bx')
            content = s1.find_all('td')
    
            i = 1 
            List = []
            for row in content:
                List.append(row.text)
                i = i+1   
                
            UP_Stocks = pd.DataFrame([List[x:x+3] for x in range(0, len(List),3)] ,columns = ['Stock Name','CMP',
                                                                                  'Contribution Points'])
            UP_Stocks.set_index(['Stock Name'],drop = True,inplace = True)  
            
    
            s2 = s.find('div', class_='contribut_bx FR')
            content1 = s2.find_all('td')
             
            List1 = []
            i = 1
            for row in content1:
                List1.append(row.text)
                i = i+1   
                
            Down_Stocks = pd.DataFrame([List1[x:x+3] for x in range(0, len(List1),3)] ,columns = ['Stock Name','CMP',
                                                                                  'Contribution Points'])
            Down_Stocks.set_index(['Stock Name'],drop = True,inplace = True)  
            
            col1, col2 = st.columns(2)
    
            with col1:
                # Display first result
                st.write(underline_text("Top Up Stocks:"), unsafe_allow_html=True)
                st.write(UP_Stocks)
            
            with col2:
                # Display second result
                st.write(underline_text("Top Down Stocks:"), unsafe_allow_html=True)
                st.write(Down_Stocks)
                
            s = soup.find('div', id ='indi_component')
            s1 = s.find('div', class_='table-responsive')
            content = s1.find_all('td')
            
            List1 = []
            i = 1
            for row in content:
                List1.append(row.text)
                i = i+1   
                
                
            Components = pd.DataFrame([List1[x:x+6] for x in range(0, len(List1),6)] ,columns = ['Company Name','Sector','CMP',
                                                                                  'Change(chg%)','Volume','Techincal Rating'])              
            Components.set_index(['Company Name'],drop = True,inplace = True) 
            
            st.write(underline_text("Components:"), unsafe_allow_html=True)
            st.write(Components)
            
    if __name__ == "__main__":
        main()    
        
with col2:        
    def main():
        Final_df1 = pd.DataFrame(columns = ['Symbol','Moving Averages','Oscillators','Final Recommendation','Interval'])
        Final_df = pd.DataFrame(columns = ['Symbol','Moving Averages','Oscillators','Final Recommendation','Interval'])
        
        Index_df = pd.read_excel("MC_General_Categories_Indices.xlsx",engine = 'openpyxl')
        
        st.title("Stock Analysis based on Category")
        #components = pd.read_html('https://en.wikipedia.org/wiki/NIFTY_500')[2]
        #components.columns = components.iloc[0]
        #components = pd.DataFrame(Index_df['Symbol'])
        
        #options = list(components['Symbol'])
        #remove_indices = [51,280,299,300,337,474]
        #options =  [options[i] for i in range(len(options)) if i not in remove_indices] 
        
        Indices = list(Index_df['Category'].unique())
        selected_Index = st.selectbox("Select an Index ", Indices )
        Stocks = Index_df[Index_df.Category == selected_Index]['Symbol'].unique().tolist()
        selected_Stocks = st.selectbox("Select an Stock ", Stocks )
        StockName = Index_df[(Index_df.Symbol == selected_Stocks) &
                             (Index_df.Category == selected_Index)]['Stock Name'].tolist()[0]
    
        st.write("Selected Stock:", StockName)
        
        url = "https://www.screener.in/company/"+selected_Stocks
        r = requests.get(url)
    
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find('section', id ='analysis')
    
        s1 = s.find('div', class_='pros')
        content = s1.find_all('li')   
        s2 = s.find('div', class_='cons')
        content1 = s2.find_all('li')
         
        Pros = []
        for row in content:
            Pros.append(row.text.strip())
        
        Cons = []
        for row in content1:
            Cons.append(row.text.strip())
    
        df_swot = pd.DataFrame([Pros,Cons]).T
        df_swot.columns = ['Pros','Cons']
        df_swot = df_swot.reset_index(drop = True) 
    
         
        tesla = TA_Handler(
            symbol=selected_Stocks,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_DAY
        )
        recommend = tesla.get_analysis()    
        
        Indicators = pd.DataFrame(recommend.indicators.items()).T
        Indicators.columns = Indicators.iloc[0]
        Indicators = Indicators.tail(1)
        Indicators['Exchange'] = recommend.exchange
        Indicators['MA Rec'] = recommend.moving_averages["RECOMMENDATION"]
        Indicators['Ocs Rec'] = recommend.oscillators["RECOMMENDATION"]        
        temp = pd.DataFrame(recommend.moving_averages["COMPUTE"].items()).T
        temp.columns = temp.iloc[0]
        temp = temp.tail(1)  
        Indicators1 = pd.concat([Indicators,temp ], axis = 1)
    
        temp = pd.DataFrame(recommend.oscillators["COMPUTE"].items()).T
        temp.columns = temp.iloc[0]
        temp = temp.tail(1)  
        Indicators2 = pd.concat([Indicators1,temp ], axis = 1)        
        
        Indicators2['Tech Summ Rec'] = recommend.summary["RECOMMENDATION"]
        Indicators2['Symbol'] = recommend.symbol   
        
        Final_df['Symbol'] = [Indicators2['Symbol'].values[0]]
        Final_df['Moving Averages'] = [Indicators2['MA Rec'].values[0]]
        Final_df['Oscillators'] = [Indicators2['Ocs Rec'].values[0]]
        Final_df['Final Recommendation'] = [Indicators2['Tech Summ Rec'].values[0]]
        Final_df['Interval'] = ['1 Day']
        Final_df1 = pd.concat([Final_df1,Final_df ], axis = 0) 
    
        tesla = TA_Handler(
            symbol=selected_Stocks,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_WEEK
        )
        recommend = tesla.get_analysis()    
        
        Indicators = pd.DataFrame(recommend.indicators.items()).T
        Indicators.columns = Indicators.iloc[0]
        Indicators = Indicators.tail(1)
        Indicators['Exchange'] = recommend.exchange
        Indicators['MA Rec'] = recommend.moving_averages["RECOMMENDATION"]
        Indicators['Ocs Rec'] = recommend.oscillators["RECOMMENDATION"]        
        temp = pd.DataFrame(recommend.moving_averages["COMPUTE"].items()).T
        temp.columns = temp.iloc[0]
        temp = temp.tail(1)  
        Indicators1 = pd.concat([Indicators,temp ], axis = 1)
    
        temp = pd.DataFrame(recommend.oscillators["COMPUTE"].items()).T
        temp.columns = temp.iloc[0]
        temp = temp.tail(1)  
        Indicators2 = pd.concat([Indicators1,temp ], axis = 1)        
        
        Indicators2['Tech Summ Rec'] = recommend.summary["RECOMMENDATION"]
        Indicators2['Symbol'] = recommend.symbol   
        
        Final_df['Symbol'] = [Indicators2['Symbol'].values[0]]
        Final_df['Moving Averages'] = [Indicators2['MA Rec'].values[0]]
        Final_df['Oscillators'] = [Indicators2['Ocs Rec'].values[0]]
        Final_df['Final Recommendation'] = [Indicators2['Tech Summ Rec'].values[0]]
        Final_df['Interval'] = ['1 WEEK']
        Final_df1 = pd.concat([Final_df1,Final_df ], axis = 0)     
        
        tesla = TA_Handler(
            symbol=selected_Stocks,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_MONTH
        )
        recommend = tesla.get_analysis()    
        
        Indicators = pd.DataFrame(recommend.indicators.items()).T
        Indicators.columns = Indicators.iloc[0]
        Indicators = Indicators.tail(1)
        Indicators['Exchange'] = recommend.exchange
        Indicators['MA Rec'] = recommend.moving_averages["RECOMMENDATION"]
        Indicators['Ocs Rec'] = recommend.oscillators["RECOMMENDATION"]        
        temp = pd.DataFrame(recommend.moving_averages["COMPUTE"].items()).T
        temp.columns = temp.iloc[0]
        temp = temp.tail(1)  
        Indicators1 = pd.concat([Indicators,temp ], axis = 1)
    
        temp = pd.DataFrame(recommend.oscillators["COMPUTE"].items()).T
        temp.columns = temp.iloc[0]
        temp = temp.tail(1)  
        Indicators2 = pd.concat([Indicators1,temp ], axis = 1)        
        
        Indicators2['Tech Summ Rec'] = recommend.summary["RECOMMENDATION"]
        Indicators2['Symbol'] = recommend.symbol   
        
        Final_df['Symbol'] = [Indicators2['Symbol'].values[0]]
        Final_df['Moving Averages'] = [Indicators2['MA Rec'].values[0]]
        Final_df['Oscillators'] = [Indicators2['Ocs Rec'].values[0]]
        Final_df['Final Recommendation'] = [Indicators2['Tech Summ Rec'].values[0]]
        Final_df['Interval'] = ['1 MONTH']
        Final_df1 = pd.concat([Final_df1,Final_df ], axis = 0)     
    
        Final_df1.set_index('Interval',inplace=True)    
    
        if st.button('Submit Stock', on_click=click_button):
            symbol = selected_Stocks+'.NS'
            ticker = yf.Ticker(symbol)
            todays_data = ticker.history(period='1d')
            Close = todays_data['Close'][0]
            st.write("Last close price is:", np.round(Close,2))
    
            #Time_Span =  ['5d', '1mo', '3mo', '6mo', '1y']
            #selected_span = st.selectbox("Graph ", Time_Span ) 
            #st.write("Selected Span is :", selected_span)
            st.write(underline_text("6 Months Graph:"), unsafe_allow_html=True)
            
            df = ticker.history(period='6mo')
            df['Date'] = pd.to_datetime( df.index)
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            df = df[['Open', 'High', 'Low', 'Close', 'Volume','Date']].reset_index(drop = True)
            df['direction'] = df[['Open', 'Close']].apply(lambda x: 'Decreasing' if x.Open>x.Close else 'Increasing',axis = 1 )
            
            if not df.empty:
                # Plot candlestick chart
                fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                                      open=df['Open'],
                                                      high=df['High'],
                                                      low=df['Low'],
                                                      close=df['Close'])])
                fig.update_layout(
                width=1000,
                height=1000            )
                    
                #st.plotly_chart(fig, use_container_width=True)
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.write("No data available for the selected period.")
                
            Buy_At,Sell_At,Buy_Target1, Buy_Target2, Buy_Target3, Buy_Target4,Sell_target1, Sell_target2, Sell_target3, Sell_target4,Resistance1, Resistance2, Resistance3, Resistance4, Resistance5,Support1, Support2, Support3, Support4,Support5 = Gann(Close)    
            
            buy_above = Buy_At
            buy_targets = [Buy_Target1, Buy_Target2, Buy_Target3, Buy_Target4]
            buy_stoploss = Sell_At
            
            sell_below = Sell_At
            sell_targets = [Sell_target1, Sell_target2, Sell_target3, Sell_target4]
            sell_stoploss = Buy_At
        
            st.write(underline_text("Recommendation:"), unsafe_allow_html=True)
            
            message = f"Buy at / above: {buy_above}\nTargets: {', '.join(map(str, buy_targets))} \n\n STOPLOSS: {buy_stoploss}\n\nSell at / below: {sell_below}\nTargets: {', '.join(map(str, sell_targets))} \n\n STOPLOSS: {sell_stoploss}\n\n"
            st.write(message)
        
            st.write(underline_text("Resistance/Support Levels:"), unsafe_allow_html=True)
            
            Resistance_targets = [Resistance1, Resistance2, Resistance3, Resistance4, Resistance5]
            Support_targets = [Support1, Support2, Support3, Support4,Support5]
            
            df = pd.DataFrame([Resistance_targets,Support_targets]).T
            df.columns = ['Resistance','Support'] 
            df.index = [1,2,3,4,5]
            df=df.round(decimals = 2)
        
            st.table(format_dataframe_with_2_decimals(df))  
            st.write(underline_text("Technical Analysis:"), unsafe_allow_html=True)        
            st.table(Final_df1)
            st.write(underline_text("Pros & Cons:"), unsafe_allow_html=True)        
            st.table(df_swot)
    if __name__ == "__main__":
        main()              

with col3:    
    
    def main():
        Final_df1 = pd.DataFrame(columns = ['Symbol','Moving Averages','Oscillators','Final Recommendation','Interval'])
        Final_df = pd.DataFrame(columns = ['Symbol','Moving Averages','Oscillators','Final Recommendation','Interval'])
        
        Index_df = pd.read_excel("MC_General_Categories_Indices.xlsx",engine = 'openpyxl')
        
        st.title("Stock Analysis")
        
        Stocks = Index_df['Symbol'].unique().tolist()
        selected_Stocks = st.selectbox("Select an Stock ", Stocks )
        StockName = Index_df[(Index_df.Symbol == selected_Stocks)]['Stock Name'].tolist()[0]
    
        st.write("Selected Stock:", StockName)
        
        url = "https://www.screener.in/company/"+selected_Stocks
        r = requests.get(url)
    
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find('section', id ='analysis')
    
        s1 = s.find('div', class_='pros')
        content = s1.find_all('li')   
        s2 = s.find('div', class_='cons')
        content1 = s2.find_all('li')
         
        Pros = []
        for row in content:
            Pros.append(row.text.strip())
        
        Cons = []
        for row in content1:
            Cons.append(row.text.strip())
    
        df_swot = pd.DataFrame([Pros,Cons]).T
        df_swot.columns = ['Pros','Cons']
        df_swot = df_swot.reset_index(drop = True) 
    
         
        tesla = TA_Handler(
            symbol=selected_Stocks,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_DAY
        )
        recommend = tesla.get_analysis()    
        
        Indicators = pd.DataFrame(recommend.indicators.items()).T
        Indicators.columns = Indicators.iloc[0]
        Indicators = Indicators.tail(1)
        Indicators['Exchange'] = recommend.exchange
        Indicators['MA Rec'] = recommend.moving_averages["RECOMMENDATION"]
        Indicators['Ocs Rec'] = recommend.oscillators["RECOMMENDATION"]        
        temp = pd.DataFrame(recommend.moving_averages["COMPUTE"].items()).T
        temp.columns = temp.iloc[0]
        temp = temp.tail(1)  
        Indicators1 = pd.concat([Indicators,temp ], axis = 1)
    
        temp = pd.DataFrame(recommend.oscillators["COMPUTE"].items()).T
        temp.columns = temp.iloc[0]
        temp = temp.tail(1)  
        Indicators2 = pd.concat([Indicators1,temp ], axis = 1)        
        
        Indicators2['Tech Summ Rec'] = recommend.summary["RECOMMENDATION"]
        Indicators2['Symbol'] = recommend.symbol   
        
        Final_df['Symbol'] = [Indicators2['Symbol'].values[0]]
        Final_df['Moving Averages'] = [Indicators2['MA Rec'].values[0]]
        Final_df['Oscillators'] = [Indicators2['Ocs Rec'].values[0]]
        Final_df['Final Recommendation'] = [Indicators2['Tech Summ Rec'].values[0]]
        Final_df['Interval'] = ['1 Day']
        Final_df1 = pd.concat([Final_df1,Final_df ], axis = 0) 
    
        tesla = TA_Handler(
            symbol=selected_Stocks,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_WEEK
        )
        recommend = tesla.get_analysis()    
        
        Indicators = pd.DataFrame(recommend.indicators.items()).T
        Indicators.columns = Indicators.iloc[0]
        Indicators = Indicators.tail(1)
        Indicators['Exchange'] = recommend.exchange
        Indicators['MA Rec'] = recommend.moving_averages["RECOMMENDATION"]
        Indicators['Ocs Rec'] = recommend.oscillators["RECOMMENDATION"]        
        temp = pd.DataFrame(recommend.moving_averages["COMPUTE"].items()).T
        temp.columns = temp.iloc[0]
        temp = temp.tail(1)  
        Indicators1 = pd.concat([Indicators,temp ], axis = 1)
    
        temp = pd.DataFrame(recommend.oscillators["COMPUTE"].items()).T
        temp.columns = temp.iloc[0]
        temp = temp.tail(1)  
        Indicators2 = pd.concat([Indicators1,temp ], axis = 1)        
        
        Indicators2['Tech Summ Rec'] = recommend.summary["RECOMMENDATION"]
        Indicators2['Symbol'] = recommend.symbol   
        
        Final_df['Symbol'] = [Indicators2['Symbol'].values[0]]
        Final_df['Moving Averages'] = [Indicators2['MA Rec'].values[0]]
        Final_df['Oscillators'] = [Indicators2['Ocs Rec'].values[0]]
        Final_df['Final Recommendation'] = [Indicators2['Tech Summ Rec'].values[0]]
        Final_df['Interval'] = ['1 WEEK']
        Final_df1 = pd.concat([Final_df1,Final_df ], axis = 0)     
        
        tesla = TA_Handler(
            symbol=selected_Stocks,
            screener="india",
            exchange="NSE",
            interval=Interval.INTERVAL_1_MONTH
        )
        recommend = tesla.get_analysis()    
        
        Indicators = pd.DataFrame(recommend.indicators.items()).T
        Indicators.columns = Indicators.iloc[0]
        Indicators = Indicators.tail(1)
        Indicators['Exchange'] = recommend.exchange
        Indicators['MA Rec'] = recommend.moving_averages["RECOMMENDATION"]
        Indicators['Ocs Rec'] = recommend.oscillators["RECOMMENDATION"]        
        temp = pd.DataFrame(recommend.moving_averages["COMPUTE"].items()).T
        temp.columns = temp.iloc[0]
        temp = temp.tail(1)  
        Indicators1 = pd.concat([Indicators,temp ], axis = 1)
    
        temp = pd.DataFrame(recommend.oscillators["COMPUTE"].items()).T
        temp.columns = temp.iloc[0]
        temp = temp.tail(1)  
        Indicators2 = pd.concat([Indicators1,temp ], axis = 1)        
        
        Indicators2['Tech Summ Rec'] = recommend.summary["RECOMMENDATION"]
        Indicators2['Symbol'] = recommend.symbol   
        
        Final_df['Symbol'] = [Indicators2['Symbol'].values[0]]
        Final_df['Moving Averages'] = [Indicators2['MA Rec'].values[0]]
        Final_df['Oscillators'] = [Indicators2['Ocs Rec'].values[0]]
        Final_df['Final Recommendation'] = [Indicators2['Tech Summ Rec'].values[0]]
        Final_df['Interval'] = ['1 MONTH']
        Final_df1 = pd.concat([Final_df1,Final_df ], axis = 0)     
    
        Final_df1.set_index('Interval',inplace=True)    
    
        if st.button('Submit', on_click=click_button):
            symbol = selected_Stocks+'.NS'
            ticker = yf.Ticker(symbol)
            todays_data = ticker.history(period='1d')
            Close = todays_data['Close'][0]
            st.write("Last close price is:", np.round(Close,2))
    
            #Time_Span =  ['5d', '1mo', '3mo', '6mo', '1y']
            #selected_span = st.selectbox("Graph ", Time_Span ) 
            #st.write("Selected Span is :", selected_span)
            st.write(underline_text("6 Months Graph:"), unsafe_allow_html=True)
            
            df = ticker.history(period='6mo')
            df['Date'] = pd.to_datetime( df.index)
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            df = df[['Open', 'High', 'Low', 'Close', 'Volume','Date']].reset_index(drop = True)
            df['direction'] = df[['Open', 'Close']].apply(lambda x: 'Decreasing' if x.Open>x.Close else 'Increasing',axis = 1 )
            
            if not df.empty:
                # Plot candlestick chart
                fig = go.Figure(data=[go.Candlestick(x=df['Date'],
                                                      open=df['Open'],
                                                      high=df['High'],
                                                      low=df['Low'],
                                                      close=df['Close'])])
                fig.update_layout(
                width=1000,
                height=1000            )
                    
                #st.plotly_chart(fig, use_container_width=True)
                st.plotly_chart(fig,use_container_width=True)
            else:
                st.write("No data available for the selected period.")
                
            Buy_At,Sell_At,Buy_Target1, Buy_Target2, Buy_Target3, Buy_Target4,Sell_target1, Sell_target2, Sell_target3, Sell_target4,Resistance1, Resistance2, Resistance3, Resistance4, Resistance5,Support1, Support2, Support3, Support4,Support5 = Gann(Close)    
            
            buy_above = Buy_At
            buy_targets = [Buy_Target1, Buy_Target2, Buy_Target3, Buy_Target4]
            buy_stoploss = Sell_At
            
            sell_below = Sell_At
            sell_targets = [Sell_target1, Sell_target2, Sell_target3, Sell_target4]
            sell_stoploss = Buy_At
        
            st.write(underline_text("Recommendation:"), unsafe_allow_html=True)
            
            message = f"Buy at / above: {buy_above}\nTargets: {', '.join(map(str, buy_targets))} \n\n STOPLOSS: {buy_stoploss}\n\nSell at / below: {sell_below}\nTargets: {', '.join(map(str, sell_targets))} \n\n STOPLOSS: {sell_stoploss}\n\n"
            st.write(message)
        
            st.write(underline_text("Resistance/Support Levels:"), unsafe_allow_html=True)
            
            Resistance_targets = [Resistance1, Resistance2, Resistance3, Resistance4, Resistance5]
            Support_targets = [Support1, Support2, Support3, Support4,Support5]
            
            df = pd.DataFrame([Resistance_targets,Support_targets]).T
            df.columns = ['Resistance','Support'] 
            df.index = [1,2,3,4,5]
            df=df.round(decimals = 2)
        
            st.table(format_dataframe_with_2_decimals(df))  
            st.write(underline_text("Technical Analysis:"), unsafe_allow_html=True)        
            st.table(Final_df1)
            st.write(underline_text("Pros & Cons:"), unsafe_allow_html=True)        
            st.table(df_swot)            
            
    if __name__ == "__main__":
        main()    
