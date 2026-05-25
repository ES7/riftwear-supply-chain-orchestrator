from fastapi import APIRouter, Query
from app.services.orchestrator import run_all_agents
from app.agents import demand_agent, inventory_agent, negotiation_agent, purchase_order_agent, seasonal_agent

router = APIRouter(prefix="/api/agents", tags=["agents"])


@router.post("/run-all")
def run_all(
    drop_name:    str = Query(default="Drop 3 - Mumbai"),
    target_units: int = Query(default=25),
):
    return run_all_agents(drop_name=drop_name, target_units=target_units)


@router.post("/demand")
def run_demand():
    return demand_agent.run()


@router.post("/inventory")
def run_inventory():
    return inventory_agent.run()


@router.post("/seasonal")
def run_seasonal():
    return seasonal_agent.run()


@router.post("/purchase-orders")
def run_po(
    drop_name:    str = Query(default="Drop 3 - Mumbai"),
    target_units: int = Query(default=25),
):
    return purchase_order_agent.run(drop_name=drop_name, target_units=target_units)


@router.post("/negotiation")
def run_negotiation():
    return negotiation_agent.run()
