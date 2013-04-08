import os
import sys
import getopt


class TestingEditor:

	filePath = ''
	language = ''
	testing = ''	
	def __init__(self,filePath,testing,language=None):
		self.filePath = filePath
		self.testing = testing
		self.language = language

		
	def run(self,filePath=None,language=None) :
				
		if filePath is None:
			filePath = self.filePath
		
		if os.path.basename(filePath).startswith('.'):
		    return

		if os.path.isdir(filePath):
			listing = os.listdir(filePath)
			for file in listing:
				self.run(os.path.abspath(os.path.join(filePath,file)))
			return
		
		originFile = open(filePath, 'r')
		
		if language is None:
			if os.path.splitext(filePath)[1] == '.js' :
				language = "javascript"
			elif os.path.splitext(filePath)[1] == '.py' :
				language = "python"
			elif os.path.splitext(filePath)[1] == '.html' :
				language = "html"
			else:
			    return
		
		#a seconda del linguaggio
		if language == "javascript": 
			basePattern = "//LOG@_"
			logFlag = "//TESTING@"
		if language == "python":	
			basePattern = "#LOG@_"
			logFlag = "#TESTING@"
		if language == "html":
			basePattern = "//LOG@_"
			logFlag = "<!--TESTING@-->"
			
		if self.testing == "true" or self.testing == "True" or self.testing == "1" :
			self.testing = True
		if self.testing == "false" or self.testing == "False" or self.testing == "0" :
			self.testing = False
			
		buffer = ""
		
		for line in originFile.readlines():
			if line.find(logFlag)!=-1:
				if self.testing:
					print "Already in testing mode"
					break
				else:
					continue
			if(line.find(basePattern)!=-1):
				if(len(line)-len(basePattern)==line.find(basePattern)+1):
					if not self.testing :
						line = line.replace(basePattern,'')
						indentation=''
						for c in line:
							if c=='\t' or c==' ' :
								indentation+=c
							else :
								break
						line = line.lstrip()
						line = indentation + basePattern + line
				else:
					if self.testing :
						line = line.replace(basePattern,'')
						line = line.replace('\n',basePattern+'\n')
			buffer+=line
		originFile.close()
		
		if buffer!='':
			originFile = open(filePath, 'w')
			if self.testing:
				originFile.write(logFlag+'\n')
			originFile.write(buffer)
			originFile.close()


if __name__ == '__main__':
	'''
	using python testingEditor.py -p ../media/shirop -t true (or false ) for activate
	or deactivate logstring for testing
	'''
	keywords = ['path=', 'language=', 'testingMode=' ]
	try:
		opts, extraparams = getopt.getopt(sys.argv[1:],'p:l:t:',keywords)
	except getopt.GetoptError, err:
		print err
		sys.exit()
	
	inputPath = None
	testing = False
	language = None

	for o,p in opts:
		if o in ['-p','--path']:
			inputPath = p
		if o in ['-t','--testingMode']:
			testing = p
		if o in ['-l','--language']:
			language = p
	
	if inputPath is None:
		print "The path is None, you must specified it!!!"
		sys.exit()
		
	temp = TestingEditor(inputPath,testing,language)
	temp.run(language=language)