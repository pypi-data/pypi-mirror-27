from nmt_chainer.additional_links.layer_normalization import LayerNormalizationLink, LayerNormalization, LayerNormalizationOther
import numpy as np
from chainer.gradient_check import check_backward
import chainer.links as L
import chainer
from __builtin__ import int

nptype = "float64"

def test1(xp, ntype):
    dtype = getattr(xp, ntype)
    a = xp.random.randn(3,7).astype(dtype)
    gamma = xp.random.randn(1,7).astype(dtype)
    beta = xp.random.randn(1,7).astype(dtype)
    gy = xp.random.randn(3,7).astype(dtype)
    ln = LayerNormalization()
    check_backward(ln, (a,gamma, beta), (gy,))
        
        
def test2(xp, ntype):
    dtype = getattr(xp, ntype)
    
    cln = L.LayerNormalization()
    if xp is not np:
        cln = cln.to_gpu()
    a = xp.random.randn(3,2).astype(dtype)
    
    
    d1 = cln(a)
    
    print "a"
    print a
    print
    print "g"
    print cln.gamma.data
    print "b"
    print cln.beta.data
    print
    d2 = LayerNormalization()(a, cln.gamma.data[None,:], cln.beta.data[None,:])
    
    print d1.data
    print
    print d2.data

import time

def measure_speed(a, gy, cln_list, name=""):
    t0 = time.clock()
    res = []
    start = []
    for repeat in range(20):
        a0 = chainer.Variable(a)
        start.append(a0)
        a_next = a0
        for cln in cln_list:
            a_next = cln(a_next)
        res.append(a_next)
    print res[-1].data
    t1 = time.clock()
    for a_final in res:
        a_final.grad = gy
        a_final.backward()
    
    print res[-1].grad
    t2 = time.clock()
    print "time %s tot:%f fwd:%f bwd:%f"%(name, t2 - t0, t1 - t0, t2 - t1)
    
def test3(xp, ntype):
    dtype = getattr(xp, ntype)
    
    print "***************************************"
    print xp
    print ntype
    print
    
    cln_list = [L.LayerNormalization() for _ in range(20)]
    
    if xp is not np:
        cln_list = [cln.to_gpu() for cln in cln_list]
        
        
    a = xp.random.randn(256, 512).astype(dtype)
    gy = xp.random.randn(256, 512).astype(dtype)
    
    
    measure_speed(a, gy, cln_list, name="old")
    
    measure_speed(a, gy, 
                  [lambda a_next:LayerNormalization(gpu_optim=False)(a_next, cln.gamma.data[None,:], cln.beta.data[None,:]) 
                   for cln in cln_list], name="ong")
    
    measure_speed(a, gy, 
                  [lambda a_next:LayerNormalization()(a_next, cln.gamma.data[None,:], cln.beta.data[None,:]) 
                   for cln in cln_list], name="own")
    
    measure_speed(a, gy, 
                  [lambda a_next:LayerNormalizationOther()(a_next, cln.gamma.data, cln.beta.data) 
                   for cln in cln_list], name="new")
    
    print
    print
    print
    
    measure_speed(a, gy, cln_list, name="old")
    
    measure_speed(a, gy, 
                  [lambda a_next:LayerNormalization(gpu_optim=False)(a_next, cln.gamma.data[None,:], cln.beta.data[None,:]) 
                   for cln in cln_list], name="ong")
    
    measure_speed(a, gy, 
                  [lambda a_next:LayerNormalization()(a_next, cln.gamma.data[None,:], cln.beta.data[None,:]) 
                   for cln in cln_list], name="own")
    
    measure_speed(a, gy, 
                  [lambda a_next:LayerNormalizationOther()(a_next, cln.gamma.data, cln.beta.data) 
                   for cln in cln_list], name="new")
        
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--gpu", type=int, default=0)
    args = parser.parse_args()
    test1(np, "float64")
    test2(np, "float32")
    test3(np, "float32")
    try:
        import cupy as cp
        cp.cuda.Device(args.gpu).use()
        test1(cp, "float64")
        test2(cp, "float32")
        test3(cp, "float32")
    except ImportError:
        print "no cupy"
    