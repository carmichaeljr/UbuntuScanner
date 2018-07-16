"""
UBUNTU SCANNER
Developer: Jack Carmichael
Email: carmichaeljr@s.dcsdk12.org
"""


from TextIO.SerialStream import SerialStream
from TextIO.TextBasedEvents import TextBasedEvent
from TextIO.TextBasedEvents import TextBasedEvents
from TextIO.SpecificEvents import CommandLineEvents
from TextIO.SpecificEvents import SerialStreamEvents

class Event(TextBasedEvent):
	def __init__(self,name):
		super(Event, self).__init__(name)

	def runEvent(self,*args):
		print(super(Event, self).name)
		
		
class Exit(TextBasedEvent):
	def __init__(self,name):
		self.exitState=False
		super(Exit, self).__init__(name)

	def runEvent(self,cmdArgs):
		print("Exit args: {0}".format(cmdArgs))
		if cmdArgs[0]=="true":
			self.exitState=True
		else:
			self.exitState=False
			
	def getExitState(self):
		return self.exitState


def testSerialStream():
	serialIn=SerialStream()
	serialIn.buffer="This is line 1\n"
	serialIn.clearBuffer()
	serialIn.writeLine("This is line 1")
	serialIn.writeLine("This is line 2")
	print(serialIn.buffer)
	while(serialIn.readLineAvailable()):
		print(serialIn.readLine())

def testCmdLineEvent():
	exit=Event("exit")
	print(exit.name)
	print("Cmd line event {0}".format(exit))
	print("Running event...")
	exit.runEvent()

def testCmdLineEvents():
	events=[Event("exit1"),Event("exit2"),Event("exit3")]
	allEvents=CommandLineEvents(events)
	allEvents.getCommand()
	allEvents.runCommand()
	
def testSerialCmdEvents():
	exitCmd=Exit("exit")
	events=[Event("one"),Event("two"),Event("three"),exitCmd]
	serialStreamEvents=SerialStreamEvents(events)
	while not exitCmd.getExitState():
		serialStreamEvents.serialStream.writeLine(input(" >"))	

if __name__=="__main__":
	testSerialStream()
	testCmdLineEvent()
	testCmdLineEvents()
	testSerialCmdEvents()
