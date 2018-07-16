"""
UBUNTU SCANNER
Developer: Jack Carmichael
Email: carmichaeljr@s.dcsdk12.org
"""


from Backend.FileWrapper import File
from Backend.ConfigFile import ConfigFile
from Backend.FileComparison import FileComparison
from TextIO.TextBasedEvents import TextBasedEvent
from TextIO.SpecificEvents import SerialStreamEvents


class BackendEvent(TextBasedEvent):
	def __init__(self,configFileRef,frontendSerialStream):
		self._configFileRef=configFileRef
		self._frontendSerialStreamEventsRef=frontendSerialStream
	
	@property
	def frontendSerialStreamEventsRef(self):
		return self._frontendSerialStreamEventsRef
		
	@frontendSerialStreamEventsRef.setter
	def frontendSerialStreamEventsRef(self,frontendSerialStream):
		self._frontendSerialStreamEventsRef=frontendSerialStream
		
	@property
	def configFileRef(self):
		return self._configFileRef
		
	@configFileRef.setter
	def configFileRef(self,configFileRef):
		self._configFileRef=configFileRef
		

class ComparePath(BackendEvent):
	def __init__(self,configFileRef,frontendSerialStreamEventsRef):
		super(ComparePath,self).__init__(configFileRef,frontendSerialStreamEventsRef)
		super(BackendEvent,self).__init__("comparepath")
		
	def runEvent(self,cmdArgs):
		# print(cmdArgs)
		if len(cmdArgs)==2 and (cmdArgs[0].lower() in ['add','del']):
			if cmdArgs[0].lower()=='add':
				self._addPath(cmdArgs[1])
			elif cmdArgs[0].lower()=='del':
				self._delPath(cmdArgs[1])
		elif len(cmdArgs)==1 and cmdArgs[0].lower()=='print':
			self._printFileContents()
		else:
			errString='"Incorrect arguments or number of argumets"'+\
					  '"Accepted arguments are:"'+\
					  '" . add [path]"'+\
					  '" . del [path]"'+\
					  '" . print"'
			self.frontendSerialStreamEventsRef.serialStream.writeLine(\
				"print error {0}".format(errString))
			
	def _addPath(self,newPath):
		rv=self.configFileRef.addFilePath(newPath)
		if len(rv)>0:
			self.frontendSerialStreamEventsRef.serialStream.writeLine(
				"print error {0}".format(rv))
		
	def _delPath(self,oldPath):
		rv=self.configFileRef.deleteLine(oldPath)
		if rv:
			errString=" . Path deleted from path list"
		else:
			errString=" . Path was not found in the path list"
		self.frontendSerialStreamEventsRef.serialStream.writeLine(\
			'print regular "{0}"'.format(errString))
			
	def _printFileContents(self):
		self.frontendSerialStreamEventsRef.serialStream.writeLine(\
			'print regular "All compare paths:"')
		for x in range(1,self.configFileRef.numLines+1):
			self.frontendSerialStreamEventsRef.serialStream.writeLine(\
				'print regular " . {0}"'.format(self.configFileRef.readLine(x)))
			
			
class Scan(BackendEvent):
	def __init__(self,configFileRef,frontendSerialStreamEventsRef):
		super(Scan,self).__init__(configFileRef,frontendSerialStreamEventsRef)
		super(BackendEvent,self).__init__("scan")
		self.diffFiles=list()
		
	def runEvent(self,cmdArgs):
		if len(cmdArgs)==1:
			if cmdArgs[0].lower()=='run':
				self._runScan()
			elif cmdArgs[0].lower()=='results':
				self._printScanResults()
		else:
			errString='"Incorrect arguments or number of argumets"'+\
					  '"Accepted arguments are:"'+\
					  '" . run"'+\
					  '" . results"'
			self.frontendSerialStreamEventsRef.serialStream.writeLine(\
				"print error {0}".format(errString))
	
	def _runScan(self):
		self.diffFiles=list()
		for x in range(1,self.configFileRef.numLines):
			line=self.configFileRef.readLine(x)
			fileLine=""
			for path in line.split('/')[0:len(line.split('/'))-1]:
				if len(path)>0:
					fileLine+="/{0}".format(path)
			fileName="{0}".format(line.split('/')[len(line.split('/'))-1:len(line.split('/'))][0])
			unchangedFile=File("Backend/ProgramResources/UnchangedConfigFiles","{0}".format(fileName))
			changedFile=File(fileLine,fileName)
			fileComparison=FileComparison(unchangedFile,changedFile)
			self.frontendSerialStreamEventsRef.serialStream.writeLine(
				'print regular "Scanning {0}..."'.format(line))
			fileComparison.runComparison()
			if len(fileComparison.changedLines)>0:
				self.diffFiles.append(fileComparison)
				
	def _printScanResults(self):
		if len(self.diffFiles)>0:
			for fileComparison in self.diffFiles:
				self._printToFrontend("The file '{0}' is differnent in these ways:".\
					format(fileComparison.changedFile.fileName))
				self._printToFrontend(fileComparison.getChangedLinesFormated()[0])
				if len(fileComparison.getChangedLinesFormated()[1])>0:
					self._printToFrontend(fileComparison.getChangedLinesFormated()[1])
		else:
			self.frontendSerialStreamEventsRef.serialStream.writeLine(
				'print error "There are no results to be shown"')
			self.frontendSerialStreamEventsRef.serialStream.writeLine(
				'print regular " . Either all the files are unchanged or a scan has not been run yet."')
				
	def _printToFrontend(self,string):
		self.frontendSerialStreamEventsRef.serialStream.writeLine(
			'print regular "{0}"'.format(string))


class Help(BackendEvent):
	def __init__(self,configFileRef,frontendSerialStreamEventsRef):
		super(Help,self).__init__(configFileRef,frontendSerialStreamEventsRef)
		super(BackendEvent,self).__init__("help")
		
	def runEvent(self,cmdArgs):
		errString='"Accepted commands are:"'+\
				  '" . scan [run or results]"'+\
				  '" . comparepath [add, del, or print] [path]"'
		self.frontendSerialStreamEventsRef.serialStream.writeLine(\
			"print regular {0}".format(errString))


class QuitProgram(TextBasedEvent):
	def __init__(self):
		super(QuitProgram,self).__init__("exit")
		self._quit=False
		
	@property
	def quit(self):
		return self._quit
		
	def runEvent(self,cmdArgs):
		self._quit=True
		
		
class Backend(object):
	def __init__(self):
		self._frontendSerialStreamEventsRef=None
		self.configFile=ConfigFile()
		
		self.comparePath=ComparePath(self.configFile,self._frontendSerialStreamEventsRef)
		self.scan=Scan(self.configFile,self._frontendSerialStreamEventsRef)
		self.help=Help(self.configFile,self._frontendSerialStreamEventsRef)
		self.quitProgram=QuitProgram()
		allEvents=[self.comparePath,self.scan,self.help,self.quitProgram]
		
		self._serialStreamEvents=SerialStreamEvents(allEvents)
		
	@property
	def serialStreamEvents(self):
		return self._serialStreamEvents
	
	@property
	def frontendSerialStreamEventsRef(self):
		return self._frontendSerialStreamEventsRef
		
	@frontendSerialStreamEventsRef.setter
	def frontendSerialStreamEventsRef(self,frontendSerialStream):
		# if isinstance(frontendSerialStream,SerialStreamEvents):
		self._frontendSerialStreamEventsRef=frontendSerialStream
		self.comparePath.frontendSerialStreamEventsRef=frontendSerialStream
		self.scan.frontendSerialStreamEventsRef=frontendSerialStream
		self.help.frontendSerialStreamEventsRef=frontendSerialStream
			
	def getQuitState(self):
		return self.quitProgram.quit
