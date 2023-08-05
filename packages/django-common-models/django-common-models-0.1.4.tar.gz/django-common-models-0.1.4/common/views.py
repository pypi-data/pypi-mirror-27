# coding: utf-8
from rest_framework.throttling import UserRateThrottle


class ThrottledView(object):

    throttle_classes = (UserRateThrottle,)
