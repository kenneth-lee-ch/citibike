# CitiBike System Data Analysis

## Introduction

Citi Bike is New York City’s bike share system established in 2013. It has become a vital part of the transportation network in New York City. It is available for use throughout the entire year. All the riders have access to thousands of bikes at hundreds of stations across Manhattan, Brooklyn, Queens and Jersey City. In this work, we would like to explore the characteristics of this bike share system and come up with recommendations that may improve the current program based on data analysis wtih the Citi Bike system 2019 data that is publicly available.

According to a New York magazine, Intelligencer (https://nymag.com/intelligencer/2014/03/citi-bikes-four-huge-problems.html), there are some problems the citi-bike share system faced in 2014. We summarize them as follows:

* How can we increase the number of customer (one-time user)?

* Do we have any suggestion to attract more users, especially customer, during Winter?

* Riders complained as bikes went missing for maintenance or protection, leaving certain stations empty for days at a time, what can we do with that problem?

In this work, we would like to explore the characteristics of this bike share system and try to come up with recommendations to provide potential solutions for the questions above based on data analysis wtih the Citi Bike system 2019 data that is publicly available.

## File Directory Description

* `/code/`: this folder contains all the python necessarily to run the code in the jupyter notebook.
	
	* `extract.py`: this file scrapes the data files directly from the source of the CitiBike webpage by making requests to a Amazon Web Serivces S3 public bucket. It downloads all citibike data file in 2019 and convert them into a table in a SQLite database. 

	* `loadEngine.py`: this file checks the `/data/` folder if it is needed to create a new SQLite file. When the data folder is empty, it will call extract.py to scrape the web and create a SQL engine instance and store all the 2019 citibike data. 

	* `getod.py`:

	* `cluster_metric:` this file contains codes to evaluate the clusters by using Silhouette score and Davies-Bouldin scores in the `sklearn` library.

* `/notebook/`: this folder contains the main report writeup.

	`Citbike System Data Analysis.ipynb`: this is our main report file name. 

* `/images/`: since we make use of a Python packaged called `keplergl` to create some geographic plots, it requires some specific setup in order to display the image properly on a jupyter notebook. We put the output static images into this folder and display them on jupyter notebook instead. 

* `/data/`: this folder stores all data files. However, this folder is empty since our data file is over 100MB (around 3.6GB), we don't include the data file as instructed.

## How to run the code

You only need to run the code on the jupyter notebook. Everything should work fine. It will take a while to download all the datafiles by using `loadEngine()` if the SQLite engine instance is not stored in the `/data/` folder beforehand. 


### Data

Source: https://s3.amazonaws.com/tripdata/index.html

We use the following datasets from Janurary to December in 2019:

* 2019[01-12]-citibike-tripdata.csv.zip


## Data Dictionary

* `tripduration`: Trip Duration (seconds)
* `starttime`: Start Time and Date
* `stoptime`: Stop Time and Date
* `start station name`: Start Station Name
* `start station latitude`: Start Station Latitude
* `start station longitude`: Start Station Longitude
* `end station latitude`: End Station Latutude 
* `end station longtitude`: End station longitude
* `end station name`: End Station Name
* `start station id`: Start Station ID
* `end station id`: End Station ID
* `bikeid`: Bike ID
* `usertype`: User Type (Customer = 24-hour pass or 3-day pass user; Subscriber = Annual Member)
* `gender`: Gender (Zero=unknown; 1=male; 2=female)
* `birth year`: Year of Birth of the Customer

##  Authors

Kenneth Lee ([@kenneth-lee-ch](https://github.com/kenneth-lee-ch))

Ivan Siu ([@ivansiu](https://github.com/ivansiu))



