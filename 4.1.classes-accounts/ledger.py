from itertools import count
from datetime import datetime, timezone
from dataclasses import dataclass

from tzone import TimeZone
from enum import Enum

transactions_count = count()

class TransactionType(Enum):
    D = 'Deposit'
    W = 'Withdrawal'
    I = 'Interest'
    X = 'Declined'

CONFIRMCODE_TFORMAT = "%Y%m%d%H%M%S"

def encode_confirmcode_dtime(dtime:datetime)->str:
    return dtime.strftime(CONFIRMCODE_TFORMAT)

def decode_confirmcode_dtime(dtime:str)->datetime:
    return datetime\
        .strptime(dtime, CONFIRMCODE_TFORMAT)\
        .replace(tzinfo=timezone.utc)

# def generate_confirmation_code(account_no:str, transaction_type:TransactionType)->str:
#     """Create a record of transaction"""
#     return '-'.join((
#         transaction_type.name,
#         account_no,
#         encode_now_confirmcode(),
#         next(transactions_count)
#     ))

@dataclass
class TransactionConfirmation:
    account_no: str
    transaction_type: TransactionType
    transaction_id: int
    _dtime: datetime
    _tz: TimeZone = None
    
    @classmethod
    def generate(cls, account_no:str,
            transaction_type:TransactionType,
            tz:TimeZone=None
        )->TransactionConfirmation:
        return cls(
            account_no,
            transaction_type,
            next(transactions_count),
            datetime.now(timezone.utc),
            tz
        )
        
    def encode(self):
        return '-'.join(
            map(str,(
                self.transaction_type.name,
                self.account_no,
                encode_confirmcode_dtime(self._dtime),
                self.transaction_id
            ))
        )
    
    @classmethod
    def decode(cls, confirmation_code:str, tz:TimeZone=None)->TransactionConfirmation:
        (
            transaction_type_name,
            account_no,
            dtime_str,
            id_str
        ) = confirmation_code.split('-')
        transaction_type = next(
            ttype for ttype in TransactionType
            if ttype.name == transaction_type_name
        )
        dtime = decode_confirmcode_dtime(dtime_str)
        return cls(
            account_no,
            transaction_type,
            int(id_str),
            dtime,
            tz
        )
    
    @property
    def time(self):
        return (self._tz or TimeZone()).tell_time(self._dtime)
    
    @property
    def time_utc(self):
        return self._dtime.isoformat(sep='T')

def parse_confirmation(confirmation_code:str, tz:TimeZone=None)->TransactionConfirmation:
    (
        transaction_type_name,
        account_no,
        dtime_str,
        id_str
    ) = confirmation_code.split('-')
    transaction_type = next(
        ttype for ttype in TransactionType
        if ttype.name == transaction_type_name
    )
    dtime = decode_confirmcode_dtime(dtime_str)
    return TransactionConfirmation(
        account_no,
        transaction_type,
        int(id_str),
        dtime,
        tz
    )
    