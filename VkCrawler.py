# -*- coding: utf-8 -*-
import VkCrawlerUi, VkWrapper, LoginDialogUi
from PyQt4 import QtGui, QtCore
from model.Node import Node
import types, urllib2

import datetime

_fromUtf8 = QtCore.QString.fromUtf8

class Utils: 
    @staticmethod
    def to_human_time(unix):
        return datetime.datetime.fromtimestamp(int(unix)).strftime('%Y-%m-%d %H:%M:%S')
    
    @staticmethod
    def download_file(url, save_folder, progress_bar = None):
        file_name = url.split('/')[-1]
        u = urllib2.urlopen(url)
        f = open(save_folder + file_name, 'wb')
        meta = u.info()
        file_size = int(meta.getheaders("Content-Length")[0])
        print "Downloading: %s Bytes: %s" % (file_name, file_size)
        
        file_size_dl = 0
        block_sz = 8192
        while True:
            buffer = u.read(block_sz)
            if not buffer:
                break
        
            file_size_dl += len(buffer)
            f.write(buffer)
            status = r"%10d  [%3.2f%%]" % (file_size_dl, file_size_dl * 100. / file_size)
            if progress_bar:
                progress_bar.setProperty('value', file_size_dl * 100. / file_size)
            status = status + chr(8)*(len(status)+1)
            print status,
        
        f.close()
        
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
class VkCrawler():
    def __init__(self, ui):
        self.window = QtGui.QMainWindow()
        self.ui = ui
        self.settings = {}
        self.vk_wrapper = VkWrapper.VkWrapper()
        self.download_list = []
                

    def setupEvents(self):
        #self.ui.columnView.setModel(self.model)    

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
        self.window.connect(self.ui.selectAllButton,
                            QtCore.SIGNAL("clicked()"),
                            self.selectAll)
    def selectAll(self):
        pass
    
    def chooseVkTarget(self):        
        self.settings['target'] = self.ui.linkToTargetLineEdit.text()
    def chooseSaveFolder(self):
        folder = str(QtGui.QFileDialog.getExistingDirectory(self.window, 
                                                            "Select Directory"))
        import os
        self.ui.saveToFolderLineEdit.setText(folder + os.path.sep)
        self.settings.update({'save_folder' :folder + os.path.sep})
    def download(self):
        total = len(self.download_list)
        save = self.settings['save_folder']
        self.notificate('Started downloading', 2000)
        self.ui.progressBar.setProperty('value', 0)
        for (i, item) in enumerate(self.download_list):            
            Utils.download_file(item['src'], save, item['pb'])
            self.notificate('Downloaded file %s successfully' % item['src'], 1000 )
            self.ui.progressBar.setProperty('value', int((i+1)*100/float(total)) )
        self.notificate('All files saved in folder %s' % save, 1000 )
        
    def scanForAlbums(self):          
        self.notificate("Started albums scanning ...", 2000)
        self._auth()
        self.ui.picturesTableWidget.clearContent() ### 
        albums = None
        
        if not self.settings.has_key('target'):           
            self.notificate("Target not setted, scanning own directory ...")
            albums = self.vk_wrapper.get_albums()
        else :            
            uid = str(self.settings['target']).rsplit('/',1)[-1].replace('id', '')
            self.show_message("", "uid: " + uid)
            albums = self.vk_wrapper.get_albums(uid)

        table = self.ui.albumsTableWidget
        self.ui.albumsTableWidget.setRowCount(len(albums))

        if len(albums) == 0:
            self.show_message("sorry", "there is no albums")
        
        for (row, album) in enumerate(albums):
            attrs = map(lambda x: QtGui.QTableWidgetItem(x), 
                                       [ _fromUtf8(album['title']), 
                                        str(album['size']), 
                                        Utils.to_human_time(album['created']),
                                        Utils.to_human_time(album['updated']),
                                        album['aid']])                                          
            title = attrs[0]            
            title.setFlags(QtCore.Qt.ItemIsUserCheckable |
                                  QtCore.Qt.ItemIsEnabled)
            title.setCheckState(QtCore.Qt.Unchecked)            
            [table.setItem(row, i, attr) for (i, attr) in enumerate(attrs)]
        table.itemClicked.connect(self.onAblumClick)    
        
        self.window.repaint()        
        self.notificate("Fetched albums successfully", 2000)

    def onAblumClick(self, item):
        albums = self.ui.albumsTableWidget
        pics = self.ui.picturesTableWidget
        if item.checkState() == QtCore.Qt.Checked:
            print('"%s" Checked' % item.text())
            album = item.text()
            self.notificate("Checking album (%s)" % (album), 1000)
            
            aid = albums.item(item.row(), 4).text() # aid column == 4
            uid = str(self.settings['target']).rsplit('/',1)[-1].replace('id', '')
            
            pictures = self.vk_wrapper.get_album(str(aid), str(uid))
            
            def get_src(pic):
                for key in ('src_xxxbig', 'src_xxbig', 'src_xbig', 'src_big', 'src'):
                    if pic.has_key(key):
                        return pic[key]
            
            for pic in pictures:
                pics.setRowCount(pics.rowCount() + 1)
                row = pics.rowCount() - 1
                attrs = map(lambda x: QtGui.QTableWidgetItem(x), 
                                           [get_src(pic), 
                                            _fromUtf8(album), 
                                            Utils.to_human_time(pic['created']),
                                            str(pic['owner_id'])]) 
                src = attrs[0]            
                src.setFlags(QtCore.Qt.ItemIsUserCheckable | 
                                      QtCore.Qt.ItemIsSelectable |
                                      QtCore.Qt.ItemIsEditable |
                                      QtCore.Qt.ItemIsEnabled)
                src.setCheckState(QtCore.Qt.Unchecked) 
                
                [pics.setItem(row, i, attr) for (i, attr) in enumerate(attrs)]

                progressBar = QtGui.QProgressBar()
                progressBar.setProperty("value", 0)
                progressBar.setInvertedAppearance(False)
                pics.setCellWidget(row, len(attrs), progressBar)
            pics.itemClicked.connect(self.onPictureClick)
        else:
            print('"%s" Clicked' % item.text())
            removed_album = str(item.text())
            removed_rows = []
            for row in range(pics.rowCount()):
                if pics.item(row, 1).text() == removed_album:
                    removed_rows.append(row)
            for row in sorted(removed_rows, reverse=True):
                pics.removeRow(row)
            self.window.repaint()

    def onPictureClick(self, item):
        pics = self.ui.picturesTableWidget
        if item.checkState() == QtCore.Qt.Checked:
            pb = pics.cellWidget(item.row(), 4)
            self.download_list.append({'src' : str(item.text()), 'pb' : pb })
        else :
            pb = pics.cellWidget(item.row(), 4)
            for download_obj in self.download_list:
                if download_obj['src'] == str(item.text()):
                    self.download_list.remove(download_obj)
            
    def notificate(self, message, msecs = 200):
        self.ui.statusbar.showMessage(message, msecs)
        self.window.repaint()
    
    def show_message(self, title, message):
        QtGui.QMessageBox.about(self.window, title, message)
        
    def _auth(self):
        if not self.vk_wrapper.is_ready():
            dialog = QtGui.QDialog()
            dialog.ui = LoginDialogUi.Ui_Dialog()
            dialog.ui.setupUi(dialog)
            #dialog.setAttribute(QtCore.Qt.WA_DeleteOnClose)
            exec_status = dialog.exec_()     
            if not exec_status == 0:
                print "exec_status", exec_status
                login = dialog.ui.loginLineEdit.text()
                password = dialog.ui.passwordLineEdit.text()
                self.vk_wrapper.login = str(login)
                self.vk_wrapper.password = str(password)
            else :
                raise Exception("Abort")
        #self.vk_wrapper.login = ""
        #self.vk_wrapper.password = ""

        try :
            self.vk_wrapper.connect()
            self.notificate("Authtenticaton -> Success", 2000)
        except Exception, e:
            print     
            self.show_message("Error", "Cannot authenticate vk, reason: " + str(e))
        


if __name__ == "__main__":
    import sys
    app = QtGui.QApplication(sys.argv)
    ui = VkCrawlerUi.Ui_MainWindow()

    crawler = VkCrawler(ui)
    ui.setupUi(crawler.window)
    crawler.setupEvents()
    
    crawler.window.show()
    sys.exit(app.exec_())
    