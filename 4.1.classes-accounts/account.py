from decimal import Decimal
from numbers import Number
from typing import Callable
from functools import wraps
# from datetime import datetime, timezone, timedelta

from tzone import TimeZone
from ledger import TransactionType, TransactionConfirmation

accounts_record = set()
class NonUniqueAccountError(Exception):
    """When the Account is initialized with existing account number"""
class TransactionDeclinedException(Exception):
    """When an account operation is not permitted and the transaction is aborted."""

class InsufficientCreditException(TransactionDeclinedException):
    """When a the transaction would bring account balance below zero."""

class InvalidAmountRequest(TransactionDeclinedException):
    """When the value passed as argument does not meet valid requirements.
    Like when trying to deposit a negative amount, that would represent a withrawal."""

def validate_amount_request(validate_func:Callable, amount:Number)->None:
    """Check is InvalidAmountRequest neeeds to be raised"""
    if not validate_func(amount):
        raise InvalidAmountRequest(
            f"Requested amount value {amount} is not valid.\n"
            + f"Amount value failed validation test by: {validate_func.__name__}."
        )

def validate_positive_amount(amount:Number)->None:
    return validate_amount_request(lambda x: x>=0, amount)

def returning_confirmation(transaction_type:TransactionType)->str:
    def decorator(func:Callable)->Callable:
        @wraps(func)
        def decorated(self, *args, **kwargs)->str:
            try:
                func(*args, **kwargs)
                return self.confirm_transaction(transaction_type)
            except TransactionDeclinedException:
                return self.confirm_transaction(TransactionType.X)
        return decorated
    return decorator

class Account:
    """Account are uniquely identified by an account number,
    they are owned by a holder with first and last name, they have a preferred time zone.
    Account balance is not allowed to drop below zero."""
    preferred_tz = TimeZone()
    monthly_interest_rate = Decimal(0.001)
    
    def __init__(self, account_no:str, first_name:str, last_name:str,
            init_balance:Decimal = Decimal(0), preferred_tz: TimeZone = None,
        )->None:
        if account_no in accounts_record:
            raise NonUniqueAccountError(f"Account number {account_no} already exists")
        self.account_no = account_no
        self.first_name = first_name
        self.last_name = last_name
        try:
            validate_positive_amount(init_balance)
            self._balance = init_balance
        except InvalidAmountRequest:
            self._balance = Decimal(0)
        if preferred_tz is not None:
            self.preferred_tz = preferred_tz
    
    def __repr__(self):
        return (f"Account({self.account_no}, {self.first_name}, {self.last_name}, "
            + f"{self.balance}, {self.preferred_tz})")
    
    @property
    def full_name(self):
        return ' '.join(
            (self.first_name, self.last_name,)
        )
    
    @property
    def balance(self)->Decimal:
        return self._balance
    
    def confirm_transaction(self, transaction_type:TransactionType)->str:
        return TransactionConfirmation.generate(
            self.account_no,
            transaction_type,
            self.preferred_tz
        ).encode()
    
    @returning_confirmation(TransactionType.D)
    def deposit(self, amount:Decimal)->None:
        validate_positive_amount(amount)
        self._balance += Decimal(amount)
    
    @returning_confirmation(TransactionType.W)
    def withdraw(self, amount:Decimal)->None:
        validate_positive_amount(amount)
        if self.balance < amount:
            raise InsufficientCreditException(
                f"Transaction Declined because of insufficient credit."
                +f"\nAttempted withdrawal: {amount}"
                +f"\nCurrent credit: {self.balance}"
            )
        else:
            self._balance -= Decimal(amount)
    
    @classmethod
    def calc_monthly_interest(cls, balance:Decimal)->Decimal:
        return cls.monthly_interest_rate * balance
    
    @returning_confirmation(TransactionType.I)
    def pay_monthly_interest(self)->None:
        self._balance += self.calc_monthly_interest(self.balance)