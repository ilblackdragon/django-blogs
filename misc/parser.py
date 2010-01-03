# -*- coding: utf-8 -*-
import xlrd
import re

class Reader(object):

    def __init__(self, FileName):
        self.filename = FileName

    def readline(self):
        return ''

class XlsReader(Reader):

    def __init__(self, fileName):
        super(XlsReader, self).__init__(self)
        self.__book__ = xlrd.open_workbook(fileName)
        self.__sheet__ = self.__book__._sheet_list[0]
        self.__row__ = 0

    def formatrow(self, types, values, wanttupledate):
        """ Internal function used to clean up the incoming excel data """
        ##  Data Type Codes:
        ##  EMPTY 0
        ##  TEXT 1 a Unicode string
        ##  NUMBER 2 float
        ##  DATE 3 float
        ##  BOOLEAN 4 int; 1 means TRUE, 0 means FALSE
        ##  ERROR 5
        returnrow = []
        for i in range(len(types)):
            type,value = types[i],values[i]
            if type == 2:
                if value == int(value):
                    value = int(value)
            elif type == 3:
                datetuple = xlrd.xldate_as_tuple(value, self.__book__.datemode)
                if wanttupledate:
                    value = datetuple
                else:
                    # time only no date component
                    if datetuple[0] == 0 and datetuple[1] == 0 and \
                       datetuple[2] == 0:
                        value = "%02d:%02d:%02d" % datetuple[3:]
                    # date only, no time
                    elif datetuple[3] == 0 and datetuple[4] == 0 and \
                         datetuple[5] == 0:
                        value = "%04d-%02d-%02d" % datetuple[:3]
                    else: # full date
                        value = "%04d-%02d-%02d %02d:%02d:%02d" % datetuple
            elif type == 5:
                value = xlrd.error_text_from_code[value]
            returnrow.append(value)
        return returnrow

    def readline(self):
        try:
            types,values = self.__sheet__.row_types(self.__row__),self.__sheet__.row_values(self.__row__)
        except IndexError:
            return ['']
        self.__row__ += 1
        return self.formatrow(types,values,False)

class CsvReader(Reader):

    def __init__(self, fileName):
        self.file = open(fileName, 'r')
        self.lines = self.file.readlines()

    def readline(self):
        if len(self.lines) == 0:
            return ['']
        line = self.lines[0]
        self.lines = self.lines[1:]
        line = line[:-1] #Last \n (that sucks, yep) 
        line = line.split(';')
        res = []
        for item in line:
            if item.isdigit(): #integer value :)
#                res.append(int(item))
                res.append(item) #there is no integer type recongition now :)
            else:   
                m = re.match(r'^(\d+)/(\d+)/(\d+)$', item) #DD/MM/YYYY, date...
                if m:
                    res.append(u"%04d-%02d-%02d" % (int(m.group(3)), int(m.group(2)), int(m.group(1))))
                else: #String :-P
                    res.append(unicode(item, "utf8"))
        return res
                                

def open_file(fileName):
    #TODO: Just find what reader to open
    ext = fileName.split('.')[-1]
    if ext.upper() == 'XLS':
        reader = XlsReader(fileName)
    elif ext.upper() == 'CSV':
        reader = CsvReader(fileName)
    else:
        raise RuntimeError("Unknown format: %s" % ext)
    return reader
