from transactionpro.import_type import ImportType


class ReceivePayment(ImportType):
    @property
    def fields(self):
        return (
            'customer', 'check_number', 'transaction_date', 'payment_method', 'memo', 'apply_to_invoice',
            'amount', 'deposit_to', 'discount_amount', 'discount_account', 'discount_class',
            'ar_account', 'exchange_rate',
        )

    @property
    def required_fields(self):
        return (
            'customer', 'check_number', 'amount'
        )
