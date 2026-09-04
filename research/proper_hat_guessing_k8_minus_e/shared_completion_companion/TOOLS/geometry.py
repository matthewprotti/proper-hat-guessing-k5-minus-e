"""K8 incidence construction for the diagonal-safe synthesis experiment.
Builder uses homogeneous determinant normalizers. Certificates are checked by
a separate program enumerating invertible projective matrices.
"""
import itertools
from functools import lru_cache
import numpy as np
from scipy.sparse import csr_matrix
from scipy.sparse.csgraph import maximum_bipartite_matching

P=13; Q=14; INF=13; BASE=(13,0,1); K=6
TAILS=tuple(itertools.permutations(range(2,13),3))

def chart(triple):
    def hom(z): return (1,0) if z==INF else (z,1)
    def det(u,v):return (u[0]*v[1]-u[1]*v[0])%P
    A,B,C=map(hom,triple)
    out=[]
    for z in range(Q):
        X=hom(z);num=det(X,B)*det(C,A)%P;den=det(X,A)*det(C,B)%P
        out.append(INF if not den else num*pow(den,-1,P)%P)
    assert tuple(out[x] for x in triple)==BASE and len(set(out))==Q
    return tuple(out)

def rid_code(j,u,v,x,y):
    return ((((j*Q+u)*Q+v)*Q+x)*Q+y)

class Geometry:
    def __init__(self):
        self.tails=TAILS
        self.charts={triple:chart(triple) for triple in itertools.permutations(range(Q),3)}
        assert len(set(self.charts.values()))==2184
        rkeys=[]
        for j in range(K):
            for u,v in itertools.permutations(range(2,13),2):
                av=[x for x in range(Q) if x not in BASE+(u,v)]
                for x,y in itertools.product(av,repeat=2):rkeys.append((j,u,v,x,y))
        self.right=np.array(rkeys,dtype=np.int16)
        codes=np.array([rid_code(*r) for r in rkeys])
        self.lookup=np.full(6*Q**4,-1,dtype=np.int32)
        self.lookup[codes]=np.arange(len(codes),dtype=np.int32)
        self.available=np.array([[x for x in range(Q) if x not in BASE+t] for t in TAILS],dtype=np.int16)
        edges=np.empty((990,8,8,6),dtype=np.int32)
        self.target=np.empty((990,6),dtype=np.int16)
        for tid,t in enumerate(TAILS):
            C=BASE+t;av=self.available[tid]
            for j in range(K):
                vis=C[:j]+C[j+1:];h=self.charts[vis[:3]]
                self.target[tid,j]=h[C[j]]
                for xi,x in enumerate(av):
                    for yi,y in enumerate(av):
                        edges[tid,xi,yi,j]=self.lookup[rid_code(j,h[vis[3]],h[vis[4]],h[x],h[y])]
        assert np.all(edges>=0)
        self.edges=edges
        self.eq_right=np.flatnonzero(self.right[:,3]==self.right[:,4])
        self.off_right=np.flatnonzero(self.right[:,3]!=self.right[:,4])
        self.eq_rmap=np.full(len(rkeys),-1,dtype=np.int32);self.eq_rmap[self.eq_right]=np.arange(5940)
        self.off_rmap=np.full(len(rkeys),-1,dtype=np.int32);self.off_rmap[self.off_right]=np.arange(47520)
        self.eq_edges=self.eq_rmap[self.edges[:,np.arange(8),np.arange(8),:].reshape(-1,6)]
        assert self.eq_edges.shape==(7920,6)
        assert set(np.bincount(self.eq_edges.ravel()))=={8}
        self.leftids=np.arange(990*64).reshape(990,8,8)
        self.eq_ids=self.leftids[:,np.arange(8),np.arange(8)].ravel()
        self.off_mask=np.broadcast_to(~np.eye(8,dtype=bool),(990,8,8))
        assert len(rkeys)==53460 and len(self.eq_right)==5940 and len(self.off_right)==47520

    def retained_mask(self,rules):
        assert rules.shape==(990,2)
        legal=(self.available[:,:,None]==rules[:,None,:]).sum(axis=1)
        assert (legal==1).all() and (rules[:,0]!=rules[:,1]).all()
        return (self.available[:,:,None]!=rules[:,0,None,None]) & (self.available[:,None,:]!=rules[:,1,None,None])

    def residual(self,rules,sector):
        keep=self.retained_mask(rules)
        if sector=='equal':
            mask=np.zeros((990,8,8),dtype=bool)
            mask[:,np.arange(8),np.arange(8)]=True
            keep &= mask
            rightmap=self.eq_rmap;nr=5940
        elif sector=='distinct':
            keep &= self.off_mask
            rightmap=self.off_rmap;nr=47520
        else:
            rightmap=np.arange(53460);nr=53460
        ids=self.leftids[keep]
        adj=rightmap[self.edges[keep]]
        assert (adj>=0).all()
        return ids,adj,nr

def match(adj,nr):
    a=csr_matrix((np.ones(adj.size,dtype=np.int8),
        (np.repeat(np.arange(len(adj)),adj.shape[1]),adj.ravel())),shape=(len(adj),nr))
    m=maximum_bipartite_matching(a,perm_type='column')
    used=m[m>=0]
    assert len(set(map(int,used)))==len(used)
    assert np.all(np.any(adj[m>=0]==used[:,None],axis=1))
    return m

class SplitMix64:
    def __init__(self,seed):self.state=seed & ((1<<64)-1)
    def next(self):
        mask=(1<<64)-1
        self.state=(self.state+0x9e3779b97f4a7c15)&mask
        z=self.state;z=((z^(z>>30))*0xbf58476d1ce4e5b9)&mask
        z=((z^(z>>27))*0x94d049bb133111eb)&mask
        return z^(z>>31)
    def randbelow(self,n):
        limit=(1<<64)-((1<<64)%n)
        while True:
            x=self.next()
            if x<limit:return x%n
    def shuffle(self,seq):
        for i in range(len(seq)-1,0,-1):
            j=self.randbelow(i+1);seq[i],seq[j]=seq[j],seq[i]

def orient(pairs,seed):
    out=np.sort(pairs,axis=1).copy()
    if seed is not None:
        g=SplitMix64(seed)
        for i in range(len(out)):
            if g.next()&1:out[i]=out[i,::-1]
    return out
