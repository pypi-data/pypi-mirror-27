import chainer
import numpy as np
import chainer.functions as F
import chainer.links as L
from chainer import Variable, Chain, ChainList

from nmt_chainer.models.feedforward.multi_attention import ConstantSizeMultiBatchMultiHeadAttention
from nmt_chainer.models.feedforward.utils import make_batch_mask


def naive_scaled_attention(Q, K, V):
    assert len(Q.shape) == 2
    assert len(K.shape) == 2
    assert len(V.shape) == 2
    
    scaling = np.sqrt(K.data.shape[1])
    scaled = F.matmul(Q, K, transb=True) / scaling
    
    assert len(scaled.shape) == 2
    weights = F.softmax(scaled)
    
    result = F.matmul(weights, V)
    return result


class NaiveMultiAttention(ConstantSizeMultiBatchMultiHeadAttention):
    def __init__(self, d_model = 512, n_heads = 8):
        
        super(NaiveMultiAttention, self).__init__(d_model=d_model, n_heads=n_heads)
#             w_Q = L.Linear(d_model, d_model, nobias=False),
#             w_K = L.Linear(d_model, d_model, nobias=True),
#             w_V = L.Linear(d_model, d_model, nobias=False),
#             )
        
#         self.size_head = d_model / n_heads
#         self.d_model = d_model
#         self.n_heads = n_heads
#         assert self.size_head * self.n_heads == self.d_model
        
    def apply_to_one_batch(self, Q, K, V):
        assert len(Q.shape) == 2
        assert len(K.shape) == 2
        assert len(V.shape) == 2
        pQ = self.w_Q(Q)
        pK = self.w_K(K)
        pV = self.w_V(V)
        
        splitted_pQ = F.split_axis(pQ, self.n_heads, axis = 1, force_tuple=True)
        splitted_pK = F.split_axis(pK, self.n_heads, axis = 1, force_tuple=True)
        splitted_pV = F.split_axis(pV, self.n_heads, axis = 1, force_tuple=True)
        
        assert len(splitted_pQ) == len(splitted_pK) == len(splitted_pV) == self.n_heads
        assert splitted_pQ[0].shape[1] == splitted_pK[0].shape[1] == splitted_pV[0].shape[1] == self.head_size
        res_attn = []
        for (hQ, hK, hV) in zip(splitted_pQ, splitted_pK, splitted_pV):
            res_attn.append(naive_scaled_attention(hQ, hK, hV))
        
        return F.concat(res_attn, axis=1)
    
def test_single_request_single_batch():
    d_model = 64
    n_heads = 4
    nK = 5
    
    Q = np.random.randn(1, d_model).astype(np.float32)
    K = np.random.randn(nK, d_model).astype(np.float32)
    V = np.random.randn(nK, d_model).astype(np.float32)
    
    nma = NaiveMultiAttention(d_model, n_heads)
    res1 = nma.apply_to_one_batch(Q, K, V)
    res2 = nma(Variable(Q[None,:,:]), Variable(K[None,:,:]), Variable(V[None,:,:]))
    diff = np.max(np.abs(res1.data[None,:,:] - res2.data))
    print res1.data
    print res2.data
    print "diff", diff
    assert diff < 1e-5
    
def test_multi_request_single_batch():
    d_model = 64
    n_heads = 4
    nK = 5
    
    Q = np.random.randn(3, d_model).astype(np.float32)
    K = np.random.randn(nK, d_model).astype(np.float32)
    V = np.random.randn(nK, d_model).astype(np.float32)
    
    nma = NaiveMultiAttention(d_model, n_heads)
    res1 = nma.apply_to_one_batch(Q, K, V)
    res2 = nma(Variable(Q[None,:,:]), Variable(K[None,:,:]), Variable(V[None,:,:]))
    diff = np.max(np.abs(res1.data[None,:,:] - res2.data))
    print res1.data
    print res2.data
    print "diff", diff
    assert diff < 1e-5
    
def test_multi_request_multi_batch():
    d_model = 64
    n_heads = 4
    nK = 5
    
    Q_list = [np.random.randn(3, d_model).astype(np.float32) for _ in xrange(7)]
    K_list = [np.random.randn(nK, d_model).astype(np.float32) for _ in xrange(7)]
    V_list = [np.random.randn(nK, d_model).astype(np.float32) for _ in xrange(7)]
    
    nma = NaiveMultiAttention(d_model, n_heads)
    
    res_list_1 = []
    for (Q, K, V) in zip(Q_list, K_list, V_list):
        res_list_1.append(nma.apply_to_one_batch(Q, K, V))
    res1 = F.concat([R[None,:,:] for R in res_list_1], axis=0)
    
    batchQ = F.concat([Q[None,:,:] for Q in Q_list], axis=0)
    batchK = F.concat([K[None,:,:] for K in K_list], axis=0)
    batchV = F.concat([V[None,:,:] for V in V_list], axis=0)
    
    res2 = nma(batchQ,batchK, batchV)
    diff = np.max(np.abs(res1.data - res2.data))
    print res1.data
    print res2.data
    print "diff", diff
    assert diff < 1e-5
    
def pad_1st_dim(M, max_length):
    assert len(M.shape) == 2
    assert M.shape[0] <= max_length
    if M.shape[0] == max_length:
        return M
    needed = max_length - M.shape[0]
    return np.concatenate((M, np.zeros((needed, M.shape[1]), dtype=np.float32)))
    
def test_batch_masking():
    d_model = 64
    n_heads = 4
    
    Q_list = [np.random.randn(3, d_model).astype(np.float32) for _ in xrange(7)]
    K_list = [np.random.randn((3*nK)%5 + 1, d_model).astype(np.float32) for nK in xrange(1, 8)]
    V_list = [np.random.randn((3*nK)%5 + 1, d_model).astype(np.float32) for nK in xrange(1, 8)]
    
    nma = NaiveMultiAttention(d_model, n_heads)
    
    res_list_1 = []
    for (Q, K, V) in zip(Q_list, K_list, V_list):
        res_list_1.append(nma.apply_to_one_batch(Q, K, V))
    res1 = F.concat([R[None,:,:] for R in res_list_1], axis=0)
    
    max_length_2 = max(K.shape[0] for K in K_list)
    batchQ = F.concat([Q[None,:,:] for Q in Q_list], axis=0)
    batchK = F.concat([pad_1st_dim(K, max_length_2)[None,:,:] for K in K_list], axis=0)
    batchV = F.concat([pad_1st_dim(V, max_length_2)[None,:,:] for V in V_list], axis=0)
    
    mask = make_batch_mask(mb_size=7, n_head=n_heads, max_length_1=3, max_length_2=max_length_2, 
                    key_seq_lengths = [(3*nK)%5 + 1 for nK in xrange(1,8)])
    
    res2 = nma(batchQ,batchK, batchV, batch_mask = mask)
    diff = np.max(np.abs(res1.data - res2.data))
    print res1.data
    print res2.data
    print "diff", diff
    assert diff < 1e-5    
    
    
def test_batch_masking2():
    d_model = 64
    n_heads = 4
    
    Q_list = [np.random.randn((5*nQ)%7+1, d_model).astype(np.float32) for nQ in xrange(7)]
    K_list = [np.random.randn((3*nK)%5 + 1, d_model).astype(np.float32) for nK in xrange(1, 8)]
    V_list = [np.random.randn((3*nK)%5 + 1, d_model).astype(np.float32) for nK in xrange(1, 8)]
    
    max_length_1 = max(Q.shape[0] for Q in Q_list)
    max_length_2 = max(K.shape[0] for K in K_list)
    
    nma = NaiveMultiAttention(d_model, n_heads)
    
    res_list_1 = []
    for (Q, K, V) in zip(Q_list, K_list, V_list):
        res_list_1.append(nma.apply_to_one_batch(Q, K, V))
    res1 = np.concatenate([pad_1st_dim(R.data, max_length_1)[None,:,:] for R in res_list_1], axis=0)
    
    batchQ = F.concat([pad_1st_dim(Q, max_length_1)[None,:,:] for Q in Q_list], axis=0)
    batchK = F.concat([pad_1st_dim(K, max_length_2)[None,:,:] for K in K_list], axis=0)
    batchV = F.concat([pad_1st_dim(V, max_length_2)[None,:,:] for V in V_list], axis=0)
    
    mask = make_batch_mask(mb_size=7, n_head=n_heads, max_length_1=max_length_1, max_length_2=max_length_2, 
                    key_seq_lengths = [(3*nK)%5 + 1 for nK in xrange(1,8)])
    
    res2 = nma(batchQ,batchK, batchV, batch_mask = mask)
    
    for nQ in xrange(7):
        res2.data[nQ, (5*nQ)%7+1:, :] = 0
    diff = np.max(np.abs(res1 - res2.data))
    print res1
    print res2.data
    print "diff", diff
    assert diff < 1e-5    
    
if __name__ == '__main__':
#     test_multi_request_single_batch()
#     test_multi_request_multi_batch()
    test_batch_masking2()
        
        