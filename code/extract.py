import boto3
import botocore
from botocore import UNSIGNED
from botocore.config import Config
import pandas as pd
import zipfile
from io import BytesIO
import sqlalchemy as sqla



def getData(bucket, files, tablename):
	"""
	This function scrapes the data files directly from the source of the CitiBike webpage

	Arguement:
		
		bucket (str): it is the name of the s3 bucket name

		files (list): it is a list of strings that specify the zip filenames for scraping

		tablename (str): this is a name of the table we want to create in a database to store the data

	Return:
		
		engine (object): an sqlalchemy Engine instance.

	"""	
	# Get resources from the default s3 session without authetication
	s3 = boto3.resource("s3", config=Config(signature_version=UNSIGNED))
	# Check if the files is an empty list, if not then we start retriving the first file
	if files:
		# Read in the first files
		file = files[0]
		try: 
			# Get the first chunk and an iterable of the data for the first file
			chunk, reader = fetch(s3, bucket, file)
			# Create an engine
			engine = createEngine(chunk, tablename)
			# Load into sql
			loadToSQL(chunk, reader, engine, tablename)
			# Get the data from the rest of the files and convert them into the database
			if len(files) > 1:
				for f in files[1:]:
					# Repeat the same procedures as above, but this time we don't need to create an engine
					# and we only convert all the data into one table
					other_chunk, next_reader = fetch(s3, bucket, f)
					# Start convert the chunk to the table in the engine we established
					loadToSQL(other_chunk, next_reader, engine, tablename)
			return engine
		# If the file cannot be found, we throw out errors
		except botocore.exceptions.ClientError as e:
			# Throw out a 404 not found error
			if e.response['Error']['Code'] == "404":
				print("Error 404: The object does not exist.")
			else:
				# Raise another type of exception
				print("Something is wrong other than a 404 error code.")

def fetch(s3, bucket, file):
	"""
	this function is get the first chunk of the csv file content from a zipped folder

	Arguments:
		
		s3 (object): a service resource instance to represent an object-oriented interface to Amazon Web Services (AWS) s3 service.
		
		bucket (str): a S3 bucket name and can be used as an identifier to look for a public bucket on Amazon S3.
		
		file (str): a file name 
	Return:
		bike_chunk (dataframe): this is the first chunk in the dataframe extracted from the csv file.
		
		bike_reader (iterable): this returns the data in sequence.
	"""
	# Get the s3 object file
	obj = s3.Object(bucket, file) 
	body = BytesIO(obj.get()['Body'].read()) # Get the actual data, in a StreamingBody format.
	zf = zipfile.ZipFile(body) # Unzip the file
	# Get the csv name
	key = zf.namelist()[0]
	# set chunksize to create a DataFrameReader out of a file inside an zipped folder
	bike_reader = pd.read_csv(zf.open(key), chunksize=100000,low_memory=False) # 
	# Get the first chunk	
	bike_chunk = next(bike_reader) # Iterable which returns the file in sequence.
	# Return the first chunk and the rest of the data
	return bike_chunk, bike_reader



def createEngine(bikechunk, tablename):
	"""
	this function creates a SQLite database engine.

	Arguments:
		
		bikechunk (dataframe): this is the first chunk in the dataframe extracted from the csv file.

		tablename (str): this is a name of the table we want to create in a database to store the data.

	Return:

		engine (object): an sqlalchemy Engine instance.

	"""
	
	sqlite_file = '../data/bike.sqlite'
	engine = sqla.create_engine('sqlite:///' + sqlite_file)
	## Work on first chunk to convert to table
	bikechunk.to_sql(tablename,engine, if_exists='replace')
	# Return the engine instance
	return engine


def loadToSQL(bikechunk, reader, engine, tablename):
	"""
	this function loads data into an established database.

	Arguments:

		bikechunk (dataframe): this is the chunk in the dataframe extracted from the csv file.

		reader (iterable): this returns the data in sequence.

		tablename (str): this is a name of the table we want to create in a database to store the data.

		engine (object): an sqlalchemy Engine instance.

	Return:
		None
	"""
	# Loop through the remaining chunks in the file
	for chunk in reader:
		# Convert the chunk to sql and append to the existing table in the database
	    chunk.to_sql(tablename, engine, if_exists='append')
	# Don't need to return anything
	return None

	

