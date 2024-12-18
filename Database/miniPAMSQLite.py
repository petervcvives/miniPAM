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
		if(self.connection == None):
			# check if the directory exists
			path = Path(self.dbfilepath)
			parentpath =  path.parent.absolute()
			os.makedirs(parentpath,exist_ok = True)
			# make the sqlite connection
			self.connection = sqlite3.connect(self.dbfilepath)
		pass

	def _disconnect(self):
		if(self.connection == None):
			self.connection.close()


	def _addAssetsDefinitionData(self, data):
		if(self.connection != None):
			cur = self.connection.cursor()
			cur.execute(f"""
					INSERT INTO  {self.ASSETDEFINITIONS}({self.ASSETDEFINITIONS_ID},{self.ASSETDEFINITIONS_Name},{self.ASSETDEFINITIONS_Description},{self.ASSETDEFINITIONS_UnitTypeID}) 
					VALUES ('{data[self.ASSETDEFINITIONS_ID]}','{data[self.ASSETDEFINITIONS_Name]}','{data[self.ASSETDEFINITIONS_Description]}','{data[self.ASSETDEFINITIONS_UnitTypeID]}');
					""")
			self.connection.commit()
		self.addCountValue(0,data[self.ASSETDEFINITIONS_ID])


	def _updateAssetsDefinitionData(self, data):
		if(self.connection != None):
			cur = self.connection.cursor()
			updatequery = f"""
					UPDATE {self.ASSETDEFINITIONS} SET
					{self.ASSETDEFINITIONS_Name} = '{data[self.ASSETDEFINITIONS_Name]}',
					{self.ASSETDEFINITIONS_Description} = '{data[self.ASSETDEFINITIONS_Description]}',
					{self.ASSETDEFINITIONS_UnitTypeID} = '{data[self.ASSETDEFINITIONS_UnitTypeID]}'
					WHERE {self.ASSETDEFINITIONS_ID} = '{data[self.ASSETDEFINITIONS_ID]}';
					"""
			cur.execute(updatequery)
			self.connection.commit()

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
						{self.ASSETDEFINITIONS_UnitTypeID} TEXT NOT NULL
						);
					""")

#						FOREIGN KEY({self.ASSETDEFINITIONS_ID}) REFERENCES {self.ASSETSCOUNT}({self.ASSETSCOUNT_ID}),
#						FOREIGN KEY({self.ASSETDEFINITIONS_UnitTypeID}) REFERENCES {self.UNITTYPES}({self.UNITTYPES_ID})

				# CREATE TABLE AssetsCount
				cur.execute(f"""
					CREATE TABLE {self.ASSETSCOUNT}(
						{self.ASSETSCOUNT_ID} TEXT,
						{self.ASSETSCOUNT_AMOUNT} INTEGER NOT NULL,
						{self.ASSETSCOUNT_DATE} DATETIME
						);
					""")

				# CREATE TABLE UnitTypes
				cur.execute(f"""
					CREATE TABLE {self.UNITTYPES}(
						{self.UNITTYPES_ID} TEXT PRIMARY KEY, 
						{self.UNITTYPES_Name} TEXT NOT NULL,
						{self.UNITTYPES_Description} TEXT NOT NULL
						);
					""")

				#INSERT DEFAULT CountTypes
				cur.execute(f"""
					INSERT INTO  {self.UNITTYPES}({self.UNITTYPES_ID},{self.UNITTYPES_Name},{self.UNITTYPES_Description}) VALUES
					("{self.getNewUUID()}","Pcs","Pieces"),
					("{self.getNewUUID()}","g","Grams"),
					("{self.getNewUUID()}","l","Liters"),
					("{self.getNewUUID()}","GL","Gallons"),
					("{self.getNewUUID()}","Bottles","Bottles")
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
		selectquery = f"SELECT {self.ASSETDEFINITIONS_ID},{self.ASSETDEFINITIONS_Name},{self.ASSETDEFINITIONS_Description},{self.ASSETDEFINITIONS_UnitTypeID} FROM {self.ASSETDEFINITIONS} where {self.ASSETDEFINITIONS_Name} LIKE '%{searchtext}%' OR {self.ASSETDEFINITIONS_Description} LIKE '%{searchtext}%';"
		res = cur.execute(selectquery)
		for row in res.fetchall():
			rowresult = {
				f"{self.ASSETDEFINITIONS_ID}":f"{row[0]}",
				f"{self.ASSETDEFINITIONS_Name}":f"{row[1]}",
				f"{self.ASSETDEFINITIONS_Description}":f"{row[2]}",
				f"{self.ASSETDEFINITIONS_UnitTypeID}":f"{row[3]}"
			}
			results.append(rowresult)
		return results


	def _getAllUnitTypes(self):
		results = []
		cur = self.connection.cursor()
		res = cur.execute(f"SELECT {self.UNITTYPES_ID},{self.UNITTYPES_Name},{self.UNITTYPES_Description} FROM {self.UNITTYPES}")
		for row in res.fetchall():
			rowresult = {
				f"{self.UNITTYPES_ID}":f"{row[0]}",
				f"{self.UNITTYPES_Name}":f"{row[1]}",
				f"{self.UNITTYPES_Description}":f"{row[2]}"
			}
			results.append(rowresult)
		return results
		pass

	def _getUnitTypeId(self,unitname):
		cur = self.connection.cursor()
		selectquery = f"SELECT {self.UNITTYPES_ID} FROM {self.UNITTYPES} where {self.UNITTYPES_Name} LIKE '{unitname}';"
		res = cur.execute(selectquery)
		for row in res.fetchall():
			return row[0]
		return ""

	def _getAllAssetsDefinitionData(self):
		results = []
		cur = self.connection.cursor()
		selectquery = f"""SELECT {self.ASSETDEFINITIONS}.*,  SUM({self.ASSETSCOUNT}.{self.ASSETSCOUNT_AMOUNT}) AS Amount , {self.UNITTYPES}.{self.UNITTYPES_Name} FROM {self.ASSETDEFINITIONS} 
		INNER JOIN {self.UNITTYPES} ON {self.ASSETDEFINITIONS}.{self.ASSETDEFINITIONS_UnitTypeID} = {self.UNITTYPES}.{self.UNITTYPES_ID}
		INNER JOIN {self.ASSETSCOUNT}  ON {self.ASSETDEFINITIONS}.{self.ASSETDEFINITIONS_ID} = {self.ASSETSCOUNT}.{self.ASSETSCOUNT_ID} GROUP BY ({self.ASSETDEFINITIONS}.{self.ASSETDEFINITIONS_ID})"""
		res = cur.execute(selectquery)
		for row in res.fetchall():
			rowresult = {
				f"{self.ASSETDEFINITIONS_ID}":f"{row[0]}",
				f"{self.ASSETDEFINITIONS_Name}":f"{row[1]}",
				f"{self.ASSETDEFINITIONS_Description}":f"{row[2]}",
				f"{self.UNITTYPES_ID}":f"{row[3]}",
				f"{self.ASSETSCOUNT_AMOUNT}":f"{row[4]}",
				f"Unit":f"{row[5]}"
			}
			results.append(rowresult)
		return results
		pass


	def _addUnitData(self,amount,assetKey,timestamp):
		print("Adding count data...")
		cur = self.connection.cursor()
		insertQuery = f"""INSERT INTO  {self.ASSETSCOUNT}({self.ASSETSCOUNT_ID},{self.ASSETSCOUNT_AMOUNT},{self.ASSETSCOUNT_DATE}) 
		VALUES ('{assetKey}',{amount},'{timestamp.strftime("%Y-%m-%d %H:%M:%S")}');""" 
		cur.execute(insertQuery)
		self.connection.commit()
		cur.close()
		pass

if __name__ == "__main__":
	testDBConn = MiniPAMSQLite(r"F:\VIVES\miniPAM\DATA\mydtabase.db")
	testDBConn.initialize()