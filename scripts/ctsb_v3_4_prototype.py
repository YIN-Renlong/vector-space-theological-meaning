#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import re
from collections import Counter, defaultdict
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, Iterable, List, Mapping, Optional, Sequence, Tuple

import numpy as np
import pandas as pd

ROOT = Path(__file__).resolve().parents[1]

RELATIONSHIP_TYPES = {
    "complementary_levels",
    "valid_but_partial",
    "normatively_conflicting",
    "alternative_lexical_senses",
    "generic_religious_vs_catholic_specific",
}

QUERY_CONDITIONS = {
    "bare",
    "natural_general",
    "natural_ambiguous",
    "critical",
    "label_free_theological",
    "explicit_catholic",
    "integrative",
}

REFERENCE_GROUPS = {"catholic", "comparison"}
VALIDATION_STAGES = {"clear_register", "integrative", "critical"}
CLEAR_TARGETS = {"catholic", "comparison"}

TABLE_COLUMNS = {
    "comparisons": [
        "audit_id",
        "concept",
        "primary_locus",
        "life_death_module",
        "comparison_register",
        "relationship_type",
        "critical_context_applicable",
        "inclusion_rationale",
        "dataset_status",
        "review_status",
    ],
    "references": [
        "reference_id",
        "audit_id",
        "reference_group",
        "reference_text",
        "source_title",
        "source_location",
        "text_status",
        "review_status",
        "review_notes",
    ],
    "queries": [
        "query_id",
        "audit_id",
        "condition",
        "paraphrase_id",
        "query_text",
        "baseline_query_id",
        "contrast_type",
        "review_status",
    ],
    "validation": [
        "validation_id",
        "audit_id",
        "validation_stage",
        "target_class",
        "validation_text",
        "ethical_review_status",
        "review_status",
        "review_notes",
    ],
}

FIXTURE_COMPARISONS = [
    {
        "audit_id": "death_biological",
        "concept": "death",
        "primary_locus": "Human Dignity and Theological Anthropology",
        "life_death_module": "true",
        "comparison_register": "biological description",
        "relationship_type": "complementary_levels",
        "critical_context_applicable": "true",
        "inclusion_rationale": "Tests whether biological and eschatological meanings remain jointly accessible.",
    },
    {
        "audit_id": "grief_psychological",
        "concept": "grief",
        "primary_locus": "Human Dignity and Theological Anthropology",
        "life_death_module": "true",
        "comparison_register": "psychological bereavement",
        "relationship_type": "valid_but_partial",
        "critical_context_applicable": "true",
        "inclusion_rationale": "Tests Catholic-pastoral accessibility alongside valid psychological bereavement language.",
    },
    {
        "audit_id": "euthanasia_assisted_dying",
        "concept": "euthanasia",
        "primary_locus": "Human Dignity and Theological Anthropology",
        "life_death_module": "true",
        "comparison_register": "permissive assisted-dying register",
        "relationship_type": "normatively_conflicting",
        "critical_context_applicable": "true",
        "inclusion_rationale": "Tests differentiation between conflicting moral registers while preserving clinical care language.",
    },
    {
        "audit_id": "grace_lexical",
        "concept": "grace",
        "primary_locus": "Sin Grace and Redemption",
        "life_death_module": "false",
        "comparison_register": "elegance and social charm",
        "relationship_type": "alternative_lexical_senses",
        "critical_context_applicable": "false",
        "inclusion_rationale": "Tests selection between theological and ordinary lexical senses.",
    },
    {
        "audit_id": "judgment_after_death_generic",
        "concept": "judgment after death",
        "primary_locus": "Sin Grace and Redemption",
        "life_death_module": "true",
        "comparison_register": "generic religious afterlife judgment",
        "relationship_type": "generic_religious_vs_catholic_specific",
        "critical_context_applicable": "false",
        "inclusion_rationale": "Tests Catholic doctrinal specificity against generic religious imagery.",
    },
]

FIXTURE_REFERENCES = {
    "death_biological": {
        "catholic": [
            "Death ends earthly life while Christian hope looks toward resurrection in Christ.",
            "The dying person is accompanied in prayer, dignity, and hope of communion with God.",
            "Bodily death is understood within creation, judgment, mercy, and the promise of resurrection.",
        ],
        "comparison": [
            "Death is the irreversible cessation of the organism's vital biological functions.",
            "Biological death marks the permanent end of integrated bodily functioning.",
            "In medical description, death is determined through irreversible loss of vital function.",
        ],
    },
    "grief_psychological": {
        "catholic": [
            "Christian mourning brings sorrow before God in prayer and hope of resurrection.",
            "The bereaved person is accompanied with compassion, prayer, consolation, and Christian hope.",
            "Grief expresses wounded love while faith continues to hope in communion with God.",
        ],
        "comparison": [
            "Grief is an emotional and psychological response to bereavement and loss.",
            "Bereavement can involve sadness, disrupted sleep, reduced concentration, and social withdrawal.",
            "Coping with grief is a psychological process of adapting to the death of a loved person.",
        ],
    },
    "euthanasia_assisted_dying": {
        "catholic": [
            "Intentionally ending innocent human life is rejected as contrary to human dignity.",
            "Compassion should relieve suffering and accompany the dying person without intentionally causing death.",
            "Palliative care can respect life, dignity, and natural death while refusing intentional killing.",
        ],
        "comparison": [
            "Assisted dying is presented as a permissible personal choice for ending unbearable suffering.",
            "Voluntary euthanasia allows a competent patient to request medical assistance in ending life.",
            "Ending life may be described as an autonomous medical option when suffering cannot be accepted.",
        ],
    },
    "grace_lexical": {
        "catholic": [
            "Grace is the freely given divine gift that draws the person into life with God.",
            "Divine grace is not earned but is received as God's transforming help and presence.",
            "Through grace the human person is healed, sanctified, and called to communion with God.",
        ],
        "comparison": [
            "Grace can mean elegance, poise, and beauty of movement.",
            "A graceful person behaves with social charm, courtesy, and refinement.",
            "She moved across the stage with balance, elegance, and grace.",
        ],
    },
    "judgment_after_death_generic": {
        "catholic": [
            "After death each person faces particular judgment before God.",
            "Particular judgment reveals the truth of a person's life before divine mercy and justice.",
            "The encounter with Christ after death brings personal moral accountability before God.",
        ],
        "comparison": [
            "Many religions imagine an afterlife judgment in which deeds receive reward or punishment.",
            "Afterlife judgment is a widespread cultural image of a cosmic moral tribunal.",
            "Stories of postmortem judgment portray souls being evaluated after death.",
        ],
    },
}

FIXTURE_QUERIES = {
    "death_biological": [
        ("bare_1", "bare", "death", "", ""),
        ("general_1", "natural_general", "The patient's vital biological functions ceased irreversibly.", "bare_1", "bare_to_general"),
        ("ambiguous_1", "natural_ambiguous", "What does death mean for a person and for those who remain?", "general_1", "general_to_ambiguous"),
        ("critical_1", "critical", "The family has been told that death is near and must decide how to accompany the patient.", "general_1", "general_to_critical"),
        ("label_free_1", "label_free_theological", "Death ends earthly life but is faced with hope in resurrection and communion with God.", "general_1", "general_to_label_free_theological"),
        ("catholic_1", "explicit_catholic", "In Catholic teaching, death ends earthly life but is faced with hope in resurrection and communion with God.", "label_free_1", "label_free_to_explicit_catholic"),
        ("integrative_1", "integrative", "Death is the biological end of earthly life and is also faced with prayer and hope in resurrection.", "general_1", "general_to_integrative"),
    ],
    "grief_psychological": [
        ("bare_1", "bare", "grief", "", ""),
        ("general_1", "natural_general", "She is grieving after the death of her mother.", "bare_1", "bare_to_general"),
        ("ambiguous_1", "natural_ambiguous", "She is trying to understand what her grief means and how to live with it.", "general_1", "general_to_ambiguous"),
        ("critical_1", "critical", "Since the death, she can barely sleep, work, or speak to anyone.", "general_1", "general_to_critical"),
        ("label_free_1", "label_free_theological", "In mourning, sorrow is brought to God in prayer and held with hope in the resurrection.", "general_1", "general_to_label_free_theological"),
        ("catholic_1", "explicit_catholic", "In Catholic life, sorrow in mourning is brought to God in prayer and held with hope in the resurrection.", "label_free_1", "label_free_to_explicit_catholic"),
        ("integrative_1", "integrative", "Grief may require psychological care while also being held in prayer and hope in the resurrection.", "general_1", "general_to_integrative"),
    ],
    "euthanasia_assisted_dying": [
        ("bare_1", "bare", "euthanasia", "", ""),
        ("general_1", "natural_general", "The patient requested medical assistance to end life because of unbearable suffering.", "bare_1", "bare_to_general"),
        ("ambiguous_1", "natural_ambiguous", "Is ending a patient's life an act of mercy or a violation of dignity?", "general_1", "general_to_ambiguous"),
        ("critical_1", "critical", "A terminally ill patient in severe pain asks the clinical team to help end life.", "general_1", "general_to_critical"),
        ("label_free_1", "label_free_theological", "Compassionate care should relieve suffering while refusing the intentional ending of innocent human life.", "general_1", "general_to_label_free_theological"),
        ("catholic_1", "explicit_catholic", "In Catholic teaching, compassionate care should relieve suffering while refusing the intentional ending of innocent human life.", "label_free_1", "label_free_to_explicit_catholic"),
        ("integrative_1", "integrative", "Palliative medicine can relieve severe suffering while respecting the person's dignity and refusing intentional killing.", "general_1", "general_to_integrative"),
    ],
    "grace_lexical": [
        ("bare_1", "bare", "grace", "", ""),
        ("general_1", "natural_general", "She moved across the stage with grace and elegance.", "bare_1", "bare_to_general"),
        ("ambiguous_1", "natural_ambiguous", "He spoke about receiving grace during a difficult time.", "general_1", "general_to_ambiguous"),
        ("label_free_1", "label_free_theological", "Human beings receive an unearned divine gift that heals and draws them into life with God.", "general_1", "general_to_label_free_theological"),
        ("catholic_1", "explicit_catholic", "In Catholic teaching, grace is the unearned divine gift that heals and draws human beings into life with God.", "label_free_1", "label_free_to_explicit_catholic"),
    ],
    "judgment_after_death_generic": [
        ("bare_1", "bare", "judgment after death", "", ""),
        ("general_1", "natural_general", "Many religions describe a judgment after death in which deeds are evaluated.", "bare_1", "bare_to_general"),
        ("ambiguous_1", "natural_ambiguous", "What might judgment after death mean for the way a person has lived?", "general_1", "general_to_ambiguous"),
        ("label_free_1", "label_free_theological", "After death each person faces judgment before God, where the truth of life is revealed in mercy and justice.", "general_1", "general_to_label_free_theological"),
        ("catholic_1", "explicit_catholic", "In Catholic teaching, after death each person faces particular judgment before God, where the truth of life is revealed in mercy and justice.", "label_free_1", "label_free_to_explicit_catholic"),
        ("integrative_1", "integrative", "Religions speak broadly of afterlife judgment, while Catholic doctrine describes a particular judgment before God.", "general_1", "general_to_integrative"),
    ],
}

FIXTURE_VALIDATION = {
    "death_biological": {
        "catholic": [
            "Christian hope faces bodily death through prayer and trust in resurrection with Christ.",
            "The dying person is accompanied with dignity before God and hope beyond death.",
        ],
        "comparison": [
            "Biological death is the irreversible end of the organism's integrated vital activity.",
            "Medical determination of death concerns permanent loss of vital bodily function.",
        ],
        "integrative": "Biological death ends bodily function while Christian faith also speaks of resurrection and communion with God.",
        "critical": "The clinical team says death is imminent and the family asks how to remain with the patient.",
    },
    "grief_psychological": {
        "catholic": [
            "Mourning is carried in prayer, consolation, and Christian hope of resurrection.",
            "The bereaved community brings sorrow before God and accompanies the grieving person in hope.",
        ],
        "comparison": [
            "Bereavement is a psychological response to loss that can disrupt sleep and concentration.",
            "Grief involves emotional adaptation and coping after the death of a loved person.",
        ],
        "integrative": "Psychological support for bereavement can accompany prayer, consolation, and hope in resurrection.",
        "critical": "After the loss, the grieving person cannot sleep, eat, work, or remain connected to friends.",
    },
    "euthanasia_assisted_dying": {
        "catholic": [
            "Compassion relieves suffering through care without intentionally causing the patient's death.",
            "Palliative accompaniment protects dignity and refuses the intentional killing of innocent life.",
        ],
        "comparison": [
            "Assisted dying is defended as an autonomous medical choice for ending intolerable suffering.",
            "Voluntary euthanasia permits a competent patient to request medical help to end life.",
        ],
        "integrative": "Palliative medicine treats severe pain while respecting dignity and refusing intentional killing.",
        "critical": "A terminal patient in severe distress asks the medical team to end life immediately.",
    },
    "grace_lexical": {
        "catholic": [
            "God's grace is a freely received divine gift that heals and sanctifies the person.",
            "Divine grace draws human beings into transforming communion with God.",
        ],
        "comparison": [
            "The dancer performed with elegance, balance, poise, and grace.",
            "Her graceful manner showed social charm, courtesy, and refinement.",
        ],
        "integrative": "The word grace can describe elegant movement or an unearned divine gift.",
    },
    "judgment_after_death_generic": {
        "catholic": [
            "Particular judgment reveals each person's life before God in mercy and justice.",
            "After death the person encounters Christ and answers personally before God.",
        ],
        "comparison": [
            "Many cultures imagine a cosmic afterlife tribunal assigning reward and punishment.",
            "Generic religious stories portray souls being evaluated after death.",
        ],
        "integrative": "General afterlife judgment imagery overlaps with but does not exhaust the doctrine of particular judgment before God.",
    },
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def sha256_text(text: str) -> str:
    return hashlib.sha256(text.encode("utf-8")).hexdigest()


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for chunk in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(chunk)
    return digest.hexdigest()


def slugify(value: str) -> str:
    cleaned = re.sub(r"[^A-Za-z0-9._-]+", "_", value.strip())
    return cleaned.strip("_") or "run"


def write_fixture(data_dir: Path, force: bool = False) -> None:
    data_dir.mkdir(parents=True, exist_ok=True)
    files = {name: data_dir / f"{name}.csv" for name in TABLE_COLUMNS}

    existing = [path for path in files.values() if path.exists()]
    if existing and not force:
        joined = "\n".join(f"  {path}" for path in existing)
        raise FileExistsError(
            "Fixture files already exist. Use --force to replace them:\n" + joined
        )

    comparison_rows = []
    for row in FIXTURE_COMPARISONS:
        enriched = dict(row)
        enriched["dataset_status"] = "synthetic_fixture"
        enriched["review_status"] = "fixture_only"
        comparison_rows.append(enriched)

    reference_rows = []
    for audit_id, groups in FIXTURE_REFERENCES.items():
        for group, texts in groups.items():
            prefix = "c" if group == "catholic" else "r"
            for index, text in enumerate(texts, start=1):
                reference_rows.append(
                    {
                        "reference_id": f"{audit_id}_{prefix}_{index}",
                        "audit_id": audit_id,
                        "reference_group": group,
                        "reference_text": text,
                        "source_title": "SYNTHETIC DEVELOPMENT FIXTURE — NOT EVIDENCE",
                        "source_location": "N/A",
                        "text_status": "synthetic_fixture",
                        "review_status": "fixture_only",
                        "review_notes": "Authored only to test the prototype pipeline.",
                    }
                )

    query_rows = []
    for audit_id, entries in FIXTURE_QUERIES.items():
        for suffix, condition, text, baseline_suffix, contrast_type in entries:
            query_rows.append(
                {
                    "query_id": f"{audit_id}_{suffix}",
                    "audit_id": audit_id,
                    "condition": condition,
                    "paraphrase_id": "p1",
                    "query_text": text,
                    "baseline_query_id": (
                        f"{audit_id}_{baseline_suffix}" if baseline_suffix else ""
                    ),
                    "contrast_type": contrast_type,
                    "review_status": "fixture_only",
                }
            )

    validation_rows = []
    for audit_id, groups in FIXTURE_VALIDATION.items():
        for group in ("catholic", "comparison"):
            for index, text in enumerate(groups[group], start=1):
                validation_rows.append(
                    {
                        "validation_id": f"{audit_id}_val_{group}_{index}",
                        "audit_id": audit_id,
                        "validation_stage": "clear_register",
                        "target_class": group,
                        "validation_text": text,
                        "ethical_review_status": "not_required_fixture",
                        "review_status": "fixture_only",
                        "review_notes": "Synthetic held-out text for code testing.",
                    }
                )

        validation_rows.append(
            {
                "validation_id": f"{audit_id}_val_integrative_1",
                "audit_id": audit_id,
                "validation_stage": "integrative",
                "target_class": "integrative",
                "validation_text": groups["integrative"],
                "ethical_review_status": "not_required_fixture",
                "review_status": "fixture_only",
                "review_notes": "Synthetic integrative text for code testing.",
            }
        )

        if groups.get("critical"):
            validation_rows.append(
                {
                    "validation_id": f"{audit_id}_val_critical_1",
                    "audit_id": audit_id,
                    "validation_stage": "critical",
                    "target_class": "critical_review",
                    "validation_text": groups["critical"],
                    "ethical_review_status": "required_before_real_benchmark",
                    "review_status": "fixture_only",
                    "review_notes": "Synthetic critical text requiring later ethical review.",
                }
            )

    tables = {
        "comparisons": pd.DataFrame(comparison_rows, columns=TABLE_COLUMNS["comparisons"]),
        "references": pd.DataFrame(reference_rows, columns=TABLE_COLUMNS["references"]),
        "queries": pd.DataFrame(query_rows, columns=TABLE_COLUMNS["queries"]),
        "validation": pd.DataFrame(validation_rows, columns=TABLE_COLUMNS["validation"]),
    }

    for name, frame in tables.items():
        frame.to_csv(files[name], index=False)

    print("Synthetic CTSB v3.4 fixture written:")
    for path in files.values():
        print(f"  {path}")
    print("WARNING: fixture texts are synthetic and are not theological evidence.")


def load_tables(data_dir: Path) -> Dict[str, pd.DataFrame]:
    tables: Dict[str, pd.DataFrame] = {}
    for name in TABLE_COLUMNS:
        path = data_dir / f"{name}.csv"
        if not path.exists():
            raise FileNotFoundError(f"Required prototype file not found: {path}")
        tables[name] = pd.read_csv(
            path,
            dtype=str,
            keep_default_na=False,
        ).fillna("")
    return tables


def _blank_values(frame: pd.DataFrame, column: str) -> int:
    return int(frame[column].astype(str).str.strip().eq("").sum())


def _check_allowed(
    frame: pd.DataFrame,
    column: str,
    allowed: set[str],
    table_name: str,
    errors: List[str],
) -> None:
    actual = {
        value.strip()
        for value in frame[column].astype(str)
        if value.strip()
    }
    invalid = sorted(actual - allowed)
    if invalid:
        errors.append(
            f"{table_name}.{column} contains invalid value(s): {invalid}"
        )


def validate_tables(
    tables: Mapping[str, pd.DataFrame],
    mode: str = "fixture",
) -> Dict[str, int]:
    errors: List[str] = []

    for table_name, required in TABLE_COLUMNS.items():
        if table_name not in tables:
            errors.append(f"Missing table: {table_name}")
            continue

        missing = sorted(set(required) - set(tables[table_name].columns))
        if missing:
            errors.append(f"{table_name}.csv is missing columns: {missing}")

    if errors:
        raise ValueError("Benchmark validation failed:\n- " + "\n- ".join(errors))

    comparisons = tables["comparisons"].copy()
    references = tables["references"].copy()
    queries = tables["queries"].copy()
    validation = tables["validation"].copy()

    id_columns = {
        "comparisons": (comparisons, "audit_id"),
        "references": (references, "reference_id"),
        "queries": (queries, "query_id"),
        "validation": (validation, "validation_id"),
    }

    for table_name, (frame, column) in id_columns.items():
        if _blank_values(frame, column):
            errors.append(f"{table_name}.{column} contains blank IDs.")
        duplicated = frame.loc[frame[column].duplicated(), column].tolist()
        if duplicated:
            errors.append(
                f"{table_name}.{column} contains duplicate IDs: {duplicated}"
            )

    for column in (
        "concept",
        "primary_locus",
        "comparison_register",
        "relationship_type",
        "inclusion_rationale",
    ):
        if _blank_values(comparisons, column):
            errors.append(f"comparisons.{column} contains blank values.")

    _check_allowed(
        comparisons,
        "relationship_type",
        RELATIONSHIP_TYPES,
        "comparisons",
        errors,
    )
    _check_allowed(
        references,
        "reference_group",
        REFERENCE_GROUPS,
        "references",
        errors,
    )
    _check_allowed(
        queries,
        "condition",
        QUERY_CONDITIONS,
        "queries",
        errors,
    )
    _check_allowed(
        validation,
        "validation_stage",
        VALIDATION_STAGES,
        "validation",
        errors,
    )

    for column in ("life_death_module", "critical_context_applicable"):
        invalid = sorted(
            {
                value.strip().lower()
                for value in comparisons[column]
                if value.strip().lower() not in {"true", "false"}
            }
        )
        if invalid:
            errors.append(
                f"comparisons.{column} contains invalid boolean values: {invalid}"
            )

    audit_ids = set(comparisons["audit_id"])
    for table_name, frame in (
        ("references", references),
        ("queries", queries),
        ("validation", validation),
    ):
        unknown = sorted(set(frame["audit_id"]) - audit_ids)
        if unknown:
            errors.append(
                f"{table_name}.audit_id contains unknown audit IDs: {unknown}"
            )

    if _blank_values(references, "reference_text"):
        errors.append("references.reference_text contains blank text.")
    if _blank_values(queries, "query_text"):
        errors.append("queries.query_text contains blank text.")
    if _blank_values(validation, "validation_text"):
        errors.append("validation.validation_text contains blank text.")

    for audit_id in sorted(audit_ids):
        subset = references[references["audit_id"] == audit_id]
        counts = Counter(subset["reference_group"])
        for group in sorted(REFERENCE_GROUPS):
            if counts[group] < 2:
                errors.append(
                    f"{audit_id} requires at least two {group} references."
                )

    query_audit = dict(zip(queries["query_id"], queries["audit_id"]))
    for row in queries.itertuples(index=False):
        baseline = row.baseline_query_id.strip()
        if not baseline:
            continue
        if baseline not in query_audit:
            errors.append(
                f"{row.query_id} has unknown baseline_query_id={baseline}."
            )
        elif query_audit[baseline] != row.audit_id:
            errors.append(
                f"{row.query_id} and baseline {baseline} belong to different audits."
            )
        if baseline == row.query_id:
            errors.append(f"{row.query_id} cannot use itself as a baseline.")
        if not row.contrast_type.strip():
            errors.append(
                f"{row.query_id} has a baseline but no contrast_type."
            )

    for row in queries.itertuples(index=False):
        lowered = row.query_text.lower()
        if row.condition == "label_free_theological" and "catholic" in lowered:
            errors.append(
                f"{row.query_id} is label-free but contains the word Catholic."
            )
        if row.condition == "explicit_catholic" and "catholic" not in lowered:
            errors.append(
                f"{row.query_id} is explicit_catholic but lacks the Catholic label."
            )

    critical_allowed = {
        row.audit_id: row.critical_context_applicable.lower() == "true"
        for row in comparisons.itertuples(index=False)
    }
    for row in queries.itertuples(index=False):
        if row.condition == "critical" and not critical_allowed.get(row.audit_id, False):
            errors.append(
                f"{row.query_id} uses a critical condition not declared applicable."
            )

    for row in validation.itertuples(index=False):
        if (
            row.validation_stage == "clear_register"
            and row.target_class not in CLEAR_TARGETS
        ):
            errors.append(
                f"{row.validation_id} has invalid clear-register target {row.target_class}."
            )
        if (
            row.validation_stage == "integrative"
            and row.target_class != "integrative"
        ):
            errors.append(
                f"{row.validation_id} must use target_class=integrative."
            )
        if (
            row.validation_stage == "critical"
            and row.target_class != "critical_review"
        ):
            errors.append(
                f"{row.validation_id} must use target_class=critical_review."
            )

    for audit_id in sorted(audit_ids):
        clear = validation[
            (validation["audit_id"] == audit_id)
            & (validation["validation_stage"] == "clear_register")
        ]
        targets = set(clear["target_class"])
        if targets != CLEAR_TARGETS:
            errors.append(
                f"{audit_id} needs held-out Catholic and comparison clear-register texts."
            )

    if mode == "benchmark":
        for row in references.itertuples(index=False):
            source = row.source_title.strip()
            location = row.source_location.strip()
            if not source or source.startswith("SYNTHETIC DEVELOPMENT FIXTURE"):
                errors.append(
                    f"{row.reference_id} lacks a real identifiable source."
                )
            if not location or location == "N/A":
                errors.append(
                    f"{row.reference_id} lacks a real source location."
                )
            if row.text_status == "synthetic_fixture":
                errors.append(
                    f"{row.reference_id} is synthetic and cannot be used in benchmark mode."
                )

    if errors:
        raise ValueError("Benchmark validation failed:\n- " + "\n- ".join(errors))

    return {
        "audits": len(comparisons),
        "references": len(references),
        "queries": len(queries),
        "validation_texts": len(validation),
        "clear_validation_texts": int(
            (validation["validation_stage"] == "clear_register").sum()
        ),
    }


def collect_text_roles(
    tables: Mapping[str, pd.DataFrame],
) -> Dict[str, set[str]]:
    roles: Dict[str, set[str]] = defaultdict(set)

    for row in tables["references"].itertuples(index=False):
        roles[row.reference_text].add(f"reference:{row.reference_group}")
    for row in tables["queries"].itertuples(index=False):
        roles[row.query_text].add(f"query:{row.condition}")
    for row in tables["validation"].itertuples(index=False):
        roles[row.validation_text].add(
            f"validation:{row.validation_stage}:{row.target_class}"
        )

    return roles


def token_features(text: str) -> List[Tuple[str, float]]:
    tokens = re.findall(r"[a-z0-9']+", text.lower())
    features: List[Tuple[str, float]] = []

    for token in tokens:
        features.append((f"tok:{token}", 1.0))
        padded = f"^{token}$"
        for index in range(max(0, len(padded) - 2)):
            features.append((f"chr:{padded[index:index + 3]}", 0.15))

    for left, right in zip(tokens, tokens[1:]):
        features.append((f"bigram:{left}_{right}", 0.60))

    return features


def deterministic_fixture_embeddings(
    texts: Sequence[str],
    dimensions: int = 512,
) -> Dict[str, np.ndarray]:
    embeddings: Dict[str, np.ndarray] = {}

    for text in texts:
        vector = np.zeros(dimensions, dtype=np.float64)
        for feature, weight in token_features(text):
            digest = hashlib.sha256(feature.encode("utf-8")).digest()
            index = int.from_bytes(digest[:8], "big") % dimensions
            sign = 1.0 if digest[8] % 2 == 0 else -1.0
            vector[index] += sign * weight

        norm = float(np.linalg.norm(vector))
        if norm == 0.0:
            vector[0] = 1.0
            norm = 1.0
        embeddings[text] = vector / norm

    return embeddings


def embedding_cache_key(config: Mapping[str, object], text: str) -> str:
    payload = {
        "config": dict(config),
        "text": text,
    }
    encoded = json.dumps(
        payload,
        ensure_ascii=False,
        sort_keys=True,
        separators=(",", ":"),
    )
    return sha256_text(encoded)


def load_json_cache(path: Path) -> Dict[str, dict]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_json_cache(path: Path, cache: Mapping[str, dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    temporary = path.with_suffix(path.suffix + ".tmp")
    temporary.write_text(
        json.dumps(cache, ensure_ascii=False),
        encoding="utf-8",
    )
    temporary.replace(path)


def azure_embeddings(
    texts: Sequence[str],
    cache_path: Path,
    env_file: Path,
    batch_size: int = 64,
    dimensions: int = 0,
) -> Tuple[Dict[str, np.ndarray], dict]:
    try:
        from dotenv import load_dotenv
        from openai import AzureOpenAI
    except ImportError as exc:
        raise RuntimeError(
            "Azure dependencies are missing. Install requirements.txt."
        ) from exc

    load_dotenv(env_file)

    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

    if not api_key:
        raise ValueError("AZURE_OPENAI_API_KEY was not found.")
    if not endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT was not found.")
    if not deployment:
        raise ValueError("AZURE_OPENAI_EMBEDDING_DEPLOYMENT was not found.")

    config = {
        "provider": "azure_openai",
        "requested_model": "text-embedding-3-large",
        "deployment": deployment,
        "api_version": api_version,
        "dimensions": dimensions or "provider_default",
    }

    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=endpoint,
    )

    cache = load_json_cache(cache_path)
    missing = [
        text
        for text in texts
        if embedding_cache_key(config, text) not in cache
    ]

    if missing:
        print(
            f"Embedding {len(missing)} new text(s) through Azure deployment "
            f"{deployment}."
        )
    else:
        print("All Azure embeddings were found in the active v3.4 cache.")

    response_model = ""
    for start in range(0, len(missing), batch_size):
        batch = missing[start:start + batch_size]
        kwargs = {
            "input": batch,
            "model": deployment,
        }
        if dimensions > 0:
            kwargs["dimensions"] = dimensions

        response = client.embeddings.create(**kwargs)
        response_model = str(getattr(response, "model", "") or "")
        items = sorted(response.data, key=lambda item: item.index)

        if len(items) != len(batch):
            raise RuntimeError("Azure returned an unexpected embedding count.")

        for text, item in zip(batch, items):
            key = embedding_cache_key(config, text)
            cache[key] = {
                "config": config,
                "text": text,
                "embedding": item.embedding,
                "created_at": utc_now(),
            }

        save_json_cache(cache_path, cache)
        print(
            f"  Completed batch {start // batch_size + 1} of "
            f"{math.ceil(len(missing) / batch_size)}."
        )

    embeddings = {
        text: np.asarray(
            cache[embedding_cache_key(config, text)]["embedding"],
            dtype=np.float64,
        )
        for text in texts
    }

    metadata = dict(config)
    metadata["response_model"] = response_model
    metadata["embedding_dimensions"] = int(
        len(next(iter(embeddings.values())))
    )
    metadata["new_embeddings"] = len(missing)
    metadata["cached_embeddings"] = len(texts) - len(missing)
    return embeddings, metadata


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denominator = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denominator == 0.0:
        raise ValueError("Cosine similarity received a zero vector.")
    return float(np.dot(a, b) / denominator)


def score_items(
    items: pd.DataFrame,
    item_type: str,
    id_column: str,
    text_column: str,
    context_column: str,
    references: pd.DataFrame,
    comparisons: pd.DataFrame,
    embeddings: Mapping[str, np.ndarray],
) -> Tuple[pd.DataFrame, pd.DataFrame]:
    comparison_lookup = comparisons.set_index("audit_id").to_dict("index")
    references_by_audit = {
        audit_id: subset.copy()
        for audit_id, subset in references.groupby("audit_id", sort=False)
    }

    similarity_rows: List[dict] = []
    summary_rows: List[dict] = []

    for row in items.to_dict("records"):
        audit_id = row["audit_id"]
        text = row[text_column]
        item_id = row[id_column]
        context = row[context_column]
        metadata = comparison_lookup[audit_id]
        audit_references = references_by_audit[audit_id]

        scored: List[Tuple[dict, float]] = []
        for reference in audit_references.to_dict("records"):
            similarity = cosine(
                embeddings[text],
                embeddings[reference["reference_text"]],
            )
            scored.append((reference, similarity))

        scored.sort(key=lambda pair: (-pair[1], pair[0]["reference_id"]))
        group_counters: Counter = Counter()

        for overall_rank, (reference, similarity) in enumerate(scored, start=1):
            group = reference["reference_group"]
            group_counters[group] += 1
            similarity_rows.append(
                {
                    "item_type": item_type,
                    "item_id": item_id,
                    "audit_id": audit_id,
                    "concept": metadata["concept"],
                    "context": context,
                    "item_text": text,
                    "reference_id": reference["reference_id"],
                    "reference_group": group,
                    "reference_text": reference["reference_text"],
                    "cosine_similarity": similarity,
                    "within_audit_rank": overall_rank,
                    "within_group_rank": group_counters[group],
                    "source_title": reference["source_title"],
                    "source_location": reference["source_location"],
                    "text_status": reference["text_status"],
                }
            )

        catholic = [
            similarity
            for reference, similarity in scored
            if reference["reference_group"] == "catholic"
        ]
        comparison = [
            similarity
            for reference, similarity in scored
            if reference["reference_group"] == "comparison"
        ]

        s_c = float(np.mean(catholic))
        s_r = float(np.mean(comparison))
        cas = s_c - s_r

        top_reference, top_similarity = scored[0]
        nearest_catholic = next(
            pair for pair in scored if pair[0]["reference_group"] == "catholic"
        )
        nearest_comparison = next(
            pair for pair in scored if pair[0]["reference_group"] == "comparison"
        )

        overall_rank_lookup = {
            reference["reference_id"]: rank
            for rank, (reference, _) in enumerate(scored, start=1)
        }

        summary_rows.append(
            {
                "item_type": item_type,
                "item_id": item_id,
                "audit_id": audit_id,
                "concept": metadata["concept"],
                "primary_locus": metadata["primary_locus"],
                "life_death_module": metadata["life_death_module"],
                "comparison_register": metadata["comparison_register"],
                "relationship_type": metadata["relationship_type"],
                "context": context,
                "item_text": text,
                "s_c": s_c,
                "s_r": s_r,
                "cas": cas,
                "top_reference_id": top_reference["reference_id"],
                "top_reference_group": top_reference["reference_group"],
                "top_reference_text": top_reference["reference_text"],
                "top_reference_similarity": top_similarity,
                "nearest_catholic_reference_id": nearest_catholic[0]["reference_id"],
                "nearest_catholic_reference_text": nearest_catholic[0]["reference_text"],
                "nearest_catholic_similarity": nearest_catholic[1],
                "nearest_catholic_rank": overall_rank_lookup[
                    nearest_catholic[0]["reference_id"]
                ],
                "nearest_comparison_reference_id": nearest_comparison[0]["reference_id"],
                "nearest_comparison_reference_text": nearest_comparison[0]["reference_text"],
                "nearest_comparison_similarity": nearest_comparison[1],
                "nearest_comparison_rank": overall_rank_lookup[
                    nearest_comparison[0]["reference_id"]
                ],
            }
        )

    return (
        pd.DataFrame(similarity_rows),
        pd.DataFrame(summary_rows),
    )


def make_query_scores(
    generic_scores: pd.DataFrame,
    queries: pd.DataFrame,
) -> pd.DataFrame:
    metadata = queries[
        [
            "query_id",
            "paraphrase_id",
            "baseline_query_id",
            "contrast_type",
            "review_status",
        ]
    ].copy()

    scores = generic_scores.rename(
        columns={
            "item_id": "query_id",
            "context": "condition",
            "item_text": "query_text",
        }
    ).drop(columns=["item_type"])

    return scores.merge(metadata, on="query_id", how="left", validate="one_to_one")


def make_validation_scores(
    generic_scores: pd.DataFrame,
    validation: pd.DataFrame,
) -> pd.DataFrame:
    metadata = validation[
        [
            "validation_id",
            "target_class",
            "ethical_review_status",
            "review_status",
            "review_notes",
        ]
    ].copy()

    scores = generic_scores.rename(
        columns={
            "item_id": "validation_id",
            "context": "validation_stage",
            "item_text": "validation_text",
        }
    ).drop(columns=["item_type"])

    return scores.merge(
        metadata,
        on="validation_id",
        how="left",
        validate="one_to_one",
    )


def make_condition_summary(query_scores: pd.DataFrame) -> pd.DataFrame:
    group_columns = [
        "audit_id",
        "concept",
        "primary_locus",
        "life_death_module",
        "comparison_register",
        "relationship_type",
        "condition",
    ]

    return (
        query_scores.groupby(group_columns, sort=False, dropna=False)
        .agg(
            query_count=("query_id", "count"),
            mean_s_c=("s_c", "mean"),
            mean_s_r=("s_r", "mean"),
            mean_cas=("cas", "mean"),
            median_cas=("cas", "median"),
        )
        .reset_index()
    )


def make_shifts(query_scores: pd.DataFrame) -> pd.DataFrame:
    lookup = query_scores.set_index("query_id").to_dict("index")
    rows: List[dict] = []

    for target in query_scores.to_dict("records"):
        baseline_id = str(target.get("baseline_query_id", "")).strip()
        if not baseline_id:
            continue

        baseline = lookup[baseline_id]
        delta_s_c = target["s_c"] - baseline["s_c"]
        delta_s_r = target["s_r"] - baseline["s_r"]
        delta_cas = target["cas"] - baseline["cas"]
        identity_error = delta_cas - (delta_s_c - delta_s_r)

        rows.append(
            {
                "audit_id": target["audit_id"],
                "concept": target["concept"],
                "comparison_register": target["comparison_register"],
                "relationship_type": target["relationship_type"],
                "contrast_type": target["contrast_type"],
                "baseline_query_id": baseline_id,
                "baseline_condition": baseline["condition"],
                "baseline_query_text": baseline["query_text"],
                "target_query_id": target["query_id"],
                "target_condition": target["condition"],
                "target_query_text": target["query_text"],
                "baseline_s_c": baseline["s_c"],
                "target_s_c": target["s_c"],
                "delta_s_c": delta_s_c,
                "baseline_s_r": baseline["s_r"],
                "target_s_r": target["s_r"],
                "delta_s_r": delta_s_r,
                "baseline_cas": baseline["cas"],
                "target_cas": target["cas"],
                "delta_cas": delta_cas,
                "decomposition_identity_error": identity_error,
            }
        )

    shifts = pd.DataFrame(rows)
    if not shifts.empty:
        maximum_error = float(
            shifts["decomposition_identity_error"].abs().max()
        )
        if maximum_error > 1e-10:
            raise RuntimeError(
                "Shift decomposition identity failed: "
                f"maximum error={maximum_error}"
            )
    return shifts


def safe_divide(numerator: float, denominator: float) -> float:
    if denominator == 0:
        return float("nan")
    return float(numerator / denominator)


def class_f1(
    actual: pd.Series,
    predicted: pd.Series,
    positive_label: str,
) -> Tuple[float, float, float]:
    true_positive = int(
        ((actual == positive_label) & (predicted == positive_label)).sum()
    )
    false_positive = int(
        ((actual != positive_label) & (predicted == positive_label)).sum()
    )
    false_negative = int(
        ((actual == positive_label) & (predicted != positive_label)).sum()
    )

    precision = safe_divide(true_positive, true_positive + false_positive)
    recall = safe_divide(true_positive, true_positive + false_negative)

    if math.isnan(precision) or math.isnan(recall) or precision + recall == 0:
        f1 = 0.0
    else:
        f1 = 2 * precision * recall / (precision + recall)

    return precision, recall, float(f1)


def make_validation_metrics(
    validation_scores: pd.DataFrame,
) -> pd.DataFrame:
    clear = validation_scores[
        validation_scores["validation_stage"] == "clear_register"
    ].copy()

    clear["predicted_class"] = np.where(
        clear["cas"] >= 0,
        "catholic",
        "comparison",
    )

    rows: List[dict] = []
    groups: List[Tuple[str, pd.DataFrame]] = [
        (audit_id, subset)
        for audit_id, subset in clear.groupby("audit_id", sort=False)
    ]
    groups.append(("ALL_AUDITS", clear))

    for scope, subset in groups:
        actual = subset["target_class"]
        predicted = subset["predicted_class"]

        catholic_precision, catholic_recall, catholic_f1 = class_f1(
            actual,
            predicted,
            "catholic",
        )
        comparison_precision, comparison_recall, comparison_f1 = class_f1(
            actual,
            predicted,
            "comparison",
        )

        balanced_accuracy = float(
            np.nanmean([catholic_recall, comparison_recall])
        )
        macro_f1 = float(np.nanmean([catholic_f1, comparison_f1]))

        rows.append(
            {
                "scope": scope,
                "n": len(subset),
                "classification_rule": "CAS >= 0 predicts catholic; CAS < 0 predicts comparison",
                "balanced_accuracy": balanced_accuracy,
                "catholic_precision": catholic_precision,
                "catholic_recall": catholic_recall,
                "catholic_f1": catholic_f1,
                "comparison_precision": comparison_precision,
                "comparison_recall": comparison_recall,
                "comparison_f1": comparison_f1,
                "macro_f1": macro_f1,
                "actual_catholic_predicted_catholic": int(
                    ((actual == "catholic") & (predicted == "catholic")).sum()
                ),
                "actual_catholic_predicted_comparison": int(
                    ((actual == "catholic") & (predicted == "comparison")).sum()
                ),
                "actual_comparison_predicted_catholic": int(
                    ((actual == "comparison") & (predicted == "catholic")).sum()
                ),
                "actual_comparison_predicted_comparison": int(
                    ((actual == "comparison") & (predicted == "comparison")).sum()
                ),
            }
        )

    metrics = pd.DataFrame(rows)
    return metrics


def make_embedding_files(
    tables: Mapping[str, pd.DataFrame],
    embeddings: Mapping[str, np.ndarray],
    output_dir: Path,
) -> Tuple[Path, Path]:
    roles = collect_text_roles(tables)
    rows: List[dict] = []
    arrays: Dict[str, np.ndarray] = {}

    for index, text in enumerate(sorted(embeddings), start=1):
        embedding_id = f"embedding_{index:05d}"
        vector = np.asarray(embeddings[text], dtype=np.float32)
        arrays[embedding_id] = vector
        rows.append(
            {
                "embedding_id": embedding_id,
                "text_sha256": sha256_text(text),
                "text": text,
                "roles": " | ".join(sorted(roles[text])),
                "dimensions": len(vector),
                "l2_norm": float(np.linalg.norm(vector)),
            }
        )

    index_path = output_dir / "embedding_index.csv"
    vectors_path = output_dir / "embeddings.npz"
    pd.DataFrame(rows).to_csv(index_path, index=False)
    np.savez_compressed(vectors_path, **arrays)
    return index_path, vectors_path


def run_pipeline(
    data_dir: Path,
    output_dir: Path,
    backend: str = "mock",
    mode: str = "fixture",
    cache_path: Optional[Path] = None,
    env_file: Optional[Path] = None,
    batch_size: int = 64,
    dimensions: int = 0,
) -> Dict[str, object]:
    tables = load_tables(data_dir)
    validation_summary = validate_tables(tables, mode=mode)
    output_dir.mkdir(parents=True, exist_ok=True)

    text_roles = collect_text_roles(tables)
    texts = sorted(text_roles)

    if backend == "mock":
        mock_dimensions = dimensions if dimensions > 0 else 512
        embeddings = deterministic_fixture_embeddings(
            texts,
            dimensions=mock_dimensions,
        )
        model_metadata = {
            "provider": "local_fixture",
            "requested_model": "deterministic lexical hashing fixture",
            "deployment": "none",
            "api_version": "none",
            "embedding_dimensions": mock_dimensions,
            "new_embeddings": len(texts),
            "cached_embeddings": 0,
        }
    elif backend == "azure":
        if cache_path is None:
            cache_path = ROOT / "outputs" / "v3_4" / "embedding_cache.json"
        if env_file is None:
            env_file = ROOT / ".env"
        embeddings, model_metadata = azure_embeddings(
            texts,
            cache_path=cache_path,
            env_file=env_file,
            batch_size=batch_size,
            dimensions=dimensions,
        )
    else:
        raise ValueError(f"Unknown backend: {backend}")

    query_similarities, generic_query_scores = score_items(
        tables["queries"],
        item_type="query",
        id_column="query_id",
        text_column="query_text",
        context_column="condition",
        references=tables["references"],
        comparisons=tables["comparisons"],
        embeddings=embeddings,
    )
    validation_similarities, generic_validation_scores = score_items(
        tables["validation"],
        item_type="validation",
        id_column="validation_id",
        text_column="validation_text",
        context_column="validation_stage",
        references=tables["references"],
        comparisons=tables["comparisons"],
        embeddings=embeddings,
    )

    query_scores = make_query_scores(
        generic_query_scores,
        tables["queries"],
    )
    validation_scores = make_validation_scores(
        generic_validation_scores,
        tables["validation"],
    )
    condition_summary = make_condition_summary(query_scores)
    shifts = make_shifts(query_scores)
    validation_metrics = make_validation_metrics(validation_scores)

    clear_mask = validation_scores["validation_stage"] == "clear_register"
    validation_scores["predicted_class"] = ""
    validation_scores.loc[clear_mask, "predicted_class"] = np.where(
        validation_scores.loc[clear_mask, "cas"] >= 0,
        "catholic",
        "comparison",
    )

    similarities = pd.concat(
        [query_similarities, validation_similarities],
        ignore_index=True,
    )

    output_frames = {
        "similarities.csv": similarities,
        "query_scores.csv": query_scores,
        "condition_summary.csv": condition_summary,
        "shifts.csv": shifts,
        "validation_scores.csv": validation_scores,
        "validation_metrics.csv": validation_metrics,
    }

    for filename, frame in output_frames.items():
        frame.to_csv(output_dir / filename, index=False)

    make_embedding_files(
        tables,
        embeddings,
        output_dir,
    )

    input_hashes = {
        f"{name}.csv": sha256_file(data_dir / f"{name}.csv")
        for name in TABLE_COLUMNS
    }

    output_hashes = {
        path.name: sha256_file(path)
        for path in sorted(output_dir.iterdir())
        if path.is_file() and path.name != "run_manifest.json"
    }

    manifest = {
        "methodology_version": "CTSB v3.4",
        "implementation_stage": "synthetic development prototype",
        "evidential_status": "NON-EVIDENTIAL CODE FIXTURE",
        "warning": (
            "Synthetic fixture references and mock-backend scores must not be "
            "presented as theological or model-audit evidence."
        ),
        "generated_at_utc": utc_now(),
        "backend": backend,
        "mode": mode,
        "data_directory": str(data_dir.resolve()),
        "output_directory": str(output_dir.resolve()),
        "model_metadata": model_metadata,
        "input_counts": validation_summary,
        "unique_embedded_texts": len(texts),
        "input_file_sha256": input_hashes,
        "output_file_sha256": output_hashes,
        "cas_definition": "CAS = S_C - S_R",
        "shift_definition": "Delta CAS = Delta S_C - Delta S_R",
        "clear_validation_rule": (
            "Provisional prototype rule: CAS >= 0 predicts Catholic; "
            "CAS < 0 predicts comparison."
        ),
    }

    manifest_path = output_dir / "run_manifest.json"
    manifest_path.write_text(
        json.dumps(manifest, ensure_ascii=False, indent=2) + "\n",
        encoding="utf-8",
    )

    return {
        "output_dir": output_dir,
        "manifest_path": manifest_path,
        "query_scores_path": output_dir / "query_scores.csv",
        "shifts_path": output_dir / "shifts.csv",
        "validation_metrics_path": output_dir / "validation_metrics.csv",
        "validation_summary": validation_summary,
    }


def build_parser() -> argparse.ArgumentParser:
    parser = argparse.ArgumentParser(
        description=(
            "CTSB v3.4 lean development prototype. Synthetic fixture results "
            "are non-evidential and must not be presented as theological findings."
        )
    )

    subparsers = parser.add_subparsers(dest="command", required=True)

    write_parser = subparsers.add_parser(
        "write-fixture",
        help="Write the five-audit synthetic development fixture.",
    )
    write_parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "data" / "benchmarks" / "v3_4" / "prototype",
    )
    write_parser.add_argument(
        "--force",
        action="store_true",
        help="Replace existing fixture CSV files.",
    )

    validate_parser = subparsers.add_parser(
        "validate",
        help="Validate the four prototype CSV files without embedding them.",
    )
    validate_parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "data" / "benchmarks" / "v3_4" / "prototype",
    )
    validate_parser.add_argument(
        "--mode",
        choices=["fixture", "benchmark"],
        default="fixture",
        help=(
            "Fixture mode permits clearly marked synthetic references. "
            "Benchmark mode requires real source provenance."
        ),
    )

    run_parser = subparsers.add_parser(
        "run",
        help="Run the complete prototype scoring pipeline.",
    )
    run_parser.add_argument(
        "--data-dir",
        type=Path,
        default=ROOT / "data" / "benchmarks" / "v3_4" / "prototype",
    )
    run_parser.add_argument(
        "--output-root",
        type=Path,
        default=ROOT / "outputs" / "v3_4" / "prototype_runs",
    )
    run_parser.add_argument(
        "--run-id",
        default="",
        help="Optional run ID. A timestamped ID is used by default.",
    )
    run_parser.add_argument(
        "--backend",
        choices=["mock", "azure"],
        default="mock",
        help=(
            "The mock backend is deterministic and tests code only. "
            "The Azure backend calls the configured embedding deployment."
        ),
    )
    run_parser.add_argument(
        "--mode",
        choices=["fixture", "benchmark"],
        default="fixture",
    )
    run_parser.add_argument(
        "--cache",
        type=Path,
        default=ROOT / "outputs" / "v3_4" / "embedding_cache.json",
    )
    run_parser.add_argument(
        "--env-file",
        type=Path,
        default=ROOT / ".env",
    )
    run_parser.add_argument(
        "--batch-size",
        type=int,
        default=64,
    )
    run_parser.add_argument(
        "--dimensions",
        type=int,
        default=0,
        help=(
            "Mock-vector dimensions or optional Azure dimensions. "
            "Zero uses 512 for mock and the provider default for Azure."
        ),
    )

    return parser


def main() -> None:
    parser = build_parser()
    args = parser.parse_args()

    if args.command == "write-fixture":
        write_fixture(
            data_dir=args.data_dir,
            force=args.force,
        )
        return

    if args.command == "validate":
        tables = load_tables(args.data_dir)
        summary = validate_tables(tables, mode=args.mode)

        print("")
        print("CTSB v3.4 prototype data validation passed.")
        print(f"Mode: {args.mode}")
        for key, value in summary.items():
            print(f"{key}: {value}")

        if args.mode == "fixture":
            print("")
            print(
                "WARNING: synthetic fixture texts are suitable only for "
                "testing code and data flow."
            )
        return

    if args.command == "run":
        run_id = args.run_id.strip()
        if not run_id:
            timestamp = datetime.now().strftime("%Y%m%d-%H%M%S")
            run_id = f"{args.backend}_{timestamp}"

        safe_run_id = slugify(run_id)
        output_dir = args.output_root / safe_run_id

        if output_dir.exists() and any(output_dir.iterdir()):
            raise FileExistsError(
                "The requested run directory already contains files:\n"
                f"  {output_dir}\n"
                "Use a new --run-id."
            )

        result = run_pipeline(
            data_dir=args.data_dir,
            output_dir=output_dir,
            backend=args.backend,
            mode=args.mode,
            cache_path=args.cache,
            env_file=args.env_file,
            batch_size=args.batch_size,
            dimensions=args.dimensions,
        )

        metrics = pd.read_csv(result["validation_metrics_path"])
        overall = metrics[metrics["scope"] == "ALL_AUDITS"]

        print("")
        print("CTSB v3.4 prototype run completed.")
        print(f"Backend: {args.backend}")
        print(f"Mode: {args.mode}")
        print(f"Output directory: {result['output_dir']}")
        print(f"Run manifest: {result['manifest_path']}")
        print(f"Query scores: {result['query_scores_path']}")
        print(f"Shift decomposition: {result['shifts_path']}")
        print(f"Validation metrics: {result['validation_metrics_path']}")

        if not overall.empty:
            row = overall.iloc[0]
            print("")
            print("Synthetic clear-register fixture check:")
            print(f"  n: {int(row['n'])}")
            print(
                "  balanced accuracy: "
                f"{float(row['balanced_accuracy']):.4f}"
            )
            print(f"  macro F1: {float(row['macro_f1']):.4f}")

        print("")
        print(
            "WARNING: this is a non-evidential development run. "
            "Do not interpret fixture scores as findings about Catholic "
            "theology or the Azure/OpenAI model."
        )
        return

    parser.error(f"Unknown command: {args.command}")


if __name__ == "__main__":
    main()
