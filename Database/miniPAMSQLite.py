from .miniPAMDB import MiniPAMDBConnection
import sqlite3
import os
from pathlib import Path

#SELECT AssetsDefinitions.*,CountUnits.Name,CountUnits.Description , SUM(AssetsCount.Amount) as Amount FROM AssetsDefinitions 
#INNER JOIN CountUnits ON AssetsDefinitions.CountUnitID = CountUnits.ID
#INNER JOIN AssetsCount ON AssetsDefinitions.Id = AssetsCount.AssetID


class MiniPAMSQLite(MiniPAMDBConnection):
	def __init__(self, dbfilepath):
		super(MiniPAMSQLite, self).__init__()
		self.dbfilepath = dbfilepath
		self.connection = None
		print(f"Database path: {self.dbfilepath} ")

	def _connect(self):
		# print("CONNECTING....")
		if(self.connection == None):
			# check if the directory exists
			path = Path(self.dbfilepath)
			parentpath =  path.parent.absolute()
			os.makedirs(parentpath,exist_ok = True)
			# make the sqlite connection
			self.connection = sqlite3.connect(self.dbfilepath)
			# print("DB CONNECTED!")
		pass

	def _disconnect(self):
		if(self.connection == None):
			self.connection.close()
			# print("DB DISCONNECTED!")


	def _addAssetsDefinitionData(self, data):
		if(self.connection != None):
			cur = self.connection.cursor()
			cur.execute(f"""
					INSERT INTO  {self.ASSETDEFINITIONS}({self.ASSETDEFINITIONS_ID},{self.ASSETDEFINITIONS_Name},{self.ASSETDEFINITIONS_Description},{self.ASSETDEFINITIONS_CountTypeID}) 
					VALUES ('{data[self.ASSETDEFINITIONS_ID]}','{data[self.ASSETDEFINITIONS_Name]}','{data[self.ASSETDEFINITIONS_Description]}','{data[self.ASSETDEFINITIONS_CountTypeID]}');
					""")
			self.connection.commit()
		print(data[self.ASSETDEFINITIONS_ID])
		print(dir(data[self.ASSETDEFINITIONS_ID]))
		print(data[self.ASSETDEFINITIONS_ID])
		self.addCountValue(0,data[self.ASSETDEFINITIONS_ID])


	def _updateAssetsDefinitionData(self, data):
		if(self.connection != None):
			cur = self.connection.cursor()
			cur.execute(f"""
					UPDATE {self.ASSETDEFINITIONS} SET
					{self.ASSETDEFINITIONS_Name} = '{data[self.ASSETDEFINITIONS_Name]}',
					{self.ASSETDEFINITIONS_Description} = '{data[self.ASSETDEFINITIONS_Description]}',
					{self.ASSETDEFINITIONS_Description} = '{data[self.ASSETDEFINITIONS_Description]}'
					WHERE {self.ASSETDEFINITIONS_CountTypeID} = '{data[self.ASSETDEFINITIONS_CountTypeID]}';
					""")
			self.connection.commit()
			# print("UPDATED!!!")

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
						{self.ASSETDEFINITIONS_Description} TEXT NOT NULL,
						{self.ASSETDEFINITIONS_CountTypeID} TEXT NOT NULL
						);
					""")

#						FOREIGN KEY({self.ASSETDEFINITIONS_ID}) REFERENCES {self.ASSETSCOUNT}({self.ASSETSCOUNT_ID}),
#						FOREIGN KEY({self.ASSETDEFINITIONS_CountTypeID}) REFERENCES {self.COUNTTYPES}({self.COUNTTYPES_ID})

				# CREATE TABLE AssetsCount
				cur.execute(f"""
					CREATE TABLE {self.ASSETSCOUNT}(
						{self.ASSETSCOUNT_ID} TEXT,
						{self.ASSETSCOUNT_AMOUNT} INTEGER NOT NULL,
						{self.ASSETSCOUNT_DATE} DATETIME
						);
					""")

				# CREATE TABLE CountTypes
				cur.execute(f"""
					CREATE TABLE {self.COUNTTYPES}(
						{self.COUNTTYPES_ID} TEXT PRIMARY KEY, 
						{self.COUNTTYPES_Name} TEXT NOT NULL,
						{self.COUNTTYPES_Description} TEXT NOT NULL
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
				while True:
					demoDataInput = input("Like to add example data (Y/N) ? ")
					if (len(demoDataInput)) > 0 and demoDataInput[0].lower() == "y":
						self.addExampleData()
						break;
					print("Please answer with 'Y' or 'N' ")


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


	def _getAllCountTypes(self):
		results = []
		cur = self.connection.cursor()
		res = cur.execute(f"SELECT {self.COUNTTYPES_ID},{self.COUNTTYPES_Name},{self.COUNTTYPES_Description} FROM {self.COUNTTYPES}")
		for row in res.fetchall():
			rowresult = {
				f"{self.COUNTTYPES_ID}":f"{row[0]}",
				f"{self.COUNTTYPES_Name}":f"{row[1]}",
				f"{self.COUNTTYPES_Description}":f"{row[2]}"
			}
			results.append(rowresult)
		return results
		pass

	def _getUnitTypeId(self,unitname):
		cur = self.connection.cursor()
		selectquery = f"SELECT {self.COUNTTYPES_ID} FROM {self.COUNTTYPES} where {self.COUNTTYPES_Name} LIKE '{unitname}';"
		print(selectquery)
		res = cur.execute(selectquery)
		for row in res.fetchall():
			return row[0]
		return ""

	def _getAllAssetsDefinitionData(self):
		results = []
		cur = self.connection.cursor()


		selectquery = f"""SELECT {self.ASSETDEFINITIONS}.*,  SUM({self.ASSETSCOUNT}.{self.ASSETSCOUNT_AMOUNT}) AS Amount , {self.COUNTTYPES}.{self.COUNTTYPES_Name} FROM {self.ASSETDEFINITIONS} 
		INNER JOIN {self.COUNTTYPES} ON {self.ASSETDEFINITIONS}.{self.ASSETDEFINITIONS_CountTypeID} = {self.COUNTTYPES}.{self.COUNTTYPES_ID}
		INNER JOIN {self.ASSETSCOUNT}  ON {self.ASSETDEFINITIONS}.{self.ASSETDEFINITIONS_ID} = {self.ASSETSCOUNT}.{self.ASSETSCOUNT_ID} GROUP BY ({self.ASSETDEFINITIONS}.{self.ASSETDEFINITIONS_ID})"""


		print(selectquery)

		res = cur.execute(selectquery)

		for row in res.fetchall():
			rowresult = {
				f"{self.ASSETDEFINITIONS_ID}":f"{row[0]}",
				f"{self.ASSETDEFINITIONS_Name}":f"{row[1]}",
				f"{self.ASSETDEFINITIONS_Description}":f"{row[2]}",
				f"{self.COUNTTYPES_ID}":f"{row[3]}",
				f"{self.ASSETSCOUNT_AMOUNT}":f"{row[4]}",
				f"Unit":f"{row[5]}"
			}
			results.append(rowresult)
		return results
		pass

	def _addCountData(self,amount,assetKey,timestamp):
		print("Adding count data...")

		print(f"=====> {assetKey}")
		cur = self.connection.cursor()
		insertQuery = f"""INSERT INTO  {self.ASSETSCOUNT}({self.ASSETSCOUNT_ID},{self.ASSETSCOUNT_AMOUNT},{self.ASSETSCOUNT_DATE}) 
		VALUES ('{assetKey}',{amount},'{timestamp.strftime("%Y-%m-%d %H:%M:%S")}');""" 
		print(insertQuery)
		cur.execute(insertQuery)
		self.connection.commit()
		cur.close()
		pass

if __name__ == "__main__":
	testDBConn = MiniPAMSQLite(r"F:\VIVES\miniPAM\DATA\mydtabase.db")
	testDBConn.initialize()