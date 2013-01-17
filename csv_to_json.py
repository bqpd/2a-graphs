import csv, json, codecs, urllib2, re
from bs4 import BeautifulSoup as bs

Data = {'name':'2A Concentration Classes', 'children': []}
ClassDescs = MiscClassDescs = {
	'2.97':		'2.97 Designing for People',
	'6.055':	'6.055 The Art of Approximation in Science and Engineering',
	'6.S196':	'6.S196 Principles and Practice of Assistive Technology',
	'6.976':	"6.976 The Founder's Journey",
	'SP.721':	'SP.721 D-Lab I: Development',
	'SP.722':	'SP.722 D-Lab II: Design',
	'SP.775':	'SP.775 D-Lab: Energy',
	'SP.779':	'Advanced Toy Product Design',
	'SP.784':	'SP.784 Wheelchair Design in Developing Countries',
	'SP.718':	'SP.718 D-Lab Health: Medical Technologies for the Developing World',
	'SP.719':	'SP.719 X PRIZE Grand Challenges Design Workshop',
	'22.813':	'22.813 Applications of Technology in Energy and the Environment',
	'6.077':	'6.077J Research Topics in Architecture',
	'15.S24':	'15.S24 Special Seminar in Management'
}

def lookForNode(name,parent,children):
	try:
		loc = (x for x in parent['children'] if x['name'] == name).next()
	except StopIteration:
		i = len(parent['children'])
		if children:  parent['children'].append({'name': name, 'children':[]})
		else:		  parent['children'].append({'name': name})
		loc = parent['children'][i]
	return loc

def increaseStat(resource,stat):
	try:				resource[stat] += 1
	except KeyError:	resource[stat] = 1

with open('conc clean.csv', 'rb') as csvfile:
	spamreader = csv.reader(csvfile, delimiter=',')
	for row in spamreader:
		classname = row[0]
		classdesc = classname
		url = False
		try:
			classdesc = ClassDescs[classname]
		except KeyError:	
			try:
				url = 'http://student.mit.edu/catalog/search.cgi?search='+classname
				soup = bs(urllib2.urlopen(url).read())
				classname_re = re.compile('\.').sub('\\.',classname)
				classdesc = re.compile(classname_re+'.*\n').findall(str(soup.h3))[0]
				classdesc = re.compile('\n').sub('',classdesc)
				ClassDescs[classname] = classdesc
			except IndexError:
				try:
					classdesc = ClassDescs[classname]
				except KeyError:
					ClassDescs[classname] = classname
					print 'An unknown class!  ' + classname
					raise
		dep = classname.split('.')[0]
		try: 				dep = "Course " + str(int(dep))
		except ValueError:	pass
		dep_ = lookForNode(dep,Data,children=True)
		num_ = lookForNode(classdesc,dep_,children=False)
		if url:
			num_['url'] = url
			print 'For '+classname+', saving url: '+url
		increaseStat(num_,'pop')
		increaseStat(dep_,'pop')

output =  json.dumps(Data, sort_keys=False,indent=4, separators=(',', ': '))

popOnSameLine = re.compile('\n +"pop"')
output = popOnSameLine.sub(' "pop"',output)

cleanNoChildren = re.compile('\{\n(.+),\n +(.+)(\n +\})')
output = cleanNoChildren.sub(r'{   \2,\n\1\3',output)

with codecs.open('2a_concentration.json', mode='w', encoding='utf-8') as outfile:
	outfile.write(output)