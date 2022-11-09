
import sqlite3
from datetime import datetime, timedelta
from dateutil import parser

from sqlalchemy import Table, Column, Integer, Float, String, Time,DateTime, MetaData, inspect, create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

Base = declarative_base()


class RESULTS(Base):
	__tablename__ = 'RESULTS'

	QUERY = Column(String, primary_key=True)
	NUMBERCOINS = Column(Float)
	PROFIT = Column(Float)
	GROWTHFACTOR = Column(Float)
	LAMBOS = Column(Float)
	INVESTMENT = Column(Float)
	SYMBOL = Column(String)
	GENERATIONDATE = Column(DateTime)


class OPENING_AVERAGE(Base):
	__tablename__ = 'OPENING_AVERAGE'

	SYMBOL = Column(String, primary_key=True)
	AVERAGE = Column(Float)


class LOGGING(Base):
	__tablename__ = 'LOGGING'

	QUERY_ID = Column(Integer, primary_key=True)
	SYMBOL = Column(String)
	INVESTMENT = Column(Float)
	GENERATIONDATE = Column(DateTime)


class DataCacheAlchemy:

	def __init__(self, coin_symbol, investment):
		self.coin_symbol = coin_symbol
		self.investment = investment
		self.engine = self.create_connection()
		self.setup_DB()

	# Set up db connection
	def create_connection(self):
		try:
			engine = create_engine('sqlite:///DudeWheresMyLambo.db', echo = True)

			print("Database connected to successfully")
			return engine
		except Exception as e:
			print(e)

	# The set up function will create the db tables if they don't already exist
	def setup_DB(self):

		if(not self.check_table_exists('RESULTS')):
			self.create_table('RESULTS')

		if(not self.check_table_exists('OPENING_AVERAGE')):
			self.create_table('OPENING_AVERAGE')

		if(not self.check_table_exists('LOGGING')):
			self.create_table('LOGGING')

		print('DB setup complete')

	# Table creation logic
	def create_table(self, table_name):
		# We will have three tables, a RESULTS table to cache the results of a full query, an OPENING_AVERAGE table to cache the average price of the coin within the first month of its listing on the exchange and finally a LOGGING table to log and measure usage

		try:
			'''
			if(table_name == 'RESULTS'):
				Base.metadata.create_all(self.engine, tables=[RESULTS])
			elif(table_name == 'OPENING_AVERAGE'):
				Base.metadata.create_all(self.engine, tables=[OPENING_AVERAGE])
			elif(table_name == 'LOGGING'):
				Base.metadata.create_all(self.engine, tables=[LOGGING])
			'''

			Base.metadata.create_all(self.engine)

		except Exception as e:
			print(e)

	# Check if there exists a freshly cached result for the current query
	def check_if_valid_final_result_exists(self):

		print('Checking if value exists')

		try:

			Session = sessionmaker(bind=self.engine)
			session = Session()
			result = session.query(RESULTS).filter(RESULTS.QUERY.like(
				f'{self.coin_symbol}-{self.investment}')).first()

			if result != None:
				return True
			else:
				return False
		except Exception as e:
			print(e)

	 # Get cached result for the current query

	def get_valid_final_result(self):

		try:

			Session = sessionmaker(bind=self.engine)
			session = Session()
			result = session.query(RESULTS).filter(RESULTS.QUERY.like(
				f'{self.coin_symbol}-{self.investment}')).first()

			if result != None:
				return(result[0])
			else:
				return({})
		except Exception as e:
			print(e)
			return({})

	# Check if we have already stored a cached version of the opening price data for the symbol
	def check_if_historical_cache_exists(self):


		query = f"SELECT * from OPENING_AVERAGE WHERE SYMBOL = '{self.coin_symbol}'"


		try:

			Session = sessionmaker(bind=self.engine)
			session = Session()
			result = session.query(OPENING_AVERAGE).filter(OPENING_AVERAGE.SYMBOL ==
				f'{self.coin_symbol}').first()


			print(result)


			if result != None and result != {}:
				print(f'There exists a historical cache for this query {query}')
				return True
			else:
				print(f'There doesn\'t exist a valid historical query {query}')
				return False
		except Exception as e:
			print(e)
			print(f'There doesn\'t exist a valid historical query {query}')
			return False

	# Get cached version of the opening price data for the symbol
	def get_historical_cache(self):
		
		try:

			Session = sessionmaker(bind=self.engine)
			session = Session()
			results = session.query(OPENING_AVERAGE).filter(OPENING_AVERAGE.SYMBOL ==
				f'{self.coin_symbol}').first()

			print(results)

			for result in results:
				print(result)


			if results != None:
				print(results)
				return(results[0])
			else:
				return({})
		except Exception as e:
			print(e)
			return({})

	# Insert current query into the logging table
	def insert_into_logging(self):

		combined_results = {'SYMBOL': self.coin_symbol,
							'INVESTMENT': self.investment, 'GENERATIONDATE': datetime.now()}

		print(combined_results)

		new_item = LOGGING(SYMBOL=combined_results["SYMBOL"], INVESTMENT=combined_results["INVESTMENT"],GENERATIONDATE=combined_results["GENERATIONDATE"])

		Session = sessionmaker(bind=self.engine)
		session = Session()

		try:
			session.add(new_item)
			session.commit()
			print('Insert into LOGGING successful')
		except Exception as e:
			print(f'insert into LOGGING unsuccessful {e}')

	# Insert final result from a query into the results table
	def insert_into_result(self, result):

		QUERY_string = f'{self.coin_symbol}-{self.investment}'

		combined_results = {**result, 'QUERY': QUERY_string, 'GENERATIONDATE': datetime.now()}

		new_item = RESULTS(QUERY=QUERY_string, NUMBERCOINS=combined_results["NUMBERCOINS"], PROFIT=combined_results["PROFIT"], GROWTHFACTOR=combined_results["GROWTHFACTOR"], LAMBOS=combined_results["LAMBOS"],
						   INVESTMENT=combined_results["INVESTMENT"], SYMBOL=combined_results["SYMBOL"], GENERATIONDATE=combined_results["GENERATIONDATE"])

		Session = sessionmaker(bind=self.engine)
		session = Session()


		try:
			session.add(new_item)
			session.commit()
			print('Insert into RESULTS successful')
		except Exception as e:
			print(f'insert into RESULTS unsuccessful {e}')

	# Insert final result from data collector into the db
	def insert_into_opening_average(self, result):

		combined_results = {**result, 'SYMBOL': self.coin_symbol}


		new_item = OPENING_AVERAGE(SYMBOL=combined_results["SYMBOL"], AVERAGE=combined_results["AVERAGE"])

		Session = sessionmaker(bind=self.engine)
		session = Session()

		try:
			session.add(new_item)
			session.commit()
			print('Insert into OPENING_AVERAGE successful')
		except Exception as e:
			print(f'insert into OPENING_AVERAGE unsuccessful {e}')

	# Check if queried table exists
	def check_table_exists(self, table_name):

		try:

			inspector = inspect(self.engine)
			table_exists = inspector.has_table(table_name)

			return table_exists
		except Exception as e:
			print(e)


