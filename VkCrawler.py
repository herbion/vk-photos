# -*- coding: utf-8 -*-
import VkCrawlerUi, VkWrapper
from PyQt4 import QtGui, QtCore
from model import ContentModel
from model.Node import Node
import types

class VkCrawler():
    def __init__(self, ui):
        self.window = QtGui.QMainWindow()
        self.ui = ui
        self.settings = {}
        self.vk_wrapper = VkWrapper.VkWrapper()
        
        self.root = Node("Hips")
        rootNode = self.root
        childNode0 = Node("Music", rootNode, type_info = "TRANSFORM")
        childNode1 = Node("RightPirateLeg_END",    childNode0)
        childNode2 = Node("Albums", rootNode, type_info = "CAMERA")
        childNode3 = Node("LeftTibia",             childNode2)
        childNode4 = Node("LeftFoot",              childNode3)
        childNode5 = Node("LeftFoot_END",          childNode4, type_info = "LIGHT")        
        
        
        rootNode = VkCrawler.buildTree({"music" : ["1", "2"],
                          "pictures" : [ {"album1" : ["pic1", "pic2"]},
                                         {"album2" : [] }, 
                          ]
        }, self.root)        
        print rootNode
        self.model = ContentModel.ContentModel(self.root)
                
    @staticmethod
    def buildTree(tree, root = None, item_type = None):
        root = root or Node("Root Node")
        for key in tree:
            parent = Node(key, root, type_info = "TRANSFORM")
            values = tree[key]
            for item in values:
                if isinstance(item, types.DictType):
                    VkCrawler.buildTree(item, root=parent)
                else :
                    Node(item, parent, type_info="CAMERA")
        return root
    def setupEvents(self):
        self.ui.columnView.setModel(self.model)    
        
        self.window.connect(self.ui.downloadButton, 
                            QtCore.SIGNAL("clicked()"), 
                            self.download)
        self.window.connect(self.ui.chooseSaveFolderButton, 
                            QtCore.SIGNAL("clicked()"), 
                            self.chooseSaveFolder)
        self.window.connect(self.ui.linkToTargetLineEdit, 
                            QtCore.SIGNAL("textChanged(QString)"),
                            self.chooseVkTarget)
        self.window.connect(self.ui.scanButton,
                            QtCore.SIGNAL("clicked()"),
                            self.scanForAlbums)
    def chooseVkTarget(self):        
        self.settings['target'] = self.ui.linkToTargetLineEdit.text()
    def chooseSaveFolder(self):
        folder = str(QtGui.QFileDialog.getExistingDirectory(self.window, 
                                                            "Select Directory"))
        self.ui.saveToFolderLineEdit.setText(folder)
        self.settings.update({'save_folder' :folder})
    def download(self):
        self.ui.progressBar.setValue(30)
    def scanForAlbums(self):
        self.notificate("Started albums scanning ...", 2000)
        self._auth()
        albums = self.vk_wrapper.get_albums()
        
        #albums = map(lambda a: (a['title'], a['aid']), albums)
        photos = {"photos" : []}
        
        for (i, album) in enumerate(albums[:10]):
            aid = album['aid']
            title = album['title']

            pics = self.vk_wrapper.get_album(aid)
            pics = map(lambda pic: pic["src"], pics)
            self.notificate("Checking album (%d/%d)" % (i, len(albums)), 1000 )
            
            
            photos['photos'].append({album['title']: pics})
        
        
        print self.buildTree(photos, self.root)
      
        self.model.emit(QtCore.SIGNAL("layoutChanged()"))
        self.window.repaint()        
        self.notificate("Fetched albums successfully", 2000)

    def notificate(self, message, msecs = 200):
        self.ui.statusbar.showMessage(message, msecs)
        self.window.repaint()
        
    def _auth(self):
        self.vk_wrapper.login = "import.future@gmail.com"
        self.vk_wrapper.password = "steadyasshegoes"
        try :
            self.vk_wrapper.connect()
            self.notificate("Authtenticaton -> Success", 2000)
        except Exception, e:
            print "Cannot authenticate vk, reason", e    
        


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = VkCrawlerUi.Ui_MainWindow()

    crawler = VkCrawler(ui)
    ui.setupUi(crawler.window)
    crawler.setupEvents()
    
    crawler.window.show()
    sys.exit(app.exec_())
    