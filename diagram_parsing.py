from bs4 import BeautifulSoup as Soup

class DiagramElemError(Exception):
	print("Diagram parametr not valid")

class DiagramObject(object):
	value = None
	obj_id = None
	con_id = []  #connection identificators
	state = None

	def __init__(self, value, obj_id):
		self.value = value
		self.my_id = obj_id

	def get_value(self):
		return self.value

	def get_connections(self):
		return self.con_id

	def get_id(self):
		return self.obj_id

	def get_state(self):
		return self.state

	def set_state(self, state):
		self.state = state

	def add_connection(self, connection_id):
		if connection_id != None:
			self.con_id.append(connection_id)
		else:
			raise DiagramElemError

	def __str__(self):
		print("ID = " + str(self.obj_id) + " | Value = " + str(self.value))
		print('Connections id ' + str(self.get_connections()))


class DiagramArrow(DiagramObject):
	#DiagramArrow - bot button
	target_id = None
	source_id = None

	def __init__(self, text, elem_id, source, target):
		super().__init__(text, elem_id)
		self.source_id = source
		self.target_id = target

	def get_target_id(self):
		return self.target_id

	def get_source_id(self):
		return self.source_id

	def add_connection(self, connection_id):
		print("Method do not use for this object")

class BotMsg(DiagramObject):

	def __init__(self, msg, obj_id):
		super().__init__(msg, obj_id)

	def get_msg(self):
		return super().get_value()

class BotDiagram(object):
	#In begining must create all messages(blocks) and just after this - buttons
	messages = []
	buttons = []

	def __init__(self):
		pass

	def find_msg(self, msg_id):
		for msg in self.messages:
			if msg.get_id() == msg_id:
				return msg
		return None

	def find_button(self, button_id):
		for button in self.buttons:
			if button.get_id() == button_id:
				return button
		return None

	def new_msg(self, msg, obj_id):
		self.messages.append(BotMsg(msg, obj_id))

	def new_button(self, value, obj_id, source_id, target_id):
		if not self.find_msg(target_id):
			print("Target block does not exist")
			print("Arrows with value \"" + str(value) + " \"")
			raise DiagramElemError
		self.buttons.append(DiagramArrow(value, obj_id, source_id, target_id))
		msg = self.find_msg(source_id)
		if msg:
			msg.add_connection(obj_id)
		else:
			print("Message does not exist")
			raise DiagramArrow

	def get_messages_id(self):
		msgs = []
		for msg in self.messages:
			msgs.append(msg.get_id())
		print(msgs)

	def get_buttons_id(self):
		butns = []
		for button in self.buttons:
			butns.append(button.get_id())
		print(butns)

	def start_point(self):
		start_msg = None
		for msg in self.messages:
			msg_id = msg.get_id()
			link = None
			for button in self.buttons:
				if button.get_target_id() == msg_id:
					link = msg_id
					break
			if link == None and start_msg != None:
				print("The diagram have more than one starting position")
				raise DiagramElemError
			if link == None:
				start_msg = msg
		if start_msg == None:
			print("The diagram does not have a clearly defined starting position")
			raise DiagramElemError
		else:
			return start_msg

	def __str__(self):
		print("Messages id " + str(self.get_messages_id()))
		print("Buttons id " + str(self.get_buttons_id()))

# def find_all_arrow(root):
	#arrow it`s "mxcell" tag with style param "edgeStyle=orthogonalEdgeStyle" or with "endArrow=classic"


def get_all_objects(root, tag_name, *attributes):
	objects = []
	for tag in root.findAll(tag_name):
		attrib_available = False
		for attrib in attributes:
			if attrib not in tag.attrs:
				attrib_available = False
				break
			else:
				attrib_available = True
		if attrib_available:
			objects.append(tag)
	return objects


def is_object_style(obj, pos_style_list=[], neg_style_list=[]):
	style = obj['style'].split(';')
	for param in pos_style_list:
		if param not in style:
			return False
	for param in neg_style_list:
		if param in style:
			return False
	return True


def get_arrows_block(obj_list):
	arrows = []
	i = 0
	while i < len(obj_list):
		if 'source' in obj_list[i].attrs and 'target' in obj_list[i].attrs:
			if is_object_style(obj_list[i], pos_style_list = ['endArrow=classic'], neg_style_list = ['startArrow=classic']) or is_object_style(obj_list[i], pos_style_list=['edgeStyle=orthogonalEdgeStyle', 'orthogonalLoop=1']):
				arrows.append(obj_list.pop(i))
				i -= 1
		i += 1
	return arrows


def get_process_block(obj_list):
	process = []
	i = 0
	while i < len(obj_list):
		if is_object_style(obj_list[i], pos_style_list=['shape=process']):
			process.append(obj_list.pop(i))
			i -= 1
		i += 1
	return process


def get_message_block(obj_list):
	messages = []
	i = 0
	while i < len(obj_list):
		if is_object_style(obj_list[i], pos_style_list=['rounded=0'], neg_style_list=['rounded=1', 'ellipse']):
			messages.append(obj_list.pop(i))
			i -= 1
		i += 1
	return messages


def create_structure(arrows, messages):
	diagram = BotDiagram()
	for message in messages:
		diagram.new_msg(message['value'], message['id'])
	for arrow in arrows:
		diagram.new_button(arrow['value'], arrow['id'], arrow['source'], arrow['target'])

def parse_diagram(file_path):
	'''
	Take path to *.xml file with diagram
	Diagram make in draw.io
	Export to XML without compress
	'''
	with open(file_path) as f:
		soup = Soup(f.read(), 'lxml')
		# print(soup.prettify())
		root = soup.find('root')
		all_obj = get_all_objects(root, 'mxcell', 'value', 'style')
		# for elem in all_obj:
		# 	print(elem.attrs)
		print("Arrows")
		arr = get_arrows_block(all_obj)
		for arrows in arr:
			print(arrows)
		print("Massages")
		message = get_message_block(all_obj)
		for mes in message:
			print(mes)
		if len(all_obj) == 0:
			create_structure(message, arr)
			print("Diagram valid")

		else:
			print("Diagram not valid")
		print("Else element")
		for elem in all_obj:
			print(elem)

#Detect graph root (1 connection, only like source)
parse_diagram('test_connect_new2.xml')