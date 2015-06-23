import pycurl
from StringIO import StringIO

class Ical_Tools:
    #this method puts the other methods into a usable order.
    def modify_ical_feed(self):
       	calendar =  pull_feed(self, feed_url)
        seperate_events = Ical_Tools.seperate_events(self, calendar)
        description_removed = Ical_Tools.remove_extra_description(self, seperate_events)
        processed_events = Ical_Tools.remove_location(self, description_removed)
        Ical_Tools.print_to_file(self, processed_events)


    def pull_feed(self):
	feed_url = 'http://calendar.activedatax.com/cnm/downloadevents.aspx?export=export&type=N&ctgrys=43-0,8-0,10-0,2-0,25-0,44-0,45-0,11-0,9-0,35-0,52-0,29-0,26-0,26-4,26-3,32-0,28-0,40-0,36-0,3-0,4-0,7-0,5-0,37-0,12-0,13-0,31-0,33-0,20-0,54-0,21-0,50-0,50-91,39-0,46-0,6-0,42-0,34-0,17-0,17-37,17-38,17-39,17-40,17-41,14-0,14-42,14-43,14-44,14-45,14-46,14-47,14-48,14-49,14-50,14-51,14-52,14-53,14-54,14-56,14-57,14-58,14-59,14-60,14-61,14-62,14-63,14-90,15-0,15-22,15-23,15-24,15-25,15-26,15-27,15-28,15-29,15-30,15-31,15-32,15-33,15-34,15-35,16-0,16-9,16-64,16-65,16-66,16-67,16-68,16-69,16-70,16-71,16-72,16-73,16-74,16-75,16-76,18-0,18-98,18-11,18-77,18-12,18-13,18-14,18-78,18-8,18-15,18-79,18-16,18-17,18-80,18-81,18-18,18-89,18-19,18-20,18-36,18-21,19-0,19-82,19-10,19-83,19-84,19-85,19-86,19-87,19-88,49-0,22-0,57-0,53-0,53-95,53-94,53-92,53-93,53-96,1-0,1-1,1-2,56-0,41-0,30-0,48-0,47-0,51-0,23-0,24-0&ihc=n&range=35&fType=ical&sort=id'
	buffer = StringIO()
	c = pycurl.Curl()
	c.setopt(c.URL, feed_url)
	c.setopt(c.WRITEDATA, buffer)
	c.perform()
	c.close()

	body = buffer.getvalue()
	print(body)

	calendar_file = 'calendar.ics'
	output = open(calendar_file, 'wb')
	output.write(body)
	output.close()

	
    #this method seperates events into individual dict items so we can iterate over them one by one
    def seperate_events(self, file_name):
        events = []
        counter = 0
        string = ''
        with open(file_name) as file:
            for line in file:
                if line.rstrip('\r\n') == 'BEGIN:VEVENT':
                   # string = line.rstrip('\r')
                    string = line.replace('\r\n', '\n')
		elif line.rstrip('\r\n') == 'END:VEVENT':
                   # string += line.rstrip('\r')
		    string += line.replace('\r\n', '\n')
		   # string.replace('^M', '')
                    events.append(string)
                    #counter += 1
                else:
                    string += line.replace('\r\n', '\n')

        return events


    def remove_extra_description(self, events):
        #make sure ACTION:DISPLAY is still in resulting file
        counter = 0
        for event in events:
            desc_beg_flag = event.find('ACTION:DISPLAY') + 14
            desc_end_flag = event.find('END:VALARM') - 1
            first_half = event[0:desc_beg_flag]
            second_half = event[desc_end_flag:len(event)]

            events[counter] = first_half + second_half
            counter += 1

        return events


    def remove_location(self, events):
        counter = 0
        for event in events:
            loc_beg_flag = event.find('LOCATION:')
            loc_end_flag = event.find('SUMMARY') - 1
            first_half = event[0:loc_beg_flag]
            second_half = event[loc_end_flag:len(event)]

            events[counter] = first_half + second_half
            counter += 1

        return events


    def print_to_file(self, events):
        output_file = 'cnm_events.ics'
        output = open(output_file, 'wb')
        output.write('BEGIN:VCALENDAR')
	output.write('METHOD:PUBLISH')
	output.write('PRODID:-//ActiveDataExchange/Calendar V3.14.7//EN')
	output.write('VERSION:2.0')
	
	for event in events:
            output.write(event)
	output.close()



