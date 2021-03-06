"""
UBUNTU SCANNER
Developer: Jack Carmichael
Email: carmichaeljr@s.dcsdk12.org
"""


from Backend.FileWrapper import File


class FileComparison(object):
	def __init__(self,unchangedFile,changedFile):
		self._changedLines=list()
		self.setFiles(unchangedFile,changedFile)
		
	def getChangedLinesFormated(self):
		tempString1=" . Line(s): "
		tempString2=""
		for i in self._changedLines:
			if isinstance(i,int):
				tempString1+=("{0}, ".format(i))
			elif isinstance(i,str):
				tempString2+=(" . {0}".format(i))
		return [tempString1,tempString2]
	
	@property
	def changedLines(self):
		return self._changedLines
		
	@property
	def unchangedFile(self):
		return self._unchangedFile
		
	@property
	def changedFile(self):
		return self._changedFile
		
	def _validateFiles(self):
		if File.exists(self._unchangedFile.absolutePath) and \
		   File.exists(self._changedFile.absolutePath):
		   	return True
		else:
			return False
			
	def setFiles(self,newUnchangedFile,newChangedFile):
		if isinstance(newUnchangedFile,File):
			self._unchangedFile=newUnchangedFile
		else:
			self._unchangedFile=None
		if isinstance(newChangedFile,File):
			self._changedFile=newChangedFile
		else:
			self._changedFile=None
		self._changedLines=list()
			
	def runComparison(self):
		if self._validateFiles():
			self._setChangedLinesList()
			if len(self._changedLines)>0:
				return True
		else:
			print("!> The given files dont seem to exist")
		return False
		
	def _setChangedLinesList(self):
		rangeMax=min(self._unchangedFile.numLines,self._changedFile.numLines)
		for x in range(0,rangeMax):
			if not self._unchangedFile.readLine(x)==self._changedFile.readLine(x):
				self._changedLines.append(x)
		if not self._unchangedFile.numLines==self._changedFile.numLines:
			self._changedLines.append("File lengths are not the same")

			
if __name__=="__main__":
	#print(File.exists("/media/jack/USB_16GB/Temp Python Programs/Ubuntu Scanner/Backend/ProgramResources/filenames.txt"))
	#print(File.exists("/media/jack/USB_16GB/Temp Python Programs/Ubuntu Scanner/Backend/ProgramResources/filenames BACKUP.txt"))
	file1=File("/media/jack/USB_16GB/Temp Python Programs/Ubuntu Scanner/Backend/ProgramResources","filenames.txt")
	file2=File("/media/jack/USB_16GB/Temp Python Programs/Ubuntu Scanner/Backend/ProgramResources","filenames BACKUP.txt")
	testFileComparison=FileComparison(file1,file2)
	print(testFileComparison._validateFiles())
	print("RESULT: {0}".format(testFileComparison.runComparison()))
	print(testFileComparison.changedLines)
	
			
