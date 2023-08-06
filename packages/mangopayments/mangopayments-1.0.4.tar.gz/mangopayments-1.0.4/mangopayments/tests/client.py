import datetime
from mangopay.resources import BankAccount, Card, CardRegistration, Document, Page, PayIn, BankWirePayOut, Refund, Transfer, \
    User, Wallet
from mangopay.utils import Money


class MockMangoPayApi:

    def __init__(self, user_id=None, bank_account_id=None,
                 card_registration_id=None, card_id=None,
                 document_id=None, wallet_id=None, refund_id=None,
                 pay_out_id=None, pay_in_id=None, transfer_id=None):
        self.user = MockUserApi(user_id, bank_account_id, document_id)
        self.card_registration = MockCardRegistrationApi(card_registration_id, card_id)
        self.card = MockCardApi(card_id)
        self.wallet = MockWalletApi(wallet_id)
        self.payout = MockPayOutApi(pay_out_id)
        self.payin = MockPayInApi(refund_id, pay_in_id)
        self.transfer = MockTransferApi(transfer_id)


class MockUserApi():

    def __init__(self, user_id, bank_account_id, document_id):
        self.user_id = user_id
        self.bank_account_id = bank_account_id
        self.document_id = document_id

    def create(self, user):
        if isinstance(user, User):
            user.id = self.user_id
            return user
        else:
            raise TypeError("User must be a User object")

    def create_bank_account(self, user_id, bank_account):
        if isinstance(bank_account, BankAccount) and isinstance(user_id, str):
            bank_account.id = self.bank_account_id
            return bank_account
        else:
            raise TypeError("Arguments are the wrong types")

    def update(self, user):
        if isinstance(user, User) and user.id:
            return user
        else:
            raise TypeError("User must be a User object with an id")

    def create_user_kyc_document(self, document, user_id):
        if isinstance(document, Document):
            document.id = self.document_id
            document.status = "CREATED"
            return document
        else:
            raise TypeError("Document must be a Document object")

    def get_user_kyc_document(self, document_id, user_id):
        document = Document()
        document.id = document_id
        document.status = "VALIDATED"
        return document

    def update_user_kyc_document(self, document, user_id, document_id):
        if (isinstance(document, Document)
                and document.id == document_id
                and document.status == "VALIDATION_ASKED"):
            return document
        else:
            raise BaseException("Arguments are of the wrong types")

    def create_user_kyc_page(self, page, user_id, document_id):
        if isinstance(page, Page):
            pass
        else:
            raise TypeError("Page must be a Page object")


class MockCardApi():

    def __init__(self, card_id):
        self.card_id = card_id

    def get(self, card_id):
        card = Card(id=card_id)
        card.alias = "497010XXXXXX4414"
        card.expiration_date = "1018"
        card.active = True
        card.validity = "VALID"
        return card


class MockCardRegistrationApi():

    def __init__(self, card_registration_id, card_id=None):
        self.card_registration_id = card_registration_id
        self.card_id = card_id

    def create(self, card_registration):
        if isinstance(card_registration, CardRegistration):
            card_registration.id = self.card_registration_id
            card_registration.card = Card()
            card_registration.card.id = self.card_id
            return card_registration
        else:
            raise TypeError(
                "Card Registration must be a CardRegistration object")

    def update(self, card_registration):
        if isinstance(card_registration, CardRegistration):
            card_registration.card = Card()
            card_registration.card.id = self.card_id
            return card_registration
        else:
            raise TypeError(
                "Card Registration must be a CardRegistration Entity")

    def get(self, card_registration_id):
            card_registration = CardRegistration(id=card_registration_id)
            card_registration.registration_data = "data=RegistrationData"
            card_registration.preregistration_data = "PreregistrationData"
            card_registration.access_key = "AccessKey"
            card_registration.card_registration_url = "CardRegistrationURL"
            return card_registration


class MockWalletApi():

    def __init__(self, wallet_id):
        self.wallet_id = wallet_id

    def create(self, wallet):
        if isinstance(wallet, Wallet) and not wallet.id:
            wallet.id = self.wallet_id
            return wallet
        else:
            raise TypeError("Wallet must be a Wallet object")

    def get(self, wallet_id):
        wallet = Wallet()
        wallet.id = wallet_id
        if self.wallet_id == 100:
            wallet.balance = Money(50000, currency="EUR")
        else:
            wallet.balance = Money(10000, currency="EUR")
        return wallet


class MockPayOutApi():

    def __init__(self, pay_out_id):
        self.pay_out_id = pay_out_id

    def create(self, pay_out):
        if isinstance(pay_out, BankWirePayOut) and not pay_out.id:
            pay_out.id = self.pay_out_id
            pay_out.execution_date = datetime.date(1970, 5, 22)
            pay_out.status = "CREATED"
            return pay_out
        else:
            raise TypeError("PayOut must be a BankWirePayOut object")

    def get(self, pay_out_id):
        pay_out = BankWirePayOut()
        pay_out.id = pay_out_id
        pay_out.execution_date = datetime.date(1970, 5, 22)
        pay_out.status = "CREATED"
        return pay_out


class MockPayInApi():

    def __init__(self, refund_id, pay_in_id):
        self.refund_id = refund_id
        self.pay_in_id = pay_in_id

    def create(self, pay_in):
        if isinstance(pay_in, PayIn) and not pay_in.id:
            pay_in.id = self.pay_in_id
            pay_in.execution_date = datetime.date(1970, 5, 22)
            pay_in.wire_reference = '4a57980154'
            pay_in.bank_account = BankAccount()
            pay_in.bank_account.iban = "FR7618829754160173622224251"
            pay_in.bank_account.bic = "CMBRFR2BCME"
            pay_in.bank_account.bic = "123"
            if self.pay_in_id == 101:
                pay_in.secure_mode_redirect_url = "https://test.com"
            else:
                pay_in.secure_mode_redirect_url = None
            if self.pay_in_id == 100:
                pay_in.status = "FAILED"
                pay_in.result_code = "001034"
                pay_in.result_message = "User has let the payment session expire without paying"
            else:
                pay_in.status = "SUCCESS"
                pay_in.result_code = "000000"
            return pay_in
        else:
            raise TypeError("PayIn must be a PayIn object")

    def get(self, pay_in_id):
        pay_in = PayIn()
        pay_in.id = pay_in_id
        pay_in.execution_date = datetime.date(1970, 5, 22)
        pay_in.secure_mode_redirect_url = "https://test.com"
        pay_in.status = "SUCCEEDED"
        pay_in.result_code = "000000"
        return pay_in

    def create_refund(self, pay_in_id, refund):
        if isinstance(refund, Refund) and pay_in_id:
            refund.id = self.refund_id
            refund.execution_date = datetime.date(1970, 5, 22)
            if self.pay_in_id == 200:
                refund.status = "FAILED"
                refund.result_message = "Refund failed"
                refund.result_code = "002100"
            else:
                refund.status = "SUCCEEDED"
                refund.result_code = "000000"
            return refund
        else:
            raise TypeError("Refund must be a Refund object")

class MockTransferApi():

    def __init__(self, transfer_id):
        self.transfer_id = transfer_id

    def create(self, transfer):
        if isinstance(transfer, Transfer) and not transfer.id:
            transfer.id = self.transfer_id
            if self.transfer_id == 30:
                transfer.status = "FAILED"
                transfer.result_code = "001401"
                transfer.result_message = "Transaction has already been successfully refunded."
            else:
                transfer.status = "SUCCEEDED"
                transfer.result_code = "000000"
            return transfer

    def get(self, transfer_id):
        transfer = Transfer()
        transfer.id = transfer_id
        transfer.execution_date = datetime.date(1970, 5, 22)
        transfer.status = "SUCCEEDED"
        transfer.result_code = "000000"
        return transfer