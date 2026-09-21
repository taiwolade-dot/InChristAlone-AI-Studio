from models import db, ActivityLog


def log_activity(user, action, module, details=""):
    try:
        log = ActivityLog(
            user_id=user.id if user else None,
            action=action,
            module=module,
            details=details
        )

        db.session.add(log)
        db.session.commit()

    except Exception as e:
        db.session.rollback()
        print("Activity Log Error:", e)
