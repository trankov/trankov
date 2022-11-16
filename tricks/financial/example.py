from descriptors import DecimalAmount, ValidCurrency


class Payment:
    amount = DecimalAmount()
    currency = ValidCurrency()

    def __repr__(self):
        return f"{self.currency} {self.amount}"


if __name__ == '__main__':

    payment = Payment()

    payment.amount = 0.1
    payment.currency = "USD"
    print(
        payment,                # 'USD 0.1'
        payment.amount,         # 0.1
        type(payment.amount),   # <class Decimal>
        payment.amount + 0.2    # Decimal('0.3')
    )

    payment.amount = "22,31"
    payment.currency = "RUB"

    print(payment)  # 'RUB 22.31'


    payment.currency = "GB"         # Value Error
    payment.currency = "22,100.45"  # Type Error
