from Logging.miniPAMLogger import Logger
import os
import sys

class MiniPAMConsole():

	def __init__(self, dbconnection):
		self.dbconn = dbconnection
		self.FunctionCallerList = {
		1:(self.showAllCountTypes,"Show all count types"),
		2:(self.addNewAsset,"Add new asset"),
		3:(self.searchInAssets,"Search in assets"),
		4:(self.showAllAssets,"Show all assets"),
		}
		self.maxRowWidth = 30

	def exitConsole(self):
		sys.exit()

	def mainMenu(self):
		while True:
			print("********* miniPAM console menu **********")
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
			#self.clearScreen()



	def start(self):
		"""
			This will start the console application and keep it running until it is existed by the user or forced stopped
		"""
		self.clearScreen()
		print(
		"""Welcome to the miniPAM console.
The mini Personal Assets Management application has been created to manage your personal assets like bottels of wine, electronics componenets, or anything you like need to manage.
It is mini so it is a simple tool without a lot of features.""")

		self.mainMenu()

	def clearScreen(self):
		os.system('cls' if os.name == 'nt' else 'clear')
		

	def searchInAssets(self):
		searchtext = input("Enter search text: ")
		results = self.dbconn.searchAssets(searchtext)
		self.__PrintAsTextTable(results)

	def addNewAsset(self):
		name = input("Asset name: ")
		descr = input("Asset description: ")
		selectedunit = self.SelectUnitType()
		print(selectedunit)
		self.dbconn.saveAssetsDefinition(name,descr,selectedunit[self.dbconn.COUNTTYPES_ID])

	def SelectUnitType(self):
		results = self.dbconn.getAllCountTypes()
		self.__PrintAsTextTable(results)
		while True:
			selection = input("Select unit type:")
			try:
				selectionInt = int(selection) - 1
				if (selectionInt >= 0 and selectionInt < len(results)):
					return results[selectionInt]
				else:
					print("Invalid selection!")
					continue
			except Exception as e:
				print("Invalid value!")

			

	def showAllAssets(self):
		results = self.dbconn.getAllAssets()
		self.__PrintAsTextTable(results)


	def showAllCountTypes(self):
		results = self.dbconn.getAllCountTypes()
		self.__PrintAsTextTable(results)
		

	def __PrintAsTextTable(self,results):
		print("")
		headerPrinted = False
		counter = 0
		for row in results:
			counter = counter + 1
			rowresults = [f"{str(counter):<5}",]
			headerresults = [f"{"":<5}",]
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





