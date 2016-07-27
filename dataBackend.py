# my databackend for huge list of 2D IP addresses

from bisect import bisect_left
from utils import *

def sliceList(u,s):
	# This function finds a slice
	# of sorted list u between s[0] and s[1]
    i1 = bisect_left(u,s[0])
    i2 = bisect_left(u,s[1])
    return u[i1:i2]

class mySparse:
	# D is a n*3 array, list os lists or tuples
    def __init__(self, D):
		# sort based on destinations
        self.l = len(D)
        quell = set([xx[0] for xx in D])
        self.srcs = sorted(list(quell)) # sorted list of sources
        self.n_srcs = len(self.srcs)
        # self.d_srcs = dict(zip(self.srcs, range(self.n_srcs))) # dictionary of srcs
        ziel = set([xx[1] for xx in D])
        dsts =sorted(list(ziel)) # sorted list of sdestinations
        self.n_dsts = len(dsts)
        #self.d_dsts = dict(zip(dsts, range(self.n_dsts))) # dictionary of srcs
        m = self.srcs[-1] - self.srcs[0] + 1
        n = dsts[-1] - dsts[0] + 1
        self.shape = (m,n)
        self.DD = {}
        self.imp = {}
        
        # making a backend dictionary
        for d in D:
            try:
                self.imp[d[0]] = self.imp[d[0]] + [d[1]]
            except KeyError:
                self.imp[d[0]] = [d[1]]
            self.DD[(d[0],d[1])] = d[2]

    # Slice query             
    def __getitem__(self,key):
        v = []
        if isinstance(key[0],slice):
            loop1 = (key[0].start,key[0].stop)
        else:
            loop1 = (key[0],key[0])
        if isinstance(key[1],slice):
            loop2 = (key[1].start,key[1].stop)
        else:
            loop2 = (key[1],key[1])
        out = []
        dim1 = sliceList(self.srcs,loop1)
        for src in dim1:
			cans = self.imp[src]
			dim2 = sliceList(cans,loop2)
			for dst in dim2:
				v.append(self.DD[(src,dst)])
        return v
        
    def query(self,rec):
		# centroid
		# vcentroid
		# volume
		# density
		# number of points
        vol = 0
        loop1 = (rec.src1, rec.src2+1)
        loop2 = (rec.dst1, rec.dst2+1)
        cen_src = (loop1[0] + loop1[1] - 1.0)/2.0
        cen_dst = (loop2[0] + loop2[1] - 1.0)/2.0
        dim1 = sliceList(self.srcs,loop1)
        np = 0
        out = {}
        
        for src in dim1:
			cans = self.imp[src]
			dim2 = sliceList(cans,loop2)
			for dst in dim2:
				val = self.DD[(src,dst)]
				np = np + 1
				vol = vol + val
				if np == 1:
					pcen_src = src
					pcen_dst = dst
					vcen_src = src
					vcen_dst = dst
				else:
				    pcen_src = (float(np-1)/np)*pcen_src + float(src)/np
				    pcen_dst = (float(np-1)/np)*pcen_dst + float(dst)/np
				    vcen_src = ((vol-val)/vol)*vcen_src + (val/vol)*src
				    vcen_dst = ((vol-val)/vol)*vcen_dst + (val/vol)*dst
        if np == 0:
			return None
        rec.vol = vol
        rec.center = (cen_src,cen_dst)
        rec.vcentroid = (vcen_src,vcen_dst)
        rec.pcentroid = (pcen_src,pcen_dst)
        rec.np = np
        return rec
      
    def __len__(self):
		return self.l

#~ if __name__ == '__main__':
	#~ D = [(10,1,5.0),(7,2,7.0),(10,8,1.0),(11,7,2.0),(13,7,3.0)]
	
	#~ I = mySparse(D)
	#~ R = REC(7,11,2,8)
	#~ print I.query(R)
	#~ print R.pcentroid
	#~ s = [3,2,5,6,4,2,8,3,9]
	#~ s = sorted(s)
	#~ print sliceList(s,(3,8))
	#REC(3219784754>174491921,3219784754>174491921|43.574256/1)
	#REC(3219784754>174024061,3219784754>174024061|40.292848/1)
	#~ r1 = REC(3219784754,174491921,43.1)
	#~ r2 = REC(3219784754,174024061,6.5)
	#~ D = [(3219784754,174024061,6.5),(3219784754,174491921,43.1)]
	#~ D1 = mySparse(D)
	#~ r = r1 + r2
	#~ print r
	#~ print D1.query(r)
