from requests import Session
import logging


class GofiliateException(Exception):
    pass


class GofiliateAuthException(GofiliateException):
    pass


class AffiliateData(object):
    """
            Stores affiliate date returned from Gofilliate.

            Will be expanded as more data is available.

            :param stats_dict: The dict as returned by the gofilliates api.
            """

    def __init__(self, stats_dict: dict) -> None:
        #: the email of the affiliate user
        self.email = stats_dict.get('email', None)  # type: str
        #: The user_id of affiliate user
        self.user_id = stats_dict.get('user_id', None)  # type: str
        #: The username of the affiliate user
        self.username = stats_dict.get('username', None)  # type:str


class Gofiliate(object):
    """
     Class for authenticating and decoding goaffiliate data.

     :param username: The gofilates admin username assigned to your account
     :param password: The gofilates admin password assigned to your account
     :param host: The gofilliates hostname for your account
     :param port: http port (default 443)
     :param retries: number of retries when auth fails.
     :param timeout: How long in seconds to wait for a response from Gofilliate
    """

    def __init__(self
                 , username: str
                 , password: str
                 , host: str
                 , port: int = None
                 , retries: int = 3
                 , timeout: int = 10) -> None:
        """
        Class for authenticating and decoding goaffiliate data.

        :param username: The gofilates admin username assigned to your account
        :param password: The gofilates admin password assigned to your account
        :param host: The gofilliates hostname for your account
        :param port: http port (default 443)
        :param retries: number of retries when auth fails.
        :param timeout: How long in seconds to wait for a response from Gofilliate
        """
        self.username = username  # type: str
        self.password = password  # type: str
        self.host = host  # type: str
        self.port = port or 443  # type: int
        self.retries = retries  # type: int
        self.timeout = timeout  # type: int
        self.auth_token = None  # type: str

        self.base_url = None  # type: int
        self.setup_base_url()  # type: str
        self.session = Session()  # type: Session

        self.session.headers.update({'Accept': 'application/json'})
        self.logger = logging.getLogger('gofilliate')
        self.logger.setLevel('INFO')

        self.authenticate()

    def setup_base_url(self):
        template = 'https://{host}:{port}'
        if self.port == 443:
            template = 'https://{host}'

        if '://' in self.host:
            self.host = self.host.split('://')[1]

        self.base_url = template.format(
            host=self.host.strip('/'),
            port=self.port)  # type: str

    @property
    def get_login_query_string(self) -> str:
        """Generates a login API path"""
        return '{base}/admin/login'.format(base=self.base_url)

    @property
    def get_decode_string(self) -> str:
        """Generates the decode API path"""
        return '{base}/admin/reports/token-analysis'.format(base=self.base_url)

    def send_request(self, method: str, url: str, data: dict) -> dict:
        """Dispatches the request and returns a response"""

        try:
            response = self.session.request(method, url=url, data=data, timeout=self.timeout)
        except Exception as e:
            # Raise exception alerting user that the system might be
            # experiencing an outage and refer them to system status page.
            message = '''Failed to receive valid reponse after {count} retries.
                Last caught exception -- {klass}: {message}
            '''.format(klass=type(e), message=e, count=self.retries)
            raise GofiliateAuthException(message)

        result_status = response.status_code
        if result_status != 200:
            raise GofiliateException('%s: %s %s' % (result_status, url, data))
        elif result_status == 200 and response.json().get('code', None) == 'FAILURE_CREDENTIAL_INVALID' :
            message = 'Authentication Failed!'
            raise GofiliateAuthException(message)
        return response.json()

    def authenticate(self):
        """Authenticate to the API

        Stores the bearer_token in self for reuse in subsequent calls.
        """
        url = self.get_login_query_string  # type: str
        post_data = dict(username=self.username, password=self.password)
        response = self.send_request('POST', url, post_data)
        try:
            self.auth_token = response.get('bearer_token', None)  # type: str
            self.session.headers["Authorization"] = self.auth_token
            self.logger.info('Authorized successfully, received token {}'.format(self.auth_token))
        except Exception:
            message = 'Problem getting auth'
            raise GofiliateAuthException(message)

    def decode_token(self, token_str: str) -> AffiliateData:
        """
        Returns affiliate information for the provided token.

        :param token_str: The guid-like token string to be decoded.
        :return:
        """
        url = self.get_decode_string
        post_data = dict(token=token_str)
        response = self.send_request('POST', url, post_data)
        try:
            return_data = AffiliateData(response.get('stats'))
        except Exception as e:
            self.logger.error(e)
            self.logger.error('Could not decode the sent token: {}'.format(token_str))
            raise GofiliateException('Could not decode the sent token. {}'.format(token_str))
        return return_data
