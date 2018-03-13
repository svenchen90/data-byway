import os
import re
import json

dir = 'byway'
def match1(string):
	return re.match('^\w(\w|\s)*: ', string)

def matchReturn(string):
	return re.match('^\n$', string)

def cleanString(string):
	if string[-1] == '\n':
		string = string[:-1]
	while string[0] == '"' and string[-1] == '"':
		string = string[1:-1]
	return string
list = []	
	
for filename in os.listdir(dir):
	if filename.endswith(".md"):
		filepath = os.path.join(dir, filename)
		with open(filepath) as fp:
			line = fp.readline()
			data = {'ps': []}
			flag = 0
			while line:
				if flag < 2:
					if re.match('---\n', line):
						flag += 1
					match = match1(line)
					if match and not line[match.end()] == '\n':
						key = match.group()[:-2]
						if not key == 'template':
							data[key] = cleanString(line[match.end():-1])
						line = fp.readline()
					elif match and line[match.end()] == '\n':
						key = match.group()[:-2]
						data[key] = []
						line = fp.readline()
						if key == 'websites':
							
							while not match1(line) and line and not matchReturn(line):
								submatch = re.search('\w*: ', line)
								if submatch and submatch.group(0)[:-2] == 'url':
									temp = {}
									temp[submatch.group(0)[:-2]] = cleanString(line[submatch.end(0):])
									line = fp.readline()
									submatch = re.search('\w*: ', line)
									temp[submatch.group(0)[:-2]] = cleanString(line[submatch.end(0):])
									data[key].append(temp)
									line = fp.readline()
								else:
									print line, 'error'
									line = fp.readline()
						elif key == 'bounds':
							geo1 = []
							geo2 = []
							geo1.append(cleanString(line[re.search('\w', line).start():]))
							line = fp.readline()
							geo1.append(cleanString(line[re.search('\w', line).start():]))
							line = fp.readline()
							geo2.append(cleanString(line[re.search('\w', line).start():]))
							line = fp.readline()
							geo2.append(cleanString(line[re.search('\w', line).start():]))
							line = fp.readline()
							data[key].append(geo1)
							data[key].append(geo2)
						else:
							while not match1(line) and line and not matchReturn(line):
								data[key].append(cleanString(line[re.search('\w', line).start():])) 
								line = fp.readline()
					else:
						#print line
						line = fp.readline()
				else:
					if not matchReturn(line):
						data['ps'].append(line)
					line = fp.readline()
			
			
			for key in ['path', 'includes', 'part of']:
				if key in data and type(data[key]) == type([]):
					data[key] = map(lambda x: x[:-1] , data[key]);
					
			list.append(data)
	else:
		continue
with open("data.min.js", "a") as myfile:
	for line in list:
		myfile.write(json.dumps(line,  sort_keys=True) + '\n', )