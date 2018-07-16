"""
UBUNTU SCANNER
Developer: Jack Carmichael
Email: carmichaeljr@outlook.com
Dependencies:
	. You have to be logged in as sudo in order for the scanner to access the files.
	. You have to have the necessary packages installed to view the config files
			. apache2, vsftpd, open-ssh-server
"""


from Backend.Backend import Backend
from Frontend.Frontend import Frontend

if __name__=="__main__":
	backend=Backend()
	frontend=Frontend()
	backend.frontendSerialStreamEventsRef=frontend.serialStreamEvents
	frontend.backendSerialStreamEventsRef=backend.serialStreamEvents
	
	while not backend.getQuitState():	
		frontend.getInput()
