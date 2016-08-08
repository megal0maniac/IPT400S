#Pseudocode (although valid Python) for some of the trickier tasks which I haven't gotten around to implementing

#Graphing methods for dealing with more data points than we want
start = 82
end = 1416
res = 100
int = 300

#For getting a graph with res data points
#Loop generates a list, use list to get average for each group and return
for x in range(1,res+1):
  print int(start + x*((end-start)/float(res)))

#For getting a graph with int interval between points. Truncates oldest data
#Same as above, otherwise
for x in reversed(range(0,1+(end-start)/int)):
  print end - x*int
for x in range((end-start)/int, -1, -1):
  print end - x*int

#Parallel list sorting
#Thanks Nick! http://stackoverflow.com/a/2223828
perm = sorted(xrange(len(foo)), key=lambda x:foo[x])
for p in perm:
  print "%s: %s" % (foo[p], bar[p])

#Get range of days from two timestamps
from datetime import date, timedelta

end = date.fromtimestamp(1472969203)
start = date.fromtimestamp(1462969203)
delta = end - start

for i in range(delta.days + 1):
  print '{}.db'.format(start + timedelta(days=i))
