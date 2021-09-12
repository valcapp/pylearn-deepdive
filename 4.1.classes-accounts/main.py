from account import Account
from tzone import TimeZone
from ledger import TransactionConfirmation

def make_transaction(account, method, amount=None):
    confirmation = getattr(account, method)(account) if amount is None\
        else getattr(account, method)(account, amount)
    print(f"\n{method.capitalize()} {amount is not None and amount or ''}: {confirmation}")
    print(f"New balance: {account.balance:.2f}")
    return confirmation

def decode_transaction(code,tz):
    trans = TransactionConfirmation.decode(code,tz)
    attrs = ('account_no', 'transaction_type', 'transaction_id', 'time_utc', 'time',)
    print(
        '\n'.join(
            f'transaction.{attr}: {getattr(trans,attr)}'
            for attr in attrs
        )
    )
    return trans

def make_check_transaction(account, method, amount=None):
    confirmation = make_transaction(account, method, amount)
    decode_transaction(confirmation, account.preferred_tz)

if __name__ == '__main__':
    mytz = TimeZone(3,30,'ABC')
    account = Account('123456','Robin','Hood',1000, mytz)
    
    print(account)
    print('Full name: ',account.full_name)
    print('Initial Balance: ', account.balance)
    
    make_check_transaction(account, 'deposit', 500)
    make_check_transaction(account, 'withdraw', 700)
    make_check_transaction(account, 'withdraw', 2000)
    make_check_transaction(account, 'pay_monthly_interest')