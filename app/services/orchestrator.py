from app.agents import demand_agent, inventory_agent, negotiation_agent, purchase_order_agent, seasonal_agent


def run_all_agents(drop_name: str = "Drop 3 - Mumbai", target_units: int = 25) -> dict:
    print("\n🤖 RIFT WEAR Orchestrator — Running all agents...\n")

    print("  [1/5] Demand Forecasting Agent...")
    demand = demand_agent.run()

    print("  [2/5] Inventory & Profitability Agent...")
    inventory = inventory_agent.run()

    print("  [3/5] Seasonal Cycle Agent...")
    seasonal = seasonal_agent.run()

    print("  [4/5] Purchase Order Agent...")
    orders = purchase_order_agent.run(drop_name=drop_name, target_units=target_units)

    print("  [5/5] Negotiation Agent...")
    negotiation = negotiation_agent.run()

    print("\n✓ All agents completed.\n")

    return {
        "demand_forecast":       demand,
        "inventory_health":      inventory,
        "seasonal_analysis":     seasonal,
        "purchase_orders":       orders,
        "supplier_negotiations": negotiation,
    }
