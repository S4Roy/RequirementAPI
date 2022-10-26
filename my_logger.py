'''
******************************Please go through ReadMe.txt and main.py before run the project**********************************

This Module contains  Logger Implementation Function

'''


import logging
from functools import wraps


logging.basicConfig(filename=f"{__name__}.log", level=logging.INFO)


def my_logger(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        res = func(*args, **kwargs)
        msg='no msg'
        try:
            for item in res:
                if isinstance(item, dict) and item.get('msg'):
                    msg=item.get('msg')
                    break
        except:
            try:
                msg=res.status
            except:
                msg='No Msg!'
                
        logging.info(f"{func.__name__} Ran with args: {args} and kwargs: {kwargs}, msg: {msg}")
       
        
        return res
    return wrapper


