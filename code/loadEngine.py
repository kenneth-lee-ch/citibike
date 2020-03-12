import os
from extract import *

def loadEngine(sqlfile):
    """
    Determine whether we can use the existing sqlite file to create an engine or we need to scrape a web to create the sqlite file

    Arg:
        sqlfile(str): a sqlite file name

    Return:
        engine (object): an sqlalchemy Engine instance.
    """
    # Load the data
    datapath = '../data/'
    # Check if the SQLite file exists in the data folder
    if os.path.exists(datapath + sqlfile):
        # If the SQL file has already been created, you can call create_engine to get the engine
        engine = sqla.create_engine('sqlite:///' + datapath + sqlfile)
    # If it doesn't exist, we create a new one
    else:
        # Set the default bucket name
        bucketname = "tripdata"
        # Get all these files
        files = ["201901-citibike-tripdata.csv.zip",
                 "201902-citibike-tripdata.csv.zip",
                 "201903-citibike-tripdata.csv.zip",
                 "201904-citibike-tripdata.csv.zip",
                 "201905-citibike-tripdata.csv.zip",
                 "201906-citibike-tripdata.csv.zip",
                 "201907-citibike-tripdata.csv.zip",
                 "201908-citibike-tripdata.csv.zip",
                 "201909-citibike-tripdata.csv.zip",
                 "201910-citibike-tripdata.csv.zip",
                 "201911-citibike-tripdata.csv.zip",
                 "201912-citibike-tripdata.csv.zip",]
        # Get the table name from the sql name e.g. if sqlfile = "bike.sqlite", then returns "bike"
        tablename = os.path.splitext(os.path.basename(sqlfile))[0]
        # Make request to the AWS S3 public bucket to get the desired files and convert them into a database
        engine = getData(bucketname, files, tablename)
    return engine