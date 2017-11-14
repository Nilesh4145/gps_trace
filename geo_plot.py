import numpy
import gmplot
import datetime


############# Create time-sorted numpy array of gps trace ##################
trace_raw = numpy.genfromtxt('gps_trace.csv', delimiter='\t', dtype=str)
trace = []
[trace.append(i.split(",")) for i in trace_raw[0:len(trace_raw)-2]]
trace = numpy.array(trace)
for i in trace:
	i[3] = i[3][1:18]
	i[4] = i[4][1:9]
sorted_trace = numpy.array(sorted(trace, key=lambda d: d[4]))
############################################################################

#### Get indices of time stamps corresponding to start and finish time #####
def left_index(a, arr):
	index = 0
	s_time = datetime.datetime.strptime(a, '%H:%M:%S').time()
	for val in arr:
		if datetime.datetime.strptime(val, '%H:%M:%S').time() >= s_time:
			return index
		index += 1

def right_index(a, arr):
	index = 0
	s_time = datetime.datetime.strptime(a, '%H:%M:%S').time()
	for val in arr:
		if datetime.datetime.strptime(val, '%H:%M:%S').time() >= s_time:
			return index-1
		index += 1
############################################################################


def process(start, finish):
	start_index = left_index(start, sorted_trace[:, 4])
	finish_index = right_index(finish, sorted_trace[:, 4])
	gmap = gmplot.GoogleMapPlotter(sorted_trace[0][0], sorted_trace[0][1], 50, apikey='AIzaSyCIZHxg9W7R4dD9_mYWi4rj1PdjDS6tEW4')
	gmap.plot(sorted_trace[:, 0][start_index:finish_index].astype(numpy.float), 
		sorted_trace[:, 1][start_index:finish_index].astype(numpy.float), '#FF6666', edge_width=10)
	gmap.draw("templates/map.html")
