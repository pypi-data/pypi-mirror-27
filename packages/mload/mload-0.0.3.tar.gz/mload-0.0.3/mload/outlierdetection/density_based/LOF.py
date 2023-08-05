#!/usr/bin/env python
#coding:utf-8
"""
  Author   : Chaos -- < chaosimpler@gmail.com >
  Purpose  : 
  Created  : 12/09/17
"""

import numpy as np
import pandas as pd

#----------------------------------------------------------------------
def LOF():
    """this function used to calculate lof scores."""
    from ...cluster import DBSCAN
    print 'this is LOF'
    print DBSCAN.getSomeValue()

#----------------------------------------------------------------------
def testLOF():
    """
    Purpose :
        this func is used to test LOF().
    """
    print 'This is test in LOF'
    LOF()
    
