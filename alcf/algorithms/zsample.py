import numpy as np
from alcf import misc
from alcf.algorithms import interp

def zsample(d, zres=None, zlim=None):
	b = d['backscatter']
	if len(b.shape) == 3:
		n, m, l = b.shape
		dims = (n, m, l)
	else:
		n, m = b.shape
		l = 0
		dims = (n, m)
	b_sd = d['backscatter_sd'] if 'backscatter_sd' in d \
		else np.zeros(dims, dtype=np.float64)
	zfull = d['zfull']
	zhalf = np.zeros((n, m+1), dtype=np.float64)
	for i in range(n):
		zhalf[i,1:-1] = 0.5*(d['zfull'][i,1:] + d['zfull'][i,:-1])
		zhalf[i,0] = 2*d['zfull'][i,0] - d['zfull'][i,1]
		zhalf[i,-1] = 2.*d['zfull'][i,-1] - d['zfull'][i,-2]
	r = d['range'] if 'range' in d \
		else np.zeros(m, dtype=np.float64)
	if m == 0:
		return
	zhalf2 = np.arange(zlim[0], zlim[-1] + zres, zres)
	zfull2 = (zhalf2[1:] + zhalf2[:-1])*0.5
	m2 = len(zfull2)
	dims2 = (n, m2, l) if len(b.shape) == 3 else (n, m2)
	b2 = np.zeros(dims2, dtype=np.float64)
	b_sd2 = np.zeros(dims2, dtype=np.float64)
	# r2 = np.zeros(m2, dtype=np.float64)
	if l == 0:
		for i in range(n):
			b2[i,:] = interp(zhalf[i,:], b[i,:], zhalf2)
			b_sd2[i,:] = interp(zhalf[i,:], b_sd[i,:], zhalf2)
	else:
		for i in range(n):
			for j in range(l):
				b2[i,:,j] = interp(zhalf[i,:], b[i,:,j], zhalf2)
				b_sd2[i,:,j] = interp(zhalf[i,:], b_sd[i,:,j], zhalf2)
	# d['range'] = r2
	d['zfull'] = zfull2
	d['backscatter'] = b2
	if 'backscatter_sd' in d:
		d['backscatter_sd'] = b_sd2
	d['.']['zfull']['.dims'] = ['level']

def stream(dd, state, zres=None, zlim=None, **options):
	return misc.stream(dd, state, zsample, zres=zres, zlim=zlim)