META = {
	'time': {
		'.dims': ['time'],
		'long_name': 'time',
		'units': 'days since -4712-01-01T12:00',
	},
	'zfull': {
		'.dims': ['time', 'level'],
		'long_name': 'height_above_reference_ellipsoid',
		'units': 'm',
	},
	'backscatter': {
		'.dims': ['time', 'level'],
		'long_name': 'backscatter',
		'units': 'm-1 sr-1',
	},
	'altitude': {
		'.dims': ['time'],
		'long_name': 'altitude',
		'units': 'm',
	},
}

from . import chm15k
from . import cl51
from . import cl31
from . import mpl
from . import mpl2nc
from . import cosp
from . import caliop

LIDARS = {
	'chm15k': chm15k,
	'cl51': cl51,
	'cl31': cl31,
	'mpl': mpl,
	'mpl2nc': mpl2nc,
	'minimpl': mpl,
	'cosp': cosp,
	'caliop': caliop,
}
