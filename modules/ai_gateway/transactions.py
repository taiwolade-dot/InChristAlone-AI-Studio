"""
InChristAlone AI Transaction Safety Layer v4.11.7

Handles:
- AI request charging
- Success confirmation
- Failed request refunds
"""

from modules.ai_gateway.billing import (
    deduct_ai_units
)

from models import db, User


def charge_ai_request(user_id, units=1):
    """
    Deduct units before AI processing.
    """

    return deduct_ai_units(
        user_id=user_id,
        units=units
    )


def refund_ai_request(user_id, units=1):
    """
    Refund units after failed AI generation.
    """

    user = User.query.get(user_id)

    if not user:
        return False

    user.wallet_balance += units
    db.session.commit()

    return True
