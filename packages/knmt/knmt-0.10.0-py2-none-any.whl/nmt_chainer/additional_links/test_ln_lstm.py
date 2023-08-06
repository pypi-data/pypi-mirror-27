from nmt_chainer.additional_links.ln_lstm import LSTMWithUngatedOutput
import numpy as np
from chainer.gradient_check import check_backward
import chainer.links as L
import chainer
from __builtin__ import int

nptype = "float64"

def test1(xp, ntype):
    dtype = getattr(xp, ntype)
    c_prev = xp.random.randn(3,7).astype(dtype)
    x = xp.random.randn(3,7*4).astype(dtype)
    gh = xp.random.randn(3,7).astype(dtype)
    gc = xp.random.randn(3,7).astype(dtype)
    go_gate = xp.random.randn(3,7).astype(dtype)
    ln = LSTMWithUngatedOutput()
    check_backward(ln, (c_prev, x), (gh,gc, go_gate))
    
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--gpu", type=int, default=0)
    args = parser.parse_args()
    test1(np, "float32")
    try:
        import cupy as cp
        cp.cuda.Device(args.gpu).use()
        test1(cp, "float32")
    except ImportError:
        print "no cupy"