"""Calculations and coaching rules from the Call Center App contract."""

from typing import Iterable, Mapping


QUALITY_TARGET = 90.0
RESOLUTION_TARGET = 80.0
SATISFACTION_TARGET = 85.0
HANDLING_TARGET_MINUTES = 8.1


def calculate_metrics(record: Mapping) -> dict:
    calls = record["calls"]
    resolved = record["resolved"]
    handling_seconds = record["handling_seconds"]
    positive = record["positive"]
    responses = record["responses"]
    quality_points = record["quality_points"]
    reviews = record["reviews"]

    zero_denominator = calls == 0
    return {
        "calls": calls,
        "resolution": None if zero_denominator else resolved / calls * 100,
        "handling_time": None if calls == 0 else handling_seconds / calls / 60,
        "satisfaction": None if responses == 0 else positive / responses * 100,
        "quality": None if reviews == 0 else quality_points / (reviews * 100) * 100,
    }


def aggregate_metrics(records: Iterable[Mapping]) -> dict:
    records = list(records)
    totals = {
        key: sum(record[key] for record in records)
        for key in (
            "calls",
            "resolved",
            "handling_seconds",
            "positive",
            "responses",
            "quality_points",
            "reviews",
        )
    }
    return calculate_metrics(totals)


def coaching_priorities(record: Mapping) -> list[dict]:
    metrics = calculate_metrics(record)
    priorities = []

    if record["calls"] >= 20:
        if record["reviews"] >= 3 and metrics["quality"] is not None:
            if metrics["quality"] < QUALITY_TARGET:
                priorities.append(
                    {"measure": "quality", "value": metrics["quality"], "target": QUALITY_TARGET}
                )
        if record["calls"] >= 20 and metrics["resolution"] is not None:
            if metrics["resolution"] < RESOLUTION_TARGET:
                priorities.append(
                    {"measure": "resolution", "value": metrics["resolution"], "target": RESOLUTION_TARGET}
                )
        if record["responses"] >= 5 and metrics["satisfaction"] is not None:
            if metrics["satisfaction"] < SATISFACTION_TARGET:
                priorities.append(
                    {
                        "measure": "satisfaction",
                        "value": metrics["satisfaction"],
                        "target": SATISFACTION_TARGET,
                    }
                )

        quality_or_resolution_below_target = any(
            priority["measure"] in ("quality", "resolution") for priority in priorities
        )
        if (
            not quality_or_resolution_below_target
            and metrics["handling_time"] is not None
            and metrics["handling_time"] > HANDLING_TARGET_MINUTES
        ):
            priorities.append(
                {
                    "measure": "efficiency",
                    "value": metrics["handling_time"],
                    "target": HANDLING_TARGET_MINUTES,
                }
            )

    return priorities


def insufficient_data(record: Mapping) -> dict:
    insufficient = {}
    if record["calls"] < 20:
        insufficient["calls"] = "Insufficient data"
    if record["responses"] < 5:
        insufficient["satisfaction"] = "Insufficient data"
    if record["reviews"] < 3:
        insufficient["quality"] = "Insufficient data"
    return insufficient


def validate_fixture(records: Iterable[Mapping], known_agents: Iterable[str]) -> list[str]:
    known_agents = set(known_agents)
    seen = set()
    errors = []

    for record in records:
        agent = record["agent"]
        date = record["date"]

        if agent not in known_agents:
            errors.append(f"Unknown agent: {agent}")
        if (agent, date) in seen:
            errors.append(f"Duplicate agent date row: {agent} on {date}")
        seen.add((agent, date))

        for name in ("calls", "resolved", "handling_seconds", "positive", "responses", "quality_points", "reviews"):
            if record[name] < 0:
                errors.append(f"Negative count: {name}")
        if record["resolved"] > record["calls"]:
            errors.append("Resolved calls exceed calls")
        if record["positive"] > record["responses"]:
            errors.append("Positive ratings exceed responses")
        if record["quality_points"] > record["reviews"] * 100:
            errors.append("Quality points exceed the allowed total")

    return errors
