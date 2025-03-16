import streamlit as st
import seaborn as sns
import pandas as pd
import yfinance as yf
import YahooFinance as yfo
from datetime import date, datetime, timedelta
import altair as alt
import matplotlib.pyplot as plt
import numpy as np

# Define the stock ticker symbols

# tickers = pd.DataFrame(
#     {
#         "symbol": ["NVDA","AAPL","SOFI","NIO","VBL.NS","NCLH"],
#         "country": ["USA","USA","USA","USA","IND","USA"],
#         "avg_cost_basis": [25.11,241.53,15.19,28.99,20,22.00],
#         "quantity": [1500,1,1,2159,1, 5000],
#         'purchased_date': ['2021-01-01','2021-01-01','2021-01-01','2021-01-01','2021-01-01','2021-01-01']
#     }
# )

tickers = pd.read_excel("stock-file.xlsx", index_col=None, header=0) #,
                         #dtype={'symbol': str, 'country': str, 'avg_cost_basis': float, 'quantity': int, 'purchased_date': str})
#tickers["purchased_date"]=pd.to_datetime(tickers["purchased_date"], errors='coerce')

stocks_df = pd.DataFrame(
    columns=(
        'symbol','country','last_price','last_price_change','today_gain_loss',
        'total_gain_loss','total_gain_loss_per','current_value','quantity','avg_cost_basis','avg_cost_basis_total',
        'analyst_price_targets','recommendations','chart_df','period_perf_df'
    )
)

@st.cache_data
def get_stock_data():
    for index, row in tickers.iterrows():
        symbol=row["symbol"].strip()
        #st.write(f"Processing {symbol}...")
        
        stock = yfo.TickerInfo(symbol)
        
        quantity=row["quantity"]
        avg_cost_basis=row["avg_cost_basis"]
        avg_cost_basis_total=quantity * avg_cost_basis
        
        current_price=stock.get_current_price()
        previous_close_price=stock.get_previous_close_price()
        current_value=quantity * current_price

        total_gain_loss=current_value - avg_cost_basis_total
        total_gain_loss_per=((current_value - avg_cost_basis_total)/avg_cost_basis_total)*100

        stocks_df.loc[index,"symbol"]=symbol
        stocks_df.loc[index,"country"]=row["country"].strip()
        stocks_df.loc[index,"quantity"]=quantity
        stocks_df.loc[index,"last_price"]=current_price
        stocks_df.loc[index,"current_value"]=current_value
        stocks_df.loc[index,"last_price_change"]=current_price - previous_close_price
        stocks_df.loc[index,"today_gain_loss"]=(current_price - previous_close_price) * quantity
        stocks_df.loc[index,"total_gain_loss"]=total_gain_loss
        stocks_df.loc[index,"avg_cost_basis"]=avg_cost_basis
        stocks_df.loc[index,"avg_cost_basis_total"]=avg_cost_basis_total
        stocks_df.loc[index,"total_gain_loss_per"]=total_gain_loss_per
        stocks_df.at[index,"analyst_price_targets"]=stock.ticker.analyst_price_targets
        stocks_df.at[index,"recommendations"]=stock.ticker.recommendations
        stocks_df.at[index,"chart_df"]=stock.get_historical_data_with_duration(period='2y')
        stocks_df.at[index,"period_perf_df"]=stock.get_last_2years_performance(quantity, avg_cost_basis, row["purchased_date"])
        stocks_df.loc[index,"yr1_min_price"]=round(stock.yr1_min_price, 2)
        stocks_df.loc[index,"yr1_max_price"]=round(stock.yr1_max_price,2)

        recommendations=stock.get_recommendations_by_dictionary()
        #st.write(recommendations)
        
        stocks_df.loc[index,"buy_count"]=recommendations.get("strongBuy")+recommendations.get("buy")
        stocks_df.loc[index,"hold_count"]=recommendations.get("hold")
        stocks_df.loc[index,"sell_count"]=recommendations.get("sell")+recommendations.get("strongSell")

        #st.write(stock.get_recommendations_by_dictionary())

    return stocks_df.query("country=='USA'"), stocks_df.query("country=='IND'")

def local_css(file_name):
    with open(file_name) as f:
        st.markdown(f'<style>{f.read()}</style>', unsafe_allow_html=True)

def gain_loss_format(value):
    if value > 0:
        #return f":green-background[{value}]"
        return f"<font color='green'>{value}</font>"
    elif value < 0:
        return f"<font color='red'>{value}</font>"
        #return f":red-background[{value}]"
    else:
        return f"{value}"

def gain_loss_format(value):
    if value > 0:
        #return f":green-background[{value}]"
        return f"<font color='green'>{value}</font>"
    elif value < 0:
        return f"<font color='red'>{value}</font>"
        #return f":red-background[{value}]"
    else:
        return f"{value}"

def green_or_red_background(value, value1):
    if value > 0:
        return f"""<span class="button-green">{value1:,.0f}</span>"""
    else:
        return f"""<span class="button-red">{value1:,.0f}</span>"""
    
st.set_page_config(
    page_title="Stock Analysis",
    page_icon="🏂",
    layout="wide",
    initial_sidebar_state='collapsed')

page_bg_img = f"""
<style>
[data-testid="stAppViewContainer"] > .main {{
background-image: url("https://i.postimg.cc/4xgNnkfX/Untitled-design.png");
background-size: cover;
background-position: center center;
background-repeat: no-repeat;
background-attachment: local;
}}
[data-testid="stHeader"] {{
background: rgba(0,0,0,0);
}}
</style>
"""

st.markdown(page_bg_img, unsafe_allow_html=True)

st.markdown("""
    <style>
body {background-color: #000000;}
            
.flex-containerx {
  display: flex;
  align-items: stretch;
  background-color: #000000;
  outline: 1px solid blue;
  gap: 0px;
}

.flex-containerx > div {
  background-color: DodgerBlue;
  color: white;
  margin: 0px;
  text-align: left;
  border-right: solid white 1px;
  line-heightx: 75px;
  font-size: 14px;
  paddingx: 0px;
  spacingx: 0px;
  margin-leftx: 0px;
}

.circle-green {
    display: inline-block;
    text-align: center;
    font-size: 12px;
    /* width: 10%; */
    /* border: 1.2em solid #dddddd; */
    background-color: green;
    width: 2.4em;
    height: 2.4em;
    line-height: 2.4em;
    border-radius: 50%;
    /* max-width: 1.2em; */
    /* max-height: 1.2em; */
    /* box-sizing: border-box; */    
    /* margin: 0 auto; */
}
.circle-orange {
    display: inline-block;
    text-align: center;
    font-size: 12px;
    /* width: 10%; */
    /* border: 1.2em solid #dddddd; */
    background-color: orange;
    width: 2.4em;
    height: 2.4em;
    line-height: 2.4em;
    border-radius: 50%;
    /* max-width: 1.2em; */
    /* max-height: 1.2em; */
    /* box-sizing: border-box; */    
    /* margin: 0 auto; */
}
.circle-red {
    display: inline-block;
    text-align: center;
    font-size: 12px;
    /* width: 10%; */
    /* border: 1.2em solid #dddddd; */
    background-color: red;
    width: 2.4em;
    height: 2.4em;
    line-height: 2.4em;
    border-radius: 50%;
    /* max-width: 1.2em; */
    /* max-height: 1.2em; */
    /* box-sizing: border-box; */    
    /* margin: 0 auto; */
}

.button-green  {
  background-color: #04AA6D; /* Green */
  border: none;
  color: white;
  padding: 1px;
  border-radius: 5px;
  text-align: center;
  text-decorationx: none;
  display: inline-block;
  font-size: 14px;
  heightx: 8px;
  margin: 1px 1px;
  cursorx: pointer;
}

.button-red {
  background-color: red; /* Green */
  border: none;
  color: white;
  padding: 1px;
  border-radius: 5px;
  text-align: center;
  text-decorationx: none;
  display: inline-block;
  font-size: 14px;
  heightx: 8px;
  margin: 1px 1px;
  cursorx: pointer;
}

[data-testid="stExpander"] details {
    border-style: none;
}

.stProgress > div > div > div > div {
    background-color: green;
}

/* Style for the empty part of the progress bar */
.stProgress > div > div > div {
    background-color: white;
}

.stProgress > div {
    padding: 0;
}
.st-emotion-cache-s1invk {
    padding: 0;
}

.st-emotion-cache-4uzi61 {
    border: 1px solid rgba(49, 51, 63, 0.2);
    border-radius: 15px;
    backgroundx: linear-gradient(180deg, #0d47a1, #1976d2);
    background-image: linear-gradient(to bottom right, #00C0FF, #4218B8);
    box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
    padding: calc(-11px + 1rem);
    }

.st-emotion-cache-1lh5cd8 {
  gap: 0rem;
}    

.top-section, .bottom-section {
    color: white;
}
.top-section {
    padding: 5px 10px; /* Reduced padding */
    display: flex;
    flex-direction: column;
    justify-content: space-between;
    height: 30%;
    border-radius: 15px 15px 0 0;
}
.top-section div {
    display: flex;
    justify-content: space-between;
    font-size: 16px; /* Adjusted font size for smaller screens */
    font-weight: 600;
}

.bottom-section {
    heightx: 70%;
    paddingx: 5px 10px; /* Reduced padding */
    backgroundx: rgba(255, 255, 255, 0.1);
    backdrop-filterx: blur(10px);
    border-radiusx: 0 0 15px 15px;
    color: white;
    border-bottomx: 1px solid white;
}

.bottom-section div {
    border-bottomx: 1px solid white;
}
</style>
"""
, unsafe_allow_html=True)

#alt.theme.enable("dark")

#local_css("style.css")
cb_view_details = st.sidebar.checkbox('View Details')
if st.sidebar.button("Refresh Data"):
    get_stock_data.clear()
    #stocks_df = get_stock_data(stocks_df)

# st.dataframe(tickers1)
# st.dataframe(tickers)

# st.write(tickers1.dtypes)
# st.write(tickers.dtypes)

usa_stocks_df, ind_stocks_df = get_stock_data()

sort_columns = st.sidebar.multiselect('Select columns to sort', usa_stocks_df.columns)
sort_orders = []

# Select sort order for each selected column
for col in sort_columns:
    sort_order = st.sidebar.radio(f'Select sort order for {col}', ['Ascending', 'Descending'])
    sort_orders.append(True if sort_order == 'Ascending' else False)

# Sort the dataframe
if sort_columns:
    usa_stocks_df = usa_stocks_df.sort_values(by=sort_columns, ascending=sort_orders)
    ind_stocks_df = ind_stocks_df.sort_values(by=sort_columns, ascending=sort_orders)

#weekly_data = yf.download("AAPL", start="2024-02-16", end="2025-02-17", interval="1wk")
#st.dataframe(weekly_data)

def tab_operation(country_tab, country_stocks_df):
    with country_tab:
        #st.dataframe(country_stocks_df)
        for index, stock in country_stocks_df.iterrows():
            with st.container(border=True):
                st.markdown(f"""
                            <div class="top-section">                                                        
                                <div class="bottom-section" style="width:100%;">
                                    <div style="width:40%;float: left;font-size: 16px;font-weight: 600;display: inline">
                                        <span>{stock['symbol']}</span>
                                        <span>
                                            <span class="circle-green">{stock['buy_count']}</span>
                                            <span class="circle-orange">{stock['hold_count']}</span>
                                            <span class="circle-red">{stock['sell_count']}</span>
                                        </span>
                                        <br>
                                        <span>""" +gain_loss_format(round(stock['last_price'],2))+f"""</span> <span>({stock['last_price_change']:,.2f})</span><br>
                                        G/L: {stock['today_gain_loss']:,.0f}
                                    </div>
                                    <div style="width:30%;float:left;text-align: right; display: inline">
                                        CB: {stock['avg_cost_basis']:,.2f}<br>                                        
                                        Q: {stock['quantity']:,.0f}<br>
                                        CB.T: {stock['avg_cost_basis_total']:,.0f}
                                    </div>
                                    <div style="width:30%;text-align: right; display: inline">
                                        G/L%: """ +
                                        green_or_red_background(stock['total_gain_loss_per'], stock['total_gain_loss_per'])                                        
                                        +f"""<br>
                                        G/L: """+
                                        green_or_red_background(stock['total_gain_loss_per'], stock['total_gain_loss'])
                                        +f"""<br>
                                        CV: """+
                                        green_or_red_background(stock['total_gain_loss_per'], stock['current_value'])
                                        +f"""
                                    </div>
                                </div>
                            </div>
                            <!--
                            <div class="bottom-section">
                                <div style="width:33%;float: left;font-size: 16px;font-weight: 600;">NVDA</div>
                                <div style="width:33%;float: left;">125.50</div>
                                <div style="width:34%;float: left;text-align: right;">+20.50</div>
                            </div>
                            <div class="bottom-section">
                                <div style="width:33%;float: left;">NVDA</div>
                                <div style="width:33%;float: left;">125.50</div>
                                <div style="width:34%;float: left;text-align: right;">+20.50</div>
                            </div>
                            <div class="bottom-section">
                                <div style="width:33%;float: left;">NVDA</div>
                                <div style="width:33%;float: left;">125.50</div>
                                <div style="width:34%;float: left;text-align: right;">+20.50</div>
                            </div>
                            <div class="line"></div>
                            -->
                            """,  unsafe_allow_html=True)

                # Calculate min, max, and current prices
                min_price = stock['yr1_min_price']
                max_price = stock['yr1_max_price']
                current_price = stock['last_price']

                # Calculate the progress percentage
                progress = (current_price - min_price) / (max_price - min_price)

                progress_text = st.empty()
                progress_bar = st.empty()

                progress_bar.progress(progress)
                progress_style = f"""
                <div style="
                    display: flex;
                    font-size: 14px;
                    font-weight: 600;
                    color: white;
                    justify-content: space-between;
                    width: 100%;">
                    <span>{min_price:.2f}</span>
                    <span style="position: absolute; left: {progress * 100}%; transform: translateX(-50%);">
                        {current_price:.2f} ({progress * 100:.1f}%)
                    </span>
                    <span>{max_price:.2f}</span>
                </div>
                """
                progress_text.markdown(progress_style, unsafe_allow_html=True)

                with st.expander("Details"):
                    perf_tab, rec_tab=st.tabs(["Performance","Recommendation/Price Targets"])
                    with perf_tab:
                        st.dataframe(stock['period_perf_df'])
                        st.dataframe(stock["chart_df"])
                    with rec_tab:
                        st.dataframe(stock.recommendations)
                        st.write(stock.analyst_price_targets)

            _=f"""
                    <div class="flex-container">
                        <div style="flex-grow: 1;">
                            <span style='background-color:red; font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size: 14px;'>                                                            
                            {stock['symbol']} {stock['last_price']:,.2f}<br>
                            {stock['last_price_change']:,.2f} {stock['today_gain_loss']:,.2f} <br>
                            {stock['avg_cost_basis']:,.2f} {stock['avg_cost_basis_total']:,.2f}<br>
                            Q. {stock['quantity']}
                            </span>
                        </div>
                        <div style="flex-grow: 1">
                            <span style='background-colorx:yellow; font-family: Arial, Helvetica, sans-serif; font-sizex: 16px; text-align: top;>
                                """+gain_loss_format(stock['total_gain_loss_per'])+f""" %
                            </span><br>
                            <span style='font-family: Arial, Helvetica, sans-serif; font-sizex: 16px; text-align: right;background-colorx:#ddd;'>
                                {stock['current_value']:,.0f} """+gain_loss_format(stock['total_gain_loss'])+f"""
                            </span>
                        </div>
                    </div>
                    """            

usa_tab, india_tab=st.tabs(["USA","IND"])
tab_operation(usa_tab, usa_stocks_df)
tab_operation(india_tab, ind_stocks_df)
