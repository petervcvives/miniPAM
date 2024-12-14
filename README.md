# miniPAM
## Mini personal asset management
An asset management for yourself, to manage items in your home. I wrote this as an assignment for my microdegree at the VIVES.
I choose to create a mini asset management tool to manage my electronic components. But I could be used to manage other asset types too.

A GUI has not (yet) been created for it, therefore it will work only using the command line interface.

The tool is not completed yet, but I hope to do so later. 

# Tested platforms
The tool has only been tested on windows and macos. It has not yet been tested on linux. 

# Installation and requirements
This script requires python 3 or higher (Create in version 3.12).

To install this tool,  create a venv and install the <b>'requirements_win'</b> for windows and <b>'requirements_macos'</b> on macOS. A single requirements file seems not possible due to 'readline' module not being compatible on both systems, therefore we need to install 'gnureadline' for macOS or 'pyreadline3' on Windows. 
The 'readline' modules are used to allow pre-enter text in a console input, for example when an asset description needs to be updated then it is nice to update the text instead of re-entering the complete text.  

To start this tool, run the 'miniPAM.py' file using python.

# First time start

When started for the first time, it will create a SQlite database and a configuration file. It will ask where to save the SQLlite database and the configuration file will be saved in root folder as 'miniPAM.config'. The default database location will be in the "DATA" folder create in the root folder.

# Implemented functionality

The following function were implemented:

|Function| Description|
| -- | -- |
|Show all unit types					  | Shows a list of the available unit types (bottles, pieces, etc..) |
|Add new asset                            | Add a new asset. |
|Search in assets                         | Allow you to search the name and description of the assets and outputs the search result.|
|Show all assets                          | Show a list of all assets available with the current amount of units available. |
|Update assets                            | Allow you to update an asset's name and description. |
|Export all assets to CSV file.           | Export a list of all assets with the current amount of units available. |
	

# Code structure

The tool exists out of 3 folders:

- ConsoleApp: Contain the console application. It is started using the class `MiniPAMConsole`with the  the start() function (This is started from main miniPAM.py file). The database connection class is provided in the  the constructor of the 'MiniPAMConsole' class.

- Database: Contains two classes `MiniPAMDBConnection` and `MiniPAMSQLite`. The `MiniPAMDBConnection` is an 'abstract' class that acts as the template for the `MiniPAMSQLite` (inherits from `MiniPAMDBConnection`). It is the `MiniPAMSQLite` class that will be instantiated and used in miniPAM.py. Because we use the "abstract" `MiniPAMDBConnection` class we can easily interchange the SQLite database with another database by implementing `MiniPAMDBConnection` into a new class. 


- Logging: Contains a class that handles some logging. The class is a singleton that can be used by calling Logger.GetInstance() to get the `Logger` object.



