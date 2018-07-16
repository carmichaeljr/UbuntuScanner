# UbuntuScanner
This is a simple file comparison program that compares all the config files on a ubuntu machine(14.04) to what should be default. If it finds anything that is different, it will print out what lines are different in each file.
Dependencies:

	. You have to be logged in as sudo in order for the scanner to access the files.

	. You have to have the necessary packages installed to view the config files

			. apache2, vsftpd, open-ssh-server
