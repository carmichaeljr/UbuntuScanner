# UbuntuScanner
This is a simple file comparison program that compares all the config files on a ubuntu machine(14.04) to what should be default. If it finds anything that is different, it will print out what lines are different in each file.

Dependencies:

	. You have to be logged in as sudo in order for the scanner to access the files.
	
	. You have to have the necessary packages installed to view the config files
	
			. apache2, vsftpd, open-ssh-server
			
<h4>Design</h4>
<p>
This project was designed with a frontend and a backend that are connected through a serial port. In this case, the frontend just writes the terminal input directly to the serial port, but in the case of a GUI much more structed input could be used to indicate actions.

This project also utilizes meta-classes to incorperate abstract methods in objects.
</p>
