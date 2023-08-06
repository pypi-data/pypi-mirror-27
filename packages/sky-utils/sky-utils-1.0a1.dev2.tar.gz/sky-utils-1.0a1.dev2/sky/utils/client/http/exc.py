# -*- coding: utf-8 -*-


class NotMasterURLError(Exception):
    """
    Raised in fail_over_strategy functions to notify
    FailOverHTTPClient to continue iterating over list of urls
    """