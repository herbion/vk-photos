# -*- coding: utf-8 -*-
import datetime

class Utils: 
    @staticmethod
    def to_human_time(unix):
        return datetime.datetime.fromtimestamp(int(unix)) \
                .strftime('%Y-%m-%d %H:%M:%S')