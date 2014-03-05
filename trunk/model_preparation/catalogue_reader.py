""""
catalogue_reader.py
This file reads data from a variety of earthquake catalogue formats and
creates an earthquake event object for each event.
"""

import earthquake_event
import sys, os
import datetime
import csv


class CatalogueReader(object):

    def __init__(self, filepathname, **kwargs):
        """
        filepathname = path and name of catalogue file.
        kwargs:
            file_format = currently supports nordic; engdahl csv
        """

        self.infile = filepathname
        # Determine file format to call right reader function
        self.file_format = kwargs.get('file_format', None)

        # If format not specified, try to guess
        if self.file_format is None:
            if self.infile.endswith('.nordic'):
                self.file_format = 'nordic'
            elif self.infile.endswith('.csv'):
                self.file_format = 'isc_csv'
            else:
                msg = 'File format unknown or not implemented'
                raise Exception(msg)

        try:
            self.read_file()
        except IOError:
            print 'File %s does not exist or could not be accessed' % self.infile
            sys.exit(-1)

    def read_file(self):
        """
        Reads a variety of file formats and can be updated to read different
        formats in the future.
        """

        ifile = open(self.infile,'r')
        event_list = []

        # Read nordic format
        if self.file_format == 'nordic':      
            for line in ifile.readlines():
                # Read time information
                year = int(line[1:5])
                month = int(line[6:8])
                day = int(line[8:10])
                hour = int(line[11:13])
                minute = int(line[13:15])
                second = int(line[16:18])
                try:
                    microsecond = int(line[19])*100000
                except ValueError:
                    microsecond = None
                
                # Approximate midnight case as datetime doesn't like seconds = 60.0
                if second >= 60.0:
                    minute += 1
                    second = second - 60
                if minute >= 60:
                    hour += 1
                    minute = minute - 60
                if hour >= 24:
                    hour = 23
                    minute = 59
                    second = 59
                    microsecond = 999999
#                print year, month, day, hour, minute, second
                if microsecond is not None:
                    event_time = datetime.datetime(year, month, day, hour, minute, second, microsecond)
                else:
                    event_time = datetime.datetime(year, month, day, hour, minute, second)
                # Read other parameters
                lat = float(line[23:30])
                lon = float(line[31:38])
                depth = float(line[38:43])
                mag = float(line[56:59])
                mag_type = line[59:60]

                # Create earthquake event object
                Event = earthquake_event.EarthquakeEvent(lon, lat, mag, event_time, 
                                                          depth = depth, mag_type = mag_type)
                event_list.append(Event)
            self.EventSet = earthquake_event.EventSet(event_list)
                                                                 
        if self.file_format == 'isc_csv':
            ifile = open(self.infile,'r')
            csvreader = csv.reader(ifile)
            for i in range(6):
                header = csvreader.next()
            for row in csvreader:
                #print 'row',row
                event_id = row[0]
                author = row[1].strip(' ')
                date = row[2]
                time = row[3]
                lat = row[4]
                lon = row[5]
                depth = row[6]
                #DEPFIX = row[7]
                magnitudes = row[8:]
                for i in range(len(magnitudes)):
                    magnitudes[i] = magnitudes[i].strip(' ')
                if magnitudes[-1] == '':
                    magnitudes = magnitudes[:-1]

                year, month, day = date.split('-')
                hour, minute, second = time.split(':')
                second, microsecond = second.split('.')
                year, month, day, hour, minute, second, microsecond = \
                      int(year), int(month), int(day), int(hour), int(minute),\
                      int(second), int(microsecond)
                event_time = datetime.datetime(year, month, day, hour, minute, second)

                magnitude_author_list = magnitudes[0::3]
                magnitude_type_list = magnitudes[1::3]
                magnitude_value_list_str = magnitudes[2::3]
                magnitude_value_list = []
                for value in magnitude_value_list_str:
                    magnitude_value_list.append(float(value))
                
                #print magnitude_value_list
                if len(magnitude_value_list) > 0:
                    Event  = earthquake_event.EarthquakeEvent(lon, lat, float(magnitudes[2]), event_time, 
                                                              depth = depth, 
                                                              event_id = event_id, author = author,
                                                              magnitude_list = magnitude_value_list,
                                                              magnitude_type_list = magnitude_type_list,
                                                              magnitude_author_list = magnitude_author_list)
                else:
                    #print 'No magnitude recorded, ignoring entry'
                    continue
                event_list.append(Event)
            self.EventSet = earthquake_event.EventSet(event_list)

        # Read  ISC/GEM extended catalogue format
        if self.file_format == 'iscgem_extended_csv':   
            ifile = open(self.infile,'r')
            csvreader = csv.reader(ifile)
            header = csvreader.next()
            # Create dictionary of which header applies to which column
            header_index = {}
            for i in range(len(header)):
                header_index[header[i]] = i
            # Note that we only collect the parameters that we want
            for row in csvreader:
                #print 'row',row
                event_id = row[header_index['eventID']]
                author = row[header_index['Agency']]
                year = row[header_index['year']]
                month = row[header_index['month']]
                day = row[header_index['day']]
                hour = row[header_index['hour']]
                minute = row[header_index['minute']]
                second = row[header_index['second']]
                lat = float(row[header_index['latitude']])
                lon = float(row[header_index['longitude']])
                depth = float(row[header_index['depth']])
                magnitude = float(row[header_index['magnitude']])
                magnitude_type = row[header_index['magnitudeType']]
                
                second, microsecond = second.split('.')
                year, month, day, hour, minute, second, microsecond = \
                      int(year), int(month), int(day), int(hour), int(minute),\
                      int(second), int(microsecond)
                event_time = datetime.datetime(year, month, day, hour, minute, second)

                magnitude_value_list = [magnitude]
                magnitude_type_list = [magnitude_type]
                magnitude_author_list = [author]
                if len(magnitude_value_list) > 0:
                    Event  = earthquake_event.EarthquakeEvent(lon, lat, magnitude, event_time, 
                                                          depth = depth, 
                                                          event_id = event_id, author = author,
                                                          magnitude_list = magnitude_value_list,
                                                          magnitude_type_list = magnitude_type_list,
                                                          magnitude_author_list = magnitude_author_list)
                else:
                    #print 'No magnitude recorded, ignoring entry'
                    continue
                event_list.append(Event)
            self.EventSet = earthquake_event.EventSet(event_list)

        # Read 'csv' Engdahl format
        if self.file_format == 'engdahl_csv':
            ifile = open(self.infile,'r')
            csvreader = csv.reader(ifile)
            header = csvreader.next()               
            # Read data       
            for row in csvreader:
                lon = float(row[0])
                lat = float(row[1])
                year = int(row[2])
                month = int(row[3])
                day = int(row[4])
                hour = int(row[7])
                minute = int(row[8])
                mag = float(row[5])
                depth = float(row[6])

                event_time = datetime.datetime(year, month, day, hour, minute)

                Event = earthquake_event.EarthquakeEvent(lon, lat, mag, event_time, 
                                                          depth = depth)
                event_list.append(Event)
            self.EventSet = earthquake_event.EventSet(event_list)

        ifile.close()
            

        
        
