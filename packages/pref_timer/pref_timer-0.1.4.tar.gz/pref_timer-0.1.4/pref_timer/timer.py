from __future__ import division
from __future__ import print_function
from __future__ import absolute_import
import time


def timer(func):
    '''
    :param func: function required
    :return: function execution time
    '''
    def check_timer(*args,**kwargs):
        before = time.time()
        pref_func = func(*args,**kwargs)
        after = time.time()
        print ("{} Taken: {:.2} Seconds".format(func.__name__, after-before))
        return pref_func
    return check_timer