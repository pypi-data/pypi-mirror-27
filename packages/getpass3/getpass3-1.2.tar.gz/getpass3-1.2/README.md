# getpass2

A module similar like getpass in python except that echos are being encrypted before being displayed in the terminal.  
You can even change the the symbol with which the echos are being displayed.  
The default symbol for the encryption is '*'.  

## Usage:
Similar like getpass.
```python
#INPUT
import getpass2
getpass2.set_echo = '#' # Setting the symbol for encryption which will going to be displayed. (Optional)
getpass2.getpass("Password: ") # Giving a label to the input (One arguement is mandatory).
# getpass2.getpass("") (If you don't want to give any label)

#OUTPUT
#Password: ####
```

## Dependency
*Works currently with **Python 2.7.x**.*
	
#### Linux and MacOS 10.x.x
	Requires getch 1.0
#### Windows
	Requires colorama 0.3.9
