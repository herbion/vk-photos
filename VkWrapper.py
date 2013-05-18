# -*- coding: utf-8 -*-
import vk_api

class VkWrapper():
    def __init__(self, login=None, password=None):
        self.login = login
        self.pasword = password
        self.vk = None
    def connect(self):
        if not self.login or not self.password:
            raise Exception("login or password is not setted")
        else:
            self.vk = vk_api.VkApi(self.login, self.password)  
    def is_ready(self):
        return not self.login == None and self
    def get_albums(self):
        albums = self.vk.method('photos.getAlbums', {})
        return albums
    def get_album(self, aid):
        return self.vk.method('photos.get', {"aid": aid})
if __name__ == "__main__" :
    test = VkWrapper()
    test.login = "im"
    test.pasword = "s"
    test.connect()