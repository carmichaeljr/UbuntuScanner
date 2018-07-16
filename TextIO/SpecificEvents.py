"""
UBUNTU SCANNER
Developer: Jack Carmichael
Email: carmichaeljr@s.dcsdk12.org
"""
"""
Class				Type		Purpose
CommandLineEvents	Regular		Adds the ability to create events for the command line
SerialStreamEvents	Regular		Adds the ability to create events for a serial stream
CustomSerialStream	Inner		Makes a custom serial stream that adds auto-execute 
									functionality, so it can interface with events
"""

from TextIO.SerialStream import SerialStream
from TextIO.TextBasedEvents import TextBasedEvents


class CommandLineEvents(TextBasedEvents):
	def __init__(self,events=None):
		if not events==None:
			super(CommandLineEvents, self).__init__(events)
		
	def getCommand(self):
		self.cmdEntry=input(" > ")
		
		
class SerialStreamEvents(TextBasedEvents):
	class CustomSerialStream(SerialStream):
		def __init__(self,outerClass,autoRun):
			self.outerClass=outerClass
			self.autoRun=autoRun
			super(SerialStreamEvents.CustomSerialStream, self).__init__()
			
		def writeLine(self,newLine):
			super(SerialStreamEvents.CustomSerialStream, self).writeLine(newLine)
			if self.autoRun:
				self.outerClass.getCommand()
				self.outerClass.runCommand()
				
	def __init__(self,events):
		self.autoRun=True
		self.serialIn=SerialStreamEvents.CustomSerialStream(self,True)
		super(SerialStreamEvents, self).__init__(events)
		
	@property
	def serialStream(self):
		return self.serialIn
		
	@serialStream.setter
	def serialStream(self,newSerialStream):
		if isinstance(newSerialStream, SerialStreamEvents.CustomSerialStream):
			self.serialIn=newSerialStream
		
	def getCommand(self):
		if self.serialIn.readLineAvailable():
			self.cmdEntry=self.serialIn.readLine()
			# print(self.cmdEntry)
		

		
	
