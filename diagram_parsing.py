from lxml import etree

class Button(object):
	text = ''
	link = None

	def __init__(self, text, link):
		self.text = text
		self.link = link

	def get_text(self):
		return self.text

	def get_link(self):
		return self.link


class BotMsg(object):
	msg = ''
	def __init__(self, msg):
		self.msg = msg

	def get_msg(self):
		return self.msg

class BotDiagram(object):

	def __init__(self):
		pass

	def new_msg(self, msg):



def parse_diagram(file_path):
	'''
	Take path to *.xml file with diagram
	Diagram make in draw.io
	Export to XML without compress
	'''
	with open(file_path, 'rb') as f:
		root = etree.XML(f.read())
		root = root[0]
		for elem in root:
			if elem.tag == 'mxCell':
				print(elem.attrib)

#Detect graph root (1 connection, only like source)
parse_diagram('linear_diagram.xml')