import boto3
import botocore
from botocore import UNSIGNED
from botocore.config import Config

def getData(bucket="tripdata", files="201901-citibike-tripdata.csv.zip"):
	"""
	This function scrapes the data files directly from the source of the CitiBike webpage

	Arguement:
	url (str): it is the 

	Return:

	"""	
	path = "../data/"
	s3 = boto3.resource("s3", config=Config(signature_version=UNSIGNED))
	try: 
		s3.Bucket(bucket).download_file(files, "../data/"+files)
	except botocore.exceptions.ClientError as e:
		if e.response['Error']['Code'] == "404":
			print("Error 404: The object does not exist.")
		else:
			raise


if __name__=="__main__":
	getData()

