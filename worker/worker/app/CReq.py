#from worker.app.WReq import WRequest
#from worker.variables import *

class CRequest:
    def __init__(self,
                name:str,   #mandatory
                salt:str,   #mandatory
                expected_status_code: int,#req['expected_status_code'],           mandatory!!!
                posible_status_code:list[int]=None,#req["posible_status_code"],#list   optional
                expected_text:str=None, # req["expected_text"],                        optional
                expected_headers: dict[str]=None,#req["expected_headers"],             optional
            ):
               self.name                 = name
               self.salt                 = salt
               self.posible_status_code  = posible_status_code
               self.expected_status_code = expected_status_code
               self.expected_text        = expected_text
               self.expected_headers     = expected_headers

