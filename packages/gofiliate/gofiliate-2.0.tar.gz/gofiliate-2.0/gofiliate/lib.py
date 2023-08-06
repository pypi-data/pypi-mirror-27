from enum import Enum
from datetime import date
from typing import Optional, NewType, List
import arrow


# Exceptions
class GofiliateException(Exception):
    pass


class GofiliateAuthException(GofiliateException):
    pass


class GofiliateDataException(GofiliateException):
    pass


# Enums
class Events(Enum):
    """
    Gofiliate Events enum.

    These are the events which the reporting endpoint returns.
    """
    GGR = "Gross Gaming Revenue"
    NRC = "NRC"
    NDC = "NDC"
    netrev = "Net Revenue"
    earnings = "Earnings"
    deposits = "Deposits"
    total_bets = "Total Bets"
    total_wins = "Total Wins"
    admin_fee = "Administraton Fee"


class AffiliateStatuses(Enum):
    ALLOWED = "ALLOWED"
    PENDING = "PENDING"
    DENIED = "DENIED"
    DELETED = "DELETED"


class ReportGroupId(Enum):
    """
    Controls how data is grouped in query. Use the value in queries (integer)

    -`NO_GROUPING` will return for all days in the query.
    -`DATE_AND_AFFILIATES` will return grouped by date and by each affiliate
    - `DATE` will group for each day in the period.
    """
    NO_GROUPING = 0
    DATE_AND_AFFILIATES = 2
    DATE = 1


# Functions
def short_date_to_date(short_date: str) -> date:
    """
    Returns a date object from a text short date in format YYYYMM
    :param short_date: String in format YYYYMM
    :return:
    """
    if len(short_date) != 6:
        raise ValueError('Expects a short data in format YYYYMM')
    year = int(short_date[0:4])
    month = int(short_date[4:6])
    try:
        date_obj = date(year=year, month=month, day=1)
    except ValueError as e:
        raise AttributeError(e.__str__())
    return date_obj


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


# noinspection PyBroadException
class Figures(object):
    def __init__(self
                 , data_dict: dict):
        try:
            self.date = short_date_to_date(data_dict.get('date', None))  # type: Optional[date]
        except Exception:
            self.date = None  # type: Optional[date]
        self.amount = float(data_dict.get('amount', None))  # type: float
        self.event_id = float(data_dict.get('amount', None))  # type: str
        self.event_name = data_dict.get('event_name', None)  # type: str


# Request Objects
class BaseRequest(object):
    def __init__(self
                 , start_date: date
                 , end_date: date):
        self.end_date = end_date.isoformat()
        self.start_date = start_date.isoformat()


class BaseWidgetReportRequest(BaseRequest):
    def __init__(self
                 , start_date: date, end_date: date, group_by: str = 'month',
                 sum_all: int = 0):
        """
        Object for Base Widget request.
        """
        super().__init__(start_date, end_date)
        self.group = group_by  # type: str
        self.sum = sum_all  # type: int


class StandardRequest(BaseRequest):
    def __init__(self
                 , start_date: date
                 , end_date: date
                 , brand_id: int = 1
                 , product_id: str = "#"
                 , sub_product_id: str = "#"
                 , group_id: ReportGroupId = ReportGroupId.DATE
                 , user_id: str = "#"):
        super().__init__(start_date, end_date)
        self.user_id = user_id
        self.group_id = group_id.value
        self.sub_product_id = sub_product_id
        self.product_id = product_id
        self.brand_id = brand_id


class AffiliateDetailsRequest(object):
    def __init__(self
                 , join_date_from: date
                 , status: AffiliateStatuses = AffiliateStatuses.ALLOWED):
        """
        Object for the Affiliate Details Request.
        :param join_date_from:
        :param status:
        """
        self.join_date = join_date_from.isoformat()
        self.status = status.name


class AffiliateDetails(object):
    def __init__(self, details_dict: dict):
        """
        Class for storing Affiliate Details, as returned by Gofiliate.

        :param details_dict: A dict of data as returned by Gofiliate.
        """
        self.username = details_dict.get("username", None)  # type: str
        self.email = details_dict.get("email", None)  # type: str
        self.first_name = details_dict.get("first_name", None)  # type: str
        self.last_name = details_dict.get("last_name", None)  # type: str
        self.dob = arrow.get(details_dict.get("dob", None)).date()  # type: date
        self.phone = details_dict.get("phone", None)  # type: str
        self.company_name = details_dict.get("company_name", None)  # type: str
        self.company_websites = details_dict.get("company_websites", None)  # type: str
        self.address1 = details_dict.get("address1", None)  # type: str
        self.address2 = details_dict.get("address2", None)  # type: str
        self.city = details_dict.get("city", None)  # type: str
        self.postcode = details_dict.get("postcode", None)  # type: str
        self.country = details_dict.get("country", None)  # type: str
        self.status = details_dict.get("status", None)  # type: str
        self.skype = details_dict.get("skype", None)  # type: str
        self.join_date = arrow.get(details_dict.get("join_date", None)).date()  # type: date


class ReportConfig(object):
    def __init__(self
                 , url: Optional[str]
                 , report_name: Optional[str] = None
                 , request_obj: Optional[object] = None
                 , data_obj: Optional[object] = None
                 , data_node: Optional[str] = 'stats'):
        """
        Storage of report configuration data.


        :param url: The URL to the report endpoint in the gofiliate API
        :param report_name: Optional name of the report.
        :param request_obj: The class used to define the request
        :param data_obj:  The class used to store each data item returned.
        :param data_node: The name of the node in the json object where data items are found.
        """
        self.data_node = data_node
        self.data_obj = data_obj
        self.request_obj = request_obj
        self.url = url
        self.report_name = report_name


class BaseData(object):
    def __init__(self, data_dict: dict):
        self.NRC = float(data_dict.get("NRC", None))  # type: float
        self.NDC = float(data_dict.get("NDC", None))  # type: float
        self.netrev = float(data_dict.get("netrev", None))  # type: float
        self.earnings = float(data_dict.get("earnings", None))  # type: float
        self.admin_fee = float(data_dict.get("admin_fee", None))  # type: float


class AffiliateEarningsData(BaseData):
    def __init__(self, data_dict: dict):
        super().__init__(data_dict)
        self.month = data_dict.get("month", None)  # type: str


class BreakdownData(BaseData):
    def __init__(self, data_dict: dict):
        super().__init__(data_dict)
        self.total_wins = float(data_dict.get("total_wins", 0))  # type: float
        self.total_bets = float(data_dict.get("total_bets", 0))  # type: float
        self.deposits = float(data_dict.get("deposits", 0))  # type: float
        self.withdrawals = float(data_dict.get("withdrawals", 0))  # type: float
        self.costs = float(data_dict.get("costs", 0))  # type: float


class BaseWidgetData(BreakdownData):
    def __init__(self, data_dict: dict):
        super().__init__(data_dict)
        self.date = data_dict.get("date", None)  # type: date
        self.period = self.date.isoformat()[0:7]  # type: str
        del self.costs


class DailyBreakDownData(BreakdownData):
    def __init__(self, data_dict: dict):
        super().__init__(data_dict)
        self.date = arrow.get(data_dict.get("date", None)).date()  # type: date


class MonthlyBreakDownData(BreakdownData):
    def __init__(self, data_dict: dict):
        super().__init__(data_dict)
        self.month = data_dict.get("month", None)  # type: str


class AffiliateNDCSData(object):
    def __init__(self, data_dict: dict):
        self.signup_date = arrow.get(data_dict.get("signup_date", None)).date()
        self.player_id = data_dict.get("player_id", None)
        self.player_name = data_dict.get("player_name", None)
        self.affiliate = data_dict.get("affiliate", None)
        self.brand = data_dict.get("brand", None)
        self.first_deposit_date = arrow.get(data_dict.get("first_deposit_date", None)).date()
        self.initial_deposit = float(data_dict.get("initial_deposit", None))
        self.total_deposits = float(data_dict.get("total_deposits", None))


class ReportConfigurations(Enum):
    """
    Used to configure each report available on the gofilliates API.

    In order to easily use the `GofiliateReportBase` class each report endpoint needs to
    be defined with a definition of the URL, request object (data sent in the POST request),
    the data object used to store the resulting data, and the data node, which is the property
    in the resulting JSON which holds the result data.
    """
    BASE_WIDGET = ReportConfig("{base}/admin/widgets/main"
                               , request_obj=BaseWidgetReportRequest
                               , data_obj=Figures
                               , data_node='figures')
    DAILY_BREAKDOWN = ReportConfig("{base}/admin/reports/daily-breakdown"
                                   , request_obj=StandardRequest
                                   , data_obj=DailyBreakDownData)
    MONTHLY_BREAKDOWN = ReportConfig("{base}/admin/reports/monthly-breakdown"
                                     , request_obj=StandardRequest
                                     , data_obj=MonthlyBreakDownData)
    AFFILIATE_EARNINGS = ReportConfig("{base}/admin/reports/affiliate-earnings"
                                      , request_obj=StandardRequest
                                      , data_obj=AffiliateEarningsData)
    AFFILIATE_NDCS = ReportConfig("{base}/admin/reports/affiliate-ndcs"
                                  , request_obj=StandardRequest
                                  , data_obj=AffiliateNDCSData)
    AFFILIATE_DETAILS = ReportConfig("{base}/admin/reports/affiliate-details"
                                     , request_obj=AffiliateDetailsRequest
                                     , data_obj=AffiliateDetails)


# Types
ListofFigures = NewType('ListofFigures', List[Figures])
