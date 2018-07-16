"""
UBUNTU SCANNER
Developer: Jack Carmichael
Email: carmichaeljr@s.dcsdk12.org
"""
"""
Class				Type		Purpose
SerialStream		Regular		Makes a serial stream that can be used for any
									text based communication
"""


class SerialStream(object):
	def __init__(self):
		self._buffer=""
		self.buffer=""
	
	@property
	def buffer(self):
		return self._buffer

	@buffer.setter
	def buffer(self,newLine):
		if isinstance(newLine,str):
			self._buffer+=newLine

	def writeLine(self,newLine):
		if isinstance(newLine,str) and newLine[len(newLine)-1]!='\n':
			self._buffer+=newLine+"\n"
		elif isinstance(newLine,str):
			self._buffer+=newLine
			
	def readLine(self):
		returnString=""
		for x in range(0,len(self._buffer)):
			if self._buffer[x]=='\n':
				self.__trimBuffer(x+1)
				break
			returnString+=self._buffer[x]
		return returnString

	def readLineAvailable(self):
		for x in range(0,len(self._buffer)):
			if self._buffer[x]=="\n":
				return True
		return False

	def clearBuffer(self):
		self._buffer=""

	def __trimBuffer(self,newFirstIndex):
		self._buffer=self._buffer[newFirstIndex:len(self._buffer)]

