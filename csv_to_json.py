import csv, json, codecs, urllib2, re

Data = {'name':'2A Concentration Classes', 'children': []}		# Initialize JSON structure
ClassDescs = {
# Classes in the course catalog will be downloaded: these are the ones that aren't there.
	'2.97':		'2.97 Designing for People',
	'6.055':	'6.055 The Art of Approximation in Science and Engineering',
	'6.S196':	'6.S196 Principles and Practice of Assistive Technology',
	'6.976':	"6.976 The Founder's Journey",
	'SP.721':	'SP.721 D-Lab I: Development',
	'SP.722':	'SP.722 D-Lab II: Design',
	'SP.775':	'SP.775 D-Lab: Energy',
	'SP.779':	'SP.779 Advanced Toy Product Design',
	'SP.784':	'SP.784 Wheelchair Design in Developing Countries',
	'SP.718':	'SP.718 D-Lab Health: Medical Technologies for the Developing World',
	'SP.719':	'SP.719 X PRIZE Grand Challenges Design Workshop',
	'22.813':	'22.813 Applications of Technology in Energy and the Environment',
	'6.077':	'6.077J Research Topics in Architecture',
	'15.S24':	'15.S24 Special Seminar in Management'
}

def lookForNode(name,parent,children=False):
	'''Given parent, look for child with 'name'.
	If such a child doesn't exist, create it (potentially with children of its own).'''
	try:
		loc = (x for x in parent['children'] if x['name'] == name).next()
	except StopIteration:
		i = len(parent['children'])
		if children:  parent['children'].append({'name': name, 'children':[]})
		else:		  parent['children'].append({'name': name})
		loc = parent['children'][i]
	return loc

def increaseStat(resource,stat):
	'''Given dictionary 'resource', increment/initialize the value of 'stat'.'''
	try:				resource[stat] += 1
	except KeyError:	resource[stat] = 1

with open('conc clean.csv', 'rb') as csvfile:
	for row in csv.reader(csvfile, delimiter=','):
		classname = row[0]  # Assume it's a valid class for now; we'll check it against the course catalog later
		newURL = False
		####################################
		# What department is the class in? #
		####################################
		dep_id = classname.split('.')[0]
		# If it's just a number, spice it up a bit
		try: 				dep = "Course " + str(int(dep_id))
		except ValueError:	dep = dep_id
		###################################
		# What's the class's description? #
		###################################
		try:	# Do we already have it stored?
			classdesc = ClassDescs[classname]
		except KeyError: # If not,
			try:	# Is the class description available from the course catalog?
				newURL = 'http://student.mit.edu/catalog/search.cgi?search='+classname  # craft URL
				soup = urllib2.urlopen(newURL).read()  # load the search in the course catalog
				classname_re = re.compile('\.').sub('\\.',classname)  # escape the period in the classname
				classdesc = re.compile('<h3>.*?('+classname_re+'.*)\n').findall(soup)[0]  # find the classname
				ClassDescs[classname] = classdesc  # save it to our descriptions dictionary
			except IndexError:	# If it isn't, get a human to find it (and use the class's number for now)
				ClassDescs[classname] = classdesc = classname
				hl = '\n-----------------------------------------------\n'
				print hl+'|> Class not found in course catalog:  '+classname+hl
		#####################################
		# Traverse and change the structure #
		#####################################
		increaseStat(Data,'pop')
		## department name
		dep_ = lookForNode(dep,Data,children=True)	# Find the department's resource in the structure
		dep_['id'] = dep_id
		increaseStat(dep_,'pop')					# One more person for this department
		## class description
		num_ = lookForNode(classdesc,dep_,children=False)	# Find the class's resource in the department
		increaseStat(num_,'pop')							# One more person for this class
		## website
		if newURL:  # First time? Attach the URL and print it for sanity-checking
			num_['url'] = newURL
			#print 'For '+classname+', the URL is\t'+newURL.split('http://')[1]

# Turn that big dictionary into JSON
output =  json.dumps(Data, sort_keys=False,indent=4, separators=(',', ': '))
# and make it pretty with regular expressions
popOnSameLine = re.compile('\n +"pop"')
output = popOnSameLine.sub(' "pop"',output)
cleanNoChildren = re.compile('\{\n(.+),\n +(.+)(\n +\})')
output = cleanNoChildren.sub(r'{   \2,\n\1\3',output)
# Write it out!
with codecs.open('2a_concentration.json', mode='w', encoding='utf-8') as outfile:
	outfile.write(output)