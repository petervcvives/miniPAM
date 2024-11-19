import uuid

class MiniPAMDBConnection(object):

	# TABLE NAMES AND COLUMS
	ASSETDEFINITIONS = "AssetsDefinitions"
	ASSETDEFINITIONS_ID = "ID"
	ASSETDEFINITIONS_Name = "Name"
	ASSETDEFINITIONS_Description = "Description"

	ASSETSCOUNT = "AssetsCount"
	ASSETSCOUNT_ID = "AssetID"
	ASSETSCOUNT_TypeID = "CountTypeID"
	ASSETSCOUNT_AMOUNT = "Amount"
	ASSETSCOUNT_DATE = "CountDate"

	COUNTTYPES = "CountTypes"
	COUNTTYPES_ID = "ID"
	COUNTTYPES_Name = "Name"
	COUNTTYPES_Description = "Description"

	"""docstring for miniPAMDbConnection"""
	def __init__(self):
		pass

	def _connect(self):
		print("CONNECTING....AAAA")
		pass


	def _initialize(self):
		pass

	def initialize(self):
		print("INITILIZING...")
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

	# DIRECT CALLABLE FUNCTIONS

	def saveAssetsDefinition(self, name, description, uuid = ""):
		self._connect()
		print("SAVING...")
		addData = False
		if (uuid == ""):
			addData = True
			uuid = self.getNewUUID()
		data = {
			f"{self.ASSETDEFINITIONS_ID}":f"{uuid}",
			f"{self.ASSETDEFINITIONS_Name}":f"{name}",
			f"{self.ASSETDEFINITIONS_Description}":f"{description}"
		}
		if (addData):
			self._addAssetsDefinitionData(data)
		else:
			self._updateAssetsDefinitionData(data)
		self._disconnect()
		return uuid

	def removeAssetsDefinition(self,uuid):
		self._connect()
		print("DELETING...")
		self._deleteAssetsDefinitionData(uuid)
		self._disconnect()
		pass

	def SearchAssets(self,searchtext):
		self._connect()
		result = self._searchAssetsDefinitionData(searchtext)
		self._disconnect()
		return result

	def getNewUUID(self):
		return uuid.uuid4().hex


