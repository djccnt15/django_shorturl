from enum import StrEnum, auto


class UrlNameEnum(StrEnum):
    INDEX = auto()
    REGISTER = auto()
    LOGIN = auto()
    LOGOUT = auto()
    URL_LIST = auto()
    URL_CREATE = auto()
    URL_CHANGE = auto()
