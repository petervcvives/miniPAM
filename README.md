# miniPAM
## Mini personal asset management
An asset management for yourself, to manage items in your home. I wrote this as a assignment for my micro degree at the VIVES.
Becasue I could choose what to make I choose to make a mini asset management tool to manage my electronic componenets. But I can be used to manage other asset types too.

A GUI has not (yet) been create for it, therefore it will work only using the command line interface.

# Tested platforms
The tool has only been tested on windows and macos. It has not yet been tested on linux. Not all functionality is implemeneted 

# Installation and requirements
This script requires python 3 or higher (Create in version 3.12).

To run the tool create a venv and install the 'requirements_win' for windows and 'requirements_macos' on macOS. A single requirements file was not possible due to readline not beeing compatible on both systems, therefore we need to install 'gnureadline' for macOS or 'pyreadline3' on Windows. The mean reason to use the 'readline' module is to ba able to pre-enter test in a console input, for example when an asset description needs to be updated then it is nice update the text instead of re-enter the complete text.  

To start the tool run "python miniPam.py" in a venv updated with the requirements_win.txt or requirements_macos installed.

# First time start

When started for the first time it wil create a SQlite database and a configuration file. It will ask where to save the SQLlite database and the configuration file will be saved in root folder as 'miniPAM.config'. The default database location will be 

# Implemented functionality

The foloowing function are implemneted
|Function| Description|
| -- | -- |
|Show all unit types					  | Shows a list of the available unit types (bottels, pieces, etc..) |
|Add new asset                            | Add a new asset. |
|Search in assets                         | Allow you to search the name and description of the assets and outputs the search result.|
|Show all assets                          | Show a list of all assets available with the with the current amount of units available. |
|Update assets                            | Allow you to update an asset's name and description. |
|Export all assets to CSV file.           | Exposrt a list of all assets with the current amount of units available. |
	

# Code structure

The tool exists out of 3 folders:

- ConsoleApp: Contain the console application. The console is startedfrom main miniPAM.py. It is not starte using the class `MiniPAMConsole`, using the start() function. The database connection class is provided duringon of the console object in the constructor.


- Database: Contains two classes `MiniPAMDBConnection` and `MiniPAMSQLite`. The `MiniPAMDBConnection` is an 'abstract' class that acts as the template for the `MiniPAMSQLite` (inherits from MiniPAMDBConnection`). It is the `MiniPAMSQLite` class that will be instatiated and used in miniPAM.py. Because we use the abstract `MiniPAMDBConnection` class we can easy interchange the SQLite database with an other database by implmenting `MiniPAMDBConnection` into a new class. 


- Logging: Conatains a class that handles some logging. The class is a singleton that can be used by calling Logger.GetInstance() to get the `Logger` object.


