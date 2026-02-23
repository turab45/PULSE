

from state import BatsmanState


# calculate strike rate
def strike_rate_node(state: BatsmanState):
    strike_rate = 0.0
    if state["balls"] == 0:
        strike_rate = 0.0
    else:
        strike_rate = (state["runs"] / state["balls"]) * 100
    return {"strike_rate": strike_rate}

# calculate boundary per ball
def boundary_per_ball_node(state: BatsmanState):
    bpb = 0.0
    if state["balls"] == 0:
        bpb = 0.0
    else:
        total_boundaries = state["fours"] * 4 + state["sixes"] * 6
        bpb = total_boundaries / state["balls"]
    return {"boundary_per_ball": bpb}
# calculate boundary percentage
def boundary_percentage_node(state: BatsmanState):
    boundary_percentage = 0.0
    if state["runs"] == 0:
        boundary_percentage = 0.0
    else:
        total_boundaries = state["fours"] * 4 + state["sixes"] * 6
        boundary_percentage = (total_boundaries / (state["runs"] + 1)) * 100 # Adding 1 to avoid division by zero
    return {"boundary_percentage": boundary_percentage}

# generate summary
def summary_node(state: BatsmanState):
    summary = f"Summary: {state['runs']} runs in {state['balls']} balls, Strike Rate: {state['strike_rate']:.2f}, Boundary Per Ball: {state['boundary_per_ball']:.2f}, Boundary Percentage: {state['boundary_percentage']:.2f}"
    return {"summary": summary}