import json
import os
from Logging.miniPAMLogger import Logger
from ConsoleApp.miniPAMConsole import MiniPAMConsole 
from Database.miniPAMSQLite import MiniPAMSQLite
CONFIGPATH =  os.path.join(os.path.split(__file__)[0],"miniPAM.config") # DETECT CONFIG FILE PATH
CONFIGDATA = None

ERRROLOGPATH = os.path.join(os.path.split(__file__)[0],"miniPAM.log") # DETECT LOG FILE PATH

Logger.SetLoggingpath(ERRROLOGPATH)

Logger.GetInstance().LogMessage("Logging started...")


def LoadConfig():
	global CONFIGDATA
	result = False
	if os.path.exists(CONFIGPATH):
		try:
			# READ CONFIG FILE
			with open(CONFIGPATH, "r") as jsonfile:
				 CONFIGDATA = json.load(jsonfile)
			result = True			
		except Exception as e:
			Logger.GetInstance().LogException(e)
	return result


def SaveConfigFile():
	global CONFIGDATA
	print(CONFIGDATA)
	result = False
	try:
		with open(CONFIGPATH, "w") as jsonfile:
			json.dump(CONFIGDATA,jsonfile)
		result = True
	except Exception as e:
		Logger.GetInstance().LogException(e)
	return result



# MAIN PROGRAM WILL BE STARTED HERE, AFTER CONFIGURATION IS CHECKED!
def main():
	# Deside what database to load
	dbconn = MiniPAMSQLite(CONFIGDATA["DatabasePath"])
	dbconn.initialize()
	MiniPAMConsole(dbconn).start()

# CHECK CONFIGURATION HERE
def firstStart():
	global CONFIGDATA
	print("You are starting this application for the first time. We need to make some configurations first.")
	while True:
		result = input("Do you like to put the SQlite data in the default location (D) or choose a location (C) ?")
		match result.upper():
			case "D":
				dbpath = os.path.join(os.path.split(__file__)[0],"DATA","mimiPam.db")
				break
			case "C":
				dbpath = input("Enter a path for the SQlite database:")
				break
	CONFIGDATA = {"DatabasePath": dbpath }
	print(CONFIGDATA)
	SaveConfigFile()

if __name__ == "__main__":
	if LoadConfig():
		main() # RUN THE PROGRAM HERE
	else:
		if firstStart():
			pass # START AMIN WHEN CONFIGURATION IS SET OK

