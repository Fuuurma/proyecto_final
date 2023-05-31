from sqlalchemy import create_engine
from sqlalchemy import MetaData
from sqlalchemy import (Table, text, Column)
from sqlalchemy.sql import (select, desc, asc, join)
import matplotlib.pyplot as plt
import pandas as pd
import os


# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
# Define Functions that'll query the Datbase
# /////////////////////////////////////////////////////////////////////////////////////////////////////////////////////////
current_dir = os.path.dirname(os.path.abspath(__file__))


# ////// Conecction /////////////////    
def connect_db(database='data_crypto'):
    """
    Function to establish connection wih MySQL server and our database (by default data_crypto)
    """
    user='root'
    password='240699'
    host='127.0.0.1'
    database=database
    
    engine = create_engine(f"mysql+pymysql://{user}:{password}@{host}/{database}")
    try:
        connection = engine.connect()
        return connection
    except Exception as e:
        raise e
    

# ///////////// coins general  /////////////////// 
def q_coins_general(sort='market_cap_rank', limit = 50): # Works (finsih All colujmns)
    """
    Gets general information of Top 250 coins (ids, mcap, vol, supply..)
    """
    with connect_db() as connection:
        metadata = MetaData()
        coins_general = Table('coins_general', metadata, autoload=True, autoload_with=connection)
        _select = select([coins_general.c.market_cap_rank,coins_general.c.image, coins_general.c.name, coins_general.c.symbol, coins_general.c.current_price,
                          coins_general.c.market_cap, coins_general.c.fully_diluted_valuation, coins_general.c.total_volume, coins_general.c.circulating_supply,
                          coins_general.c.total_supply, coins_general.c.max_supply, coins_general.c.to_ATH_pct, coins_general.c.Price_Change_24h,
                          coins_general.c.Price_Change_7d, coins_general.c.Price_Change_30d,coins_general.c.Price_Change_200d, coins_general.c.Price_Change_1Y])
        _select = _select.limit(limit)
        result = _select.order_by(asc(sort))
        result = connection.execute(result)
        return result
    

# ////// coins general select only specific columns ///////////////// 
def q_coins_general_specific_columns(columns, sort='market_cap_rank', descending=True, limit=5):
    """
    Gets specific columns of Top 250 coins
    """
    with connect_db() as connection:
        metadata = MetaData()
        coins_general = Table('coins_general', metadata, autoload=True, autoload_with=connection)
        selected_columns = [getattr(coins_general.c, column) for column in columns]
        _select = select(selected_columns)
        _select = _select.limit(limit)
        if descending ==True:
            result = _select.order_by(desc(sort))
            result = connection.execute(result)
        else:
            result = _select.order_by(asc(sort))
            result = connection.execute(result)   
        return result







        
        
 # ///////////// TVL of Today  ///////////////////                          

def get_tvl_today(limit = 1):
    with connect_db() as connection:
        metadata = MetaData()
        tvl = Table('tvl_historic_pct', metadata, autoload=True, autoload_with=connection)
        _select = select([tvl.c.totalLiquidityUSD, ])
        
        _select = select([tvl.c.date, tvl.c.totalLiquidityUSD, tvl.c.pct_change_yesterday, tvl.c.pct_change_7days, 
                           tvl.c.pct_change_30days, tvl.c.pct_change_90days, tvl.c.pct_change_200days, tvl.c.pct_change_1y])
         
        _select = _select.order_by(desc(tvl.c.date))
        _select = _select.limit(limit)
        result = connection.execute(_select)
        return result
    

 # ///////////// Table coins with other stats like median and averages  /////////////////// 
def get_coins_general_statistics(limit=1):
    with connect_db() as connection:
        metadata = MetaData()
        
        data = Table('coins_general_statistics', metadata, autoload=True, autoload_with=connection)
        _select = select ([data.c.market_cap_rank, data.c.id, data.c.symbol, data.c.name, data.c.market_cap_sum, data.c.market_cap_avg, data.c.market_cap_median,
                           data.c.total_volume_sum, data.c.total_volume_avg, data.c.total_volume_median, data.c.Price_Change_24h_avg, data.c.Price_Change_24h_median, 
                           data.c.Price_Change_7d_avg, data.c.Price_Change_7d_median, data.c.Price_Change_30d_avg, data.c.Price_Change_30d_median, 
                           data.c.Price_Change_200d_avg, data.c.Price_Change_200d_median, data.c.Price_Change_1y_avg, data.c.Price_Change_1y_median])
        _select = _select.limit(limit)
        result = connection.execute(_select)
        return result
        
    
# ////// Coins Price change by timeframes (Winners and Losers)   ///////////////// 
def q_coin_winners_timeframe(timeframe='24h', limit=5):
    with connect_db() as connection:
        metadata = MetaData()
        winners = Table(f'winners_{timeframe}_top', metadata, autoload=True, autoload_with=connection)
        if timeframe == '24h':
            col = winners.c.Price_Change_24h
        elif timeframe == '7d':
            col = winners.c.Price_Change_7d
        elif timeframe == '30d':
            col = winners.c.Price_Change_30d
        elif timeframe == '200d':
            col = winners.c.Price_Change_200d
        elif timeframe == '1y':
            col = winners.c.Price_Change_1Y
        else:
            raise ValueError(f"Invalid timeframe: {timeframe}")
            
        _select = select([winners.c.name, col])
        _select = _select.limit(limit)
        result = connection.execute(_select)
        return result
    
    

def q_coin_losers_timeframe(timeframe='24h', limit=5):
    with connect_db() as connection:
        metadata = MetaData()
        losers = Table(f'losers_{timeframe}_top', metadata, autoload=True, autoload_with=connection)
        if timeframe == '24h':
            col = losers.c.Price_Change_24h
        elif timeframe == '7d':
            col = losers.c.Price_Change_7d
        elif timeframe == '30d':
            col = losers.c.Price_Change_30d
        elif timeframe == '200d':
            col = losers.c.Price_Change_200d
        elif timeframe == '1y':
            col = losers.c.Price_Change_1Y
        else:
            raise ValueError(f"Invalid timeframe: {timeframe}")
            
        _select = select([losers.c.name, losers.c.image, col])
        _select = _select.where(col.isnot(None))
        _select = _select.limit(limit)
        result = connection.execute(_select)
        return result
    


        
        


def q_tvl_prototocols_general():
    """
    Get general tvl data from all protocols
    """
    pass

 # ///////////// Get coins ordered by x columns  /////////////////// 

def q_top_coins_by_price_change(time_interval, number_of_coins):
    """
    Top x Coins by price change %. Interval (24h, 7d, 30d...)
    """
    with connect_db() as connection:
        metadata = MetaData()
        top_coins = Table(f'top_coins_{time_interval}', metadata, autoload=True, autoload_with=connection)
        _select = select([top_coins.c.name, top_coins.c.Price_Change_24h])
        _select = _select.order_by(desc(top_coins.c.Price_Change_24h))
        _select = _select.limit(number_of_coins)
        result = connection.execute(_select)
        return result

def q_top_protocols_by_tvl_change(time_interval, number_of_protocols):
    """
    Top x Dapps by TVL change %. (24h, 7d, 30d...)
    """
    pass

def q_top_chains_by_tvl_change(time_interval, number_of_chains):
    """
    Top x Chains by TVL change %. (24h, 7d, 30d...)
    """
    
    pass

# ////// Monthly TVL Historic with Plot  ///////////////// 
def q_tvl_historic(plot=False): # Works
    """
    Get Historic TVL of the Global Space.
    """
    if not plot:
        with connect_db() as connection:
            metadata = MetaData()
            tvl_historic = Table('tvl_historic', metadata, autoload=True, autoload_with=connection)
            _select = select([tvl_historic.c.date, tvl_historic.c.totalLiquidityUSD]).filter(text("date LIKE '%-%-01%'"))
            _select = _select.order_by(desc(tvl_historic.c.date))
            result = connection.execute(_select)
            return result
    else:
        result = q_tvl_historic()

        dates = []
        tvl = []

        for row in result:
            dates.append(row[0])
            tvl.append(row[1])

        plt.plot(dates, tvl)
        plt.xlabel('Date')
        plt.ylabel('TVL (in Millions$)')
        plt.title('Total Value Locked')
        plt.show()
        
        
        

 # ///////////// Get TVL (used for tvl Actual and ATH)  /////////////////// 

def q_tvl_historic_specific(columns, sort='date', descending=True, interval='monthly', limit=1): # Works
    """
    Get Historic TVL of the Global Space.
    """
    with connect_db() as connection:
        metadata = MetaData()
        tvl_historic = Table('tvl_historic', metadata, autoload=True, autoload_with=connection)
        selected_columns = [getattr(tvl_historic.c, column) for column in columns]
        if 'date' in columns:
            if interval == 'monthly':
                _select = select(selected_columns).filter(text("date LIKE '%-%-01%'"))
            elif interval == 'daily':
                _select = select(selected_columns)
            elif interval == 'weekly':
                _select = select(selected_columns).filter(text("date LIKE '%-%-01%'"))
            else:
                _select = select(selected_columns).filter(text("date LIKE '%-01-01%'"))
        if descending:
            _select = _select.order_by(desc(sort))
        else:
            _select = _select.order_by(asc(sort))
        _select = _select.limit(limit)
        result = connection.execute(_select)
        return result


 # ///////////// Get TVL change pct's  /////////////////// 

def q_tvl_pct_change():
    with connect_db() as connection:
        metadata = MetaData()
        tvl_pct = Table('tvl_historic_pct', metadata, autoload=True, autoload_with=connection)
        _select = select([tvl_pct.c.index, tvl_pct.c.date, tvl_pct.c.totalLiquidityUSD, tvl_pct.c.pct_change_yesterday, tvl_pct.c.pct_change_7days, 
                          tvl_pct.c.pct_change_30days, tvl_pct.c.pct_change_90days, tvl_pct.c.pct_change_200days, tvl_pct.c.pct_change_1y])
        _select = _select.order_by(desc(tvl_pct.c.index)).limit(1)
        result = connection.execute(_select)
        return result



# ////// Historic TVL of each Chain  ///////////////// 
def q_tvl_chain_historic(chain): 
    """
    Get Historic TVL of each chain.
    """
    with connect_db() as connection:
        metadata = MetaData()
        tvl_chain_historic = Table(f'tvl_{chain}', metadata, autoload=True, autoload_with=connection)
        _select = select([tvl_chain_historic.c.date, tvl_chain_historic.c.totalLiquidityUSD])
        _select = _select.order_by(asc(tvl_chain_historic.c.date))
        result = connection.execute(_select)
        
        return result
    

# ////// DAPPS Current TVL and other metrics  ///////////////// 
def q_dapps_tvl():
    """
    Get actual TVL from all dapps
    """
    with connect_db() as connection: 
        metadata = MetaData()
        dapps_tvl = Table('tvl_protocols_general', metadata, autoload=True, autoload_with=connection)
        _select = select([dapps_tvl.c.index, dapps_tvl.c.name, dapps_tvl.c.symbol, dapps_tvl.c.category, dapps_tvl.c.tvl, dapps_tvl.c.change_1d, dapps_tvl.c.change_7d]).limit(100)
        result = connection.execute(_select)
        return result


# ////// DAPPS Current TVL and other metrics specific columns  ///////////////// 
def q_dapps_tvl_specific(columns, sort='tvl', descending=True, limit=5):
    """
    Get actual TVL from all dapps
    """
    with connect_db() as connection: 
        metadata = MetaData()
        dapps_tvl = Table('tvl_protocols_general', metadata, autoload=True, autoload_with=connection)
        selected_columns = [getattr(dapps_tvl.c, column) for column in columns]
        _select = select(selected_columns)
        for column in columns:
            if column.startswith('change_'):
                _select = _select.where(getattr(dapps_tvl.c, column).isnot(None))
        if descending:
            _select = _select.order_by(desc(sort))
        else:  
            _select = _select.order_by(asc(sort))
        _select = _select.limit(limit)
        result = connection.execute(_select)
        return result




# ////// Historic Stables  /////////////////
def q_stables_historic_monthly():
    with connect_db() as connection: 
        metadata = MetaData()
        hist_stables = Table('hist_stables', metadata, autoload=True, autoload_with=connection)
        _select = select([hist_stables.c.Date, hist_stables.c.Total_Circulating, hist_stables.c.Total_Unreleased, hist_stables.c.Total_Circulating_USD])
        _select = _select.filter(text("Date LIKE '%-%-01%'"))
        result = connection.execute(_select)
        return result
    
    
 # ///////////// Get Stables General Information of all stables  /////////////////// 
def q_stables_general():
    with connect_db() as connection: 
        metadata = MetaData()
        stables = Table('stables_general', metadata, autoload=True, autoload_with=connection)
        _select = select([stables])
        _select = _select.limit(100)
        result = connection.execute(_select)
        return result
    
    
    

# ////// Chains actual TVL  /////////////////
def q_chains_actual_tvl():
    with connect_db() as connection: 
        metadata = MetaData()
        chains_tvl = Table('chains_tvl', metadata, autoload=True, autoload_with=connection)
        _select = select([chains_tvl.c.gecko_id, chains_tvl.c.tvl, chains_tvl.c.tokenSymbol, chains_tvl.c.cmcId, chains_tvl.c.name, chains_tvl.c.chainId])
        result = connection.execute(_select)
        return result


 # ///////////// Get Stables MCAP  /////////////////// 
def q_get_actual_stablecoins_mcap():
    with connect_db() as connection:
       stables =  pd.read_sql('select round(sum(market_cap),0) from stables_general', connection)
    return stables.iloc[0, 0]

 # ///////////// Get Volume Today /////////////////// 
def q_get_actual_volume_today():
    with connect_db() as connection:
       volume =  pd.read_sql('select sum(total_volume) from coins_general', connection)
    return volume.iloc[0, 0]

 # ///////////// Get Dex Volumes sort by columns /////////////////// 
def q_top_dex_volume(limit=10, sort='dailyVolume', descending=True):
    with connect_db() as connection:
        dex_df = pd.read_sql('SELECT name, logo, change_1d, change_7d, change_1m, dailyVolume, total7d, total30d, totalAllTime, chains FROM dex_volumes ORDER BY total24h DESC', connection)
        metadata = MetaData()
        dex = Table('dex_volumes', metadata, autoload=True, autoload_with=connection)
        _select = select([dex.c.name, dex.c.logo, dex.c.dailyVolume, dex.c.change_1d,
                          dex.c.change_7d, dex.c.change_1m, dex.c.total7d, dex.c.total30d,
                          dex.c.totalAllTime, dex.c.chains])
        if descending:
            _select = _select.order_by(desc(sort))
        else:
            _select = _select.where(dex.c[sort].isnot(None)).order_by(asc(sort))
            _select = _select.where(dex.c[sort] > 1)
        
        _select = _select.limit(limit)
        result = connection.execute(_select)
        return result
    
 # ///////////// Get SUM of Total Volume  ///////////////////   
def q_get_daily_total_volume():
    with connect_db() as connection:
        dex_df = pd.read_sql('select sum(dailyVolume) as vol from dex_volumes', connection)
        return dex_df

    
        
# ///////////// DF with coins_general + tvl_general  ////////////////////
def df_coins_general_with_tvl():
    with connect_db() as connection:
        df =  pd.read_sql('select * from coins_general as c join tvl_protocols_general as tvl on (c.symbol)=(tvl.symbol) or (c.name)=(tvl.name) or c.id = tvl.name order by tvl.tvl desc;', connection)
        return df
    
# ///////////// Query with coins_general + tvl_general  ////////////////////
def coins_general_with_tvl(): 
    with connect_db() as connection:
        metadata = MetaData()
        coins_general = Table('coins_general', metadata, autoload=True, autoload_with=connection)
        tvl_protocols_general = Table('tvl_protocols_general', metadata, autoload=True, autoload_with=connection)
        
        join_condition = ((coins_general.c.symbol == tvl_protocols_general.c.symbol) | (coins_general.c.name == tvl_protocols_general.c.name) | (coins_general.c.id == tvl_protocols_general.c.name))
        
        _select = select([coins_general, tvl_protocols_general]).select_from(coins_general.join(tvl_protocols_general, join_condition)).order_by(tvl_protocols_general.c.tvl.desc())
        
        
        result = connection.execute(_select)
    return result
        
        
# ///////////// DQuery coins_general + chains_general  ////////////////////
def chains_with_all_metrics():
    with connect_db() as connection: 
        metadata = MetaData()
        coins_general = Table('coins_general', metadata, autoload=True, autoload_with=connection)
        chains_tvl = Table('chains_tvl', metadata, autoload=True, autoload_with=connection)
        
        joins = ((coins_general.c.symbol == chains_tvl.c.tokenSymbol) | 
                      (coins_general.c.name == chains_tvl.c.name) |
                      (coins_general.c.id == chains_tvl.c.gecko_id))
        
        
        _select = select([
                coins_general.c.id, coins_general.c.market_cap, 
                chains_tvl.c.tvl, coins_general.c.symbol, 
                coins_general.c.name, chains_tvl.c.name, 
                chains_tvl.c.index, chains_tvl.c.gecko_id , 
                chains_tvl.c.chainId, 
                (coins_general.c.market_cap / chains_tvl.c.tvl).label('MCAP_ratio'),  
                (coins_general.c.fully_diluted_valuation / chains_tvl.c.tvl).label('FDV_ratio'), 
                (coins_general.c.total_volume / chains_tvl.c.tvl).label('Vol_ratio')
            ]).select_from(coins_general.join(chains_tvl, joins))
        
        _select = _select.order_by(chains_tvl.c.tvl.desc())       
        
        result = connection.execute(_select)
        return result
    

# ///////////// Query table with all data (coins + chains + tvl) not all cols have values!  ////////////////////
def table_coins_general_tvl(limit=1):
    with connect_db() as connection:
        metadata = MetaData()
        coins = Table('coins_general_tvl', metadata, autoload=True, autoload_with=connection)
        _select = select([coins])
        _select = _select.limit(limit)
        result = connection.execute(_select)
        return result
    
    
    
# ///////////// Return df of chains historic of today (TVL of ALL chains)  ////////////////////   
def tvl_chains_historic():
    tvl_path = os.path.join(current_dir, 'static', 'csv', 'chains_tvl_historic.csv')
    tvl = pd.read_csv(tvl_path, index_col='Date')
    
    # tvl = pd.read_csv(r"C:\Users\34633\Desktop\HelloWorld\mis_mierdas\jupyter_Notebook\data_crypto_page\chains_tvl_historic.csv", index_col='Date')
    return tvl.iloc[-1]


# ///////////// Returns 3 df's of  TVL pct change of chains (1d, 7d, 30d)  ////////////////////


def tvl_chains_pct_change():
    
    csv_1d_path = os.path.join(current_dir, 'static', 'csv', 'chains_historic_1d_pct_change.csv')
    csv_7d_path = os.path.join(current_dir, 'static', 'csv', 'chains_historic_7d_pct_change.csv')
    csv_30d_path = os.path.join(current_dir, 'static', 'csv', 'chains_historic_30d_pct_change.csv')
    
    change_1d = pd.read_csv(csv_1d_path, index_col='Date')
    change_7d = pd.read_csv(csv_7d_path, index_col='Date')
    change_30d = pd.read_csv(csv_30d_path, index_col='Date')
    
    # today
    change_1d = change_1d.iloc[-1]
    change_7d = change_7d.iloc[-1]
    change_30d = change_30d.iloc[-1]
    
    return change_1d, change_7d, change_30d



# ///////////// Get Categories with TVL  ////////////////////
def q_categories_tvl():
     with connect_db() as connection:
        metadata = MetaData()
        categories = Table('categories_tvl', metadata, autoload=True, autoload_with=connection)
        _select = select([categories])
        result = connection.execute(_select)
        return result
    
    


# ///////////// Get NFT collections ////////////////////
def q_nfts_collections():
    # Need to pass before the names of each nft collection
    nfts = ['cryptopunks', 'bored-ape-yacht-club', 'mutant-ape-yacht-club',
            'the-crop-collective', 'azuki', 'chromie-squiggle-by-snowfro',
            'the-captainz', 'autoglyphs', 'degods',
            'otherdeed-for-otherside', 'sandbox', 'clonex',
            'decentraland', 'fidenza-by-tyler-hobbs', 'milady-maker',
            'wrapped-cryptopunks', 'metamon', 'pudgy-penguins',
            'bored-ape-kennel-club', 'meebits', 'otherside-koda',
            'the-potatoz', 'ringers-by-dmitri-cherniak', 'otherdeed-expanded', 'beanz-official']
    
    with connect_db() as connection:
        metadata = MetaData()
        result = []

        for nft in nfts:
            table_name = f"nft_{nft}" 
            nfts_ = Table(table_name, metadata, autoload=True, autoload_with=connection)
            
            table_name_img = f"nft_{nft}_images" 
            imgs = Table(table_name_img, metadata, autoload=True, autoload_with=connection)
            
            join_condition = (nfts_.c.id == imgs.c.id )
            
            join_stmt = join(nfts_, imgs, join_condition)
            
            _select = select([nfts_, imgs.c.image]).select_from(join_stmt)
            
            result.extend(connection.execute(_select))
        
        return result

# ///////////// Get Chains by pct Change (1d, 7d, 30d)  ////////////////////
def q_get_chains_by_pct_change(asc=False, limit=5, days=1):
    with connect_db() as connection:
        if days==1:
            chains_path = os.path.join(current_dir, 'static', 'csv', 'chains_historic_1d_pct_change.csv')
            chains = pd.read_csv(chains_path, index_col='Date')
    
            # chains = pd.read_csv(r"C:\Users\34633\Desktop\HelloWorld\mis_mierdas\jupyter_Notebook\data_crypto_page\chains_historic_1d_pct_change.csv", index_col='Date')
        elif days==7:
            chains_path = os.path.join(current_dir, 'static', 'csv', 'chains_historic_7d_pct_change.csv')
            chains = pd.read_csv(chains_path, index_col='Date')
            # chains = pd.read_csv(r"C:\Users\34633\Desktop\HelloWorld\mis_mierdas\jupyter_Notebook\data_crypto_page\chains_historic_7d_pct_change.csv", index_col='Date')
        elif days==30:
            chains_path = os.path.join(current_dir, 'static', 'csv', 'chains_historic_30d_pct_change.csv')
            chains = pd.read_csv(chains_path, index_col='Date')
            # chains = pd.read_csv(r"C:\Users\34633\Desktop\HelloWorld\mis_mierdas\jupyter_Notebook\data_crypto_page\chains_historic_30d_pct_change.csv", index_col='Date')
            
        
        if not asc:
            results = chains.iloc[-1].sort_values(ascending=False).head(limit)
            
        else: results = chains.iloc[-1].sort_values(ascending=True).head(limit)

        return results
        
    

def tvl_top100_protocols(days):
    tvl_protocols_path = os.path.join(current_dir, 'static', 'csv', 'top_100_protocols_tvl.csv')
    tvl_protocols = pd.read_csv(tvl_protocols_path, index_col='Date')
    # Add a new index column
    tvl_protocols = tvl_protocols.reset_index()

    tvl_protocols = tvl_protocols.sort_values('index', ascending=False).head(days)
    return tvl_protocols





# class Coins_General(db.Model):
#     __tablename__ = 'coins_general'

#     market_cap_rank = db.Column(db.Integer, primary_key=True)
#     id = db.Column(db.String(50))
#     symbol = db.Column(db.String(10))
#     name = db.Column(db.String)
#     image = db.Column(db.String(100))
#     current_price = db.Column(db.Float)
#     market_cap = db.Column(db.Float(12,2))
#     fully_diluted_valuation = db.Column(db.Float(12,2))
#     total_volume = db.Column(db.Float(12,2))
#     circulating_supply = db.Column(db.Float)
#     total_supply = db.Column(db.Float)
#     max_supply = db.Column(db.Float)
#     ath = db.Column(db.Float(12,2))
#     to_ATH_pct = db.Column(db.Float(4,2))
#     price_change_24h = db.Column(db.Float(5,2))
#     price_change_7d = db.Column(db.Float(5,2))
#     price_change_30d = db.Column(db.Float(6,2))
#     price_change_200d = db.Column(db.Float(6,2))
#     price_change_1Y = db.Column(db.Float(6,2))

#     def __repr__(self):
#         return f'<Coins_General {self.name}>'


    
