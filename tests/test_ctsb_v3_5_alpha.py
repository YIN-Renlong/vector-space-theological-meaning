#!/usr/bin/env python3
from __future__ import annotations

import importlib.util
import json
import tempfile
import unittest
from collections import Counter
from pathlib import Path

import numpy as np
import pandas as pd

PROJECT = Path(__file__).resolve().parents[1]
SCRIPT = PROJECT / "scripts" / "ctsb_v3_5_alpha.py"

spec = importlib.util.spec_from_file_location(
    "ctsb_v3_5_alpha",
    SCRIPT,
)
if spec is None or spec.loader is None:
    raise RuntimeError(f"Could not import alpha script: {SCRIPT}")

alpha = importlib.util.module_from_spec(spec)
spec.loader.exec_module(alpha)


class CTSBV35AlphaTests(unittest.TestCase):
    def test_registry_has_expected_balance_and_retained_audits(self) -> None:
        registry = alpha.parse_registry()

        self.assertEqual(len(registry), 100)
        self.assertEqual(
            Counter(row["locus_code"] for row in registry),
            {"F": 25, "A": 25, "L": 25, "R": 25},
        )

        audit_ids = {row["audit_id"] for row in registry}
        retained = {
            "death_biological",
            "grief_psychological",
            "euthanasia_assisted_dying",
            "grace_lexical",
            "judgment_after_death_generic",
        }
        self.assertTrue(retained.issubset(audit_ids))

    def test_generated_table_counts_and_validation(self) -> None:
        tables = alpha.build_tables()
        summary = alpha.validate_alpha_tables(tables)

        self.assertEqual(len(tables["comparisons"]), 100)
        self.assertEqual(len(tables["references"]), 600)
        self.assertEqual(len(tables["queries"]), 1624)
        self.assertEqual(len(tables["validation"]), 808)
        self.assertEqual(summary["critical_audits"], 8)

    def test_reference_and_validation_warnings_are_preserved(self) -> None:
        tables = alpha.build_tables()
        references = tables["references"]
        validation = tables["validation"]

        self.assertEqual(
            set(references["text_status"]),
            {"generated_unreviewed"},
        )
        self.assertEqual(
            set(references["review_status"]),
            {"human_review_pending"},
        )
        self.assertTrue(
            references["source_title"]
            .str.startswith("CANDIDATE SOURCE —")
            .all()
        )
        self.assertTrue(
            validation["review_status"]
            .eq("human_review_pending")
            .all()
        )

    def test_explicit_catholic_queries_are_strict_label_pairs(self) -> None:
        queries = alpha.build_tables()["queries"]
        lookup = queries.set_index("query_id").to_dict("index")
        explicit = queries[
            queries["condition"] == "explicit_catholic"
        ]

        self.assertEqual(len(explicit), 300)

        for row in explicit.itertuples(index=False):
            baseline = lookup[row.baseline_query_id]
            baseline_text = baseline["query_text"]
            expected = (
                "In Catholic teaching, "
                + baseline_text[:1].lower()
                + baseline_text[1:]
            )
            self.assertEqual(row.query_text, expected)

    def test_complete_mock_alpha_pipeline(self) -> None:
        with tempfile.TemporaryDirectory() as temporary:
            root = Path(temporary)
            data_dir = root / "generated_100"
            output_dir = root / "mock_run"

            alpha.write_tables(data_dir, force=True)
            result = alpha.run_alpha(
                data_dir=data_dir,
                output_dir=output_dir,
                backend="mock",
                cache_path=root / "unused_cache.json",
                env_file=root / "unused.env",
                batch_size=64,
                dimensions=128,
            )

            expected = {
                "run_manifest.json",
                "query_scores.csv",
                "shifts.csv",
                "similarities.csv",
                "validation_metrics.csv",
                "alpha_condition_statistics.csv",
                "alpha_shift_statistics.csv",
                "leave_one_reference_out.csv",
                "leave_one_reference_out_summary.csv",
                "paraphrase_condition_sensitivity.csv",
                "paraphrase_leave_one_out.csv",
                "paraphrase_shift_sensitivity.csv",
                "alpha_run_report.md",
            }
            actual = {
                path.name
                for path in output_dir.iterdir()
                if path.is_file()
            }
            self.assertTrue(expected.issubset(actual))

            manifest = json.loads(
                result["manifest"].read_text(encoding="utf-8")
            )
            self.assertEqual(
                manifest["methodology_version"],
                "CTSB v3.5-alpha",
            )
            self.assertEqual(manifest["backend"], "mock")
            self.assertIn(
                "NON-EVIDENTIAL",
                manifest["evidential_status"],
            )

            query_scores = pd.read_csv(
                output_dir / "query_scores.csv"
            )
            np.testing.assert_allclose(
                query_scores["cas"],
                query_scores["s_c"] - query_scores["s_r"],
                atol=1e-12,
            )

            shifts = pd.read_csv(output_dir / "shifts.csv")
            self.assertLessEqual(
                float(
                    shifts["decomposition_identity_error"]
                    .abs()
                    .max()
                ),
                1e-10,
            )

            similarities = pd.read_csv(
                output_dir / "similarities.csv"
            )
            self.assertEqual(len(similarities), 14592)

            loro = pd.read_csv(
                output_dir
                / "leave_one_reference_out_summary.csv"
            )
            self.assertEqual(len(loro), 1624)


if __name__ == "__main__":
    unittest.main(verbosity=2)
