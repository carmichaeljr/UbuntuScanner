"""
UBUNTU SCANNER
Developer: Jack Carmichael
Email: carmichaeljr@s.dcsdk12.org
"""


import os
import platform
import linecache


class File(object):
	@staticmethod
	def exists(absoultePath):
		returnValue=True
		try:
			_file=open(absoultePath,'r')
			_file.close()
		except IOError:
			returnValue=False
		return returnValue
			
			
	numOpenFiles=0	
	@classmethod
	def incrementNumOpenFiles(cls):
		cls.numOpenFiles+=1
		
	@classmethod
	def dincrementNumOpenFiles(cls):
		cls.numOpenFiles-=1
		
	
	def __init__(self,filePath,fileName):
		self._initPathVars(filePath,fileName)
		self._openForFirstTime()
		self._initFileVars()
		
	def __del__(self):
		if self._file!=None:
			self._closeFile()
		
	def _initPathVars(self,filePath,fileName):
		self._filePath=filePath
		self._fileName=fileName
		#print(fileName.split("."))
		if len(fileName.split("."))>1:
			self._fileExtension=fileName.split(".")[1]
		if platform.system().lower()=="linux":
			self._absolutePath=self._filePath+"/"+self._fileName
			# print("Linux!")
		elif platform.system().lower()=="windows":
			self._absolutePath=self._filePath+"\\"+self._fileName
			# print("Windows...")
		else :
			pass
			# print("Crapppppllle")
		# print(self._absolutePath)
		
	def _initFileVars(self):
		for _file in self.openCloseFileGenerator('r'):
			self._numLines=0
			for line in _file:
				self._numLines+=1 
				
	@property	
	def filePath(self):
		return self._filePath
		
	@property
	def fileName(self):
		return self._fileName
		
	@property
	def fileExtension(self):
		return self._fileExtension
		
	@property
	def absolutePath(self):
		return self._absolutePath
		
	@property
	def numLines(self):
		return self._numLines
		
	def _openForFirstTime(self):
		try:
			self._file=open(self._absolutePath,'r')
		except IOError:
			self._file=open(self._absolutePath,'w')
		finally:
			self._file.close()
			self._file=None
	
	def openCloseFileGenerator(self,newMode):
		self._openFile(newMode)
		yield self._file
		self._closeFile()
			
	def _openFile(self,newMode):
		if newMode.lower() in ['r','rb','r+','rb+','w','wb','w+','wb+','a','ab','a','ab+']:
			self._file=open(self._absolutePath,newMode)
			File.incrementNumOpenFiles()
		
	def _closeFile(self):
		self._file.close()
		self._file=None
		File.dincrementNumOpenFiles()
		
	def readLine(self,line):
		if isinstance(line,int) and line<=self._numLines:
			if linecache.checkcache(self._absolutePath):
				linecache.clearcache()
			return linecache.getline(self.absolutePath, line).rstrip()
		else:
			print("!> The given line({0}) excedes the files length({1})".
				  format(line,self.numLines))
			return ""
			
	def writeLine(self,newLine):
		if not isinstance(newLine,str):
			newLine=str(newLine)
		for _file in self.openCloseFileGenerator('a'):
			_file.write(newLine if newLine[len(newLine)-1]=='\n' else newLine+'\n')
			self._numLines+=1
			
	def deleteLine(self,lineContents):
		returnValue=False
		if not(isinstance(lineContents,str) and 
		   lineContents[len(lineContents)-1]=='\n'):
			lineContents=str(lineContents)+'\n'
		for _file in self.openCloseFileGenerator('r+'):
			allLines=self._file.readlines()
			_file.seek(0)
			for line in allLines:
				if not line.lower()==lineContents.lower():
					_file.write(line)
				else:
					# print("Deleted")
					self._numLines-=1
					returnValue=True
			_file.truncate()
		return returnValue
		
		
if __name__=="__main__":
	 #testFile=File("/media/falcon/USB_16GB/Temp Python Programs/Ubuntu Scanner/ProgramResources/Backend","TestFile.txt")
	#testFile=File("D:\\Temp Python Programs\\Ubuntu Scanner\\Backend\\ProgramResources","filenames.txt")
	#print(testFile.readLine(2))
	#print(testFile.readLine(30))
	#testFile.writeLine("THIS IS A TEST")
	#testFile.writeLine("THIS IS A TEST")
	#print(testFile.numLines)
	#testFile.deleteLine("HELLO")
	print(File.exists("/media/falcon/USB_16GB/Temp Python Programs/Ubuntu Scanner/Backend/ProgramResources/filenames.txt"))
	 
