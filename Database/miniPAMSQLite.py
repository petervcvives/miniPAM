from .miniPAMDB import MiniPAMDBConnection
import sqlite3
import os
from pathlib import Path

class MiniPAMSQLite(MiniPAMDBConnection):
	def __init__(self, dbfilepath):
		super(MiniPAMSQLite, self).__init__()
		self.dbfilepath = dbfilepath
		self.connection = None
		print(f"Database path: {self.dbfilepath} ")

	def _connect(self):
		print("CONNECTING....")
		if(self.connection == None):
			# check if the directory exists
			path = Path(self.dbfilepath)
			parentpath =  path.parent.absolute()
			if not os.path.exists(path):
				os.makedirs(parentpath)
			# make the sqlite connection
			self.connection = sqlite3.connect(self.dbfilepath)
			print("DB CONNECTED!")
		pass

	def _disconnect(self):
		if(self.connection == None):
			self.connection.close()
			print("DB DISCONNECTED!")


	def _addAssetsDefinitionData(self, data):
		if(self.connection != None):
			cur = self.connection.cursor()
			cur.execute(f"""
					INSERT INTO  {self.ASSETDEFINITIONS}({self.ASSETDEFINITIONS_ID},{self.ASSETDEFINITIONS_Name},{self.ASSETDEFINITIONS_Description}) 
					VALUES ('{data[self.ASSETDEFINITIONS_ID]}','{data[self.ASSETDEFINITIONS_Name]}','{data[self.ASSETDEFINITIONS_Description]}');
					""")
			self.connection.commit()
			print("INSERTED!!!")


	def _updateAssetsDefinitionData(self, data):
		if(self.connection != None):
			cur = self.connection.cursor()
			cur.execute(f"""
					UPDATE {self.ASSETDEFINITIONS} SET
					{self.ASSETDEFINITIONS_Name} = '{data[self.ASSETDEFINITIONS_Name]}',
					{self.ASSETDEFINITIONS_Description} = '{data[self.ASSETDEFINITIONS_Description]}'
					WHERE {self.ASSETDEFINITIONS_ID} = '{data[self.ASSETDEFINITIONS_ID]}';
					""")
			self.connection.commit()
			print("UPDATED!!!")

	def _deleteAssetsDefinitionData(self, uuid):
		pass

	def _initialize(self):
		print("Initializing...")
		if(self.connection != None):
			cur = self.connection.cursor()
			res = cur.execute("SELECT * FROM sqlite_master where type='table';")
			tables = cur.fetchall()
			if (len(tables) == 0):
				print("Creating tables...")
				
				# CREATE TABLE AssetsDefinitions
				cur.execute(f"""
					CREATE TABLE {self.ASSETDEFINITIONS}(
						{self.ASSETDEFINITIONS_ID} TEXT PRIMARY KEY , 
						{self.ASSETDEFINITIONS_Name} TEXT NOT NULL,
						{self.ASSETDEFINITIONS_Description} TEXT NOT NULL
						);
					""")

				# CREATE TABLE AssetsCount
				cur.execute(f"""
					CREATE TABLE {self.ASSETSCOUNT}(
						{self.ASSETSCOUNT_ID} TEXT PRIMARY KEY , 
						{self.ASSETSCOUNT_TypeID} TEXT NOT NULL,
						{self.ASSETSCOUNT_AMOUNT} INTEGER NOT NULL,
						{self.ASSETSCOUNT_DATE} DATETIME,
						FOREIGN KEY({self.ASSETSCOUNT_ID}) REFERENCES {self.ASSETDEFINITIONS}({self.ASSETDEFINITIONS_ID})
						);
					""")

				# CREATE TABLE CountTypes
				cur.execute(f"""
					CREATE TABLE {self.COUNTTYPES}(
						{self.COUNTTYPES_ID} TEXT PRIMARY KEY, 
						{self.COUNTTYPES_Name} TEXT NOT NULL,
						{self.COUNTTYPES_Description} TEXT NOT NULL,
						FOREIGN KEY({self.COUNTTYPES_ID}) REFERENCES {self.ASSETSCOUNT}({self.ASSETSCOUNT_TypeID})
						);
					""")

				#INSERT DEFAULT CountTypes
				cur.execute(f"""
					INSERT INTO  {self.COUNTTYPES}({self.COUNTTYPES_ID},{self.COUNTTYPES_Name},{self.COUNTTYPES_Description}) VALUES
					("{self.getNewUUID()}","Pcs","Pieces"),
					("{self.getNewUUID()}","g","Grams"),
					("{self.getNewUUID()}","l","Liters"),
					("{self.getNewUUID()}","GL","Gallons"),
					("{self.getNewUUID()}","Botles","Botles")
					;
					""")
				self.connection.commit()
				print("Creating tables. DONE.")


			cur.close()

	def _searchAssetsDefinitionData(self, searchtext):
		results = []
		cur = self.connection.cursor()
		res = cur.execute(f"SELECT {self.ASSETDEFINITIONS_ID},{self.ASSETDEFINITIONS_Name},{self.ASSETDEFINITIONS_Description} FROM {self.ASSETDEFINITIONS} where {self.ASSETDEFINITIONS_Name} LIKE '%{searchtext}%' OR {self.ASSETDEFINITIONS_Description} LIKE '%{searchtext}%';")
		for row in res.fetchall():
			rowresult = {
				f"{self.ASSETDEFINITIONS_ID}":f"{row[0]}",
				f"{self.ASSETDEFINITIONS_Name}":f"{row[1]}",
				f"{self.ASSETDEFINITIONS_Description}":f"{row[2]}"
			}
			results.append(rowresult)
		return results

if __name__ == "__main__":
	testDBConn = MiniPAMSQLite(r"F:\VIVES\miniPAM\DATA\mydtabase.db")
	testDBConn.initialize()