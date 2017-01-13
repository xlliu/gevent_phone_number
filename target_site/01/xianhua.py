# -*- coding: utf-8 -*-
__author__ = 'xlliu'


class XianHua(object):
    """
    处理过程
    生成结果文件 ==>> xianhua.xlsx
    """

    def run(self, tel_num, session):
        session.get()
        
        return tel_num