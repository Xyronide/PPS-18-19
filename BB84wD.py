"""BB84 with Decoherence"""
from __future__ import division
import numpy
import random
import matplotlib.pyplot as pyplot

def Alice(baseA):
    bitA = numpy.random.randint(2)
    A = bitA * 90 + baseA * 45
    return (bitA, A)

def Bob(A, baseB):
    if numpy.random.rand() >= abs(numpy.sin( numpy.radians( A- 45 * baseB )) )** 2:
        bitB = 0
    else:
        bitB = 1
    return bitB

def decho(A, scale):
    D = A + ( ( numpy.random.rand() * 2 ) - 1 ) * scale
    return D

def BB84(keyLength):
    key = numpy.zeros(1)
    workingKey = numpy.zeros(1)
    while len(key) <= (keyLength):
        baseA = numpy.random.randint(2)
        baseB = numpy.random.randint(2)
        if baseB != baseA:
            continue
        A = Alice(baseA)
        D = decho(A[1], 45)
        B = Bob(D, baseB)
        workingKey =  numpy.append( workingKey, [ A[0] ])
        if numpy.random.rand() >= 0.5:
            print "tested"
            if A[0] != B:
                print "Eavesdropper Detected"
                return None
            else:
                continue
        else:
            print "untested"
            key = numpy.append( key, [ A[0] ] )
    print workingKey[1:]
    return key[1:]

print BB84(5)
#Benjamin Collins
