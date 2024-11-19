from Logging.miniPAMLogger import Logger
import os
import sys

class MiniPAMConsole():

	def __init__(self, dbconnection):
		self.dbconn = dbconnection
		self.FunctionCallerList = {
		1:(self.showAllCountTypes,"Show all count types"),
		2:(self.SearchInAssets,"Search in assets"),
		99:(self.addDummyDataToDatabase,"Add example data to database")
		}
		self.maxRowWidth = 30

	def exitConsole(self):
		sys.exit()

	def mainMenu(self):
		while True:
			selectedMenuNr = -1
			print("Select action:")
			for k,v in self.FunctionCallerList.items():
				print(f"{k:<3} {v[1]}")
			choice = input("Enter menu number (q to quit):")
			if ("q" in choice):
				self.exitConsole()
				break
			try:
				selectedMenuNr = int(choice)
			except Exception as e:
				self.clearScreen()
				print("Incorrect selection!")

			if not (selectedMenuNr in self.FunctionCallerList.keys()):
				self.clearScreen()
				print("Invalid selection!")
				continue
			if selectedMenuNr > 0 :
				self.FunctionCallerList[selectedMenuNr][0]()
			self.clearScreen()



	def start(self):
		"""
			This will start the console application and keep it running until it is existed by the user or forced stopped
		"""
		self.clearScreen()
		print("********* Starting miniPAM **********")
		self.mainMenu()

	def clearScreen(self):
		# os.system('cls' if os.name == 'nt' else 'clear')
		pass
		
	def addDummyDataToDatabase(self):
		uuid = self.dbconn.saveAssetsDefinition("R10_SMB","Resitor 10ohm SMB")
		self.dbconn.saveAssetsDefinition("R10_SMBAAAAA","Resitor 10ohm SMBBBBBBB",uuid)
		print("Adding example data...")
		pass


	def SearchInAssets(self):
		searchtext = input("Enter search text: ")
		results = self.dbconn.SearchAssets(searchtext)
		self.__PrintAsTextTable(results)


	def showAllCountTypes(self):
		pass


	def __PrintAsTextTable(self,results):
		print("printing result...")
		headerPrinted = False
		for row in results:
			rowresults = []
			headerresults = []
			for key in row.keys():
				match(key):
					case self.dbconn.ASSETDEFINITIONS_ID:
						continue
					case self.dbconn.ASSETSCOUNT_ID:
						continue
					case self.dbconn.COUNTTYPES_ID:
						continue
				
				headerresults.append(f"{key:<{self.maxRowWidth}}")
				rowresults.append(f"{row[key]:<{self.maxRowWidth}}")

			if (not headerPrinted):
				print(" ".join(headerresults))
				headerPrinted = True
			print(" ".join(rowresults))
		print("")





