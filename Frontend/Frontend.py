"""
UBUNTU SCANNER
Developer: Jack Carmichael
Email: carmichaeljr@s.dcsdk12.org
"""


from TextIO.TextBasedEvents import TextBasedEvent
from TextIO.SpecificEvents import SerialStreamEvents


class Printout(TextBasedEvent):
	def __init__(self):
		super(Printout,self).__init__("print")
	
	def runEvent(self,cmdArgs):
		# print(cmdArgs)
		if len(cmdArgs)>=2:
			if cmdArgs[0]=="error":
				self._printError(cmdArgs[1:len(cmdArgs)])
			elif cmdArgs[0]=="regular":
				self._printRegular(cmdArgs[1:len(cmdArgs)])
				
	def _printError(self,lines):
		print("!> {0}".format(lines[0]))
		for line in lines[1:len(lines)]:
			print("   {0}".format(line))
			
	def _printRegular(self,lines):
		print("   {0}".format(lines[0]))
		for line in lines[1:len(lines)]:
			print("   {0}".format(line))
		
		
class Frontend(object):
	def __init__(self):
		self._backendSerialStreamEventsRef=None
		printout=Printout()
		self._serialStreamEvents=SerialStreamEvents(printout)
		
	@property
	def serialStreamEvents(self):
		return self._serialStreamEvents
	
	@property
	def backendSerialStreamEventsRef(self):
		return self._backendSerialStreamEventsRef
	
	@backendSerialStreamEventsRef.setter
	def backendSerialStreamEventsRef(self,backendSerialStream):
		# if isinstance(backendSerialStream,SerialStreamEvents):
		self._backendSerialStreamEventsRef=backendSerialStream
			
	def getInput(self):
		_input=input("_> ")
		self._backendSerialStreamEventsRef.serialStream.writeLine(_input)
