import numpy as np
import pandas as pd
import sqlalchemy as db
from sklearn import preprocessing

## Create database engine
sqlite_file = 'data/bike.sqlite'
engine = db.create_engine('sqlite:///' + sqlite_file)

def get_OD(h1,h2):
    """
    obtain mean duration for pickups/returns
    and number of starts/ends per hour
    return a joined dataframe for data storage
    """
    #getting number of pickups / returns between hour1 and hour2
    hour1 = '"'+h1+'"'
    hour2 = '"'+h2+'"'
    #mean duration when pickup and number of pickups
    O_hour = pd.read_sql_query('SELECT [start station name] AS Station, '
                                 '[start station id] AS ID, '
                                 'AVG(tripduration)/60 AS mean_duration_O' + h1 + h2 + 
                               ' , COUNT (*) AS O_' + h1 + h2 + 
                               ' FROM bike '
                               'WHERE strftime(\'%H\', starttime) >= ' + hour1 + 
                               ' AND strftime(\'%H\', starttime) < ' + hour2 + 
                               ' AND tripduration < 86400 '
                               'GROUP BY [start station name]', engine)
    #mean duration when return and number of returns
    D_hour = pd.read_sql_query('SELECT [end station name] AS Station, '
                                 '[end station id] AS ID, '
                               'AVG(tripduration)/60 AS mean_duration_D' + h1 + h2 + 
                               ', COUNT (*) AS D_' + h1 + h2 + 
                               ' FROM bike '
                               'WHERE strftime(\'%H\', stoptime) >= ' + hour1 + 
                               ' AND strftime(\'%H\', stoptime) < ' + hour2 + 
                               ' AND tripduration < 86400 '
                               'GROUP BY [end station name]', engine)
    #merge two dataframes
    OD_hour = pd.merge(O_hour, D_hour, on=['Station','ID'], how='outer')
    #drop missing values
    OD_hour = OD_hour.dropna()
    
    print(h1+h2,'\t','completed.')
    return OD_hour

def clean_OD(OD):
    """
    clean the OD data.
    Argument: 
        OD: the dataframe of extracted temporal dataset. 
    """
    #obtain daily average pickups/returns
    for i in np.arange(3, 3+2*48, 2):
        OD.iloc[:,i] = OD.iloc[:,i]/365 #365: converting total annual value to daily

    #ID should be positive and unique
    OD = OD.drop_duplicates('ID')
    OD = OD[OD['ID']>0]
    #sort ID ascending
    OD = OD.sort_values(by='ID')
    #avoid missing values when calculating
    OD = OD.fillna(0)

    #calculation of total daily pickups and returns
    OD['pickup_sum'] = OD.iloc[:,np.arange(3,3+4*24,4)].sum(axis=1)
    OD['return_sum'] = OD.iloc[:,np.arange(5,5+4*24,4)].sum(axis=1)

    #calculation of average daily pickup-trip duration and return-trip duration
    p,r=0,0
    for i in range(24):
        #weighted daily pickup sumation = mean duration of pickup * number of pickups
        p = p+ OD.iloc[:,2+i*4]*OD.iloc[:,3+i*4]
        #weighted daily return sumation = mean duration of return * number of return
        r = r+ OD.iloc[:,4+i*4]*OD.iloc[:,5+i*4]
    #average daily pickup-trip duration and return-trip duration
    OD['pickup_duration'] = p/OD['pickup_sum']
    OD['return_duration'] = r/OD['return_sum']
    
    return OD

def standardize(df):
    """
    Conduct standardization of da dataframe. 
    Argument: a pandas dataframe without standardization
    Return: a standardized dataframe
    """
    
    x0 = df.values      #returns a numpy array
    min_max_scaler = preprocessing.MinMaxScaler()
    x_scaled = min_max_scaler.fit_transform(x0)
    df_s = pd.DataFrame(x_scaled)
    
    return df_s