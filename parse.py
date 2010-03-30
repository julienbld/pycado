import yaml
import sys

from string import maketrans

stream = file('./charriot', 'r')
representation = yaml.load(stream)

#print representation['ln_sqr1_one']

def get_dependencies(data):
	val = set([])
	if isinstance(data, str):
		intab = "+-*/"
		outtab = "    "
		transtable = maketrans(intab, outtab)
		data = data.translate(transtable)
		if data.find(" ") != -1:
			for i in data.split(" "):
				val.update(get_dependencies(i))
			return val
		elif data == '':
			return val
		else:
			return [data]
			#print "variable :" + data
	if isinstance(data, list):
		for i in data:
			val.update(get_dependencies(i))
		return val
	if isinstance(data, int):
		#print "int : " + str(data)
		return val
	if isinstance(data, float):
		#print "float : " + str(data)
		return val

deps = {}
for k, v in representation.items():
	deps['k'] = get_dependencies(v)
	print k, deps['k']
#	for param in v:
#		print param

#print yaml.dump(representation)

