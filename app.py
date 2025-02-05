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


pd.set_option('display.float_format', '{:.2f}'.format)

if 'symbol' not in st.session_state:
    st.session_state.symbol = None
if 'selected_period' not in st.session_state:
    st.session_state.selected_period = '6mo'
if 'chart_type' not in st.session_state:
    st.session_state.chart_type = 'Candlestick'
if 'selected_stock_category' not in st.session_state:
    st.session_state.selected_stock_category = None
if 'selected_stock' not in st.session_state:
    st.session_state.selected_stock = None


st.set_page_config(layout="wide")
st.header("Stocks - Analytics")

st.markdown(f'''
    <style>
        .reportview-container .sidebar-content {{
            padding-top: 0rem;
        }}
        .reportview-container .main .block-container {{
            padding-top: 0rem;
            padding-right: 10rem;
            padding-left: 1rem;
            padding-bottom: 10rem;
        }}
        .stTabs [data-baseweb="tab-list"] {{
            gap: 8px;
        }}
        .stTabs [data-baseweb="tab"] {{
            height: 50px;
            background-color: #F0F2F6;
            border-radius: 4px 4px 0px 0px;
            gap: 5px;
            padding-top: 10px;
            padding-bottom: 10px;
        }}
        .stTabs [aria-selected="true"] {{
            background-color: #F0F2F6;
        }}
        .stTabs [data-baseweb="tab-list"] button [data-testid="stMarkdownContainer"] p {{
            font-size: 26px;
            color: Blue;
        }}
    </style>
''', unsafe_allow_html=True)


listTabs = ["Nifty Indices", "Stocks based on Category", "Stock Analysis"]
whitespace = 9
col1, col2, col3 = st.tabs([s.center(whitespace, "\u2001") for s in listTabs])

with col1:
    def main():
        Index_df = pd.read_excel("Nifty_Index_List_V1.xlsx", sheet_name='UniqueIndices', engine='openpyxl')
        st.title("Nifty Index Analysis")

        Indices = list(Index_df['Indices'].unique())
        selected_Index = st.selectbox("Select an Index", Indices)
        Symbol = Index_df[Index_df.Indices == selected_Index]['YahooIndex'].values[0]
        st.write("Selected option:", selected_Index)

        if st.button('Submit Index'):
            st.session_state.symbol = Symbol

        if st.session_state.symbol:
            symbol = st.session_state.symbol
            ticker = yf.Ticker(symbol)
            todays_data = ticker.history(period='1d')
            Close = todays_data['Close'][0]
            st.write("Last close price is:", np.round(Close, 2))

            
            st.write(underline_text("Select Time Period:"), unsafe_allow_html=True)
            cols = st.columns(5)
            periods = {
                '1M': '1mo',
                '3M': '3mo',
                '6M': '6mo',
                '1Y': '1y',
                '5Y': '5y'
            }

            for i, (label, period) in enumerate(periods.items()):
                with cols[i]:
                    if st.button(label):
                        st.session_state.selected_period = period

            st.write(underline_text("Chart Type:"), unsafe_allow_html=True)
            chart_type = st.radio(
                "",
                ['Candlestick', 'Line'],
                horizontal=True,
                key='chart_type'
            )
            df = ticker.history(period=st.session_state.selected_period)
            df.reset_index(inplace=True)
            df['Date'] = pd.to_datetime(df['Date']).dt.date
            df['direction'] = df[['Open', 'Close']].apply(
                lambda x: 'Decreasing' if x.Open > x.Close else 'Increasing', axis=1
            )

            period_display_map = {
                '1mo': '1 Month',
                '3mo': '3 Months',
                '6mo': '6 Months',
                '1y': '1 Year',
                '5y': '5 Years'
            }
            selected_period_display = period_display_map.get(
                st.session_state.selected_period, '6 Months'
            )

            st.write(underline_text(f"{selected_period_display} Graph:"), unsafe_allow_html=True)

            
            if st.session_state.chart_type == 'Candlestick':
                fig = go.Figure(data=[go.Candlestick(
                    x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close']
                )])
            else:
                fig = go.Figure(data=[go.Scatter(
                    x=df['Date'],
                    y=df['Close'],
                    mode='lines',
                    name='Close Price',
                    line=dict(color='blue')
                )])

            fig.update_layout(
                xaxis_rangeslider_visible=False,
                width=1000,
                height=600,
                margin=dict(l=20, r=20, t=40, b=20)
            )

            st.plotly_chart(fig, use_container_width=True)

            Buy_At, Sell_At, Buy_Target1, Buy_Target2, Buy_Target3, Buy_Target4, Sell_target1, Sell_target2, Sell_target3, Sell_target4, Resistance1, Resistance2, Resistance3, Resistance4, Resistance5, Support1, Support2, Support3, Support4, Support5 = Gann(Close)

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
            Support_targets = [Support1, Support2, Support3, Support4, Support5]

            df = pd.DataFrame([Resistance_targets, Support_targets]).T
            df.columns = ['Resistance', 'Support']
            df.index = [1, 2, 3, 4, 5]
            df = df.round(decimals=2)

            st.table(format_dataframe_with_2_decimals(df))

            
            MC_Symbol = Index_df[Index_df.Indices == selected_Index]['MoneyControlIndices'].unique().tolist()[0]
            r = requests.get('https://www.moneycontrol.com/indian-indices/' + MC_Symbol + '.html')
            soup = BeautifulSoup(r.content, 'html.parser')

            
            s = soup.find('div', id='indi_contribute')
            s1 = s.find('div', class_='contribut_bx')
            content = s1.find_all('td')
            List = []
            for row in content:
                List.append(row.text)
            UP_Stocks = pd.DataFrame([List[x:x + 3] for x in range(0, len(List), 3)], columns=['Stock Name', 'CMP', 'Contribution Points'])
            UP_Stocks.set_index(['Stock Name'], drop=True, inplace=True)

            
            s2 = s.find('div', class_='contribut_bx FR')
            content1 = s2.find_all('td')
            List1 = []
            for row in content1:
                List1.append(row.text)
            Down_Stocks = pd.DataFrame([List1[x:x + 3] for x in range(0, len(List1), 3)], columns=['Stock Name', 'CMP', 'Contribution Points'])
            Down_Stocks.set_index(['Stock Name'], drop=True, inplace=True)

           
            col1, col2 = st.columns(2)
            with col1:
                st.write(underline_text(" Today Top Up Stocks:"), unsafe_allow_html=True)
                st.write(UP_Stocks)
            with col2:
                st.write(underline_text(" Today Top Down Stocks:"), unsafe_allow_html=True)
                st.write(Down_Stocks)

            
            s = soup.find('div', id='indi_component')
            s1 = s.find('div', class_='table-responsive')
            content = s1.find_all('td')
            List1 = []
            for row in content:
                List1.append(row.text)
            Components = pd.DataFrame([List1[x:x + 6] for x in range(0, len(List1), 6)], columns=['Company Name', 'Sector', 'CMP', 'Change(chg%)', 'Volume', 'Technical Rating'])
            Components.set_index(['Company Name'], drop=True, inplace=True)

            st.write(underline_text("Components:"), unsafe_allow_html=True)
            st.write(Components)

    if __name__ == "__main__":
        main()
with col2:        
    def main():
        Final_df1 = pd.DataFrame(columns=['Symbol', 'Moving Averages', 'Oscillators', 'Final Recommendation', 'Interval'])
        Final_df = pd.DataFrame(columns=['Symbol', 'Moving Averages', 'Oscillators', 'Final Recommendation', 'Interval'])
        
        Index_df = pd.read_excel("MC_General_Categories_Indices.xlsx", engine='openpyxl')
        
        st.title("Stock Analysis based on Category")

        Indices = list(Index_df['Category'].unique())
        selected_Index = st.selectbox("Select a Category", Indices)
        Stocks = Index_df[Index_df.Category == selected_Index]['Symbol'].unique().tolist()
        selected_Stocks = st.selectbox("Select a Stock", Stocks)
        StockName = Index_df[(Index_df.Symbol == selected_Stocks) &
                             (Index_df.Category == selected_Index)]['Stock Name'].tolist()[0]

        st.write("Selected Stock:", StockName)

        
        col1, col2, col3 = st.columns(3)
        with col1:
            chart_type = st.selectbox("Chart Type", ["Candlestick", "Line", "Area", "Baseline", "Mountain"], key='chart_type2')
        with col2:
            time_period = st.selectbox("Time Period", ["Today", "1 Week", "1 Month", "6 Months", "1 Year", "5 Years"], key='time_period2')
        with col3:
            selected_indicators = st.multiselect("Technical Indicators", 
                                   ["VWAP", "MVWAP", "EMA 34", "EMA 50", "EMA 20"], key='indicators2')

        
        url = "https://www.screener.in/company/"+selected_Stocks
        r = requests.get(url)
    
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find('section', id='analysis')
    
        pros = []
        cons = []
        if s:
            s1 = s.find('div', class_='pros')
            s2 = s.find('div', class_='cons')
            if s1:
                pros = [li.text.strip() for li in s1.find_all('li')]
            if s2:
                cons = [li.text.strip() for li in s2.find_all('li')]
    
        df_swot = pd.DataFrame([pros, cons]).T
        df_swot.columns = ['Pros', 'Cons']
        df_swot = df_swot.reset_index(drop=True)

       
        intervals = [
            (Interval.INTERVAL_1_DAY, '1 Day'),
            (Interval.INTERVAL_1_WEEK, '1 WEEK'),
            (Interval.INTERVAL_1_MONTH, '1 MONTH')
        ]
        
        if st.button('Submit Stock Category'):
            st.session_state.selected_stock_category = selected_Stocks

        if st.session_state.selected_stock_category:
            symbol = st.session_state.selected_stock_category + '.NS'
            ticker = yf.Ticker(symbol)
            
           
            period_params = {
                "Today": ("1d", "15m"),
                "1 Week": ("5d", "60m"),
                "1 Month": ("1mo", "1d"),
                "6 Months": ("6mo", "1d"),
                "1 Year": ("1y", "1d"),
                "5 Years": ("5y", "1wk")
            }
            
            period, interval = period_params[time_period]
            df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                st.error("No data available for selected period")
                return
                
            df = df.reset_index()
            df.rename(columns={'Datetime': 'Date'}, inplace=True)
            Close = df['Close'].iloc[-1]
            st.write(f"Last close price: {Close:.2f}")

            
            df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()
            df['Typical Price'] = (df['High'] + df['Low'] + df['Close']) / 3
            df['MVWAP'] = (df['Typical Price'] * df['Volume']).rolling(window=20).sum() / df['Volume'].rolling(window=20).sum()
            df['EMA 34'] = df['Close'].ewm(span=34, adjust=False).mean()
            df['EMA 50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA 20'] = df['Close'].ewm(span=20, adjust=False).mean()

            
            fig = go.Figure()
            
            if chart_type == "Candlestick":
                fig.add_trace(go.Candlestick(
                    x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name="Price"
                ))
            elif chart_type == "Line":
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df['Close'],
                    mode='lines', name="Price"
                ))
            elif chart_type == "Area":
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df['Close'],
                    fill='tozeroy', mode='none',
                    name="Price"
                ))
            elif chart_type == "Baseline":
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df['Close'],
                    line=dict(color='blue', width=2),
                    name="Price"
                ))
            elif chart_type == "Mountain":
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df['Close'],
                    fill='tozeroy', 
                    fillcolor='rgba(0,100,80,0.2)',
                    name="Price"
                ))

            
            colors = {
                "VWAP": "purple",
                "MVWAP": "cyan",
                "EMA 34": "orange",
                "EMA 50": "green",
                "EMA 20": "red"
            }
            
            for indicator in selected_indicators:
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df[indicator],
                    line=dict(color=colors[indicator], width=2),
                    name=indicator
                ))

            fig.update_layout(
                title=f"{StockName} {time_period} Chart",
                xaxis_title="Date",
                yaxis_title="Price",
                hovermode="x unified",
                height=600,
                showlegend=True
            )
            st.plotly_chart(fig, use_container_width=True)

            
            (Buy_At, Sell_At, 
             Buy_Target1, Buy_Target2, Buy_Target3, Buy_Target4,
             Sell_target1, Sell_target2, Sell_target3, Sell_target4,
             Resistance1, Resistance2, Resistance3, Resistance4, Resistance5,
             Support1, Support2, Support3, Support4, Support5) = Gann(Close)

           
            st.write(underline_text("Trading Recommendations:"), unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:
                st.markdown(f"""
                **Buy Zone**  
                Entry: {Buy_At:.2f}  
                Targets:  
                {Buy_Target1:.2f} | {Buy_Target2:.2f}  
                {Buy_Target3:.2f} | {Buy_Target4:.2f}  
                Stop Loss: {Sell_At:.2f}
                """)
            with col2:
                st.markdown(f"""
                **Sell Zone**  
                Entry: {Sell_At:.2f}  
                Targets:  
                {Sell_target1:.2f} | {Sell_target2:.2f}  
                {Sell_target3:.2f} | {Sell_target4:.2f}  
                Stop Loss: {Buy_At:.2f}
                """)

            
            st.write(underline_text("Key Levels:"), unsafe_allow_html=True)
            levels = pd.DataFrame({
                'Resistance': [Resistance1, Resistance2, Resistance3, Resistance4, Resistance5],
                'Support': [Support1, Support2, Support3, Support4, Support5]
            }, index=range(1,6))
            st.dataframe(levels.style.format("{:.2f}"))

            
            st.write(underline_text("Technical Signals:"), unsafe_allow_html=True)
            for interval, interval_name in intervals:
                try:
                    handler = TA_Handler(
                        symbol=selected_Stocks,
                        screener="india",
                        exchange="NSE",
                        interval=interval
                    )
                    analysis = handler.get_analysis()
                    
                    new_row = pd.DataFrame([{
                        'Symbol': selected_Stocks,
                        'Moving Averages': analysis.moving_averages['RECOMMENDATION'],
                        'Oscillators': analysis.oscillators['RECOMMENDATION'],
                        'Final Recommendation': analysis.summary['RECOMMENDATION'],
                        'Interval': interval_name
                    }])
                    Final_df1 = pd.concat([Final_df1, new_row], ignore_index=True)
                    
                except Exception as e:
                    st.error(f"Error fetching data for {interval_name}: {str(e)}")

            Final_df1.set_index('Interval', inplace=True)
            st.dataframe(Final_df1.style.map(
                lambda x: "color: green" if "BUY" in x.upper() 
                else "color: red" if "SELL" in x.upper() 
                else "color: orange"))

            
            st.write(underline_text("Fundamental Analysis (SWOT):"), unsafe_allow_html=True)
            st.dataframe(df_swot.style.set_table_styles([{
                'selector': 'th',
                'props': [('background-color', '#4b77be'), ('color', 'white')]
            }]))

    if __name__ == "__main__":
        main()
with col3:
    def main():
        Final_df1 = pd.DataFrame(columns=['Symbol', 'Moving Averages', 'Oscillators', 'Final Recommendation', 'Interval'])
        Final_df = pd.DataFrame(columns=['Symbol', 'Moving Averages', 'Oscillators', 'Final Recommendation', 'Interval'])

        Index_df = pd.read_excel("MC_General_Categories_Indices.xlsx", engine='openpyxl')

        st.title("Stock Analysis")

        Stocks = Index_df['Symbol'].unique().tolist()
        selected_Stocks = st.selectbox("Select a Stock", Stocks, key='stock_select3')
        StockName = Index_df[(Index_df.Symbol == selected_Stocks)]['Stock Name'].tolist()[0]

        st.write("Selected Stock:", StockName)

    
        col1, col2, col3 = st.columns(3)
        with col1:
            chart_type = st.selectbox("Chart Type", ["Candlestick", "Line", "Area", "Baseline", "Mountain"], key='chart_type3')
        with col2:
            time_period = st.selectbox("Time Period", ["Today", "1 Week", "1 Month", "6 Months", "1 Year", "5 Years"], key='time_period3')
        with col3:
            selected_indicators = st.multiselect("Technical Indicators", 
                                   ["VWAP", "MVWAP", "EMA 34", "EMA 50", "EMA 20"], key='indicators3')

        
        url = "https://www.screener.in/company/" + selected_Stocks
        r = requests.get(url)
    
        soup = BeautifulSoup(r.content, 'html.parser')
        s = soup.find('section', id='analysis')
    
        pros = []
        cons = []
        if s:
            s1 = s.find('div', class_='pros')
            s2 = s.find('div', class_='cons')
            if s1:
                pros = [li.text.strip() for li in s1.find_all('li')]
            if s2:
                cons = [li.text.strip() for li in s2.find_all('li')]
    
        df_swot = pd.DataFrame([pros, cons]).T
        df_swot.columns = ['Pros', 'Cons']
        df_swot = df_swot.reset_index(drop=True)

        
        intervals = [
            (Interval.INTERVAL_1_DAY, '1 Day'),
            (Interval.INTERVAL_1_WEEK, '1 WEEK'),
            (Interval.INTERVAL_1_MONTH, '1 MONTH')
        ]
        
        if st.button('Submit Stock', key='submit_stock3'):
            st.session_state.selected_stock = selected_Stocks

        if 'selected_stock' in st.session_state and st.session_state.selected_stock:
            symbol = st.session_state.selected_stock + '.NS'
            ticker = yf.Ticker(symbol)
            
            
            period_params = {
                "Today": ("1d", "15m"),
                "1 Week": ("5d", "60m"),
                "1 Month": ("1mo", "1d"),
                "6 Months": ("6mo", "1d"),
                "1 Year": ("1y", "1d"),
                "5 Years": ("5y", "1wk")
            }
            
            period, interval = period_params[time_period]
            df = ticker.history(period=period, interval=interval)
            
            if df.empty:
                st.error("No data available for selected period")
                return
                
            df = df.reset_index()
            df.rename(columns={'Datetime': 'Date'}, inplace=True)
            Close = df['Close'].iloc[-1]
            st.write(f"Last close price: {Close:.2f}")

            
            df['VWAP'] = (df['Volume'] * (df['High'] + df['Low'] + df['Close']) / 3).cumsum() / df['Volume'].cumsum()
            df['Typical Price'] = (df['High'] + df['Low'] + df['Close']) / 3
            df['MVWAP'] = (df['Typical Price'] * df['Volume']).rolling(window=20).sum() / df['Volume'].rolling(window=20).sum()
            df['EMA 34'] = df['Close'].ewm(span=34, adjust=False).mean()
            df['EMA 50'] = df['Close'].ewm(span=50, adjust=False).mean()
            df['EMA 20'] = df['Close'].ewm(span=20, adjust=False).mean()

            fig = go.Figure()
            
            if chart_type == "Candlestick":
                fig.add_trace(go.Candlestick(
                    x=df['Date'],
                    open=df['Open'],
                    high=df['High'],
                    low=df['Low'],
                    close=df['Close'],
                    name="Price"
                ))
            elif chart_type == "Line":
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df['Close'],
                    mode='lines', name="Price"
                ))
            elif chart_type == "Area":
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df['Close'],
                    fill='tozeroy', mode='none',
                    name="Price"
                ))
            elif chart_type == "Baseline":
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df['Close'],
                    line=dict(color='blue', width=2),
                    name="Price"
                ))
            elif chart_type == "Mountain":
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df['Close'],
                    fill='tozeroy', 
                    fillcolor='rgba(0,100,80,0.2)',
                    name="Price"
                ))
            colors = {
                "VWAP": "purple",
                "MVWAP": "cyan",
                "EMA 34": "orange",
                "EMA 50": "green",
                "EMA 20": "red"
            }
            
            for indicator in selected_indicators:
                fig.add_trace(go.Scatter(
                    x=df['Date'], y=df[indicator],
                    line=dict(color=colors[indicator], width=2),
                    name=indicator
                ))

            fig.update_layout(
                title=f"{StockName} {time_period} Chart",
                xaxis_title="Date",
                yaxis_title="Price",
                hovermode="x unified",
                height=600,
                showlegend=True
            )
            
            
            st.plotly_chart(
                fig, 
                use_container_width=True,
                key=f"chart_{selected_Stocks}_{time_period.replace(' ', '_')}"
            )

            
            (Buy_At, Sell_At, 
             Buy_Target1, Buy_Target2, Buy_Target3, Buy_Target4,
             Sell_target1, Sell_target2, Sell_target3, Sell_target4,
             Resistance1, Resistance2, Resistance3, Resistance4, Resistance5,
             Support1, Support2, Support3, Support4, Support5) = Gann(Close)

            st.write(underline_text(" Trading Recommendation:"), unsafe_allow_html=True)
            message = f"""Buy at / above: {Buy_At:.2f}
Targets: {Buy_Target1:.2f}, {Buy_Target2:.2f}, {Buy_Target3:.2f}, {Buy_Target4:.2f}

STOPLOSS: {Sell_At:.2f}

Sell at / below: {Sell_At:.2f}
Targets: {Sell_target1:.2f}, {Sell_target2:.2f}, {Sell_target3:.2f}, {Sell_target4:.2f}

STOPLOSS: {Buy_At:.2f}"""
            
            st.write(message)
                

           
            st.write(underline_text("Key Levels:"), unsafe_allow_html=True)
            levels = pd.DataFrame({
                'Resistance': [Resistance1, Resistance2, Resistance3, Resistance4, Resistance5],
                'Support': [Support1, Support2, Support3, Support4, Support5]
            }, index=range(1,6))
            st.dataframe(levels.style.format("{:.2f}"))

            
            st.write(underline_text("Technical Signals:"), unsafe_allow_html=True)
            for interval, interval_name in intervals:
                try:
                    handler = TA_Handler(
                        symbol=selected_Stocks,
                        screener="india",
                        exchange="NSE",
                        interval=interval
                    )
                    analysis = handler.get_analysis()
                    
                    new_row = pd.DataFrame([{
                        'Symbol': selected_Stocks,
                        'Moving Averages': analysis.moving_averages['RECOMMENDATION'],
                        'Oscillators': analysis.oscillators['RECOMMENDATION'],
                        'Final Recommendation': analysis.summary['RECOMMENDATION'],
                        'Interval': interval_name
                    }])
                    Final_df1 = pd.concat([Final_df1, new_row], ignore_index=True)
                    
                except Exception as e:
                    st.error(f"Error fetching data for {interval_name}: {str(e)}")

            Final_df1.set_index('Interval', inplace=True)
            st.dataframe(Final_df1.style.map(
                lambda x: "color: green" if "BUY" in x.upper() 
                else "color: red" if "SELL" in x.upper() 
                else "color: orange"))

            st.write(underline_text("Fundamental Analysis (SWOT):"), unsafe_allow_html=True)
            st.dataframe(df_swot.style.set_table_styles([{
                'selector': 'th',
                'props': [('background-color', '#4b77be'), ('color', 'white')]
            }]))

    if __name__ == "__main__":
        main()
