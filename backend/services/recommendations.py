def generate_recommendations(forecast):
    recs = []

    for cat, data in forecast.items():
        budget = data["budget"]
        projected = data["projected_end_of_month"]
        spent_so_far = data.get("spent_so_far", 0)

        # Overspending tips (trigger if > 80% of budget for demo)
        if projected > budget * 0.8:
            if cat in ["Entertainment", "Subscriptions"]:
                recs.append(f"Consider re-evaluating your {cat.lower()} to save an estimated ${round(projected - budget)} monthly.")
                recs.append(f"Look for discounts or bundle deals for your {cat.lower()}.")
            elif cat == "Transport":
                recs.append(f"Explore public transport options; you could save ${round(projected - budget)} monthly on fuel and parking.")
                recs.append("Consider carpooling or ride-sharing for extra savings.")
            elif cat == "Food and Drink":
                recs.append(f"Reduce dining out; cooking at home could save ${round(projected - budget)} monthly.")
                recs.append("Plan meals ahead to avoid impulsive spending.")
            elif cat == "Shops":
                recs.append(f"Review your shopping habits; you could save ${round(projected - budget)} monthly.")
                recs.append("Use price comparison tools before purchases.")

        # On-track but encourage more saving
        if cat == "Savings" and spent_so_far < budget * 0.5:
            recs.append("Increase your investment contributions by 5% to reach your saving goal faster.")
        elif projected <= budget:
            recs.append(f"Good job on {cat}! You could save even more by monitoring small daily expenses.")

    # Ensure at least one recommendation for demo
    if not recs:
        recs.append("Keep an eye on your budgets this month to maximize your savings!")

    return recs
