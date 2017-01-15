# -*- coding: utf-8 -*-
__author__ = 'xlliu'


class ErShouChe(object):
    """
    处理过程
    生成返回result, 绘画DF
    """

    def run(self, tel_num, session):
        session.get()
        
        return tel_num