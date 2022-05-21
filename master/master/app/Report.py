#import time
#import datetime as dt
import copy

class Timestamp:

    def __init__(   self,
                    timestamp:str,
                    ok:int,
                    nok:int,
                ):
        err = 'Error: Timestamp: __init__: '
        # timestamp
        if isinstance(timestamp,str):
            # "01:12:46"
            if timestamp.count(':') == 2:
                tmp = timestamp.split(':')
                for num in tmp:
                    if not num.isdigit():
                        raise Exception(err + "'timestamp' is 'str' but don't math patern '01:12:46'.")
                
                if 0 <= int(tmp[0]) <= 23 and 0 <= int(tmp[1]) <= 59 and 0 <= int(tmp[2]) <= 59:        
                    # simple check        
                    self.timestamp = self._to_10( timestamp )
                else: 
                    raise Exception(err + "'timestamp' is 'str' but don't math patern '01:12:46'.")
            else:
                raise Exception(err + "'timestamp' is 'str' but don't math patern '01:12:46'.")
        else:
            raise Exception(err + "'timestamp' is not 'str'.")
        # nok
        if isinstance(nok,int):
            if   0 <= nok <= 5000:
                self.nok = nok
            else:
                raise Exception(err + f"'nok' is out of diapazone 0 <= {nok} <= 5000.")
        else:
            raise Exception(err + "'nok' is not 'str'.")
        
        # ok
        if isinstance(ok,int):
            if   0 <= ok <= 5000:
                self.ok = ok
            else:
                raise Exception(err + f"'ok' is out of diapazone 0 <= {ok} <= 5000.")
        else:
            raise Exception(err + "'ok' is not 'str'.")
    def simple(self):
        return (self.timestamp, self.ok, self.nok )
    
    def _to_10(self,t):
        return  t[:-1] + '0'
    def __eq__(self,other):
        return self.timestamp == other.timestamp
    def __str__(self):
        return f"\ntimestamp: {self.timestamp} \tok: {self.ok} \tnok: {self.nok}."
    def __add__(self,other):
        err = "Error: Timestamp: __add__: "
        if self.timestamp == other.timestamp:
            return Timestamp(self.timestamp, self.ok+other.ok, self.nok+other.nok)
        else:
            Exception(err + "can't add them. a.timestamp != b.timestamp ." )
class Timereport:
    def __init__(self, name:str='None', l_timestamps:list[Timestamp]=[]):
        err = 'Error: Timereport: __init__:  '
        # 'name'
        # 'l_timestamps' 
        #
        if isinstance(name,str):
            self.name = name
        else:
            raise Exception(err + "'name' isn't 'str'.")
        for t in l_timestamps:
            if not isinstance(t,Timestamp):
                Exception(err + "'timestamp' in 'l_timestamps' ins't type of 'Timestamp'.")
        self.l_timestamps = l_timestamps

    def add_timestamp(self, timestamp):
        for t in range( len(self.l_timestamps) ):
            if  timestamp in self.l_timestamps:
                self.l_timestamps[t] = self.l_timestamps[t] + timestamp
                print(t)
            else:
                self.l_timestamps.append( timestamp )
    def __eq__(self,other):
        return self.name == other.name

    def __str__(self):
        resa = f' name: {self.name} '
        for i in self.l_timestamps:
            resa+= str(i)
        return resa 
    def __add__(self,other):
        err = "Error: Timereport: __add__: " 
        if self == other:
            tmp = Timereport(self.name, copy.copy(self.l_timestamps) )
            if not self.l_timestamps and not other.l_timestamps:
                raise Exception(err+"a.l_timestamps and b.l_timestamps both is empty.")
            elif not self.l_timestamps:
                raise Exception(err + 'a.l_timestamps is empty.')
            elif not other.l_timestamps:
                raise Exception(err+'b.l_timestamps is empty.')
            for i in range(len( self.l_timestamps )):
                for j in range(len( other.l_timestamps )):
                    if self.l_timestamps[i] == other.l_timestamps[j]:
                        tmp.l_timestamps[i] = other.l_timestamps[j] + self.l_timestamps[i]
            return tmp
        else:
            raise Exception( err + "'name' isn't equal. a.name != b.name .")


    def simple(self):
        resault = {}
        resault['name'] = self.name
        tmp = []
        for timestamp in self.l_timestamps:
            tmp.append( timestamp.simple() )

        resault['timestamps'] = tmp
        return resault
        
    def put(self,block):
        self.name = block['name']
        tmp = block['timestamps']
        self.l_timestamps = []
        for item in tmp:
            self.l_timestamps.append(Timestamp(item[0],item[1],item[2]))
    

