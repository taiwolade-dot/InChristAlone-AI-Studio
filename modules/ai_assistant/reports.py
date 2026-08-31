from models import AIConversation, db
from sqlalchemy import func
from datetime import datetime, timedelta


def get_period_start(period):

    now = datetime.utcnow()

    if period == "today":
        return now.replace(
            hour=0,
            minute=0,
            second=0,
            microsecond=0
        )

    elif period == "week":
        return now - timedelta(days=7)

    elif period == "month":
        return now - timedelta(days=30)

    return None



def generate_ai_report(user_id, period="week"):

    query = AIConversation.query.filter_by(
        user_id=user_id
    )


    start_date = get_period_start(period)


    if start_date:
        query = query.filter(
            AIConversation.created_at >= start_date
        )


    total_requests = query.count()


    module_data = (
        query.with_entities(
            AIConversation.module,
            func.count(AIConversation.id)
        )
        .group_by(
            AIConversation.module
        )
        .all()
    )


    modules = {}

    for module, count in module_data:
        modules[module] = count


    top_module = None

    if modules:
        top_module = max(
            modules,
            key=modules.get
        )


    return {
        "period": period,
        "total_requests": total_requests,
        "modules": modules,
        "top_module": top_module
    }
