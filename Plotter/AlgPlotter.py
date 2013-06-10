from itertools import product,groupby
from copy import copy

class Plotter(object):
    def __init__(self, **args):
        dic = {}
        for k in args: dic[(self.t,k)] = args[k]
        self.data = [dic]

    def __add__(self, other):
        if other.t != self.t: 
            raise TypeError("You cannot connect (with \"+\") {0} and {1}".format(self.t,other.t))
        ret = copy(self)
        ret.data = self.data + other.data
        return ret

    def __mul__(self, other):
        ret = copy(self) if other.t == self.t else Product(self,other)
        ret.data = [dict(s.items() + o.items()) for s,o in product(self.data,other.data)]
        return ret

class Hist(Plotter):
    def __init__(self,**args):
        self.t = "hist" 
        super(Hist,self).__init__(**args)

class Pad(Plotter):
    def __init__(self,**args):
        self.t = "pad" 
        super(Pad,self).__init__(**args)

class Page(Plotter):
    def __init__(self,**args):
        self.t = "page" 
        super(Page,self).__init__(**args)

class Sec(Plotter):
    def __init__(self,**args):
        self.t = "sec" 
        super(Sec,self).__init__(**args)

class Product(Plotter):
    def __init__(self,p1,p2):
        self.t = tuple(sorted([p1.t,p2.t]))

    def Transpose(self):
        ret = []
        for datum in self.data:
            dic = {}
            for k in datum:
                if k[0] not in dic: dic[k[0]] = {}
                dic[k[0]][k[1]] = datum[k] 
            ret.append(dic)
        return ret

    def Draw(self, pdfname):
        dt = self.Transpose()
        for secset, scgrp in groupby(dt, lambda x: x['sec']):
            print scgrp
            for pagset, pggrp in groupby(scgrp, lambda x: x['page']):
                print pggrp
                for padset, pdgrp in groupby(pggrp, lambda x: x['pad']):
                    print pdgrp
                    for histset, hsgrp in groupby(pdgrp, lambda x: x['hist']):
                        print hsgrp
