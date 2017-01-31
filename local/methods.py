#Pseudocode (although valid Python) for some of the trickier tasks. Mostly just a reference

#Graphing methods for dealing with more data points than we want
start = 82
end = 1416
res = 100
interval = 300

#For getting a graph with res data points
#Loop generates a list, use list to get average for each group and return
for x in range(1,res+1):
  print int(start + x*((end-start)/float(res)))

#Same thing as above, but for getting 'value' out of biglist
for x in range(0,res):
  print average([biglist[x]['value'] for x in range(int(x*((end+1.0)/res)),int((x+1)*((end+1.0)/res)))])

#For getting a graph with int interval between points. Truncates oldest data
#Same as above, otherwise
for x in reversed(range(0,1+(end-start)/interval)):
  print end - x*interval
for x in range((end-start)/interval, -1, -1):
  print end - x*interval

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

#List comprehension to get specific parameter from dataset
#Generates list [2, 5, 8]
data = []
data.append({'one':1, 'two':2, 'three':3})
data.append({'one':4, 'two':5, 'three':6})
data.append({'one':7, 'two':8, 'three':9})
test = [data[x]['two'] for x in range(0,len(data))]

#Select average value per hour
select min(time), avg(temperature) as 'average temperature' from weather group by strftime('%H', datetime(time, 'unixepoch', 'localtime'));

#Shelved averaging code
#Only works for numerical values
#def average(avglist):
#    print 'avglistlen:{}'.format(len(avglist))
#    print 'avglist:{}'.format(avglist)
#    return sum([avglist[x] for x in range(0, len(avglist))])/len(avglist)

#def blockaverage(blavglist, blavgkey):
#    return average([blavglist[x][blavgkey] for x in range(int(x*((len(blavglist)+1.0)/res)),int((x+1)*((len(blavglist)+1.0)/res)))])

# This is broken. Don't know why. TODO
#    
#    if len(queryDataSorted) > res:
#        queryDataAveraged = []
#        for x in range(0,res):
#            print 'res:{} x:{} qdlen:{}'.format(res,x,len(queryDataSorted))
#            queryDataAveraged.append({'timestamp' : int(average([queryDataSorted[y]['timestamp'] for y in range(int(x*((len(queryDataSorted)+1.0)/res)),int((x+1)*((len(queryDataSorted)+1.0)/res))-1)])),
#                                    'windspeed' : '{0:.2f}'.format(average([queryDataSorted[y]['windspeed'] for y in range(int(x*((len(queryDataSorted)+1.0)/res)),int((x+1)*((len(queryDataSorted)+1.0)/res))-1)])),
#                                    'winddirection' : int(average([queryDataSorted[y]['winddirection'] for y in range(int(x*((len(queryDataSorted)+1.0)/res)),int((x+1)*((len(queryDataSorted)+1.0)/res))-1)])),
#                                    'temperature' : '{0:.2f}'.format(average([queryDataSorted[y]['temperature'] for y in range(int(x*((len(queryDataSorted)+1.0)/res)),int((x+1)*((len(queryDataSorted)+1.0)/res))-1)])),
#                                    'humidity' : '{0:.2f}'.format(average([queryDataSorted[y]['humidity'] for y in range(int(x*((len(queryDataSorted)+1.0)/res)),int((x+1)*((len(queryDataSorted)+1.0)/res))-1)])),
#                                    'rain' : average([queryDataSorted[y]['rain'] for y in range(int(x*((len(queryDataSorted)+1.0)/res)),int((x+1)*((len(queryDataSorted)+1.0)/res))-1)])})
#        print time() - timethen
#        return queryDataAveraged