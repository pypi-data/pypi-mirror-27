from fei_ws import config
from urlparse import urljoin
from requests import Session
from zeep.transports import Transport
from zeep.cache import InMemoryCache
from zeep.client import Client



class FEIWSBaseClient(object):
    """FEI Base Client contains logic shared among FEI Clients. It should not
    be used on its own.

    """
    def __init__(self, version, username=None, password=None):
        """ Initializes the base client.

        Params:
            version: A tuple containing the version numbering.
            username: The username used to authenticate. The username from the
                config file is used when it is not supplied.
            password: The password used to authenticate. The password from the
                config file is used when it is not supplied.

        """
        self.__AUTH_WSDL = urljoin(config.FEI_WS_BASE_URL,
                                   '/_vti_bin/Authentication.asmx?WSDL')
        self.__ORGANIZER_WSDL = urljoin(
            config.FEI_WS_BASE_URL, '/_vti_bin/FEI/OrganizerWS_%s_%s.asmx?WSDL'
                                 % version)

        self.__COMMON_WSDL = urljoin(config.FEI_WS_BASE_URL,
                                     '/_vti_bin/FEI/CommonWS.asmx?WSDL')

        self._version = version
        # self._my_cache = Cache()
        self._cache = InMemoryCache(timeout=24*3600)
        self._common_data = {}
        self._username = username if username else config.FEI_WS_USERNAME
        self._password = password if password else config.FEI_WS_PASSWORD
        self._session = Session()

        self._ows_client = Client(self.__ORGANIZER_WSDL, transport=Transport(cache=self._cache, session=self._session))
        self._ows_factory = self._ows_client.type_factory('ns0')
        self._cs_client = Client(self.__COMMON_WSDL, transport=Transport(cache=self._cache, session=self._session))
        self._cs_factory = self._cs_client.type_factory('ns0')
        self._authenticate([self._cs_client, self._ows_client])
        self._message_types = self.get_common_data('getMessageTypeList')

    def _authenticate(self, clients):
        """Used to authenticate clients with the FEI WS.

        """
        auth_client = Client(self.__AUTH_WSDL, transport=Transport(cache=self._cache, session=self._session))
        if not self._username or not self._username:
            raise Exception("Could not login: username and password are empty. "
                            "Please provide a username and password to init or "
                            "set the username and password in the settings "
                            "file.")
        auth_login = auth_client.service.Login(self._username, self._password)
        if auth_login['ErrorCode'] != 'NoError':
            #TODO create own Exception class for these kind of exceptions.
            raise Exception('Could not login: %s' % auth_login['ErrorCode'])
        for client in clients:
            client.set_default_soapheaders({'AuthHeader': self._cs_factory.AuthHeader(UserName=self._username, Language='en')})

    def _handle_messages(self, result):
        """Generic message handler, used to determine if an exception needs to
        be thrown.

        """
        #TODO How to feedback warnings back to the user?
        if not result['body']['Messages']:
            return
        warnings = ''    
        for message in result['body']['Messages'].Message:
            msg = filter(lambda x: x.Id == message.UID,
                         self._message_types.body.getMessageTypeListResult.MessageType)[0]
            description = ('%s: %s\nDetails: %s' %
                           (msg.Id, msg.Description, message.Detail))
            if msg.IsCritical or msg.IsError:
                raise Exception(description)
            warnings += '%s\n' % description
        if warnings:
            print warnings

    def get_common_data(self, method, **kwargs):
        """Generic method for retrieving data from the common data web service.

        Params:
            method: The name of the common data WS method you want to use.
            **kwargs: Contains the keyword arguments you want to pass to the
                method you are calling.

        Return value: The raw result from the Common Data WS.

        """
        if not kwargs and method in self._common_data:
            return self._common_data[method]
        result = getattr(self._cs_client.service, method)(**kwargs)
        self._common_data['method'] = result
        return result
