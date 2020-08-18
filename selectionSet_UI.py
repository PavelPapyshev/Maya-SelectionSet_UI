import maya.cmds as mc
from PySide2 import QtWidgets, QtCore, QtGui
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin


class MyButton(QtWidgets.QWidget):
	
	"""
	creates a button widget
	
	accepts arguments:
		@objectName[str] - widget name
		@label[str] - inscription on the button
		@font[int] - lettering font
		@width[int] - minimum button width
		@height[int] - minimum button height
	"""
	
	#signal when releasing the pressed button
	myButtonClick = QtCore.Signal(str)
	
	def __init__(self, objectName="button", label="Button", font=15, width=375, height=40):
		
		super(MyButton, self).__init__()
		self.myButtonSetSettings(objectName, label, font, width, height)
	
	
	def myButtonSetSettings(self, objectName="button", label="Button", font=15, width=375, height=40):
		
		"""
		attribute initialization
		
		accepts arguments:
			@objectName[str] - widget name
			@label[str] - inscription on the button
			@font[int] - lettering font
			@width[int] - minimum button width
			@height[int] - minimum button height
		"""
		
		self.setObjectName(objectName)
		self.titleLabel = label
		self.fontLabel = font
		self.width = width
		self.height = height
		
		self.createUI()
	
	
	def createUI(self):
	
		"""
		sets the button and its elements settings
		"""
		
		#size
		self.setMinimumWidth(self.width)
		self.setMinimumHeight(self.height)
		
		#background color
		self.setAutoFillBackground(1)
		color = 85
		self.pal = self.palette()
		self.pal.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
		self.setPalette(self.pal)
		
		#main Layout
		self.mainLayout = QtWidgets.QHBoxLayout()
		self.setLayout(self.mainLayout)
		
		#label
		self.label = QtWidgets.QLabel()
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		
		self.label.setText(self.titleLabel)
		
		font = self.label.font()
		font.setPointSize(self.fontLabel)
		self.label.setFont(font)
		
		self.mainLayout.addWidget(self.label)
	

	def enterEvent(self, event):
		
		"""
		triggered when the cursor is hovered over
		"""
		
		color = 95
		
		self.pal.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
		self.setPalette(self.pal)
		
		super(MyButton, self).enterEvent(event)
	
	
	def leaveEvent(self, event):
	
		"""
		triggered when the cursor is removed
		"""
		
		color = 85
		
		self.pal.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
		self.setPalette(self.pal)
		
		super(MyButton, self).leaveEvent(event)
		
	
	def mousePressEvent(self, event):
		
		"""
		triggered when the mouse button is clicked
		"""
		
		if event.button() == QtCore.Qt.LeftButton:	
			
			color = 125
		
			self.pal.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
			self.setPalette(self.pal)
		
			super(MyButton, self).mousePressEvent(event)
	
	
	def mouseReleaseEvent(self, event):
	
		"""
		triggered when the mouse button is released
		"""
		
		if event.button() == QtCore.Qt.LeftButton:
		
			color = 95
		
			self.pal.setColor(self.backgroundRole(), QtGui.QColor(color, color, color))
			self.setPalette(self.pal)
		
			self.myButtonClick.emit(self.objectName())
		
			super(MyButton, self).mouseReleaseEvent(event)

#----------------END CLASS MyButton


class MySelSetButton(MyButton):
	
	"""
	creates a button selection set widget
	
	accepts arguments:
		@objectName[str] - widget name
		@label[str] - inscription on the button
		@font[int] - lettering font
		@width[int] - minimum button width
		@height[int] - minimum button height
		@objList[list] - set objects
	"""
	
	def __init__(self, objectName="button", label="Button", font=15, width=375, height=40, objList=None):
		
		super(MySelSetButton, self).__init__(objectName, label, font, width, height)
		self.MySelSetButtonSetSettings(selObj=objList)
		
	
	def MySelSetButtonSetSettings(self, selObj=None):
		
		"""
		attribute initialization
		
		accepts arguments:
			@objList[list] - set objects
		"""
	
		self.selObj = selObj
	
	
	def createUI(self):
	
		"""
		sets the button and its elements settings
		"""
		
		super(MySelSetButton, self).createUI()
		
		#context menu
		self.popMenu = QtWidgets.QMenu(self)
		
		#add to set
		self.popMenuAdd = QtWidgets.QAction("Add to set", self)
		self.popMenu.addAction(self.popMenuAdd)
		self.popMenuAdd.triggered.connect(self.addToSelSet)
		
		#remove from set
		self.popMenuRemFromSet = QtWidgets.QAction("Remove from set", self)
		self.popMenu.addAction(self.popMenuRemFromSet)
		self.popMenuRemFromSet.triggered.connect(self.removeFromSelSet)
		
		#rename set
		self.popMenuRenameSet = QtWidgets.QAction("Rename set", self)
		self.popMenu.addAction(self.popMenuRenameSet)
		self.popMenuRenameSet.triggered.connect(self.renameSelSet)
		
		#delete set
		self.popMenuDelSet = QtWidgets.QAction("Delete set", self)
		self.popMenu.addAction(self.popMenuDelSet)
		self.popMenuDelSet.triggered.connect(self.deleteSelSet)
		
		#settings menu
		self.setMouseTracking(True)
		self.setContextMenuPolicy(QtCore.Qt.CustomContextMenu)
		self.customContextMenuRequested.connect(self.onContextMenu)
		
	
	def onContextMenu(self, point):
		
		"""
		add context menu
		"""
		
		self.popMenu.exec_(self.mapToGlobal(point))
		
	
	def addToSelSet(self):
	
		"""
		add a new objects to the set
		"""
		
		objects = mc.ls(sl=1, l=1)
		
		for obj in objects:
			
			if not self.selObj.count(obj):
				self.selObj.append(obj)
	
	
	def removeFromSelSet(self):
		
		"""
		removes selected objects from the set
		"""
		
		objects = mc.ls(sl=1, l=1)
		
		for obj in objects:
			
			if self.selObj.count(obj):
				self.selObj.remove(obj)
	
	
	def renameSelSet(self):
	
		"""
		rename title button
		"""
		
		#delete label
		self.oldTitle = self.label.text()
		self.label.deleteLater()
		
		#create line edit
		self.lineEdit = QtWidgets.QLineEdit()
		self.lineEdit.setAlignment(QtCore.Qt.AlignCenter)
		self.lineEdit.setText(self.oldTitle)
		self.lineEdit.editingFinished.connect(self.setNewTitle)
		
		self.lineEdit.setStyleSheet("* { background-color: rgba(0, 0, 0, 0); border-radius: 0px; }")
		
		font = self.lineEdit.font()
		font.setPointSize(self.fontLabel)
		self.lineEdit.setFont(font)

		self.mainLayout.addWidget(self.lineEdit)
		self.lineEdit.selectAll()
		self.lineEdit.setFocus()
		
	
	def setNewTitle(self, newTitle=None):
		
		"""
		create new title button
		"""
		
		if not newTitle:
			newTitle = self.lineEdit.text()
		
		if not newTitle:
			newTitle = self.oldTitle
		
		self.lineEdit.deleteLater()
		self.createLabel(newTitle)
	
	
	def createLabel(self, title=None):
	
		"""
		create label
		"""
		self.label = QtWidgets.QLabel()
		self.label.setAlignment(QtCore.Qt.AlignCenter)
		
		if title:
			self.label.setText(title)
			
		else:
			self.label.setText(self.titleLabel)
		
		font = self.label.font()
		font.setPointSize(self.fontLabel)
		self.label.setFont(font)
		
		self.mainLayout.addWidget(self.label)

	
	def deleteSelSet(self):
		
		"""
		removes a set
		"""
		
		self.deleteLater()
	
	
	def mouseReleaseEvent(self, event):
		
		"""
		triggered when the mouse button is released
		"""
		
		if event.button() == QtCore.Qt.LeftButton:
		
			mc.select(cl=1)
		
			for obj in self.selObj:
			
				#if the object is not found in the scene, then remove it from the set
				try:
					mc.select(obj, tgl=1)
				except:
					mc.warning("Object '{}' not found and will be deleted from the set!".format(obj))
					self.selObj.remove(obj)
		
			super(MySelSetButton, self).mouseReleaseEvent(event)
		
	
	def keyPressEvent(self, event):
		
		"""
		triggered when pressed 'Escape', when entering a new title button
		"""
		
		if event.key() == QtCore.Qt.Key_Escape:
			self.setNewTitle(self.oldTitle)
				
		
		
#----------------END CLASS MySelSetButton


class SelectionSets(MayaQWidgetDockableMixin, QtWidgets.QDialog):
	
	"""
	creates a dialog window
	"""
	
	def __init__(self):
	
		super(SelectionSets, self).__init__()
		
		self.setObjectName("SelectionSets")
		self.createUI()
	
	
	def createUI(self):
		
		"""
		sets the window and its elements settings
		"""
		
		#settings
		#self.setMinimumWidth(400)
		#self.setMaximumWidth(400)
		#self.setMinimumHeight(500)
		self.setWindowTitle("Selection Sets")
		
		#main layout----------------------------------
		self.mainLayout = QtWidgets.QVBoxLayout()
		self.setLayout(self.mainLayout)
		
		#scroll----------------------------------
		self.scroll = QtWidgets.QScrollArea()
		self.scroll.setMinimumHeight(200)
		self.scroll.setWidgetResizable(True)
		self.scroll.setMinimumWidth(390)
		self.scroll.setFocusPolicy(QtCore.Qt.NoFocus)
		self.scroll.setFrameShape(QtWidgets.QFrame.NoFrame)
		self.scroll.setVerticalScrollBarPolicy(QtCore.Qt.ScrollBarAlwaysOn)
		
		self.scrollWidget = QtWidgets.QWidget()
		self.scroll.setWidget(self.scrollWidget)
		
		
		self.scrollLayout = QtWidgets.QVBoxLayout()
		self.scrollLayout.setAlignment(QtCore.Qt.AlignTop)
		self.scrollLayout.setContentsMargins(0,0,0,0)
		self.scrollLayout.setSpacing(5)
		self.scrollWidget.setLayout(self.scrollLayout)
		
		self.mainLayout.addWidget(self.scroll)
		
		#seporator----------------------------------
		self.seporator = QtWidgets.QFrame()
		self.seporator.setFrameShape(QtWidgets.QFrame.HLine)
		self.mainLayout.addWidget(self.seporator)
		
		#create set button----------------------------------
		self.btnCreateSet = MyButton(objectName="newSetBtn", 
									label="NEW SET", 
									font=13, 
									width=375, 
									height=70)
		self.btnCreateSet.myButtonClick.connect(self.clickNewSetBtn)
		self.mainLayout.addWidget(self.btnCreateSet)
		
	
	def clickNewSetBtn(self, name=None):
	
		"""
		triggered when a button "NEW SET" is pressed
		
		accepts arguments:
			@name[str] - name button
		"""
		
		#gets the name and label of the new button
		nameSet, titleSet = self.getNewObjName()
		
		#gets selected objects in the scene
		slList = mc.ls(sl=1, l=1)
		
		#create new button
		setBtn = MySelSetButton(objectName=nameSet, label=titleSet, font=10, objList=slList)
		self.scrollLayout.insertWidget(0, setBtn)

	
	def getNewObjName(self):
		
		"""
		selects the default button name
		
		return arguments:
			@name[str] - name button
			@title[str] - label button
			
		"""
		
		i = 1
		widgets = []
		
		for j in range(self.scrollLayout.count()):
			
			item = self.scrollLayout.itemAt(j)
			widget = item.widget()
			widgets.append(widget.objectName())
		
		while True:
			
			name = "SelectionSetBtn{}".format(i)
			title = None
			
			if widgets.count(name):
				i += 1
			
			else:
				title = "Selection Set {}".format(i)
				return name, title

				
	
#----------------END CLASS SelectionSets

def main():
	
	"""
	shows a dialog window
	"""

	if mc.workspaceControl("SelectionSetsWorkspaceControl", exists=1):
		mc.deleteUI("SelectionSetsWorkspaceControl", control = 1)
		mc.workspaceControlState("SelectionSetsWorkspaceControl", remove=1)
		
	window = SelectionSets()
	window.show(dockable=1, area="right", allowedArea="right", floating=1)
	
	mc.workspaceControl("SelectionSetsWorkspaceControl",
						label="Selection Sets",
						edit=1,
						tabToControl=["AttributeEditor", -1],
						widthProperty="fixed",
						initialWidth=400)