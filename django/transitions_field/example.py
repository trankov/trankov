from django.core.exceptions import ValidationError
from django.db import models

from .transitions import StateField, TransitionRule


class IncomingPaymentStates(models.TextChoices):
    START = 'start', 'Payment started'
    KASSA_INIT = 'init_data_received', 'Init data received'
    KASSA_INIT_DATA_SAVED = (
        'init_data_saved',
        'Init data saved',
    )
    KASSA_QR_CODE = 'qr_code_received', 'QR code received'
    KASSA_QR_CODE_SAVED = (
        'qr_code_saved',
        'Request GetQR and response saved',
    )
    ONE_MORE_STEP = 'one_more_step', 'One more step not completed'


class ModelState(models.Model):
    class Meta:
        app_label = 'cycle'

    state = StateField(  # type: ignore
        verbose_name='State',
        default=IncomingPaymentStates.START,
        rules=[
            TransitionRule(
                start_state=IncomingPaymentStates.START,
                target_states=[IncomingPaymentStates.KASSA_INIT],
            ),
            (
                'init_data_received',
                [
                    IncomingPaymentStates.KASSA_INIT_DATA_SAVED,
                    IncomingPaymentStates.KASSA_QR_CODE,
                ],
            ),
            (IncomingPaymentStates.KASSA_INIT_DATA_SAVED, [...]),
            (
                IncomingPaymentStates.KASSA_QR_CODE,
                [IncomingPaymentStates.KASSA_QR_CODE_SAVED],
            ),
            ('qr_code_saved', None),
            TransitionRule(
                start_state=IncomingPaymentStates.ONE_MORE_STEP,
                target_states=[...],
            ),
        ],
    )


ms = ModelState()
ms.state = IncomingPaymentStates.KASSA_INIT
ms.state = IncomingPaymentStates.KASSA_INIT_DATA_SAVED
ms.state = IncomingPaymentStates.ONE_MORE_STEP
ms.state = IncomingPaymentStates.KASSA_QR_CODE
ms.state = IncomingPaymentStates.KASSA_QR_CODE_SAVED

try:
    ms.state = IncomingPaymentStates.START
except Exception as e:
    assert isinstance(e, ValidationError)
