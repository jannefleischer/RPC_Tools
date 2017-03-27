# -*- coding: utf-8 -*-


from enum import Enum


class Filter(object):

    _filter_types = ['ValueList',
                     'Range',
                     'FeatureClass',
                     'File',
                     'Field',
                     'Workspace']

    """Dummy Filter"""
    def __init__(self, list=[], type='ValueList'):
        self.list = list
        self._type = type

    @property
    def type(self):
        return self._type
    @type.setter
    def type(self, value):
        if value not in self._filter_types:
            raise ValueError('{} not in {}'.format(value, self._filter_types))
        self._type = value

    def __repr__(self):
        return '{}: {}'.format(self.type, self.list)



class Parameter(object):
    """Dummy Parameter"""
    def __init__(self):
        self.name = None
        self.displayName = None
        self.direction = None
        self.datatype = None
        self.parameterType = None
        self.enabled = False
        self.category = None
        self.symbology = None
        self.multiValue = False
        self._value = None
        self.filter = Filter()

        self.columns = []
        self.defaultEnvironmentName = ''
        self.parameterDependencies = []

        self._altered = False
        self._validated = False
        self._message = ''
        self._status = 'INFORMATIVE'

    @property
    def value(self):
        return self._value
    @value.setter
    def value(self, val):
        self._value = val
        self._altered = True
        self._validated = False

    @property
    def altered(self):
        return self._altered

    @property
    def hasBeenValidated(self):
        return self._validated

    @property
    def message(self):
        return self._message

    @property
    def valueAsText(self):
        return str(self.value)

    def clearMessages(self):
        self._status = 'INFORMATIVE'
        self.message = ''

    def hasError(self):
        return self._status == 'ERROR'

    def hasWarning(self):
        return self._status == 'WARNING'

    def isInputValueDerived(self):
        return False

    def setErrorMessage(self, message):
        self._status = 'ERROR'
        self.message = message

    def setIDMessage(self, message_type, message_ID, *args):
        pass

    def setWarningMessage(self, message):
        self._status = 'WARNING'
        self.message = message

    def __repr__(self):
        name = self.name
        try:
            name = name.decode('cp1252')
        except UnicodeDecodeError:
            pass
        except AttributeError:
            pass

        value = self.value
        try:
            value = value.decode('cp1252')
        except UnicodeDecodeError:
            pass
        except AttributeError:
            pass

        return u'{}: {}'.format(name, value).encode('utf8')


class Messages(object):
    """Mock Messages object"""
    def __init__(self):
        self.message = ''
        self._status = 'INFORMATIVE'

    def AddMessage(self, message):
        self.addMessage(message)

    def addMessage(self, message):
        self._status = 'INFORMATIVE'
        self.message = message
        print(message)

    def AddErrorMessage(self, message):
        self.addErrorMessage(message)

    def addErrorMessage(self, message):
        self._status = 'ERROR'
        self.message = message
        print(message)

    def AddIDMessage(self, message):
        self.addIDMessage(message)

    def addIDMessage(self, message_type, message_ID, *args):
        pass

    def AddWarningMessage(self, message):
        self.addWarningMessage(message)

    def addWarningMessage(self, message):
        self._status = 'WARNING'
        self.message = message
        print(message)

    def AddGPMessages(self, message):
        self.addGPMessages()

    def addGPMessages(self):
        pass


def AddMessage(message):
    print(message)


def AddWarning(message):
    print(message)


def AddError(message):
    print(message)


def AddIDMessage(message, message_ID, add_argument1=None, add_argument2=None):
    print(message)
