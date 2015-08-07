import sys 
#print 'Number of arguments:', len(sys.argv), 'arguments'
#print 'Argument list:', str(sys.argv)
ipfile = open(sys.argv[1], 'r')
for line in ipfile:
	print line.strip()
ipfile.close()
