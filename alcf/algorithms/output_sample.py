import copy
import numpy as np
from alcf import misc
import ds_format as ds

def output_sample(d, tres, output_sampling):
	t1 = d['time'][0] - ((d['time'][0] + 0.5) % 1.0)
	t2 = t1 + output_sampling
	dims = ds.get_dims(d)
	n = dims['time']
	n2 = int(output_sampling/tres)
	time = d['time']
	time_half = np.zeros(n + 1, dtype=np.float64)
	time_half[1:-1] = 0.5*(time[1:] + time[:-1])
	time_half[0] = time[0] - 0.5*(time[1] - time[0])
	time_half[-1] = time[-1] + 0.5*(time[-1] - time[-2])
	time_half2 = np.linspace(t1, t2, n2 + 1)
	time2 = 0.5*(time_half2[1:] + time_half2[:-1])
	for var in ds.get_vars(d):
		if 'time' not in d['.'][var]['.dims']:
			continue
		i = d['.'][var]['.dims'].index('time')
		x = d[var]
		size = x.shape
		size2 = list(size)
		size2[i] = n2
		x2 = np.full(size2, np.nan, dtype=x.dtype)
		for j in range(n2):
			mask = np.maximum(0,
				np.minimum(time_half[1:], time_half2[j + 1]) -
				np.maximum(time_half[:-1], time_half2[j])
			)
			s = np.sum(mask)
			if s > 0.:
				mask /= np.sum(mask)
			sel2 = tuple([
				slice(None) if l != i else j
				for l in range(len(size))
			])
			for k in range(len(mask)):
				sel = tuple([
					slice(None) if l != i else k
					for l in range(len(size))
				])
				x2[sel2] = np.where(np.isnan(x2[sel2])*mask[k], 0, x2[sel2]) + \
					x[sel]*mask[k]
		d[var] = x2
	d['time'] = time2

def stream(dd, state, tres=None, tlim=None, output_sampling=None, **options):
	if tres is not None:
		state['aggregate_state'] = state.get('aggregate_state', {})
		dd = misc.aggregate(dd, state['aggregate_state'], output_sampling)
		return misc.stream(dd, state, output_sample,
			tres=tres,
			output_sampling=output_sampling
		)
	return dd
