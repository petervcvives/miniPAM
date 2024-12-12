import json
import os
from Logging.miniPAMLogger import Logger
from ConsoleApp.miniPAMConsole import MiniPAMConsole 
from Database.miniPAMSQLite import MiniPAMSQLite
from pathlib import Path


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
	try:
		# Deside what database to load (dbconn), for no only SQLite exists but whe could implment an other database by implementing the 'abstract' class MiniPAMDBConnection
		dbconn = MiniPAMSQLite(CONFIGDATA["DatabasePath"])
		dbconn.initialize() 

		# Deside here what unser inteface to load, here we choose the for now only existing the MiniPAMConsole as as interface.
		# When we would create and other user interce, for example a web interface, then we can make desired selection here. 
		MiniPAMConsole(dbconn).start()
	except Exception as e:
		Logger.GetInstance().LogException(e)




def getFileLocation():
	while True:
		filepath = input("Enter a path for the SQlite database:")
		if(os.path.splitext(filepath)[1] != ".db"):
			print("Invalid file extention, must be '.db'")
			continue
		if (os.path.exists(filepath)):
			print("File already exists, please enter an oter file location.")
			continue
		try:
			parentpath =  Path(filepath).parent.absolute()
			os.makedirs(parentpath,exist_ok = True)
			with open(filepath,"x") as teststream:
				teststream.write("test")
			os.remove(filepath)
		except Exception as e:
			print(f"File path invalid, try an other location. ({e})")
			continue
		return filepath

			

# CHECK CONFIGURATION HERE
def checkConfig():
	global CONFIGDATA
	try:
		print("You are starting this application for the first time. We need to make some configurations first.")
		while True:
			result = input("Do you like to put the SQlite data in the default location (D) or choose a location (C) ?")
			match result.upper():
				case "D":
					dbpath = os.path.join(os.path.split(__file__)[0],"DATA","mimiPam.db")
					break
				case "C":
					dbpath = getFileLocation()
					break
		CONFIGDATA = {"DatabasePath": dbpath }
		SaveConfigFile()
		return True
	except Exception as e:
		Logger.GetInstance().LogException(e)
		return False

if __name__ == "__main__":
	if LoadConfig():  # TRY TO LOAD THE CONFIGURATION HERE
		main() # RUN THE PROGRAM HERE
	else:
		if checkConfig(): # TRY TO CONFIGURE THE APPLICATION HERE
			main() # RUN THE PROGRAM HERE
			pass # START MAIN WHEN CONFIGURATION IS SET OK
		else:
			print("Something went wrong, configuration is not set correct!")


