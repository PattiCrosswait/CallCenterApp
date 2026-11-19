import unittest

from src.call_center_contract import (
    aggregate_metrics,
    calculate_metrics,
    coaching_priorities,
    insufficient_data,
    validate_fixture,
)


class ContractCalculationTests(unittest.TestCase):
    def test_at02_one_agent_fixture(self):
        record = {
            "calls": 100,
            "resolved": 80,
            "handling_seconds": 48000,
            "positive": 17,
            "responses": 20,
            "quality_points": 270,
            "reviews": 3,
        }
        metrics = calculate_metrics(record)

        self.assertEqual(metrics["calls"], 100)
        self.assertAlmostEqual(metrics["resolution"], 80.0)
        self.assertAlmostEqual(metrics["handling_time"], 8.0)
        self.assertAlmostEqual(metrics["satisfaction"], 85.0)
        self.assertAlmostEqual(metrics["quality"], 90.0)

    def test_at03_resolution_is_aggregated_from_totals_not_meaned_rates(self):
        records = [
            {
                "calls": 10,
                "resolved": 8,
                "handling_seconds": 0,
                "positive": 0,
                "responses": 0,
                "quality_points": 0,
                "reviews": 0,
            },
            {
                "calls": 90,
                "resolved": 45,
                "handling_seconds": 0,
                "positive": 0,
                "responses": 0,
                "quality_points": 0,
                "reviews": 0,
            },
        ]

        self.assertAlmostEqual(aggregate_metrics(records)["resolution"], 53.0)

    def test_at06_coaching_priority_order_and_targets(self):
        record = {
            "calls": 20,
            "resolved": 14,
            "handling_seconds": 12000,
            "positive": 15,
            "responses": 20,
            "quality_points": 240,
            "reviews": 3,
        }
        priorities = coaching_priorities(record)

        self.assertEqual(
            [priority["measure"] for priority in priorities],
            ["quality", "resolution", "satisfaction"],
        )

    def test_at07_no_priority_then_efficiency_only(self):
        healthy = {
            "calls": 20,
            "resolved": 16,
            "handling_seconds": 9600,
            "positive": 17,
            "responses": 20,
            "quality_points": 270,
            "reviews": 3,
        }
        slow = dict(healthy, handling_seconds=9780)

        self.assertEqual(coaching_priorities(healthy), [])
        self.assertEqual(
            [priority["measure"] for priority in coaching_priorities(slow)],
            ["efficiency"],
        )

    def test_at08_insufficient_observations(self):
        record = {
            "calls": 19,
            "resolved": 10,
            "handling_seconds": 0,
            "positive": 3,
            "responses": 4,
            "quality_points": 100,
            "reviews": 2,
        }
        insufficient = insufficient_data(record)

        self.assertIn("calls", insufficient)
        self.assertIn("satisfaction", insufficient)
        self.assertIn("quality", insufficient)
        self.assertEqual(coaching_priorities(record), [])

    def test_at09_rejects_invalid_fixture_shapes(self):
        duplicate = [
            {"agent": "A1", "date": "2026-01-01", "calls": 100, "resolved": 80, "handling_seconds": 48000, "positive": 17, "responses": 20, "quality_points": 270, "reviews": 3},
            {"agent": "A1", "date": "2026-01-01", "calls": 100, "resolved": 80, "handling_seconds": 48000, "positive": 17, "responses": 20, "quality_points": 270, "reviews": 3},
        ]

        errors = validate_fixture(duplicate, {"A1"})
        self.assertTrue(any("Duplicate" in error for error in errors))

        invalid_record = {
            "agent": "UNKNOWN",
            "date": "2026-01-01",
            "calls": -1,
            "resolved": 2,
            "handling_seconds": 0,
            "positive": 6,
            "responses": 5,
            "quality_points": 301,
            "reviews": 3,
        }
        errors = validate_fixture([invalid_record], {"A1"})

        self.assertTrue(any("Unknown agent" in error for error in errors))
        self.assertTrue(any("Negative count" in error for error in errors))
        self.assertTrue(any("Resolved calls" in error for error in errors))
        self.assertTrue(any("Positive ratings" in error for error in errors))
        self.assertTrue(any("Quality points" in error for error in errors))


class WorkflowContractTests(unittest.TestCase):
    def test_workflow_runs_pull_requests_and_main_pushes(self):
        with open(".github/workflows/unit-tests.yml", "r", encoding="utf-8") as workflow:
            contents = workflow.read()

        self.assertIn("pull_request:", contents)
        self.assertIn("push:", contents)
        self.assertIn("- main", contents)
        self.assertIn("python -m unittest discover", contents)


if __name__ == "__main__":
    unittest.main()
