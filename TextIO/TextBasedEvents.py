"""
UBUNTU SCANNER
Developer: Jack Carmichael
Email: carmichaeljr@s.dcsdk12.org
"""
"""
Class				Type		Purpose
TextBasedEvent		Abstract	Defines the base functionality for any text based event
TextBasedEvents		Abstract	Defines the base for the management of any group
									of text based events
"""


from abc import ABCMeta,abstractmethod


class TextBasedEvents(metaclass=ABCMeta):
	def __init__(self,events=None):
		self._cmdEntry=""
		self._cmdEvents=list()
		if events!=None:
			self.addEvents(events)
	
	@property
	def cmdEntry(self):
		return self._cmdEntry

	@cmdEntry.setter
	def cmdEntry(self,entry):
		self._cmdEntry=entry

	def addEvents(self,events):
		if isinstance(events,list):
			for event in events:
				self.addEvent(event)
		elif isinstance(events,TextBasedEvent):
			self.addEvent(events)

	def addEvent(self,newEvent):
		addEvent=True
		if isinstance(newEvent,TextBasedEvent):
			for event in self._cmdEvents:
				if event.name==newEvent.name:
					addEvent=False
		if addEvent:
			self._cmdEvents.append(newEvent)
		else:
			print("!> The '{0}' event already exists".format(newEvent))
	
	@abstractmethod
	def getCommand():
		raise NotImplementedError

	def runCommand(self):
		eventRun=False
		args=self._splitCmdEntry()
		for event in self._cmdEvents:
			if event.name==args[0]:
				event.runEvent(args[1:len(args)])
				eventRun=True
		if not eventRun:
			print("!> The entry '{0}' was not recognized".format(self._cmdEntry))
			
	def _splitCmdEntry(self):
		args=list()
		tempString=""
		quoteFound=False
		for x in range(0,len(self._cmdEntry)):
			if self._cmdEntry[x]==' ' and not quoteFound:
				args.append(tempString)
				tempString=""
			elif self._cmdEntry[x]=='"' and quoteFound:
				args.append(tempString)
				tempString=""
				quoteFound=False
			elif self._cmdEntry[x]=='"' and not quoteFound:
				quoteFound=True
			else:
				tempString+=self._cmdEntry[x]
		if len(tempString)>0:
			args.append(tempString)
		return args			


class TextBasedEvent(metaclass=ABCMeta):
	def __init__(self,name):
		self._name=name

	def __str__(self):
		return "<Cmd Line Event Obj::[Name:{0:>10}]>".format(self._name)
	
	def __format__(self,other):
		return "<Cmd Line Event Obj::[Name:{0:>10}]>".format(self._name)

	@property
	def name(self):
		return self._name

	@name.setter
	def name(self,newName):
		self._name=newName
	
	@abstractmethod
	def runEvent(self,cmdArgs):
		raise NotImplementedError
		

	
