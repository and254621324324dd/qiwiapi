import requests
import time

class qiwi_api:
    def __init__(self, api_access_token: str):
        self.api_access_token = api_access_token

    def get_profile(self):
        s = requests.Session()
        s.headers['Accept']= 'application/json'
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        p = s.get('https://edge.qiwi.com/person-profile/v1/profile/current?authInfoEnabled=true&contractInfoEnabled=true&userInfoEnabled=true')
        return p.json()

    def get_identification(self):
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        res = s.get('https://edge.qiwi.com/identification/v1/persons/' + self.get_profile(self)['authInfo']['personId'] + '/identification')
        return res.json()

    def downgrade_identification(self):
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        payload = {'identificationLevel':'VERIFIED'}
        res = s.post('https://edge.qiwi.com/qw-ident-downgrade-api/v1/persons/' + self.get_profile(self)['authInfo']['personId'] + '/identification-downgrade/operations', params=payload)
        return res.json()

    def confirm_downgrade_identification(self, downgradeOperationId: str):
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        payload = {'identificationLevel':'VERIFIED'}
        res = s.post('https://edge.qiwi.com/qw-ident-downgrade-api/v1/persons/' + self.get_profile(self)['authInfo']['personId'] + '/identification-downgrade/operations/' + request_id + '/confirm', params=payload)
        return res.json()

    def limits(self, types: list):
        """TURNOVER - Month turnover
REFILL - Max summ on account
PAYMENTS_P2P - Month p2p transfers
PAYMENTS_PROVIDER_INTERNATIONALS - Transfers to foreign companies
PAYMENTS_PROVIDER_PAYOUT - Transfers to bank accounts and card, wallets of other systems
WITHDRAW_CASH - Cash withdraw per month
"""
        types = ['PAYMENTS_PROVIDER_INTERNATIONALS', 'PAYMENTS_PROVIDER_PAYOUT', 'WITHDRAW_CASH']
        s = requests.Session()
        s.headers['Accept']= 'application/json'
        s.headers['Content-Type']= 'application/json'
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        parameters = {}
        for i, type in enumerate(types):
            parameters['types[' + str(i) + ']'] = type
        b = s.get('https://edge.qiwi.com/qw-limits/v1/persons/' + self.get_profile(self)['authInfo']['personId'] + '/actual-limits', params = parameters)
        return b.json()

    def get_p2p_payment_count(self):
        s = requests.Session()
        s.headers['Accept']= 'application/json'
        s.headers['Content-Type']= 'application/json'
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        b = s.get('https://edge.qiwi.com/qw-limits/v1/persons/' + self.get_profile(self)['authInfo']['personId'] + '/p2p-payment-count-limit')
        return b.json()

    def get_restrictions(self):
        s7 = requests.Session()
        s7.headers['Accept']= 'application/json'
        s7.headers['authorization'] = 'Bearer ' + self.api_access_token
        p = s7.get('https://edge.qiwi.com/person-profile/v1/persons/' + self.get_profile(self)['authInfo']['personId'] + '/status/restrictions')
        return p.json()

    def payment_history_last(self, rows_num: int, sources: list = None, operation: str = "ALL", next_TxnId: int = None, next_TxnDate: str = None, startDate: str = None, endDate: str = None):
        """SOURCES (nothing = all):
QW_RUB - ruble account
QW_USD - dollar account
QW_EUR - euro account
CARD - linked and non-linked cards
MK - mobile operator"""
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        parameters = {'rows': rows_num,
                      'sources': sources,
                      'nextTxnId': next_TxnId,
                      'nextTxnDate': next_TxnDate,
                      'operation': operation,
                      'startDate': startDate,
                      'endDate': endDate}
        h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + self.get_profile(self)['authInfo']['personId'] + '/payments', params = parameters)
        return h.json()

    def payment_history_summ_dates(self, startDate: str, endDate: str, operation = 'ALL': str, sources = []: list):
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        parameters = {'startDate': startDate,
                      'endDate': endDate,
                      'operation': operation
                      'sources': sources}
        h = s.get('https://edge.qiwi.com/payment-history/v2/persons/' + self.get_profile(self)['authInfo']['personId'] + '/payments/total', params = parameters)
        return h.json()

    def payment_history_transaction(self, transaction_id: int, transaction_type: str):
        s = requests.Session()
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        parameters = {'type': transaction_type}
        h = s.get('https://edge.qiwi.com/payment-history/v1/transactions/'+transaction_id, params = parameters)
        return h.json()

    def payment_history_cheque_file(self, transaction_id: int, transaction_type: str, filename: str = 'PDF'):
        s = requests.Session()
        s.headers['Accept'] ='application/json'
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        parameters = {'type': transaction_type,'format': 'PDF'}
        h = s.get('https://edge.qiwi.com/payment-history/v1/transactions/'+transaction_id+'/cheque/file', params=parameters)
        h.status_code
        return h.content

    def payment_history_cheque_send(self, transaction_id: int, transaction_type: str, email: str):
        s = requests.Session()
        s.headers['content-type'] ='application/json'
        s.headers['Accept'] ='application/json'
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        postjson = {'email':email}
        h = s.post('https://edge.qiwi.com/payment-history/v1/transactions/' + transaction_id + '/cheque/send?type=' + transaction_type, json = postjson)
        return h.status_code

    def balance(self):
        s = requests.Session()
        s.headers['Accept']= 'application/json'
        s.headers['authorization'] = 'Bearer ' + self.api_access_token  
        b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' + self.get_profile(self)['authInfo']['personId'] + '/accounts')
        return b.json()

    def add_balance(self, alias: str):
        s = requests.Session()
        s.headers['Accept']= 'application/json'
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        payload = {'alias': alias}
        b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' + self.get_profile(self)['authInfo']['personId'] + '/accounts', params=payload)
        return b.json()

    def accounts(self):
        s = requests.Session()
        s.headers['Accept']= 'application/json'
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' + self.get_profile(self)['authInfo']['personId'] + '/accounts/offer')
        return b.json()

    def set_default_account(self, accountAlias: str, isDefault: bool):
        s = requests.Session()
        s.headers['Accept']= 'application/json'
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        payload = {'defaultAccount': isDefault}
        b = s.get('https://edge.qiwi.com/funding-sources/v2/persons/' + self.get_profile(self)['authInfo']['personId'] + '/accounts/' + accountAlias)
        return b.json()

    def send_p2p(self, to_qiwi: str, comment: str = '', summ: int, currency: str = '643'):
        """ISO_4217 currencies. Examples:
Russian ruble - 643
United States dollar - 840
Kazakhstani tenge - 398
"""
        s = requests.Session()
        s.headers = {'content-type': 'application/json'}
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        s.headers['User-Agent'] = 'Android v3.2.0 MKT'
        s.headers['Accept'] = 'application/json'
        postjson = {"id":"","sum":{"amount":"","currency":""},"paymentMethod":{"type":"Account","accountId":"643"}, "comment":"'+comment+'","fields":{"account":""}}
        postjson['id'] = str(int(time.time() * 1000))
        postjson['sum']['amount'] = sum_p2p
        postjson['sum']['currency'] = currency
        postjson['fields']['account'] = to_qiwi
        res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/99/payments',json = postjson)
        return res.json()

    def exchange(self, sum_exchange: int, currency: str, to_qw: str):
        """ISO_4217 currencies. Examples:
Russian ruble - 643
United States dollar - 840
Kazakhstani tenge - 398
"""
        s = requests.Session()
        currencies = ['398', '840', '978']
        if currency not in currencies:
            print('This currency not available')
            return
        s.headers = {'content-type': 'application/json'}
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        s.headers['User-Agent'] = 'Android v3.2.0 MKT'
        s.headers['Accept'] = 'application/json'
        postjson = {"id":"","sum":{"amount":"","currency":""},"paymentMethod":{"type":"Account","accountId":currency}, "comment":"'comment'","fields":{"account":""}}
        postjson['id'] = str(int(time.time() * 1000))
        postjson['sum']['amount'] = sum_exchange
        postjson['sum']['currency'] = currency
        postjson['fields']['account'] = to_qw
        res = s.post('https://edge.qiwi.com/sinap/api/v2/terms/1099/payments',json = postjson)
        return res.json()

    def exchange(self, currency_to: str, currency_from: str):
        """ISO_4217 currencies. Examples:
Russian ruble - 643
United States dollar - 840
Kazakhstani tenge - 398
"""
        s = requests.Session()
        s.headers = {'content-type': 'application/json'}
        s.headers['authorization'] = 'Bearer ' + self.api_access_token
        s.headers['User-Agent'] = 'Android v3.2.0 MKT'
        s.headers['Accept'] = 'application/json'
        res = s.get('https://edge.qiwi.com/sinap/crossRates')

        rates = res.json()['result']

        rate = [x for x in rates if x['from'] == currency_from and x['to'] == currency_to]
        if (len(rate) == 0):
            print('No rate for this currencies!')
            return
        else:
            return rate[0]['rate']
