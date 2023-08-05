# -*- coding: utf-8 -*-
'''
'''

from faker.providers import BaseProvider
from collections import OrderedDict


class DataProvider(BaseProvider):
    '''
    '''
    account_name_labels = [
        '401(K)',
        'Business Account',
        'College Fund',
        'Custodial Account',
        'Emergency Expenses',
        'Family Trust',
        'Flexible Spending',
        'Health Savings',
        'Healthcare Fund',
        'House Money',
        'IRA-SEP',
        'Individual Account',
        'Joint Account',
        'New Car',
        'Non-Taxable Trust',
        'Pension Account',
        'Play Money',
        'Retirement Fund',
        'Rollover IRA',
        'Roth 401(K)',
        'Roth IRA',
        'Savings Account',
        'Traditional IRA',
        'Vacation Account'
    ]

    exchange_names = {
        'AMEX':   0.25,
        'NASDAQ': 0.25,
        'NYSE':   0.25,
        'PCX':    0.25
    }

    exchange_ids = {
        'AMEX':   'EX00000001',
        'NASDAQ': 'EX00000002',
        'NYSE':   'EX00000003',
        'PCX':    'EX00000004'
    }

    issue_names = {
        'COMMON': 0.90,
        'PREF_A': 0.01,
        'PREF_B': 0.02,
        'PREF_C': 0.03,
        'PREF_D': 0.05,
    }

    symbol_formats = {
        '?':     0.01,
        '??':    0.01,
        '???':   0.22,
        '????':  0.75,
        '?????': 0.01,
    }

    symbol_letters = 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

    tax_id_formats = {
        '##-#######':  0.5,
        '###-##-####': 0.5
    }

    trading_tiers = {
        'A': .20,
        'B': .60,
        'C': .20,
    }

    accounts_per_tier = {
        'A': range(1,4),
        'B': range(2,8),
        'C': range(5,10)
    }


    def tax_id(self):
        '''A US tax identfier in either EIN or SSN format.
        '''
        tax_id_fmt = self.random_element(self.tax_id_formats)
        return self.numerify(tax_id_fmt)

    def identifier(self, prefix=None, count=16):
        '''A string numeric identifier with optional prefix.
        '''
        digit = '#'
        prefix = (prefix or '')
        return self.numerify(f'{prefix}{digit * count}')

    def trading_tier(self):
        '''A customer's trading tier.
        '''
        return self.random_element(self.trading_tiers)

    def gendered_name_tuple(self, gender=None):
        '''Returns a tuple: (gender, first, middle, last)
        '''
        gender = (gender or self.random_element({'F': 0.5, 'M': 0.5}))
        if gender == 'F':
            f, m, l = (self.generator.first_name_female(),
                       self.generator.first_name_female(),
                       self.generator.last_name_female())
        else:
            f, m, l = (self.generator.first_name_male(),
                       self.generator.first_name_male(),
                       self.generator.last_name_male())
        return (gender, f, m, l)

    def customer(self, customer_id=None):
        '''A customer record in an OrderedDict.
        '''
        customer_id = (customer_id or self.identifier())
        gender, f_name, m_name, l_name = self.gendered_name_tuple()
        return OrderedDict([
            ('C_ID',        customer_id),
            ('C_TAX_ID',    self.tax_id()),
            ('C_ST_ID',     self.identifier(prefix='ST')),
            ('C_L_NAME',    l_name),
            ('C_F_NAME',    f_name),
            ('C_M_NAME',    m_name),
            ('C_GENDER',    gender),
            ('C_TIER',      self.trading_tier()),
            ('C_DOB',       self.generator.past_date().isoformat()),
            ('C_AD_ID',     self.generator.address()),
            ('C_COUNTRY_1', self.numerify('+!')),
            ('C_AREA_1',    self.numerify('###')),
            ('C_LOCAL_1',   self.numerify('###-####')),
            ('C_EXT_1',     self.numerify('####')),
            ('C_COUNTRY_2', self.numerify('+#')),
            ('C_AREA_2',    self.numerify('###')),
            ('C_LOCAL_2',   self.numerify('###-####')),
            ('C_EXT_2',     self.numerify('####')),
            ('C_COUNTRY_3', self.numerify('+#')),
            ('C_AREA_3',    self.numerify('###')),
            ('C_LOCAL_3',   self.numerify('###-####')),
            ('C_EXT_3',     self.numerify('####')),
            ('C_EMAIL_1',   self.generator.email()),
            ('C_EMAIL_2',   self.generator.email()),
        ])

    def customer_account_name(self, customer=None):
        '''A customer account name string.
        '''
        customer = (customer or self.customer())
        label = self.random_element(self.account_name_labels)
        return ' '.join([customer['C_F_NAME'],
                         customer['C_L_NAME'],
                         label])

    def cash(self):
        '''A positive floating point number with a two digit mantissa.
        '''
        return self.generator.pyfloat(right_digits=2, positive=True)

    def customer_accounts(self, customer=None, min=1, max=8):
        '''A list of customer account OrderedDicts.
        '''
        customer = (customer or self.customer())
        tier = customer['C_TIER']
        n = self.random_int(min=self.accounts_per_tier[tier].start,
                            max=self.accounts_per_tier[tier].stop)
        return [self.customer_account(customer) for _ in range(n)]

    def customer_account(self, customer=None, min=1, max=20):
        '''A customer account record in an OrderedDict.
        '''
        customer = (customer or self.customer())
        
        return OrderedDict([
            ('CA_C_ID',   customer['C_ID']),
            ('CA_ID',     self.identifier(prefix='CA')),
            ('CA_TAX_ID', customer['C_TAX_ID']),
            ('CA_B_ID',   self.identifier(prefix='B')),
            ('CA_NAME',   self.customer_account_name(customer=customer)),
            ('CA_BAL',    self.cash()),
            ('CA_L_NAME', customer['C_L_NAME']),
            ('CA_F_NAME', customer['C_F_NAME']),
            ('CA_M_NAME', customer['C_M_NAME']),
        ])

    def symbol(self):
        '''A company ticker symbol.
        '''
        fmt = self.random_element(self.symbol_formats)
        return self.lexify(text=fmt, letters=self.symbol_letters)


    def exchange(self):
        '''A stock exchange record in an OrderedDict.
        '''
        name = self.random_element(self.exchange_names)
        exid = self.exchange_ids[name]
        return OrderedDict([
            ('EX_ID',          exid),
            ('EX_NAME',        name),
            ('EX_NUM_SYMBOLS', 0),
            ('EX_OPEN',        self.generator.past_datetime().isoformat()),
            ('EX_CLOSE',       self.generator.past_datetime().isoformat()),
            ('EX_DESC',        self.generator.catch_phrase()),
            ('EX_AD_ID',       self.generator.address()),
        ])

    def issue(self):
        '''An security issue type.
        '''
        return self.random_element(self.issue_names)

    def dividend(self):
        '''A positive floating point number ##.##
        '''
        return self.generator.pyfloat(right_digits=2,
                                      left_digits=2,
                                      positive=True)

    def securities(self, company, min=1, max=20):
        '''A list of Security OrderedDicts.
        '''
        securities = []
        n_securities = self.random_int(min=min, max=max)
        for _ in range(n_securities):
            securities.append(self.security(company))
        return securities

    def security(self, company):
        '''A company security record in an OrderedDict.

        company: A Company OrderedDict.
        '''
        return OrderedDict([
            ('S_SYMBOL',         company['CO_SYMBOL']),
            ('S_ISSUE',          self.issue()),
            ('S_ST_ID',          self.identifier(prefix='ST')),
            ('S_NAME',           company['CO_NAME']),
            ('S_EX_ID',          company['CO_EX_ID']),
            ('S_CO_ID',          self.identifier(prefix='CO')),
            ('S_NUM_OUT',        0),
            ('S_START_DATE',     self.generator.past_date().isoformat()),
            ('S_EXCH_DATE',      self.generator.past_date().isoformat()),
            ('S_PE',             self.cash()),
            ('S_52WK_HIGH',      self.cash()),
            ('S_52WK_HIGH_DATE', self.generator.past_datetime().isoformat()),
            ('S_52WK_LOW',       self.cash()),
            ('S_52WK_LOW_DATE',  self.generator.past_datetime().isoformat()),
            ('S_DIVIDEND',       self.dividend()),
            ('S_YIELD',          self.cash()),
        ])

    def holdings(self, account, securities, min=1, max=20):
        '''A list of Holding OrderedDicts.
        '''
        
        n_holdings = self.random_int(min=min,
                                     max=max)

        symbols = [s['S_SYMBOL'] for s in securities]
        
        self.generator.random.shuffle(symbols)
        
        return [self.holding(account, symbol)
                for symbol in symbols[:n_holdings]]

    def holding(self, account, symbol):
        '''An account holding record in an OrderedDict.

        account:    customer_account OrderedDict

        '''
        
        return OrderedDict([
            ('H_T_ID',     self.identifier(prefix='T')),
            ('H_CA_ID',    account['CA_ID']),
            ('H_S_SYMBOL', symbol),
            ('H_DTS',      self.generator.past_datetime().isoformat()),
            ('H_PRICE',    self.cash()),
            ('H_QUANTITY', self.random_int(min=1)),
        ])

    def last_trade(self, securities):
        '''A last trade record in an OrderedDict
        '''
        security = self.random_element(securities)
        return OrderedDict([
            ('LT_S_SYMBOL',   security['S_SYMBOL']),
            ('LT_DTS',        self.generator.past_datetime().isoformat()),
            ('LT_PRICE',      self.cash()),
            ('LT_OPEN_PRICE', self.cash()),
            ('LT_VOL',        self.random_int(min=1)),
        ])


    def Company(self, exchanges=None):
        '''A Company record in a OrderedDict.
        '''
        if exchanges:
            exchange = self.random_element(exchanges)
        else:
            exchange = self.exchange()
            
        return OrderedDict([
            ('CO_ID', self.identifier(prefix='CO_')),
            ('CO_NAME', self.generator.company()),
            ('CO_SYMBOL', self.symbol()),
            ('CO_EX_ID', exchange['EX_ID']),
            ('CO_EX_NAME', exchange['EX_NAME']),
        ])
