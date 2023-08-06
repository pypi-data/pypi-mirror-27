"""which module to find executables"""
from os import X_OK, access, environ, name as osname
from os.path import abspath, join as pjoin, exists

def which(prog, delim=':'):
	"""which function like the linux 'which' program"""
	delim = delim if osname != 'nt' else ';'
	for path in environ['PATH'].split(delim):
		if osname == 'nt':
			for (d, s, fs) in walk(path):
				for f in fs:
					trg = pjoin(d, f)
					if exists(trg):
						return trg
		elif access(pjoin(path, prog), X_OK):
			return pjoin(abspath(path), prog)
