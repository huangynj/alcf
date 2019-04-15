import numpy as np

def stats_map(d, stats):
	stats['zfull'] = stats.get('zfull', d['zfull'][0,:])
	stats['n'] = stats.get('n', 0)
	if len(d['cloud_mask'].shape) == 3:
		n, m, l = d['cloud_mask'].shape
		dims = (m, l)
	else:
		n, m = d['cloud_mask'].shape
		l = 0
		dims = (m,)
	stats['cloud_occurrence'] = stats.get(
		'cloud_occurrence',
		np.zeros(dims, dtype=np.float64)
	)
	for i in range(n):
		if not np.all(d['zfull'][i,:] == stats['zfull']):
			raise ValueError('Irregular vertical zfull - interpolate with "alcf lidar ... zres: <zres>" first')
		if l > 0:
			stats['cloud_occurrence'][:,:] += d['cloud_mask'][i,:,:]
		else:
			stats['cloud_occurrence'][:] += d['cloud_mask'][i,:]
		stats['n'] += 1

def stats_reduce(stats):
	return {
		'cloud_occurrence': 100.*stats['cloud_occurrence']/stats['n'],
		'zfull': stats['zfull'],
		'n': stats['n'],
		'.': {
			'zfull': {
				'.dims': ['zfull'],
				'standard_name': 'height_above_reference_ellipsoid',
				'units': 'm',
			},
			'cloud_occurrence': {
				'.dims': ['zfull', 'column']
					if len(stats['cloud_occurrence'].shape) == 2
					else ['zfull'],
				'long_name': 'cloud_occurrence',
				'units': '%',
			},
			'n': {
				'.dims': [],
				'long_name': 'number_of_profiles',
				'units': '1',
			}
		}
	}

def stream(dd, state, **options):
	state['stats'] = state.get('stats', {})
	for d in dd:
		if d is None:
			return [stats_reduce(state['stats'])]
		stats_map(d, state['stats'])
	return []