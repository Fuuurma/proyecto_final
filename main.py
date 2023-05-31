from flask import Flask, render_template
from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import (Table, Column, Integer, String,  Enum, Numeric, DateTime,Date, text)
from sqlalchemy.sql import (select, desc, asc)
import pandas as pd
import os 

# Import all queries to the db or dataframes from crypto queries using pandas or sqlAlchemy
from crypto_queries import (q_coins_general, q_tvl_historic, q_coin_winners_timeframe, q_coin_losers_timeframe, q_dapps_tvl, q_coins_general_specific_columns, 
                            q_tvl_historic_specific, q_chains_actual_tvl, q_stables_historic_monthly, q_dapps_tvl_specific, q_tvl_pct_change, q_get_actual_stablecoins_mcap, 
                            q_get_actual_volume_today, q_top_dex_volume, df_coins_general_with_tvl, coins_general_with_tvl, get_tvl_today, get_coins_general_statistics,
                            table_coins_general_tvl, tvl_chains_pct_change, tvl_chains_historic, q_categories_tvl, q_nfts_collections, q_stables_general, q_get_chains_by_pct_change,
                            q_get_daily_total_volume)

# Import all plots and charts using plotly
from plotly_grphs import (tvl_historic_graph, top_10_dapps_pie, categories_bar_plot, coins_price_change_bar_chart, coins_price_change_heatmap, a, 
                          historic_coin_price, top10_chains_tvl_pie, top10_stablecoins_pie, histogram_unreleased_stablecoins_plot, get_ohlc_plot, coins_general_scatter_plot,
                          dapps_tvl_bar_plot, dapps_tvl_pie_plot, get_chains_area_plot, get_chains_daily_pct_plot, hero_plot, chains_bar_tvl_mcap )


# --------------------

def tvl_top100_protocols(days):
    # tvl_protocols = pd.read_csv('top_100_protocols_tvl.csv')
    current_dir = os.path.dirname(os.path.abspath(__file__))
    tvl_protocols_path = os.path.join(current_dir, 'static', 'csv', 'top_100_protocols_tvl.csv')
    tvl_protocols = pd.read_csv(tvl_protocols_path)
    
    tvl_protocols = tvl_protocols.reset_index()
    tvl_protocols = tvl_protocols.sort_values('index', ascending=False).head(days)
    return tvl_protocols

# ------------

def connect_db():
    user='root'
    password='240699'
    host='localhost'
    database='crypto_data'

    # Connect to the database
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    try:
        connection = engine.connect()
        return connection
    except Exception as e:
        raise e
    
    
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Flask Flask Flask
# //////////////////////////////////////////////////////////////////////////////////////////////////////////////////

app = Flask(__name__)

@app.route('/')
def home():    
    # Front page
    plot = hero_plot()
    
    actual_tvl = get_tvl_today()
    actual_stables = q_get_actual_stablecoins_mcap()
    actual_mcap_vol = get_coins_general_statistics()
    dominance = table_coins_general_tvl(limit=2)
    actual_vol = q_get_daily_total_volume()
    
    # Coins Top/Bottom
    top_coins_24h = q_coins_general_specific_columns(['name','image', 'symbol', 'Price_Change_24h'], 'Price_Change_24h', True,5 )
    top_coins_7d = q_coins_general_specific_columns(['name','image', 'symbol', 'Price_Change_7d'], 'Price_Change_7d',True, 5)
    top_coins_30d = q_coins_general_specific_columns(['name','image', 'symbol', 'Price_Change_30d'], 'Price_Change_30d',True, 5)
    top_coins_200d = q_coins_general_specific_columns(['name','image', 'symbol', 'Price_Change_200d'], 'Price_Change_200d',True, 5)
    
    botom_coins_24h = q_coin_losers_timeframe(timeframe='24h', limit=5)
    botom_coins_7d = q_coin_losers_timeframe(timeframe='7d', limit=5)
    botom_coins_30d = q_coin_losers_timeframe(timeframe='30d', limit=5)
    botom_coins_200d = q_coin_losers_timeframe(timeframe='200d', limit=5)
    
    
    # Dapps Top/Bottom
    top_dapps_24h = q_dapps_tvl_specific(['name', 'symbol', 'change_1d' ], 'change_1d', True, 5)
    top_dapps_7d = q_dapps_tvl_specific(['name', 'symbol', 'change_7d' ], 'change_7d', True, 5)
    
    botom_dapps_24h = q_dapps_tvl_specific(['name', 'symbol', 'change_1d' ], 'change_1d', False, 5)
    botom_dapps_7d = q_dapps_tvl_specific(['name', 'symbol', 'change_7d' ], 'change_7d', False, 5)
    
    # Chains Top/Bottom
    top_chains_24h = q_get_chains_by_pct_change(False, 5, 1)
    top_chains_7d = q_get_chains_by_pct_change(False, 5, 7)
    top_chains_30d = q_get_chains_by_pct_change(False, 5, 30)
    botom_chains_24h = q_get_chains_by_pct_change(True, 5, 1)
    botom_chains_7d = q_get_chains_by_pct_change(True, 5, 7)
    botom_chains_30d = q_get_chains_by_pct_change(True, 5, 30)
    
    # Dex Top/Bottom
    top_dex_24h = q_top_dex_volume(5,'dailyVolume', True)
    top_dex_7d = q_top_dex_volume(5,'total7d', True)
    top_dex_30d = q_top_dex_volume(5,('total30d'), True)
    
    botom_dex_24h = q_top_dex_volume(5,'dailyVolume', False)
    botom_dex_7d = q_top_dex_volume(5,'total7d', False)
    botom_dex_30d = q_top_dex_volume(5,('total30d'), False)
    
    # Plots
    coins_bar_chart = coins_price_change_bar_chart()
    coins_heatmap =  coins_price_change_heatmap()
    coins_log_scatter_plot = coins_general_scatter_plot()
    
    btc_candle = get_ohlc_plot(['bitcoin']) # ohlc

    coins_general_home = q_coins_general() # coins_genral_table
    
    return render_template('home.html', top_coins_24h=top_coins_24h, top_coins_7d=top_coins_7d, top_coins_30d=top_coins_30d, top_coins_200d=top_coins_200d, actual_tvl = actual_tvl, plot=plot,
                           botom_coins_24h=botom_coins_24h, botom_coins_7d=botom_coins_7d, botom_coins_30d=botom_coins_30d, botom_coins_200d=botom_coins_200d, coins_general_home = coins_general_home,
                           top_dapps_24h=top_dapps_24h, top_dapps_7d=top_dapps_7d, botom_dapps_24h=botom_dapps_24h, botom_dapps_7d=botom_dapps_7d, coins_bar_chart=coins_bar_chart, coins_heatmap=coins_heatmap,
                           btc_candle=btc_candle, coins_log_scatter_plot=coins_log_scatter_plot, actual_stables=actual_stables, actual_mcap_vol=actual_mcap_vol, dominance=dominance, top_chains_24h=top_chains_24h,
                           top_chains_7d=top_chains_7d, top_chains_30d=top_chains_30d,botom_chains_24h=botom_chains_24h,botom_chains_7d=botom_chains_7d, botom_chains_30d=botom_chains_30d, top_dex_24h=top_dex_24h,
                           top_dex_7d=top_dex_7d, top_dex_30d=top_dex_30d, botom_dex_24h= botom_dex_24h, botom_dex_7d=botom_dex_7d, botom_dex_30d=botom_dex_30d, actual_vol=actual_vol )

@app.route('/tvl')
def tvl():
        # Area chart
        tvl_graph = tvl_historic_graph()
        # Values of today
        actual_tvl = q_tvl_historic_specific(['date', 'totalLiquidityUSD'], sort='date', descending=True, interval='daily', limit=1)
        tvl_ath = q_tvl_historic_specific(['date', 'totalLiquidityUSD'], sort='totalLiquidityUSD', descending=True, interval='daily', limit=1)
        tvl_pct = q_tvl_pct_change()
        
        # TVL historic table
        tvl_historic = q_tvl_historic()
        # dapps tvl table
        dapps_tvl = q_dapps_tvl()
        
        # Categories table & plot
        categories_bar = categories_bar_plot()
        categories = q_categories_tvl()
        return render_template('tvl.html', tvl_historic=tvl_historic, dapps_tvl = dapps_tvl, actual_tvl = actual_tvl, tvl_ath = tvl_ath, tvl_graph=tvl_graph, categories_bar=categories_bar, 
                               tvl_pct=tvl_pct,categories=categories)   
    


@app.route('/tvl/chains')
def tvl_chains():
    # chains table tvl for each chain
    tvl_chains = q_chains_actual_tvl()
    # not using
    tvl_historic = tvl_chains_historic()
    # Coins plot hero
    chains_plot = get_chains_area_plot()
    # pct change
    chains_pct = tvl_chains_pct_change()
    # plot of daily pct change
    chains_pct_plot = get_chains_daily_pct_plot()
    
    # plot of chains (mcap & tvl) LOG
    chains_tvl_mcap = chains_bar_tvl_mcap()
    
    return render_template('tvl_chains.html', tvl_chains=tvl_chains, tvl_historic=tvl_historic, chains_plot=chains_plot, chains_pct=chains_pct, 
                           chains_pct_plot=chains_pct_plot, chains_tvl_mcap=chains_tvl_mcap)


@app.route('/tvl/dapps')
def tvl_dapps():
    # bottom table chains historic tvl 
    tvl_dapps = tvl_top100_protocols(100)
    dex_volume = q_top_dex_volume(limit=50, sort='dailyVolume', descending=True)
    # plots. dapps (tvl) => pie & bar
    dapps_tvl_plot = dapps_tvl_bar_plot()
    dapps_tvl_pie = dapps_tvl_pie_plot()
    # left table of tvl
    tvl_dapps_today = coins_general_with_tvl()
    
    return render_template('tvl_dapps.html', tvl_dapps = tvl_dapps,
                           dex_volume=dex_volume, tvl_dapps_today= tvl_dapps_today, dapps_tvl_plot= dapps_tvl_plot, dapps_tvl_pie=dapps_tvl_pie )
                      

@app.route('/coins')
def coins():
    # all data for coins. 
    other_btc = q_coins_general_specific_columns(['market_cap_rank','image', 'name', 'symbol','current_price', 'id',
                          'market_cap', 'fully_diluted_valuation', 'total_volume','circulating_supply',
                          'total_supply', 'max_supply', 'to_ATH_pct' , 'Price_Change_24h',
                          'Price_Change_7d', 'Price_Change_30d','Price_Change_200d', 'Price_Change_1Y'], sort='market_cap_rank', descending=False, limit=20)


    # List of names from the coins to plot the ohlc 
    chart_ids=['bitcoin', 'ethereum', 'tether' ,'binancecoin', 'usd-coin', 'ripple', 'cardano', 'staked-ether', 'dogecoin', 'solana' , 'matic-network', 'litecoin',
               'polkadot', 'tron', 'binance-usd', 'shiba-inu', 'avalanche-2', 'dai', 'wrapped-bitcoin', 'uniswap','chainlink', 'leo-token']
    
    # OHLC plots
    charting = get_ohlc_plot(chart_ids)
    

    return render_template('coins_general.html', other_btc=other_btc, charting=charting)
     

@app.route('/dashboard')
def dashboard():
    # All plots here
    tvl_graph = tvl_historic_graph()
    categories_bar = categories_bar_plot()
    coins_bar_chart = coins_price_change_bar_chart(), 
    coins_heatmap =  coins_price_change_heatmap(), 
    coins_group_bar_chart = a()
    historic_btc = historic_coin_price('bitcoin')
    dapps_pie = top_10_dapps_pie()
    top10_stables = top10_stablecoins_pie()
    top10_chains = top10_chains_tvl_pie()
    tvl_historic = histogram_unreleased_stablecoins_plot()
    coins_log_scatter_plot = coins_general_scatter_plot()
    btc_candle = get_ohlc_plot(['bitcoin'])

    return render_template('dashboard.html', tvl_graph=tvl_graph, dapps_pie=dapps_pie, categories_bar = categories_bar, coins_bar_chart=coins_bar_chart,
                           coins_heatmap=coins_heatmap, coins_group_bar_chart=coins_group_bar_chart, historic_btc=historic_btc, top10_stables=top10_stables,
                           top10_chains=top10_chains, tvl_historic=tvl_historic, btc_candle=btc_candle, coins_log_scatter_plot=coins_log_scatter_plot)

@app.route('/categories')
def categories(): # nope
    return render_template('categories.html')

@app.route('/contact')
def contact(): # nope
    return render_template('contact.html')

@app.route('/nft')
def nfts():
    # gets all collections
    nfts = q_nfts_collections() 
    return render_template('nfts.html', nfts = nfts)

@app.route('/other')
def other(): # nope
    return render_template('other.html')

@app.route('/stablecoins')
def stablecoins():
    # mothly table
    stables = q_stables_historic_monthly()
    # stables general 
    stables_general = q_stables_general()
    return render_template('stablecoins.html', stables=stables, stables_general=stables_general)




if __name__ == '__main__':
    app.run(debug=True)
    
    
    
    
metadata = MetaData()
coins_general = Table('coins_general', metadata,
                      Column('id', String(50), primary_key=True),
                      Column('symbol', String(10), nullable=False),
                      Column('image', String(100)),
                      Column('current_price', Numeric(15,2), nullable=False),
                      Column('market_cap', Numeric(15,2)),
                      Column('market_cap_rank', Integer(), nullable=False),
                      Column('fully_diluted_valuation', String(10), ),
                      Column('total_volume', Numeric(15,2)),
                      Column('circulating_supply',Numeric(15,0)),
                      Column('total_supply', Numeric(15,0)),
                      Column('max_supply', Numeric(15,0)),
                      Column('ath', Numeric(15,4)),
                      Column('to_ATH %', Numeric(4,2)),
                      Column('Price_Change_1Y', Numeric(4,4)),
                      Column('Price_Change_200d', Numeric(4,4)),
                      Column('Price_Change_24h', Numeric(4,4)),
                      Column('Price_Change_30d', Numeric(4,4)),
                      Column('Price_Change_7d', Numeric(4,4))
                      )  
    
    
    
    
#     import requests

# # 1. Send a GET request to the webpage containing the button
# response = requests.get('https://example.com')

# # 2. Parse the HTML content
# html_content = response.text

# # 3. Use BeautifulSoup to locate the button element
# # Find the appropriate selector or XPath that matches the button
# # For example, using a CSS selector:
# button = soup.select_one('button.download-csv-button')

# # 4. Trigger a click action on the button (if applicable)
# if button:
#     button.click()

# # 5. Wait for the file to download or handle any confirmation dialogs

# # 6. Retrieve the URL or file path of the downloaded CSV file
# # Extract the URL or file path from the response or obtain it from the browser session

# # 7. Process the downloaded CSV file as needed
# # For example, read the file using a CSV library and perform further operations

