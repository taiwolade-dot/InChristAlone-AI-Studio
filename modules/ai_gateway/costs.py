"""
InChristAlone AI Cost Engine v4.11.10

Uses AI Service Catalog as the single
source of pricing truth.
"""

from modules.ai_gateway.catalog import get_service


def get_task_cost(task=None):
    """
    Return AI unit cost from service catalog.

    Unknown tasks default to general.
    """

    service = get_service(task)

    if service:
        return service["units"]

    general = get_service("general")

    return general["units"]
