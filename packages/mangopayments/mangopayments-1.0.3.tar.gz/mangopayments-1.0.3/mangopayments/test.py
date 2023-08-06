import django

django.setup()

from mangopayments.models import MangoPayPayOut

acc = MangoPayPayOut.objects.get(id=1)

acc.create()