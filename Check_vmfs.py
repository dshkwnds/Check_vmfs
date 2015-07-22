#!/usr/bin/python
#  -*- coding:UTF-8 -*-
author__ = 'ethan_huang'
from pysphere import VIServer
import sys


class CheckVCenter():
    def __init__(self):
        self.server = VIServer()
        self.STAT_OK=0
        self.STAT_WARNING=1
        self.STAT_CRITICAL=2
        self.vc = sys.argv[1]
        self.user = sys.argv[2]
        self.password = sys.argv[3]


    @staticmethod
    def PrintDict(i,status):
        for k,v in i.items():
            print "VMFS %s lun:%s -----*----*---- usage:%d%%" %(status,k,v)

    def Check(self):
        self.server.connect(self.vc,self.user,self.password)
        Value = self.server.get_datastores()
        c = {}
        w = {}
        n = {}
        for k,v in Value.items():
            props = self.server._retrieve_properties_traversal(property_names=['name','summary.capacity',
                                                                               'summary.freeSpace'],
                                                          from_node=k,obj_type='Datastore')
            for p_set in props:
                for p1 in p_set.PropSet:
                    if p1.Name == "summary.capacity":
                        DatastoreCapacity = (p1.Val/1073741824)
                    elif p1.Name == "summary.freeSpace":
                        DatastoreFreespace = (p1.Val/1073741824)

            Percent = (((DatastoreCapacity - DatastoreFreespace) * 100)/DatastoreCapacity)
            if  Percent > 90 and 'ISO' not in v:
                c[v] = Percent
            elif Percent > 85  < 90 and 'ISO' not in v:
                w[v] = Percent
            elif Percent < 85 and 'ISO' not in v:
                n[v] = Percent
        if dict(c):
            CheckVCenter.PrintDict(c,'CRITICAL')
            sys.exit(self.STAT_CRITICAL)
        elif dict(w):
            CheckVCenter.PrintDict(w,'WARNING')
            sys.exit(self.STAT_WARNING)
        else:
            print("All Lun is OK")
            sys.exit(self.STAT_OK)



if __name__ == '__main__':
    VC = CheckVCenter()
    VC.Check()
