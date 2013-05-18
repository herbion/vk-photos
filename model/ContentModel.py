# -*- coding: utf-8 -*-
"""
Created on Sat May 18 09:59:31 2013

@author: herbion
"""

from PyQt4 import QtCore, QtGui
import sys
import icons_rc



class ContentModel(QtCore.QAbstractItemModel):
    
    """INPUTS: Node, QObject"""
    def __init__(self, root, parent=None):
        super(ContentModel, self).__init__(parent)
        self._rootNode = root

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def rowCount(self, parent):
        if not parent.isValid():
            parentNode = self._rootNode
        else:
            parentNode = parent.internalPointer()

        return parentNode.childCount()

    """INPUTS: QModelIndex"""
    """OUTPUT: int"""
    def columnCount(self, parent):
        return 1
    
    """INPUTS: QModelIndex, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def data(self, index, role):
        
        if not index.isValid():
            return None

        node = index.internalPointer()

        if role == QtCore.Qt.DisplayRole or role == QtCore.Qt.EditRole:
            if index.column() == 0:
                return node.name()
        if role == QtCore.Qt.DecorationRole:
            if index.column() == 0:
                typeInfo = node.typeInfo()
                
                if typeInfo == "LIGHT":
                    return QtGui.QIcon(QtGui.QPixmap(":/Light.png"))
                
                if typeInfo == "TRANSFORM":
                    return QtGui.QIcon(QtGui.QPixmap(":/Transform.png"))
                
                if typeInfo == "CAMERA":
                    return QtGui.QIcon(QtGui.QPixmap(":/Camera.png"))



    """INPUTS: QModelIndex, QVariant, int (flag)"""
    def setData(self, index, value, role=QtCore.Qt.EditRole):

        if index.isValid():
            
            if role == QtCore.Qt.EditRole:
                
                node = index.internalPointer()
                node.setName(value)
                
                return True
        return False

    
    """INPUTS: int, Qt::Orientation, int"""
    """OUTPUT: QVariant, strings are cast to QString which is a QVariant"""
    def headerData(self, section, orientation, role):
        if role == QtCore.Qt.DisplayRole:
            if section == 0:
                return "Scenegraph"
            else:
                return "Typeinfo"

        
    
    """INPUTS: QModelIndex"""
    """OUTPUT: int (flag)"""
    def flags(self, index):
        return QtCore.Qt.ItemIsEnabled | QtCore.Qt.ItemIsSelectable | QtCore.Qt.ItemIsEditable

    

    """INPUTS: QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return the parent of the node with the given QModelIndex"""
    def parent(self, index):
        
        node = self.getNode(index)
        parentNode = node.parent()
        
        if parentNode == self._rootNode:
            return QtCore.QModelIndex()
        
        return self.createIndex(parentNode.row(), 0, parentNode)
        
    """INPUTS: int, int, QModelIndex"""
    """OUTPUT: QModelIndex"""
    """Should return a QModelIndex that corresponds to the given row, column and parent node"""
    def index(self, row, column, parent):
        
        parentNode = self.getNode(parent)

        childItem = parentNode.child(row)


        if childItem:
            return self.createIndex(row, column, childItem)
        else:
            return QtCore.QModelIndex()



    """CUSTOM"""
    """INPUTS: QModelIndex"""
    def getNode(self, index):
        if index.isValid():
            node = index.internalPointer()
            if node:
                return node
            
        return self._rootNode

    
    """INPUTS: int, int, QModelIndex"""
    def insertRows(self, position, rows, parent=QtCore.QModelIndex()):
        
        parentNode = self.getNode(parent)
        
        self.beginInsertRows(parent, position, position + rows - 1)
        
        for row in range(rows):
            
            childCount = parentNode.childCount()
            childNode = Node("untitled" + str(childCount))
            success = parentNode.insertChild(position, childNode)
        
        self.endInsertRows()

        return success
    
    def insertLights(self, position, rows, parent=QtCore.QModelIndex()):
        
        parentNode = self.getNode(parent)
        
        self.beginInsertRows(parent, position, position + rows - 1)
        
        for row in range(rows):
            
            childCount = parentNode.childCount()
            childNode = Node("light" + str(childCount), type_info="LIGHT")
            success = parentNode.insertChild(position, childNode)
        
        self.endInsertRows()

        return success

    """INPUTS: int, int, QModelIndex"""
    def removeRows(self, position, rows, parent=QtCore.QModelIndex()):
        
        parentNode = self.getNode(parent)
        self.beginRemoveRows(parent, position, position + rows - 1)
        
        for row in range(rows):
            success = parentNode.removeChild(position)
            
        self.endRemoveRows()
        
        return success


    
    
    
    
if __name__ == '__main__':
    
    app = QtGui.QApplication(sys.argv)

    
    rootNode   = Node("Hips")
    childNode0 = Node("Music", rootNode, type_info = "TRANSFORM")
    childNode1 = Node("RightPirateLeg_END",    childNode0)
    childNode2 = Node("Albums", rootNode, type_info = "CAMERA")
    childNode3 = Node("LeftTibia",             childNode2)
    childNode4 = Node("LeftFoot",              childNode3)
    childNode5 = Node("LeftFoot_END",          childNode4, type_info = "LIGHT")

    print rootNode
    
    model = ContentModel(rootNode)
   
    treeView = QtGui.QColumnView()#QtGui.QTreeView()
    treeView.show()
    
    treeView.setModel(model)
    
    
    rightPirateLeg = model.index(0, 0, QtCore.QModelIndex())
    
    #model.insertRows(1, 5, rightPirateLeg)
    #model.insertLights(1, 5 , rightPirateLeg)

    sys.exit(app.exec_())