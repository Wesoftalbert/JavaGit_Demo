#!/usr/bin/env python
#-*- coding: utf -*-


import copy

seq = [1, 2, 3] 
seq_1 = seq
seq_2 = copy.copy(seq)
seq_3 = copy.deepcopy(seq)
seq.append(4) 

print seq_2 
print seq
print seq_3