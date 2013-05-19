# -*- coding: utf-8 -*-
import VkCrawlerUi, VkWrapper, LoginDialogUi
from PyQt4 import QtGui, QtCore
import types, urllib2
from Utils import Utils
import datetime

_fromUtf8 = QtCore.QString.fromUtf8

class Downloader(QtCore.QThread):
    def __init__(self, urls, save_to):
        QtCore.QThread.__init__(self)
        self.urls = urls
        self.save_folder = save_to
        
    def download_file(self, url, save_folder, progress_bar = None):
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
            percent = str(int(file_size_dl * 100. / file_size))
            self.emit(QtCore.SIGNAL("download_part(QString, QString)"), url, percent)
        
        f.close()

    def run(self):
        total = float(len(self.urls))
        for i, url in enumerate(self.urls):
            self.download_file(url, self.save_folder)
            left = str(int((i+1)*100/total))
            self.emit(QtCore.SIGNAL('download_done(QString, QString)'), url, left)



class VkCrawler():
    def __init__(self, ui):
        self.window = QtGui.QMainWindow()
        self.ui = ui
        self.settings = {}
        self.vk_wrapper = VkWrapper.VkWrapper()
        self.download_list = []
                

    def setupEvents(self):
        self.window.connect(self.ui.downloadButton, 
                            QtCore.SIGNAL("clicked()"), 
                            self.download)
        self.window.connect(self.ui.chooseSaveFolderButton, 
                            QtCore.SIGNAL("clicked()"), 
                            self.select_save_folder)
        self.window.connect(self.ui.linkToTargetLineEdit, 
                            QtCore.SIGNAL("textChanged(QString)"),
                            self.select_vk_target)
        self.window.connect(self.ui.scanButton,
                            QtCore.SIGNAL("clicked()"),
                            self.scanForAlbums)
        self.window.connect(self.ui.selectAllButton,
                            QtCore.SIGNAL("clicked()"),
                            self.selectAll)
        self.ui.picturesTableWidget.itemClicked.connect(self.onPictureClick)
        
    def selectAll(self):
        pass
    
    def select_vk_target(self):        
        self.settings['target'] = self.ui.linkToTargetLineEdit.text()
    
    def select_save_folder(self):
        folder = str(QtGui.QFileDialog.getExistingDirectory(self.window, 
                                                            "Select Directory"))
        import os
        self.ui.saveToFolderLineEdit.setText(folder + os.path.sep)
        self.settings.update({'save_folder' :folder + os.path.sep})
    
    def download(self):
        save = self.settings['save_folder']
        self.notificate('Started downloading', 2000)
        self.ui.progressBar.setProperty('value', 0)
        
        if len(self.download_list) == 0:
            self.show_message("Warning", "Please choose some urls first")
            return
        
        self.downloader = Downloader(map(lambda item: item['src'], 
                                         self.download_list), save)
        
        _items = dict(map(lambda item: (item['src'], item['pb']), 
                          self.download_list))        
    
        def on_downloaded_file(fname, processed_percent):
            _items[str(fname)].setProperty('value', 100)
            self.ui.progressBar.setProperty('value', processed_percent)
            if processed_percent == "100":
                self.notificate("[Done] All files are downloaded ..", 2000)
        def on_downloaded_part(fname, percent):
            _items[str(fname)].setProperty('value', int(percent))
        
        QtCore.QObject.connect(self.downloader, 
                               QtCore.SIGNAL('download_done(QString, QString)'), 
                               on_downloaded_file, 
                               QtCore.Qt.QueuedConnection)
                             
        QtCore.QObject.connect(self.downloader, 
                               QtCore.SIGNAL("download_part(QString, QString)"), 
                               on_downloaded_part, 
                               QtCore.Qt.QueuedConnection)
        self.downloader.start()       
        
    def scanForAlbums(self):          
        self.notificate("Started albums scanning ...", 2000)
        self._auth()
        #self.ui.picturesTableWidget.clearContent() ### 
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
            
        else:
            print('"%s" Clicked' % item.text())
            removed_album = str(item.text())
            removed_rows = []
            for row in range(pics.rowCount()):
                if str(pics.item(row, 1).text()) == removed_album:
                    removed_rows.append(row)
            for row in sorted(removed_rows, reverse=True):
                pics.removeRow(row)
            is_removed_album = lambda x: str(x['album']) != removed_album
            self.download_list = filter(is_removed_album, self.download_list)
            self.window.repaint()

    def onPictureClick(self, item):
        pics = self.ui.picturesTableWidget
        if item.checkState() == QtCore.Qt.Checked:
            print "adding to donwload list", item.text()
            pb = pics.cellWidget(item.row(), 4)
            album = pics.item(item.row(), 1).text()
            self.download_list.append({'src' : str(item.text()), 
                                       'pb' : pb,
                                       'album' : str(album)})
        else :
            pb = pics.cellWidget(item.row(), 4)
            print len(self.download_list)
            for download_obj in self.download_list:
                if download_obj['src'] == str(item.text()):
                    print "removing from list "
                    self.download_list.remove(download_obj)
            print len(self.download_list)
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
        self.vk_wrapper.login = ""
        self.vk_wrapper.password = ""

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
    
