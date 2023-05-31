import plotly.express as px
import plotly.graph_objects as go
import plotly.figure_factory as ff
import plotly.io as pio
from plotly.subplots import make_subplots
import pandas as pd
import numpy as np
from plotly.offline import plot
from crypto_queries import connect_db
import yfinance as yf
import os

# Default parameters for all plots
pio.templates.default = "simple_white"
px.defaults.template = "seaborn"
px.defaults.template = "simple_white"

current_dir = os.path.dirname(os.path.abspath(__file__))


# ///////////// Line plot of historic TVL  ////////////////////
def tvl_historic_graph():
    """
    Line chart of the global historic TVL. With range selector.
    """
    with connect_db() as connection:
        tvl = pd.read_sql('SELECT date, totalLiquidityUSD FROM tvl_historic', connection)

        fig = px.area(tvl, x='date', y="totalLiquidityUSD", title='TVL Historic', template='seaborn',
                      )
        # Update area color
        # fig.update_traces(fillcolor='blue', line_color='red')
        
        fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(count=2, label="2y", step="year", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(step="all")])))
        tvl_plot = plot(fig, output_type='div')
        
        return tvl_plot
    
    

# ///////////// Pie chart of 1o Dapps by TVL  ////////////////////
def top_10_dapps_pie():
    with connect_db() as connection:
        dapps = pd.read_sql('select name, symbol, tvl from tvl_protocols_general limit 10', connection)
        fig = px.pie(dapps, values='tvl', names='name')
        fig.update_traces(textposition='inside', textinfo='percent+label+value', hole=0.2, marker=dict(line=dict(color='black', width=1)))
        dapps_pie = plot(fig, output_type='div')
        return dapps_pie


# ///////////// Bar plot of categories (TVL and # of protocols)  ////////////////////  
def categories_bar_plot():
    with connect_db() as connection:
        categories = pd.read_sql('select tvl, protocols, avg_tvl, category from categories_tvl where  tvl > 100', connection)
        fig = px.bar(categories, x='category', y=['tvl', 'protocols'], text='tvl', title='Categories and their TVL', barmode='group')
        fig.update_traces(hovertemplate='Category: %{x}<br>TVL: %{y:,.0f}M')
        fig.update_traces(texttemplate='%{text:,.0f}M', textposition='outside', marker=dict(line=dict(color='black', width=1)))
        
        categories_bar = plot(fig, output_type='div')
        return categories_bar

# ///////////// bar chart of categories w/ their tvl and protocols on them (count)  ////////////////////
def a():
    with connect_db() as c:
        
        categories = pd.read_sql('select tvl, protocols, avg_tvl, category from categories_tvl where category not like "CEX" and tvl > 100', c)
        
        fig = go.Figure()

        fig.add_trace(go.Bar(
            x=categories.category,
            y=categories.tvl,
            name='TVL',
            offsetgroup=0,
            marker_color='blue',
            width=0.2
        ))
        
        fig.add_trace(go.Bar(
        x=categories.category,
        y=categories.protocols,
        name='protocols',
        offsetgroup=1,
        marker_color='red',
        width=0.2
        ))
        
        fig.update_layout(
            title='Categories and TVL',
            xaxis_title='Categories',
            yaxis_title='TVL',
            barmode='group',
            bargroupgap=0,
            bargap=0,
            yaxis=dict(title='TVL', side='left'),
            yaxis2=dict(title='Protocols', side='right', overlaying='y'),
            plot_bgcolor='white'
        )  
        
        fig.update_traces(marker=dict(line=dict(color='black', width=1)))

        fig = plot(fig, output_type='div')
        return fig
        
        
        
# ///////////// Heatmap of coins by price change (24h, 7d, 30d) ////////////////////
def coins_price_change_heatmap():
    with connect_db() as connection:
        coins = pd.read_sql('select name, Price_Change_24h, Price_Change_7d, Price_Change_30d from coins_general limit 30', connection)
        coin_values = []
        coin_names = []
        for index, row in coins.iterrows():
            coin_names.append(row['name'])
            coin_values.append([row['Price_Change_24h'], row['Price_Change_7d'], row['Price_Change_30d']])
        
        coin_names.reverse()
        coin_values.reverse()
        fig = ff.create_annotated_heatmap(z=coin_values, x=['24h', '7d', '30d'], y=coin_names)

        fig.update_layout(
            coloraxis=dict(colorscale='reds'),
            title='Coins Price Change Heatmap',
            font=dict(family='Arial', size=12, color='black'),
        )
        
        # fig.update_traces(textposition='inside', textinfo='percent+label+value', hole=0.2, marker=dict(line=dict(color='black', width=1)))
        coins_heatmap = plot(fig, output_type='div')
        return coins_heatmap






# ///////////// TRY to: Heatmap of coins by price change (24h, 7d, 30d) each period is a diferent heatmap ////////////////////
def coins_price_change_heatmap_per_interval(): # Not working yet! Blank plot
    with connect_db() as connection:
        coins = pd.read_sql('SELECT name, Price_Change_24h, Price_Change_7d, Price_Change_30d FROM coins_general LIMIT 10', connection)
        
        coin_24h = []
        coin_7d = []
        coin_30d = []
        coin_names = []
        for index, row in coins.iterrows():
            coin_names.append(row['name'])
            coin_24h.append([row['Price_Change_24h']])
            coin_7d.append([row['Price_Change_7d']])
            coin_30d.append([row['Price_Change_30d']])
        
        coin_names.reverse()
        
        # Reverse the order of the values
        coin_24h.reverse()
        coin_7d.reverse()
        coin_30d.reverse()
        print (coin_names)
        print (coin_30d)
        
        # Create a single heatmap with three sections
        heatmap = go.Heatmap(
            z=[coin_24h, coin_7d, coin_30d],
            x=['24h', '7d', '30d'],
            y=coin_names,
        )
        
        # Create figure and add heatmap trace
        fig = go.Figure(data=[heatmap])
        
        # Additional styling parameters
        fig.update_layout(
            font=dict(family='Arial', size=12, color='black')
        )
        
        fig.show()
        # coins_heatmap = plot(fig, output_type='div')
        
        return fig
    
# coins_price_change_heatmap_per_interval()



# ///////////// Bar plot of coins by Price change (similar to heatmap) ////////////////////
def coins_price_change_bar_chart():
    with connect_db() as connection:
        coins = pd.read_sql('select name, Price_Change_24h, Price_Change_7d, Price_Change_30d from coins_general limit 25', connection)
        coin_names = coins['name'].tolist()
        price_changes_24h = coins['Price_Change_24h'].tolist()
        price_changes_7d = coins['Price_Change_7d'].tolist()
        price_changes_30d = coins['Price_Change_30d'].tolist()

    fig = go.Figure()

    colors = ['#97DEFF', '#E5BEEC', '#002B5B']

    # bar for each price change 
    fig.add_trace(go.Bar(x=coin_names, y=price_changes_24h, name='24h',text=price_changes_24h, marker=dict(color=colors[0])))
    fig.add_trace(go.Bar(x=coin_names, y=price_changes_7d, name='7d' ,text=price_changes_7d, marker=dict(color=colors[1])))
    fig.add_trace(go.Bar(x=coin_names, y=price_changes_30d, name='30d', text=price_changes_30d, marker=dict(color=colors[2])))

    fig.update_layout(
        barmode='group',
        title='Coins Price Change',
        xaxis=dict(title='Coins'),
        yaxis=dict(title='Price Change'),
        font=dict(family='Arial', size=12, color='black'),
        plot_bgcolor='white',
    )
    
    fig.update_layout(
        shapes=[
            dict(
                type='line',
                x0=0,
                x1=len(coin_names),
                y0=0,
                y1=0,
                line=dict(color='#002B5B', width=1),
                
            )])
    fig.update_traces(textposition='outside', texttemplate='%{text:.2f}%',
                    marker=dict(line=dict(color='black', width=0.5)))
                      
    coins_bar_chart = plot(fig, output_type='div')
    return coins_bar_chart





# ///////////// Line chart of historic price of coin ////////////////////
def historic_coin_price(coin):
    with connect_db('cryptocoins') as connection:
        historic = pd.read_sql(f'SELECT timestamp, price, market_cap, total_volume FROM {coin}', connection)

        fig = px.area(historic, x='timestamp', y="price", title=f'{coin} Historic', template='seaborn', 
                    #   height=500, width=450
                      )
        
        fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(count=2, label="2y", step="year", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(step="all")])))
        historic = plot(fig, output_type='div')
        
        return historic




# ///////////// Pie plot tvl of 9 chains + others ////////////////////
def top10_chains_tvl_pie():
    with connect_db() as connection: 
        chains = pd.read_sql('select name, tokenSymbol, tvl from chains_tvl limit 10', connection)
        fig = px.pie(chains, values='tvl', names='name')
        fig.update_traces(textposition='inside', textinfo='percent+label+value', hole=0.2, marker=dict(line=dict(color='black', width=1)))
        chains_pie = plot(fig, output_type='div')
        return chains_pie



# ///////////// Plot historic Stablecoins ////////////////////
def historic_stablecoins_plot():
    with connect_db() as connection:
        stables = pd.read_sql('SELECT Date, Total_Circulating, Total_Unreleased, Total_Circulating_USD FROM hist_stables', connection)
        fig = px.line(stables, x='Date', y='Total_Circulating')
        stables_plot = plot(fig, output_type='div')
        return stables_plot
    



# ///////////// Plot historic Stablecoins w/ unreleased  ////////////////////
def histogram_unreleased_stablecoins_plot():
    with connect_db() as connection:
        
        stables = pd.read_sql('SELECT Date, Total_Circulating, Total_Unreleased, Total_Circulating_USD FROM hist_stables', connection)
        tvl = pd.read_sql('SELECT date, totalLiquidityUSD FROM tvl_historic', connection)

        fig = px.histogram(stables, x='Date', y='Total_Unreleased', nbins=50,
                        opacity=0.75, barmode='overlay', title="Stablecoins Historic & Unreleased Coins")

        line_trace = px.line(stables, x='Date', y='Total_Circulating')

        fig.add_trace(line_trace.data[0])
        
        # # Add Historical TVL (no working -- length)
        # line_trace = px.line(tvl, x=stables.Date, y='totalLiquidityUSD')

        # fig.add_trace(line_trace.data[0])
        fig = plot(fig, output_type='div')
        
        return fig



# ///////////// Pie Plot Stablecoins (10) ////////////////////        
def top10_stablecoins_pie():
    with connect_db() as connection: 
        stables = pd.read_sql('select name, market_cap, price from stables_general limit 10', connection)
        fig = px.pie(stables, values='market_cap', names='name')
        fig.update_traces(textposition='inside', textinfo='percent+label+value', hole=0.2, marker=dict(line=dict(color='black', width=1)))
        stables_plot = plot(fig, output_type='div')
        return stables_plot






# ///////////// OHLC PLOT of coins price  ////////////////////


def get_ohlc_plot(coins=['bitcoin']): # pass coins by list
    

    with connect_db() as connection:
        figures=[]
        for coin in coins:
            table_name = f"`{coin}_ohlc`" 
            ohlc = pd.read_sql(f'select date, high, low, open, close, coin from {table_name}', connection)
            fig = go.Figure(data=[go.Candlestick(x=ohlc['date'],
                                                open=ohlc.open,
                                                high=ohlc.high,
                                                low=ohlc.low,
                                                close=ohlc.close)] )
            fig.update_traces(line_width=1, selector=dict(type='candlestick'))
            
            ohlc['moving_avg_10'] = ohlc.close.rolling(window=10).mean()
            fig.add_trace(go.Scatter(x=ohlc['date'], y=ohlc['moving_avg_10'], mode='lines', name='MA-10', line_color='blue', line_width=0.25))
            
            ohlc['moving_avg_25'] = ohlc.close.rolling(window=25).mean()
            fig.add_trace(go.Scatter(x=ohlc['date'], y=ohlc['moving_avg_25'], mode='lines', name='MA-25', line_color='yellow', line_width=0.25))
            
            ohlc['moving_avg_50'] = ohlc.close.rolling(window=50).mean()
            fig.add_trace(go.Scatter(x=ohlc['date'], y=ohlc['moving_avg_50'], mode='lines', name='MA-50', line_color='black', line_width=0.25))
            
            figures.append(fig)  

    plots_html = []  # List to store the HTML plots
    for fig in figures:
        plot_html = plot(fig, output_type='div')
        plots_html.append(plot_html) 

    return plots_html

        


        
        
        

# ///////////// Coins scatter plot (vol & mcap) ////////////////////
def coins_general_scatter_plot():
    with connect_db() as connection:
        
        coins = pd.read_sql('select symbol, name, image,  market_cap, total_volume,Price_Change_24h, Price_Change_7d, Price_Change_30d, Price_Change_200d, Price_Change_1Y from coins_general limit 55', connection)

        # Outliers (btc & eth) apply log scale
        coins['total_volume'] = np.log10(coins['total_volume'])
        coins['market_cap'] = np.log10(coins['market_cap'])

        fig = px.scatter(coins, x=coins.market_cap, y=coins.total_volume, color=coins.Price_Change_24h, 
                         hover_data=['name'],
                        #  marginal_x='histogram', marginal_y="histogram", 
                         trendline="ols", trendline_color_override="black",
                         color_continuous_scale='RdYlGn', 
                        #  trendline_options=dict(log_y=True, log_x=True) # y has negative values..
                         )
        # fig = px.get_trendline_results(fig)
        
        fig = plot(fig, output_type='div')
        
        return fig



# ///////////// Vol plot ////////////////////
def volume_bar_plot(): # shitty plot
    with connect_db() as connection:
        vol = pd.read_sql('select id, symbol, name, total_volume, Price_Change_24h from coins_general limit 250', connection)
        
        # Determine the range of values for the x-axis
        x_min = vol['total_volume'].min()
        x_max = vol['total_volume'].max()

        # Adjust the number of bins for a more balanced histogram
        num_bins = 20 

        # Create the histogram
        fig = px.histogram(vol, x="total_volume", nbins=num_bins, range_x=[x_min, x_max])

        fig.show()
        return fig



# ///////////// Hero plot for front page (TVL, SNP500 & ETH price)////////////////////
def hero_plot():
    with connect_db() as connection:
        tvl = pd.read_sql('SELECT date, totalLiquidityUSD FROM tvl_historic', connection)
        snp = yf.download('^GSPC', start='2015-08-01', end='2023-05-01')
        eth = pd.read_sql('select date, close from ethereum_ohlc', connection)

        snp.index = pd.to_datetime(snp.index,unit='s')
        snp['date'] = snp.index
        merged_data = pd.concat([eth, snp])

        fig = go.Figure()

        # Add ETH line plot
        fig.add_trace(go.Scatter(x=merged_data['date'], y=merged_data['close'], mode='lines', name='ETH', yaxis='y'))

        # Add S&P 500 line plot 
        fig.add_trace(go.Scatter(x=merged_data['date'], y=merged_data['Close'], mode='lines', name='S&P 500', yaxis='y'))

        # Add TVL line plot
        fig.add_trace(go.Scatter(x=tvl['date'], y=tvl['totalLiquidityUSD'], mode='lines', name='TVL', yaxis='y2'))


        fig.update_layout(title='Total Value Locked (TVL) vs S&P 500 vs Ethereum',
                        yaxis=dict(title='Price S&P 500 & Eth', side='left'),
                        yaxis2=dict(title='TVL', side='right', overlaying='y'))
        
        fig.update_xaxes(
        rangeslider_visible=True,
        rangeselector=dict(
        buttons=list([
            dict(count=1, label="1m", step="month", stepmode="backward"),
            dict(count=6, label="6m", step="month", stepmode="backward"),
            dict(count=1, label="1y", step="year", stepmode="backward"),
            dict(count=2, label="2y", step="year", stepmode="backward"),
            dict(count=1, label="YTD", step="year", stepmode="todate"),
            dict(step="all")])))

        fig = plot(fig, output_type='div')
        return fig


# ///////////// Historic price but in area chart ////////////////////
def area_from0(): # not imllemented
    with connect_db() as connection:
        btc = pd.read_sql(f'select date, high, low, open, close, coin from bitcoin_ohlc', connection)
        # btc = btc(indexed=True)-1
        fig=px.area(btc, x=btc.date, y=btc.close)
        fig.show()
        return fig
    
  


# ///////////// Dapps ordered by category and their TVL ////////////////////
def dapps_tvl_bar_plot():
    with connect_db() as connection:
        tvl = pd.read_sql('select tvl.name, c.image, c.market_cap, c.Price_Change_24h, tvl.category, tvl.tvl, tvl.change_1d from coins_general as c join tvl_protocols_general as tvl on (c.symbol)=(tvl.symbol) or (c.name)=(tvl.name) or c.id = tvl.name order by tvl.tvl desc limit 20', connection)

        fig = px.bar(data_frame=tvl,
                          x='tvl',
                          y='name',
                          color='category',
                          opacity=0.9,
                          orientation='h',
                          barmode='relative',
                          text='tvl')
        
        fig.update_traces(texttemplate='%{text:,.0f}M', textposition='outside', marker=dict(line=dict(color='black', width=1)))
        fig = plot(fig, output_type='div')
        return fig
    

# ///////////// Dapps top10 pie plot ////////////////////
def dapps_tvl_pie_plot():
    with connect_db() as connection:
        tvl = pd.read_sql('select tvl.name, c.image, c.market_cap, c.Price_Change_24h, tvl.category, tvl.tvl, tvl.change_1d from coins_general as c join tvl_protocols_general as tvl on (c.symbol)=(tvl.symbol) or (c.name)=(tvl.name) or c.id = tvl.name order by tvl.tvl desc limit 20', connection)
        
        tvl = tvl.sort_values('tvl', ascending=False)
        top_9 = tvl.iloc[:10] # top 9 coins
        
        other_sum = tvl.iloc[10:]['tvl'].sum() # sum all other coins as #10th coin
        
        other_row = {'name': 'Other', 'tvl': other_sum} # add other coins in the df
        tvl = top_9.append(other_row, ignore_index=True)
        
        fig = px.pie(
            data_frame=tvl,
            values='tvl',
            names='name',
            color='category',
            title='TVL Distribution',
            hole=0.2,
            labels={"name":"Name",
                    "tvl":"TVL",
                    "market_cap":"Market Cap",
                    "category":"Category",},
            opacity=0.8,
            
        )
        fig.update_traces(textposition='inside', textinfo='percent+label+value', marker=dict(line=dict(color='black', width=1)))
        fig = plot(fig, output_type='div')
        return fig

    

# ///////////// Chains bar plot (tvl & mcap) ////////////////////
def chains_bar_plot():
    with connect_db() as connection:
        chains = pd.read_sql('select cg.id, cg.market_cap, ct.tvl, cg.symbol, cg.name,ct.index, ct.gecko_id , ct.chainId  from coins_general as cg join chains_tvl as ct on cg.id = ct.gecko_id or cg.name = ct.name or cg.symbol = ct.tokenSymbol order by ct.tvl desc limit 25', connection)
        fig = px.bar(data_frame=chains,
                          x='tvl',
                          y='name',
                          color='market_cap',
                          opacity=0.9,
                          orientation='h',
                          barmode='relative',
                          text='tvl',
                          color_continuous_scale=px.colors.diverging.RdBu,
                          
                          )
        
        
        # fig = px.colors.sequential.Purples()
        
        fig.update_traces(texttemplate='%{text:,.0f}M', textposition='outside', marker=dict(line=dict(color='black', width=1)))
        # fig = plot(fig, output_type='div') 
        fig.show()
        return fig

# chains_bar_plot()


# ///////////// Hero plot for Chains page. All, distributed ////////////////////
def get_chains_area_plot():
    with connect_db() as connection:
        path = os.path.join(current_dir, 'static', 'csv', 'chains_tvl_historic_top10.csv')
        df = pd.read_csv(path, index_col='Date')
            
        fig = px.area(df, x=df.index, y=df.columns,
#               hover_data={df.index: "|%B %d, %Y"},
              title='Top 10 Chains Over Time')
        fig.update_xaxes(
            dtick="M1",
            tickformat="%b\n%Y")
        fig = plot(fig, output_type='div') 
        return fig


# ///////////// Plot with the daily pct change of the coin + moving avgs ////////////////////
def get_chains_daily_pct_plot(coin='Ethereum'):
        # pct_change_1d = pd.read_csv(r"C:\Users\34633\Desktop\HelloWorld\mis_mierdas\jupyter_Notebook\data_crypto_page\chains_historic_1d_pct_change.csv", index_col='Date')

        pct_change_1d_path = os.path.join(current_dir, 'static', 'csv', 'chains_historic_1d_pct_change.csv')
        pct_change_1d = pd.read_csv(pct_change_1d_path, index_col='Date')
    
    
        # calculate the 7-day moving average using rolling window
        ma_7d = pct_change_1d.rolling(window=7).mean()
        ma_30d = pct_change_1d.rolling(window=30).mean()


        fig = px.bar(pct_change_1d, x=pct_change_1d.index, y=coin, title=f'{coin} Daily pct Change')

        fig.add_trace(
            go.Scatter(x=ma_7d.index, y=ma_7d[coin], mode="lines", line=dict(color="red", width=0.8))
            )

        fig.add_trace( go.Scatter(x=ma_30d.index, y=ma_30d[coin], mode="lines", line=dict(color="black", width=0.8))
        )
        fig = plot(fig, output_type='div') 
        return fig
    
    
def chains_bar_tvl_mcap():
    with connect_db() as connection:
            chains = pd.read_sql('select cg.id, cg.market_cap, ct.tvl, cg.symbol, cg.name,ct.index, ct.gecko_id , ct.chainId  from coins_general as cg join chains_tvl as ct on cg.id = ct.gecko_id or cg.name = ct.name or cg.symbol = ct.tokenSymbol order by ct.tvl desc limit 25', connection)
            fig = px.bar(data_frame=chains,
                            x='tvl',
                            y='name',
                            color='market_cap',
                            opacity=0.9,
                            orientation='h',
                            barmode='relative',
                            text='tvl',
                            color_continuous_scale=px.colors.diverging.RdBu,
                            log_x=True,
                        
                            
                            )
        
        
        # fig = px.colors.sequential.Purples()
        
            fig.update_traces(texttemplate='%{text:,.0f}M', textposition='outside', marker=dict(line=dict(color='black', width=1)), )
            fig = plot(fig, output_type='div')
            return fig
        
    
# get_chains_daily_pct_plot()    
# format: https://github.com/d3/d3-format/tree/v1.4.5#d3-format


        





        
 



    
