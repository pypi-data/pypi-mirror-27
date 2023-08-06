from nmt_chainer.models.feedforward.encoder_decoder import EncoderDecoder
from chainer import optimizers
import chainer.functions as F
import chainer
import numpy as np

def test1(gpu):
    src_b = [[3,4], [4,4,4],[2,3,5]]
    tgt_b = [[1,1,5,5,6], [1,2,3,4], [2,2]]
    
    encdec = EncoderDecoder(10, 10, 128, 4, nb_layers_tgt = 2, nb_layers_src = 2)
    
    if gpu is not None:
        encdec = encdec.to_gpu(gpu)
        import cupy
        xp = cupy
    else:
        xp = np
    
    with chainer.cuda.get_device(gpu):
        loss = encdec.compute_loss(src_b, tgt_b)
        
        print loss.data
        
        optimizer = optimizers.Adam()
        optimizer.setup(encdec)
        
        def train_once():
            encdec.zerograds()
            loss = encdec.compute_loss(src_b, tgt_b)
            loss.backward()
            optimizer.update()
            print "loss", loss.data
            
            print "greedy:"
            print encdec.greedy_translate(src_b, 10)
            print
            
        for num in xrange(1000):
            print num
            train_once()
        
def test2():
#     src_b = [[3,4], [4,4,4],[2,3,5]]
#     tgt_b = [[1,2,3,4], [1,1,5,5,6], [2,2]]
    
    src_b = [[0, 1],
             [0]]
    tgt_b = [[1, 0],
             [0]]
    
    encdec = EncoderDecoder(2, 2, 4, 1, nb_layers_tgt = 1, nb_layers_src = 1, dropout=None)
    
    logits1 = encdec.compute_logits(src_b, tgt_b, train=False)
    print logits1.data.shape
    print logits1.data
    print
    print
    
    print "seq to seq"
    logits2_splitted = encdec.compute_logits_step_by_step(src_b, tgt_b, train=False)
    logits2= F.concat(tuple(F.reshape(lo, (lo.shape[0], 1, -1) ) for lo in logits2_splitted), axis=1)
    
    print logits2.data.shape
    print logits2.data
    print
    
    print logits1.data.shape, logits2.data.shape
    print np.abs(logits1.data -logits2.data) < 1e-5
#     print
#     print [l.data.shape for l in logits2]
#     print [l.data for l in logits2]
     
def test_multilayer():
#     src_b = [[3,4], [4,4,4],[2,3,5]]
#     tgt_b = [[1,2,3,4], [1,1,5,5,6], [2,2]]
    
    src_b = [[0]]
    tgt_b = [[1]]
    
    encdec = EncoderDecoder(2, 2, 4, 1, nb_layers_tgt = 2, nb_layers_src = 1, dropout=None)
    
    logits1 = encdec.compute_logits(src_b, tgt_b, train=False)
    print logits1.data.shape
    print logits1.data
    print
    print
    
    print "seq to seq"
    logits2_splitted = encdec.compute_logits_step_by_step(src_b, tgt_b, train=False)
    logits2= F.concat(tuple(F.reshape(lo, (lo.shape[0], 1, -1) ) for lo in logits2_splitted), axis=1)
    
    print logits2.data.shape
    print logits2.data
    print
    
    print logits1.data.shape, logits2.data.shape
    print np.abs(logits1.data -logits2.data) < 1e-5
#     print
     
def test3():
    src_b = [[3,4], [4,4,4],[2,3,5]]
    tgt_b = [[1,1,5,5,6], [1,2,3,4], [2,2]]
    
#     src_b = [[0, 1, 0],
#              [0]]
#     tgt_b = [[1, 0, 0],
#              [0]]
    
    encdec = EncoderDecoder(10, 10, 4, 2, nb_layers_tgt = 2, nb_layers_src = 2)
    
    logits1 = encdec.compute_logits(src_b, tgt_b, train=False)
     
    logits2_splitted = encdec.compute_logits_step_by_step(src_b, tgt_b, train=False)
    logits2= F.concat(tuple(F.reshape(lo, (lo.shape[0], 1, -1) ) for lo in logits2_splitted), axis=1)
        
    diff = np.max(np.abs(logits1.data-logits2.data))
    print "diff", diff
    assert diff < 1e-5
    
def test_batching(gpu):
    
    
    
    src_b = [[3,4], [4,4,4],[2,3,5], [4], [5,5,5,5,5,5,5]]
    tgt_b = [[1,1,5,5,6], [1,2,3,4], [2,2], [6,7,8,7,6,8,4], [3]]
    
#     src_b = [[0, 1, 0],
#              [0]]
#     tgt_b = [[1, 0, 0],
#              [0]]
    
    encdec = EncoderDecoder(10, 10, 4, 2, nb_layers_tgt = 2, nb_layers_src = 2)
    
    if gpu is not None:
        encdec = encdec.to_gpu(gpu)
        import cupy
        xp = cupy
    else:
        xp = np
        
    with chainer.cuda.get_device(gpu):
        logits1 = encdec.compute_logits(src_b, tgt_b, train=False)
         
        for num_sub, (src_sub, tgt_sub) in enumerate(zip(src_b, tgt_b)):
            logits2_splitted = encdec.compute_logits_step_by_step([src_sub], [tgt_sub], train=False)
            logits2= F.concat(tuple(F.reshape(lo, (lo.shape[0], 1, -1) ) for lo in logits2_splitted), axis=1)
            
            assert xp.max(xp.abs(logits1.data[num_sub:num_sub+1, :logits2.shape[1], :] - logits2.data)) < 1e-5
        
        
if __name__ == '__main__':
    import argparse
    parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
    parser.add_argument("--gpu", type=int)
    args = parser.parse_args()
#     test1()
    test_batching(args.gpu)
    test1(args.gpu)
    
    