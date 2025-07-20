from enum import Enum, unique


@unique
class ExceptionType(Enum):
    API = "API Exception"
    ARGUMENT = "INVALID_ARGUMENT"
    DB_INSERTION = "DB Insertion Failure"
    DB_DUPLICACY = "Duplicate Entity"
    REQUEST_BODY = "Request Body Error"
    REQUEST_HEADER = "Request Header Error"
    REQUIRED_FIELD = "Required Field Error"
    DATABASE_TIMEOUT = "DB Timed Out"
    INVALID_DB_OPERATION = "Unsupported DB Operation"
    DB_CLOSED = "DB Connection Closed"
    DB = "DB Exceptions"
    DB_OPERATION_FAILED = "DB Operation Failure"
    COLLECTION_INVALID = "Invalid Collection Chosen"
    DB_CONNECTION_FAILURE = "DB Connection Error"
    DUPLICATE_KEY_ERROR = "Found Duplicate Key"
    EMAIL_VALIDATION = "Email Validation Exception"
    PHONE_VALIDATION = "Phone Number Validation Exception"
    NOT_FOUND = "Not Found Exception"
    TOKEN_INVALID = "Invalid Token"
    TOKEN_EXPIRED = "Token Expired"
    TOKEN_MISSING = "Token Missing"
    TOKEN_ERROR = "Token Error"
    REFRESH_TOKEN_ERROR = "Refresh Token Error"
    ACCESS_DENIED_ERROR = "Access Denied Error"
    SUCCESS = "Success"


@unique
class StatusCode(Enum):
    intial_setup_pending = 428


@unique
class DefaultRoles(Enum):
    SUPER_ADMIN = "super_admin"
    ADMIN = "admin"
    MANAGER = "manager"
    USER = "user"


@unique
class CountryCode(Enum):
    INDIA = "IN"
    USA = "US"
    UK = "GB"
    CANADA = "CA"
    AUSTRALIA = "AU"
    GERMANY = "DE"
    FRANCE = "FR"
    JAPAN = "JP"
    BRAZIL = "BR"
    SOUTH_AFRICA = "ZA"


@unique
class CountryTimezone(Enum):
    INDIA = "Asia/Kolkata"
    USA = "America/New_York"
    UK = "Europe/London"
    CANADA = "America/Toronto"
    AUSTRALIA = "Australia/Sydney"
    GERMANY = "Europe/Berlin"
    FRANCE = "Europe/Paris"
    JAPAN = "Asia/Tokyo"
    BRAZIL = "America/Sao_Paulo"
    SOUTH_AFRICA = "Africa/Johannesburg"


@unique
class CountryDialCode(Enum):
    INDIA = "+91"
    USA = "+1"
    UK = "+44"
    CANADA = "+1"
    AUSTRALIA = "+61"
    GERMANY = "+49"
    FRANCE = "+33"
    JAPAN = "+81"
    BRAZIL = "+55"
    SOUTH_AFRICA = "+27"
