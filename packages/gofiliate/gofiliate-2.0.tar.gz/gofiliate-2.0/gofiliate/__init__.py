from requests import Session
import logging
from typing import Iterator, Generator
from datetime import date
from gofiliate.lib import short_date_to_date, Figures, ListofFigures \
    , GofiliateDataException, GofiliateException, GofiliateAuthException \
    , AffiliateData, BaseWidgetReportRequest, AffiliateDetailsRequest, AffiliateDetails \
    , DailyBreakDownData, StandardRequest, MonthlyBreakDownData, AffiliateEarningsData \
    , AffiliateNDCSData, ReportConfigurations, BaseRequest, BreakdownData, BaseWidgetData
import pandas
from typing import Optional, List, Dict, Iterator


class Gofiliate(object):
    """
     Base class for Gofiliate.

     Handles authentication and base URL retrieval mechanisms.

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
        Base class for Gofiliate.

        Handles authentication and base URL retrieval mechanisms.

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
    def _get_login_query_string(self) -> str:
        """Generates a login API path"""
        return '{base}/admin/login'.format(base=self.base_url)

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
        elif result_status == 200 and response.json().get('code', None) == 'FAILURE_CREDENTIAL_INVALID':
            message = 'Authentication Failed!'
            raise GofiliateAuthException(message)
        return response.json()

    def authenticate(self):
        """Authenticate to the API

        Stores the bearer_token in self for reuse in subsequent calls.
        """
        url = self._get_login_query_string  # type: str
        post_data = dict(username=self.username, password=self.password)
        response = self.send_request('POST', url, post_data)
        try:
            self.auth_token = response.get('bearer_token', None)  # type: str
            self.session.headers["Authorization"] = self.auth_token
            self.logger.info('Authorized successfully, received token {}'.format(self.auth_token))
        except Exception:
            message = 'Problem getting auth'
            raise GofiliateAuthException(message)


class GofiliateTokenDecoder(Gofiliate):
    def __init__(self, username: str, password: str, host: str, token: str) -> None:
        super().__init__(username, password, host)
        """
        Retrieves affiliate information for the passed token.
        
        The decoded token info is found in the affiliate_data property

        :param token_str: The guid-like token string to be decoded.
        """
        self.token = token

    @property
    def affiliate_data(self) -> Optional[AffiliateData]:
        url = self._get_decode_string
        post_data = dict(token=self.token)
        response = self.send_request('POST', url, post_data)
        try:
            return AffiliateData(response.get('stats'))  # type: Optional[AffiliateData]
        except Exception as e:
            self.logger.error(e)
            self.logger.error('Could not decode the sent token: {}'.format(self.token))
            return None

    @property
    def _get_decode_string(self) -> str:
        """Generates the decode API path"""
        return '{base}/admin/reports/token-analysis'.format(base=self.base_url)


class GofiliateReportBase(object):
    """
    Generates data reports from gofiliate endpoints.

    Takes a gofiliate client instance

    To choose the report to run, pass a ReportConfiguration ENUM choice.

    """

    def __init__(self
                 , gofiliate_client: Gofiliate
                 , report_config_enum: ReportConfigurations
                 , request_object: BaseRequest):

        self.client = gofiliate_client
        self.report_raw_data = list()  # type: ListofFigures
        self.report_config = report_config_enum  # type: ReportConfigurations
        # Check to ensure that the sent request_object is of the correct type:
        self.client.logger.debug("Sent request object is {}".format(type(request_object)))
        self.client.logger.debug("Required request object is {}".format(self.report_config.value.request_obj))
        try:
            assert type(request_object) == self.report_config.value.request_obj
        except AssertionError:
            raise GofiliateException('The sent request object'
                                     ' is of type {}, required type is {}'
                                     .format(type(request_object), self.report_config.value.request_obj))
        # Set up the REST call
        url = report_config_enum.value.url.format(base=gofiliate_client.base_url)
        # Transform the dates to text
        # Create The payload
        response = self.client.send_request('POST', url, request_object.__dict__)
        return_data = response
        if return_data.get("action", None) == "SUCCESS" and return_data.get("code", None) is True:
            self.client.logger.info('Successfully retrieved data.')
        else:
            self.client.logger.error("Unable to retrieve data")
            self.client.logger.error(response)
            raise GofiliateDataException("Unable to retrieve data.")

        # First Extract the raw response
        data_node = report_config_enum.value.data_node
        self.report_raw_data = return_data.get(data_node, list())  # type: list
        self.client.logger.info('Received {} items'.format(len(self.report_raw_data)))

    # noinspection PyTypeChecker
    @property
    def report_data(self) -> Generator[object, object, object]:
        if len(self.report_raw_data) == 0:
            self.client.logger.warning("No figures were returned from the query, check your query.")
            yield
        else:
            for figure in self.report_raw_data:
                try:
                    a_figure = self.report_config.value.data_obj(data_dict=figure)

                    yield a_figure
                except Exception as e:
                    self.client.logger.error('Could not parse a sent figure, will not  be included in list')
                    self.client.logger.error(e.__str__())
                    self.client.logger.error(a_figure)
                    yield None

    @property
    def report_data_dict(self) -> List[Dict]:
        """
        Returns an iteration of report_data as dicts.
        """
        for figure in self.report_data:
            yield figure.__dict__


class BaseWidgetReport(GofiliateReportBase):
    """
    Overview report, as seen on the landing page of the Gofiliate dashboard.

    Has extra types, since the data is easier to consume in pivoted form.
    """
    def __init__(self, gofiliate_client: Gofiliate, start_date: date, end_date: date):
        request_object = BaseWidgetReportRequest(start_date=start_date
                                                 , end_date=end_date)
        super().__init__(gofiliate_client, ReportConfigurations.BASE_WIDGET, request_object)

    @property
    def report_pivot(self) -> pandas.DataFrame:
        """
        Pivoted report data.

        As a pandas dataframe.
        :return:
        """
        columns = ['amount', 'date', 'event_id', 'event_name']
        df = pandas.DataFrame.from_records(self.report_data_dict, columns=columns)  # type: pandas.DataFrame
        df['date'] = pandas.to_datetime(df['date'])
        df.index = df['date']
        return df.pivot(index='date', columns='event_name',
                        values='amount')  # type: pandas.DataFrame

    @property
    def report_pivot_csv(self) -> str:
        """
        The pivoted data as CSV
        """
        return self.report_pivot.to_csv()

    @property
    def report_pivot_objects(self) -> Iterator[BaseWidgetData]:
        """
        Report pivoted data as a iterator of BaseWidgetData objects.

        One object per period.
        """
        for an_item in self.report_pivot.itertuples():
            data_dict = dict(
                date=an_item[0].to_pydatetime().date()
                , GGR=an_item[1]
                , NDC=an_item[2]
                , NRC=an_item[3]
                , admin_fee=an_item[4]
                , deposits=an_item[5]
                , earnings=an_item[6]
                , netrev=an_item[7]
                , total_bets=an_item[8]
                , total_wins=an_item[9]
                , withdrawals=an_item[10]
            )
            data_item = BaseWidgetData(data_dict=data_dict)
            yield data_item

    @property
    def report_pivot_dicts(self) -> Iterator[dict]:
        """
        Report pivoted data as a list of dicts, based on the BaseWidgetData class.

        One dict per period.
        """
        for an_item in self.report_pivot_objects:
            yield an_item.__dict__


class DailyBreakdownReport(GofiliateReportBase):
    """
    Daily grouped report of key stats for the entire instance.
    """

    def __init__(self, gofiliate_client: Gofiliate, start_date: date, end_date: date):
        request_object = StandardRequest(start_date=start_date, end_date=end_date)
        super().__init__(gofiliate_client, ReportConfigurations.DAILY_BREAKDOWN, request_object)


class MonthlyBreakdownReport(GofiliateReportBase):
    """
    Monthly grouped report of key stats for the entire instance.
    """

    def __init__(self, gofiliate_client: Gofiliate, start_date: date, end_date: date):
        request_object = StandardRequest(start_date=start_date, end_date=end_date)
        super().__init__(gofiliate_client, ReportConfigurations.MONTHLY_BREAKDOWN, request_object)
