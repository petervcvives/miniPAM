import uuid
from datetime import datetime

class MiniPAMDBConnection(object):

	# TABLE NAMES AND COLUMS
	ASSETDEFINITIONS = "AssetsDefinitions"
	ASSETDEFINITIONS_ID = "ID"
	ASSETDEFINITIONS_Name = "Name"
	ASSETDEFINITIONS_Description = "Description"
	ASSETDEFINITIONS_CountTypeID = "CountUnitID"

	ASSETSCOUNT = "AssetsCount"
	ASSETSCOUNT_ID = "AssetID"
	ASSETSCOUNT_AMOUNT = "Amount"
	ASSETSCOUNT_DATE = "CountDate"
	#ASSETSCOUNT_TypeID = "CountUnitID"

	COUNTTYPES = "CountUnits"
	COUNTTYPES_ID = "ID"
	COUNTTYPES_Name = "Name"
	COUNTTYPES_Description = "Description"

	"""docstring for miniPAMDbConnection"""
	def __init__(self):
		pass

	def _connect(self):
		pass


	def _initialize(self):
		pass

	def initialize(self):
		self._connect()
		self._initialize()
		self._disconnect()

	def _disconnect(self):
		pass


	def _addAssetsDefinitionData(self, data):
		pass

	def _updateAssetsDefinitionData(self, data):
		pass

	def _deleteAssetsDefinitionData(self, uuid):
		pass

	def _searchAssetsDefinitionData(self, searchtext):
		pass



	def _getAllCountTypes(self):
		pass


	def _addCountData(self,value,assetKey,timestamp):
		pass

	def _getAllAssetsDefinitionData(self):
		pass


	def _getUnitTypeId(self,unitname):
		pass

	# DIRECT CALLABLE FUNCTIONS

	def saveAssetsDefinition(self, name, description, unitId , uuid = ""):
		self._connect()
		
		addData = False
		if (uuid == ""):
			addData = True
			uuid = self.getNewUUID()
		data = {
			f"{self.ASSETDEFINITIONS_ID}":f"{uuid}",
			f"{self.ASSETDEFINITIONS_Name}":f"{name}",
			f"{self.ASSETDEFINITIONS_Description}":f"{description}",
			f"{self.ASSETDEFINITIONS_CountTypeID}":f"{unitId}",
		}
		if (addData):
			self._addAssetsDefinitionData(data)
		else:
			self._updateAssetsDefinitionData(data)
		self._disconnect()
		return uuid


	def removeAssetsDefinition(self,uuid):
		self._connect()
		self._deleteAssetsDefinitionData(uuid)
		self._disconnect()
		pass

	def searchAssets(self,searchtext):
		self._connect()
		result = self._searchAssetsDefinitionData(searchtext)
		self._disconnect()
		return result



	def getAllCountTypes(self):
		self._connect()
		result = self._getAllCountTypes()
		self._disconnect()
		return result

	def addCountValue(self,value, assetkey):
		timenow = datetime.now()
		self._connect()
		self._addCountData(value,assetkey,timenow)
		self._disconnect()

	def getAllAssets(self):
		self._connect()
		result = self._getAllAssetsDefinitionData()
		self._disconnect()
		return result

	def getNewUUID(self):
		return uuid.uuid4().hex



	def addExampleData(self):
		print("creating example data...")
		unitType = self._getUnitTypeId("pcs")
		newuuid = self.saveAssetsDefinition("R10_SMB","Resitor 10ohm SMB",unitType)
		self.addCountValue(10,newuuid)
		self.addCountValue(-5,newuuid)
		self.addCountValue(2,newuuid)
		self.addCountValue(6,newuuid)
		unitType = self._getUnitTypeId("pcs")
		newuuid = self.saveAssetsDefinition("R100k_SMB","Resitor 10 kilo ohm SMB",unitType)
		self.addCountValue(6,newuuid)
		self.addCountValue(-5,newuuid)
		self.addCountValue(-2,newuuid)
		self.addCountValue(6,newuuid)

		unitType = self._getUnitTypeId("pcs")
		newuuid = self.saveAssetsDefinition("C10mf","Capasitor 10 microfarad ",unitType)
		self.addCountValue(10,newuuid)
		self.addCountValue(-5,newuuid)
		self.addCountValue(-8,newuuid)
		self.addCountValue(6,newuuid)

		pass

