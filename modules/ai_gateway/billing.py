"""
InChristAlone AI Billing Service v4.11.6

Handles AI unit checking and deduction.

Designed for:
- AI Gateway
- API requests
- Mobile clients
- Church websites

Uses user_id instead of Flask current_user.
"""

from models import db, User


def check_ai_units(user_id, required_units=1):
    """
    Check whether a user has enough AI units.

    Returns:
        True if sufficient units
        False otherwise
    """

    user = User.query.get(user_id)

    if not user:
        return False

    return user.wallet_balance >= required_units


def deduct_ai_units(user_id, units=1):
    """
    Deduct AI units after successful generation.

    Returns:
        True if deducted
        False if insufficient balance or user missing
    """

    user = User.query.get(user_id)

    if not user:
        return False

    if user.wallet_balance < units:
        return False

    user.wallet_balance -= units
    db.session.commit()

    return True
