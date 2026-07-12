#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import tempfile
import unittest
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT = Path(
    "/Users/Renlong/Projects/GitHub/YIN-Renlong/"
    "vector-space-theological-meaning"
)
SCRIPT = PROJECT / "scripts" / "ctsb_v3_4_prototype.py"

spec = importlib.util.spec_from_file_location(
    "ctsb_v3_4_prototype",
    SCRIPT,
)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not import prototype script: {SCRIPT}")

prototype = importlib.util.module_from_spec(spec)
spec.loader.exec_module(prototype)


class CTSBV34PrototypeTests(unittest.TestCase):
    def setUp(self) -> None:
        self.temporary = tempfile.TemporaryDirectory()
        self.root = Path(self.temporary.name)
        self.data_dir = self.root / "prototype"
        self.output_dir = self.root / "run"

        prototype.write_fixture(
            self.data_dir,
            force=True,
        )

    def tearDown(self) -> None:
        self.temporary.cleanup()

    def test_fixture_schema_and_links(self) -> None:
        tables = prototype.load_tables(self.data_dir)
        summary = prototype.validate_tables(
            tables,
            mode="fixture",
        )

        self.assertEqual(summary["audits"], 5)
        self.assertGreaterEqual(summary["references"], 30)
        self.assertGreater(summary["queries"], 20)
        self.assertGreater(summary["validation_texts"], 20)

    def test_benchmark_mode_rejects_synthetic_sources(self) -> None:
        tables = prototype.load_tables(self.data_dir)

        with self.assertRaises(ValueError):
            prototype.validate_tables(
                tables,
                mode="benchmark",
            )

    def test_mock_embeddings_are_deterministic(self) -> None:
        texts = [
            "Grace is a divine gift.",
            "She moved with grace and elegance.",
        ]

        first = prototype.deterministic_fixture_embeddings(
            texts,
            dimensions=256,
        )
        second = prototype.deterministic_fixture_embeddings(
            texts,
            dimensions=256,
        )

        for text in texts:
            np.testing.assert_array_equal(
                first[text],
                second[text],
            )

    def test_cosine_identity(self) -> None:
        vector = np.array([1.0, 2.0, 3.0])
        self.assertAlmostEqual(
            prototype.cosine(vector, vector),
            1.0,
            places=12,
        )

    def test_complete_mock_pipeline(self) -> None:
        result = prototype.run_pipeline(
            data_dir=self.data_dir,
            output_dir=self.output_dir,
            backend="mock",
            mode="fixture",
            dimensions=256,
        )

        expected = {
            "run_manifest.json",
            "embedding_index.csv",
            "embeddings.npz",
            "similarities.csv",
            "query_scores.csv",
            "condition_summary.csv",
            "shifts.csv",
            "validation_scores.csv",
            "validation_metrics.csv",
        }

        actual = {
            path.name
            for path in self.output_dir.iterdir()
            if path.is_file()
        }

        self.assertTrue(expected.issubset(actual))
        self.assertTrue(result["manifest_path"].exists())

        query_scores = pd.read_csv(
            self.output_dir / "query_scores.csv"
        )
        self.assertTrue(
            {"s_c", "s_r", "cas"}.issubset(query_scores.columns)
        )

        recalculated = query_scores["s_c"] - query_scores["s_r"]
        np.testing.assert_allclose(
            query_scores["cas"],
            recalculated,
            atol=1e-12,
        )

        shifts = pd.read_csv(
            self.output_dir / "shifts.csv"
        )
        self.assertFalse(shifts.empty)
        self.assertLessEqual(
            float(
                shifts["decomposition_identity_error"]
                .abs()
                .max()
            ),
            1e-10,
        )

        validation_metrics = pd.read_csv(
            self.output_dir / "validation_metrics.csv"
        )
        self.assertIn(
            "ALL_AUDITS",
            set(validation_metrics["scope"]),
        )


if __name__ == "__main__":
    unittest.main(verbosity=2)
