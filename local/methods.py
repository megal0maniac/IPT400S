#For getting a graph with res data points
#Loop generates a list, use list to get average for each group and return

start = 82
end = 1416
res = 100
int = 300

for x in range(1,res+1):
  print int(start + x*((end-start)/float(res)))

#For getting a graph with int interval between points. Truncates oldest data
#Same as above, otherwise
for x in reversed(range(0,1+(end-start)/int)):
  print end - x*int
for x in range((end-start)/int, -1, -1):
  print end - x*int
