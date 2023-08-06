class CurrencyImpl(object):
    def __init__(self, name, sign):
        self.name = name
        self.sign = sign


class Currency(object):
    EUR = CurrencyImpl('EUR', u'\u20ac')
    NONE = CurrencyImpl('', u'')

    all = [EUR]

    @staticmethod
    def for_name(name):
        for currency in Currency.all:
            if currency.name == name:
                return currency
        return Currency.NONE


class Contractor(object):
    def __init__(self, data):
        self.name = data['name']
        self.address = data['address']
        self.ico = data['ico']
        self.dic = data['dic']
        self.icdph = data['icdph']
        self.phone = data['phone']
        self.email = data['email']
        self.signature = data['signature']


class Client(object):
    def __init__(self, data):
        self.name = data['name']
        self.address = data['address']
        self.ico = data['ico']
        self.dic = data['dic']
        self.icdph = data['icdph']

    def is_foreign(self):
        return self.address[len(self.address) - 1] != 'Slovensko'


class BankAccount(object):
    def __init__(self, data):
        self.iban = data['iban']
        self.swift = data['swift']


class Item(object):
    def __init__(self, data):
        self.name = data['name']
        self.amount = float(data['amount'])
        self.unit = data.get('unit', '')
        self.price = float(data['price'])

    def total(self):
        return self.amount * self.price


class Document(object):
    def __init__(self, data):
        self.number = data['number']
        self.due_date = data['due_date']
        self.issue_date = data['issue_date']
        self.delivery_date = data['delivery_date']
        self.currency = Currency.for_name(data['currency'])
        self.discount = data.get('discount', 0)

        self.contractor = Contractor(data['contractor'])
        self.client = Client(data['client'])
        self.bank_account = BankAccount(data['bank_account'])
        self.items = []
        items_data = data.get('items', [])
        for item_data in items_data:
            self.items.append(Item(item_data))

    def total(self):
        return self._item_total() - self.discount

    def _item_total(self):
        sum = 0
        for item in self.items:
            sum += item.total()
        return sum

    def discount_percentage(self):
        return self.discount / self._item_total() * 100
