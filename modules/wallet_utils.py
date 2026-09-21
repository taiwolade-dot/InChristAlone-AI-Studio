from flask import redirect, url_for, flash
from flask_login import current_user
from models import db


def spend_units(amount, redirect_endpoint='prompt_marketplace.recharge'):
    """
    Attempts to deduct `amount` units from the current user's wallet.
    Returns True if successful, or a redirect response if insufficient funds.
    Usage in a route:

        result = spend_units(5)
        if result is not True:
            return result
        # continue with the action...
    """
    if current_user.wallet_balance < amount:
        flash(
            f'This action costs {amount} units, but you only have {current_user.wallet_balance}. Please recharge.',
            'error'
        )
        return redirect(url_for(redirect_endpoint))

    current_user.wallet_balance -= amount
    db.session.commit()
    return True

def refund_units(amount):
    """
    Refunds units back to the current user's wallet, typically after
    a paid AI generation call fails (so the user isn't charged for nothing).
    """
    current_user.wallet_balance += amount
    db.session.commit()
