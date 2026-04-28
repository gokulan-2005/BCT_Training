def qualify_lead(state):
    lead = state["lead"]

    score = 0

    if lead["budget"] > 5000:
        score += 1
    if lead["interest"] == "high":
        score += 1
    if lead["company_size"] == "large":
        score += 1

    if score >= 2:
        status = "Hot"
    elif score == 1:
        status = "Warm"
    else:
        status = "Cold"

    return {"qualification": status}