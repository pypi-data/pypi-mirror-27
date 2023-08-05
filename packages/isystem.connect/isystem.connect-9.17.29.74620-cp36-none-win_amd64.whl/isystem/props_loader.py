# This module loads/saves key/value pairs from/to file. For
# internal iSYSTEM use only.
#
# (c) iSYSTEM Labs, 2017

import sys
import re


class Properties(object):
    """ This class reads properties from text file in one of formats:
          key = value 
          key: value
          key value
          # Value is a single string: "value1,value2"
          key     value1,value2
          # Value is empty string
          key
          # Value is a single string: "value1 value2 value3"
          key = value1 value2 value3

        Keys must be composed of non-whitespace characters, and without
        characters ':' or '='.
        Whitespaces are trimmed. '#' as first non-whitespace character
        can be used as comment char.
    """
    
    def __init__(self, props=None):

        self._props = {}
        
        self.othercharre = re.compile(r'(?<!\\)(\s*\=)|(?<!\\)(\s*\:)')
        self.othercharre2 = re.compile(r'(\s*\=)|(\s*\:)')
        self.bspacere = re.compile(r'\\(?!\s$)')

        
    def __str__(self):
        s = '{'
        for key,value in self._props.items():
            s = s + key + '=' + value + ', '

        s = s[:-2] + '}'   # removes the last ', '
        return s

    
    def _parse(self, inFile):
        """ 
        Format desc: https://en.wikipedia.org/wiki/.properties
        """
        
        lineno = 0
        for line in inFile:
            lineno += 1
            line = line.strip()
            
            if not line:
                continue  # Skip empty lines
            
            if line[0] == '#':
                continue  # skip comment lines

            colonIdx = line.find(':')
            equalIdx = line.find('=')
            spaceIdx = line.find(' ')
            tabIdx = line.find('\t')
            separatorIdx = min(colonIdx, equalIdx, spaceIdx, tabIdx)

            if separatorIdx >= 0:
                key = line[:separatorIdx].strip()
                value = line[separatorIdx + 1:].strip()
            else:
                key = line   # empty value
                value = ''
                
            # Now split to key,value according to separation char
            if separatorIdx != -1:
                key, value = line[:separatorIdx], line[separatorIdx+1:]
            else:
                key,value = line,''

            self._props[key] = value
            
        
    def getProperty(self, key, default = None):
        """ Returns a property for the given key """
        return self._props.get(key, default)


    def setProperty(self, key, value):
        """ Sets the property for the given key """

        if type(key) is str and type(value) is str:
            self.processPair(key, value)
        else:
            raise Exception('Key and value should be strings!')

        
    def getKeys(self):
        """ Return an iterator over all the keys of the property
        dictionary, i.e the names of the properties """

        return self._props.keys()

    
    def list(self, out=sys.stdout):
        """ Writes properties to stream. """

        for key,value in self._props.items():
            out.write(key + ' = ' + value + '\n')


    def load(self, fileName):
        """ Reads properties from file. """

        with open(fileName, 'rt') as inFile:
            self._parse(inFile)
            
            
    def store(self, fileName, header=""):
        """ Writes properties to file with optional header. """

        with open(fileName, 'wt') as of:
            if header:
                of.write('# ' + header + '\n')

            list(of)
                
                
    def getPropertyDict(self):
        return self._props

    
    def __getitem__(self, name):
        """ Support dictionary like access. """

        return self.getProperty(name)

    
    def __setitem__(self, name, value):
        """ Support dictionary like access. """

        self.setProperty(name, value)
