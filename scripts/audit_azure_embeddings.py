#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import math
import os
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Optional
import html as html_lib

import numpy as np
import pandas as pd
from dotenv import load_dotenv
from openai import AzureOpenAI
import plotly.graph_objects as go
import plotly.io as pio

try:
    import umap
except Exception as exc:
    raise RuntimeError("Could not import umap. Install dependencies with: pip install -r requirements.txt") from exc

try:
    from scipy import stats as scipy_stats
except Exception:
    scipy_stats = None


ROOT = Path(__file__).resolve().parents[1]

MODEL_METADATA = {
    "model_name": "text-embedding-3-large",
    "model_version": "1",
    "life_cycle_status": "GenerallyAvailable",
    "date_created": "Jan 25, 2024 1:00 AM",
    "date_updated": "Jan 25, 2024 1:00 AM",
    "model_retirement_date": "Apr 15, 2027 2:00 AM",
}

CONDITION_ORDER = ["bare", "ordinary", "academic", "catholic"]
PRIMARY_SHIFT = "ordinary_to_catholic_shift"

LOCUS_COLORS = {
    "Sin Grace and Redemption": "#ef4444",
    "Love Communion and Sacramentality": "#3b82f6",
    "Human Dignity and Theological Anthropology": "#22c55e",
    "Freedom Truth and Moral Teleology": "#a855f7",
}

CONDITION_COLORS = {
    "bare": "#94a3b8",
    "ordinary": "#f97316",
    "academic": "#38bdf8",
    "catholic": "#22c55e",
    "bare_to_catholic_shift": "#facc15",
    "ordinary_to_catholic_shift": "#f59e0b",
    "academic_to_catholic_shift": "#ec4899",
}


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


def display_path(path: Path) -> str:
    try:
        rel = path.resolve().relative_to(ROOT.resolve())
        return "/" + ROOT.name + "/" + rel.as_posix()
    except Exception:
        return "/" + ROOT.name + "/" + path.name


def parse_descriptors(value: str) -> List[str]:
    if pd.isna(value):
        return []
    return [part.strip() for part in str(value).split("||") if part.strip()]


def cache_key(deployment: str, text: str) -> str:
    return hashlib.sha256(f"{deployment}\n{text}".encode("utf-8")).hexdigest()


def load_cache(path: Path) -> Dict[str, dict]:
    if not path.exists():
        return {}
    return json.loads(path.read_text(encoding="utf-8"))


def save_cache(path: Path, cache: Dict[str, dict]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(cache, ensure_ascii=False), encoding="utf-8")


def cosine(a: np.ndarray, b: np.ndarray) -> float:
    denom = float(np.linalg.norm(a) * np.linalg.norm(b))
    if denom == 0.0:
        return float("nan")
    return float(np.dot(a, b) / denom)


def embed_texts(
    texts: List[str],
    client: AzureOpenAI,
    deployment: str,
    cache: Dict[str, dict],
    cache_path: Optional[Path] = None,
    batch_size: int = 64,
) -> Dict[str, np.ndarray]:
    unique_texts = list(dict.fromkeys([t.strip() for t in texts if t and t.strip()]))
    missing = [t for t in unique_texts if cache_key(deployment, t) not in cache]

    if missing:
        print(f"Embedding {len(missing)} new strings through Azure deployment: {deployment}")
    else:
        print("All required embeddings found in local cache.")

    for start in range(0, len(missing), batch_size):
        batch = missing[start : start + batch_size]
        response = client.embeddings.create(input=batch, model=deployment)
        for text, item in zip(batch, response.data):
            key = cache_key(deployment, text)
            cache[key] = {
                "deployment": deployment,
                "text": text,
                "embedding": item.embedding,
                "created_at": utc_now(),
            }
        if cache_path is not None:
            save_cache(cache_path, cache)
        if missing:
            print(f"  Embedded batch {start // batch_size + 1} / {math.ceil(len(missing) / batch_size)}")

    return {
        text: np.array(cache[cache_key(deployment, text)]["embedding"], dtype=np.float32)
        for text in unique_texts
    }


def rank_descriptors(
    query_vec: np.ndarray,
    catholic_desc: List[str],
    secular_desc: List[str],
    embeddings: Dict[str, np.ndarray],
) -> List[dict]:
    ranked = []
    for descriptor in catholic_desc:
        ranked.append({
            "descriptor": descriptor,
            "descriptor_group": "catholic",
            "similarity": cosine(query_vec, embeddings[descriptor]),
        })
    for descriptor in secular_desc:
        ranked.append({
            "descriptor": descriptor,
            "descriptor_group": "secular",
            "similarity": cosine(query_vec, embeddings[descriptor]),
        })
    ranked.sort(key=lambda row: row["similarity"], reverse=True)
    for idx, row in enumerate(ranked, start=1):
        row["rank"] = idx
    return ranked


def evaluate_benchmark(df: pd.DataFrame, embeddings: Dict[str, np.ndarray]) -> pd.DataFrame:
    records = []

    for _, row in df.iterrows():
        locus = str(row["locus"]).strip()
        concept = str(row["concept"]).strip()
        concept_type = str(row.get("concept_type", "unspecified")).strip()
        ambiguity_level = str(row.get("ambiguity_level", "unspecified")).strip()
        condition = str(row["query_condition"]).strip()
        query_template_id = str(row.get("query_template_id", "")).strip()
        query = str(row["query"]).strip()

        catholic_desc = parse_descriptors(row["catholic_descriptors"])
        secular_desc = parse_descriptors(row["secular_descriptors"])

        if not catholic_desc or not secular_desc:
            raise ValueError(f"Missing descriptors for concept={concept}, condition={condition}")

        query_vec = embeddings[query]
        catholic_scores = [cosine(query_vec, embeddings[d]) for d in catholic_desc]
        secular_scores = [cosine(query_vec, embeddings[d]) for d in secular_desc]

        catholic_score = float(np.mean(catholic_scores))
        secular_score = float(np.mean(secular_scores))
        cas = catholic_score - secular_score

        ranked = rank_descriptors(query_vec, catholic_desc, secular_desc, embeddings)
        top = ranked[0]
        nearest_catholic = next(item for item in ranked if item["descriptor_group"] == "catholic")
        nearest_secular = next(item for item in ranked if item["descriptor_group"] == "secular")

        records.append({
            "locus": locus,
            "concept": concept,
            "concept_type": concept_type,
            "ambiguity_level": ambiguity_level,
            "query_condition": condition,
            "query_template_id": query_template_id,
            "query": query,
            "catholic_score": catholic_score,
            "secular_score": secular_score,
            "catholic_alignment_score": cas,
            "top_descriptor": top["descriptor"],
            "top_descriptor_group": top["descriptor_group"],
            "top_descriptor_similarity": top["similarity"],
            "top_is_catholic": 1 if top["descriptor_group"] == "catholic" else 0,
            "nearest_catholic_descriptor": nearest_catholic["descriptor"],
            "nearest_catholic_similarity": nearest_catholic["similarity"],
            "nearest_catholic_rank": nearest_catholic["rank"],
            "nearest_secular_descriptor": nearest_secular["descriptor"],
            "nearest_secular_similarity": nearest_secular["similarity"],
            "nearest_secular_rank": nearest_secular["rank"],
        })

    return pd.DataFrame.from_records(records)


def collect_all_texts(df: pd.DataFrame) -> List[str]:
    texts: List[str] = []
    for _, row in df.iterrows():
        texts.append(str(row["query"]).strip())
        texts.extend(parse_descriptors(row["catholic_descriptors"]))
        texts.extend(parse_descriptors(row["secular_descriptors"]))
    return list(dict.fromkeys([text for text in texts if text]))


def make_condition_summary(results_df: pd.DataFrame) -> pd.DataFrame:
    group_cols = ["locus", "concept", "concept_type", "ambiguity_level", "query_condition"]
    return (
        results_df.groupby(group_cols, dropna=False)
        .agg(
            query_count=("query", "count"),
            catholic_score=("catholic_score", "mean"),
            secular_score=("secular_score", "mean"),
            catholic_alignment_score=("catholic_alignment_score", "mean"),
            top_catholic_rate=("top_is_catholic", "mean"),
            mean_nearest_catholic_rank=("nearest_catholic_rank", "mean"),
            mean_nearest_secular_rank=("nearest_secular_rank", "mean"),
        )
        .reset_index()
    )


def make_concept_summary(condition_df: pd.DataFrame) -> pd.DataFrame:
    rows = []
    base_cols = ["locus", "concept", "concept_type", "ambiguity_level"]

    for keys, subset in condition_df.groupby(base_cols, dropna=False, sort=False):
        locus, concept, concept_type, ambiguity_level = keys
        record = {
            "locus": locus,
            "concept": concept,
            "concept_type": concept_type,
            "ambiguity_level": ambiguity_level,
        }

        for condition in CONDITION_ORDER:
            part = subset[subset["query_condition"] == condition]
            record[f"{condition}_cas"] = float(part["catholic_alignment_score"].mean()) if len(part) else float("nan")
            record[f"{condition}_top_catholic_rate"] = float(part["top_catholic_rate"].mean()) if len(part) else float("nan")
            record[f"{condition}_query_count"] = int(part["query_count"].sum()) if len(part) else 0

        catholic = record.get("catholic_cas", float("nan"))
        for condition in ["bare", "ordinary", "academic"]:
            base = record.get(f"{condition}_cas", float("nan"))
            record[f"{condition}_to_catholic_shift"] = catholic - base if not (math.isnan(catholic) or math.isnan(base)) else float("nan")

        record["default_cas"] = float(np.nanmean([record.get("bare_cas", float("nan")), record.get("ordinary_cas", float("nan"))]))
        record["default_to_catholic_shift"] = catholic - record["default_cas"] if not math.isnan(catholic) else float("nan")
        rows.append(record)

    return pd.DataFrame.from_records(rows)


def bootstrap_ci(values: np.ndarray, n_boot: int = 5000, seed: int = 42) -> tuple[float, float]:
    arr = np.array(values, dtype=float)
    arr = arr[~np.isnan(arr)]
    if len(arr) == 0:
        return float("nan"), float("nan")
    if len(arr) == 1:
        return float(arr[0]), float(arr[0])
    rng = np.random.default_rng(seed)
    means = np.empty(n_boot, dtype=float)
    for i in range(n_boot):
        sample = rng.choice(arr, size=len(arr), replace=True)
        means[i] = np.mean(sample)
    return float(np.percentile(means, 2.5)), float(np.percentile(means, 97.5))


def practical_effect_label(mean_value: float) -> str:
    if math.isnan(mean_value):
        return "unavailable"
    magnitude = abs(mean_value)
    if magnitude < 0.02:
        return "negligible"
    if magnitude < 0.05:
        return "small"
    if magnitude < 0.10:
        return "meaningful"
    return "strong"


def interpret_ci(ci_low: float, ci_high: float, metric: str) -> str:
    band = 0.02
    if math.isnan(ci_low) or math.isnan(ci_high):
        return "insufficient data"
    if ci_low > 0:
        if "shift" in metric:
            return "positive shift toward Catholic descriptors"
        return "positive Catholic alignment"
    if ci_high < 0:
        if "shift" in metric:
            return "negative shift away from Catholic descriptors"
        return "negative Catholic alignment"
    if ci_low >= -band and ci_high <= band:
        return "within pre-declared negligible band"
    return "confidence interval overlaps zero"


def one_sample_summary(values, analysis: str, subset: str, metric: str, alternative: str) -> dict:
    arr = np.array(values, dtype=float)
    arr = arr[~np.isnan(arr)]
    n = int(len(arr))

    if n == 0:
        return {
            "analysis": analysis,
            "subset": subset,
            "metric": metric,
            "n": 0,
            "mean": float("nan"),
            "sd": float("nan"),
            "bootstrap_ci_low": float("nan"),
            "bootstrap_ci_high": float("nan"),
            "cohens_d": float("nan"),
            "t_statistic": float("nan"),
            "p_value": float("nan"),
            "wilcoxon_p": float("nan"),
            "positive_count": 0,
            "negative_count": 0,
            "zero_count": 0,
            "positive_rate": float("nan"),
            "practical_effect": "unavailable",
            "interpretation": "insufficient data",
        }

    mean_value = float(np.mean(arr))
    sd_value = float(np.std(arr, ddof=1)) if n > 1 else 0.0
    ci_low, ci_high = bootstrap_ci(arr)
    cohens_d = float(mean_value / sd_value) if sd_value > 0 else float("nan")
    positive_count = int(np.sum(arr > 0))
    negative_count = int(np.sum(arr < 0))
    zero_count = int(np.sum(arr == 0))
    positive_rate = positive_count / n if n else float("nan")

    t_statistic = float("nan")
    p_value = float("nan")
    wilcoxon_p = float("nan")

    if scipy_stats is not None and n > 1:
        try:
            t_res = scipy_stats.ttest_1samp(arr, popmean=0.0, alternative=alternative)
            t_statistic = float(t_res.statistic)
            p_value = float(t_res.pvalue)
        except TypeError:
            t_res = scipy_stats.ttest_1samp(arr, popmean=0.0)
            t_statistic = float(t_res.statistic)
            p2 = float(t_res.pvalue)
            if alternative == "greater":
                p_value = p2 / 2 if t_statistic > 0 else 1 - (p2 / 2)
            elif alternative == "less":
                p_value = p2 / 2 if t_statistic < 0 else 1 - (p2 / 2)
            else:
                p_value = p2

        if np.any(arr != 0):
            try:
                w_res = scipy_stats.wilcoxon(arr, alternative=alternative, zero_method="wilcox")
                wilcoxon_p = float(w_res.pvalue)
            except Exception:
                wilcoxon_p = float("nan")

    return {
        "analysis": analysis,
        "subset": subset,
        "metric": metric,
        "n": n,
        "mean": mean_value,
        "sd": sd_value,
        "bootstrap_ci_low": ci_low,
        "bootstrap_ci_high": ci_high,
        "cohens_d": cohens_d,
        "t_statistic": t_statistic,
        "p_value": p_value,
        "wilcoxon_p": wilcoxon_p,
        "positive_count": positive_count,
        "negative_count": negative_count,
        "zero_count": zero_count,
        "positive_rate": positive_rate,
        "practical_effect": practical_effect_label(mean_value),
        "interpretation": interpret_ci(ci_low, ci_high, metric),
    }


def make_statistical_summary(concept_df: pd.DataFrame) -> pd.DataFrame:
    rows = []

    for condition in CONDITION_ORDER:
        metric = f"{condition}_cas"
        rows.append(
            one_sample_summary(
                concept_df[metric],
                analysis=f"Overall {condition} CAS vs zero",
                subset="all concepts",
                metric=metric,
                alternative="two-sided",
            )
        )

    for shift_metric in [
        "bare_to_catholic_shift",
        "ordinary_to_catholic_shift",
        "academic_to_catholic_shift",
        "default_to_catholic_shift",
    ]:
        rows.append(
            one_sample_summary(
                concept_df[shift_metric],
                analysis=f"Overall {shift_metric.replace('_', ' ')}",
                subset="all concepts",
                metric=shift_metric,
                alternative="greater",
            )
        )

    for locus, subset in concept_df.groupby("locus", sort=False):
        for condition in CONDITION_ORDER:
            metric = f"{condition}_cas"
            rows.append(
                one_sample_summary(
                    subset[metric],
                    analysis=f"Locus {condition} CAS vs zero",
                    subset=locus,
                    metric=metric,
                    alternative="two-sided",
                )
            )
        for shift_metric in ["ordinary_to_catholic_shift", "academic_to_catholic_shift"]:
            rows.append(
                one_sample_summary(
                    subset[shift_metric],
                    analysis=f"Locus {shift_metric.replace('_', ' ')}",
                    subset=locus,
                    metric=shift_metric,
                    alternative="greater",
                )
            )

    for concept_type, subset in concept_df.groupby("concept_type", sort=True):
        if len(subset) >= 3:
            rows.append(
                one_sample_summary(
                    subset[PRIMARY_SHIFT],
                    analysis="Concept-type ordinary to Catholic shift",
                    subset=concept_type,
                    metric=PRIMARY_SHIFT,
                    alternative="greater",
                )
            )

    return pd.DataFrame.from_records(rows)


def build_points(df: pd.DataFrame, results_df: pd.DataFrame, embeddings: Dict[str, np.ndarray]) -> pd.DataFrame:
    result_lookup = {
        (r["concept"], r["query_condition"], r["query"]): r
        for _, r in results_df.iterrows()
    }

    points = []
    seen = set()

    for _, row in df.iterrows():
        locus = str(row["locus"]).strip()
        concept = str(row["concept"]).strip()
        concept_type = str(row.get("concept_type", "unspecified")).strip()
        ambiguity_level = str(row.get("ambiguity_level", "unspecified")).strip()
        condition = str(row["query_condition"]).strip()
        query = str(row["query"]).strip()

        key = (query, locus, concept, condition, "query")
        if key not in seen:
            seen.add(key)
            rr = result_lookup.get((concept, condition, query))
            cas = float(rr["catholic_alignment_score"]) if rr is not None else float("nan")
            points.append({
                "phrase": query,
                "locus": locus,
                "concept": concept,
                "concept_type": concept_type,
                "ambiguity_level": ambiguity_level,
                "condition": condition,
                "role": "query",
                "cas": cas,
                "vector": embeddings[query],
            })

        for descriptor in parse_descriptors(row["catholic_descriptors"]):
            key = (descriptor, locus, concept, condition, "catholic descriptor")
            if key not in seen:
                seen.add(key)
                points.append({
                    "phrase": descriptor,
                    "locus": locus,
                    "concept": concept,
                    "concept_type": concept_type,
                    "ambiguity_level": ambiguity_level,
                    "condition": condition,
                    "role": "catholic descriptor",
                    "cas": float("nan"),
                    "vector": embeddings[descriptor],
                })

        for descriptor in parse_descriptors(row["secular_descriptors"]):
            key = (descriptor, locus, concept, condition, "secular descriptor")
            if key not in seen:
                seen.add(key)
                points.append({
                    "phrase": descriptor,
                    "locus": locus,
                    "concept": concept,
                    "concept_type": concept_type,
                    "ambiguity_level": ambiguity_level,
                    "condition": condition,
                    "role": "secular descriptor",
                    "cas": float("nan"),
                    "vector": embeddings[descriptor],
                })

    return pd.DataFrame(points)


def apply_opaque_layout(fig: go.Figure, is_3d: bool = False) -> go.Figure:
    fig.update_layout(
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font={"color": "#e5e7eb"},
    )
    if is_3d:
        fig.update_layout(
            scene={
                "bgcolor": "#111827",
                "xaxis": {"backgroundcolor": "#111827", "gridcolor": "#475569", "zerolinecolor": "#94a3b8"},
                "yaxis": {"backgroundcolor": "#111827", "gridcolor": "#475569", "zerolinecolor": "#94a3b8"},
                "zaxis": {"backgroundcolor": "#111827", "gridcolor": "#475569", "zerolinecolor": "#94a3b8"},
            }
        )
    return fig


def compute_umap_coords(vectors: np.ndarray) -> np.ndarray:
    n_points = vectors.shape[0]
    if n_points < 3:
        padded = np.zeros((n_points, 3), dtype=float)
        if n_points:
            padded[:, 0] = np.arange(n_points)
        return padded

    n_neighbors = max(2, min(20, n_points - 1))
    reducer = umap.UMAP(
        n_components=3,
        n_neighbors=n_neighbors,
        min_dist=0.15,
        metric="cosine",
        random_state=42,
    )
    return reducer.fit_transform(vectors)


def make_distribution_figure(concept_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for condition in CONDITION_ORDER:
        fig.add_trace(
            go.Box(
                y=concept_df[f"{condition}_cas"],
                name=f"{condition.title()} CAS",
                boxpoints="all",
                marker_color=CONDITION_COLORS[condition],
            )
        )
    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="#e5e7eb")
    fig.update_layout(
        title="Concept-Level CAS by Query Context",
        template="plotly_dark",
        height=560,
        yaxis_title="Catholic Alignment Score",
        margin={"l": 40, "r": 20, "t": 60, "b": 60},
    )
    return apply_opaque_layout(fig)


def make_shift_distribution_figure(concept_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for metric in ["bare_to_catholic_shift", "ordinary_to_catholic_shift", "academic_to_catholic_shift"]:
        fig.add_trace(
            go.Box(
                y=concept_df[metric],
                name=metric.replace("_", " "),
                boxpoints="all",
                marker_color=CONDITION_COLORS.get(metric, "#f59e0b"),
            )
        )
    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="#e5e7eb")
    fig.update_layout(
        title="Catholic Context Shift Distributions",
        template="plotly_dark",
        height=520,
        yaxis_title="Shift in CAS",
        margin={"l": 40, "r": 20, "t": 60, "b": 80},
    )
    return apply_opaque_layout(fig)


def make_slope_figure(concept_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    x_axis = CONDITION_ORDER

    for locus, subset in concept_df.groupby("locus", sort=False):
        x_values = []
        y_values = []
        hover_values = []
        for _, row in subset.iterrows():
            values = [row[f"{c}_cas"] for c in CONDITION_ORDER]
            x_values.extend(x_axis + [None])
            y_values.extend(values + [None])
            hover = (
                f"{row['concept']}<br>"
                f"Locus: {row['locus']}<br>"
                f"Bare CAS: {row['bare_cas']:.4f}<br>"
                f"Ordinary CAS: {row['ordinary_cas']:.4f}<br>"
                f"Academic CAS: {row['academic_cas']:.4f}<br>"
                f"Catholic CAS: {row['catholic_cas']:.4f}<br>"
                f"Ordinary to Catholic shift: {row['ordinary_to_catholic_shift']:.4f}"
            )
            hover_values.extend([hover] * len(x_axis) + [None])

        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=y_values,
                mode="lines+markers",
                name=locus,
                line={"width": 1.4, "color": LOCUS_COLORS.get(locus, "#94a3b8")},
                marker={"size": 6, "color": LOCUS_COLORS.get(locus, "#94a3b8")},
                hovertext=hover_values,
                hoverinfo="text",
            )
        )

    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="#e5e7eb")
    fig.update_layout(
        title="Four-Context Semantic Shift by Concept",
        template="plotly_dark",
        height=660,
        yaxis_title="Catholic Alignment Score",
        xaxis_title="Query context",
        margin={"l": 40, "r": 20, "t": 60, "b": 60},
    )
    return apply_opaque_layout(fig)


def make_locus_figure(concept_df: pd.DataFrame) -> go.Figure:
    group = concept_df.groupby("locus", sort=False).agg(
        bare_cas=("bare_cas", "mean"),
        ordinary_cas=("ordinary_cas", "mean"),
        academic_cas=("academic_cas", "mean"),
        catholic_cas=("catholic_cas", "mean"),
        ordinary_to_catholic_shift=("ordinary_to_catholic_shift", "mean"),
    ).reset_index()

    fig = go.Figure()
    for col in ["bare_cas", "ordinary_cas", "academic_cas", "catholic_cas", "ordinary_to_catholic_shift"]:
        color_key = col.replace("_cas", "")
        fig.add_trace(
            go.Bar(
                x=group["locus"],
                y=group[col],
                name=col.replace("_", " "),
                marker_color=CONDITION_COLORS.get(color_key, CONDITION_COLORS.get(col, "#94a3b8")),
            )
        )

    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="#e5e7eb")
    fig.update_layout(
        title="Mean Scores by Theological Locus",
        template="plotly_dark",
        barmode="group",
        height=600,
        yaxis_title="Mean score",
        xaxis_title="Theological locus",
        margin={"l": 40, "r": 20, "t": 60, "b": 160},
    )
    fig.update_xaxes(tickangle=25)
    return apply_opaque_layout(fig)


def make_heatmap_figure(concept_df: pd.DataFrame) -> go.Figure:
    plot_df = concept_df.sort_values("ordinary_to_catholic_shift", ascending=True).copy()
    plot_df["label"] = plot_df["locus"].str.replace(" and ", " / ", regex=False) + " — " + plot_df["concept"]

    cols = [
        "bare_cas",
        "ordinary_cas",
        "academic_cas",
        "catholic_cas",
        "ordinary_to_catholic_shift",
        "academic_to_catholic_shift",
    ]
    z = plot_df[cols].to_numpy()
    z_abs = np.nanmax(np.abs(z)) if np.isfinite(z).any() else 0.1
    z_abs = max(float(z_abs), 0.1)

    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=[c.replace("_", " ") for c in cols],
            y=plot_df["label"],
            zmin=-z_abs,
            zmax=z_abs,
            colorscale=[
                [0.0, "#991b1b"],
                [0.5, "#f8fafc"],
                [1.0, "#166534"],
            ],
            colorbar={"title": "Score"},
            hovertemplate="<b>%{y}</b><br>%{x}: %{z:.4f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="CTSB-100 v2 Concept-Level Heatmap",
        template="plotly_dark",
        height=max(900, int(len(plot_df) * 15)),
        margin={"l": 340, "r": 20, "t": 60, "b": 80},
    )
    return apply_opaque_layout(fig)


def make_query_umap_figure(results_df: pd.DataFrame, embeddings: Dict[str, np.ndarray]) -> go.Figure:
    plot_df = results_df.copy()
    vectors = np.vstack([embeddings[q] for q in plot_df["query"]])
    coords = compute_umap_coords(vectors)
    plot_df["x"] = coords[:, 0]
    plot_df["y"] = coords[:, 1]
    plot_df["z"] = coords[:, 2]

    max_abs = max(0.1, float(np.nanmax(np.abs(plot_df["catholic_alignment_score"]))))

    symbols = {
        "bare": "circle",
        "ordinary": "square",
        "academic": "diamond",
        "catholic": "cross",
    }

    fig = go.Figure()
    for condition in CONDITION_ORDER:
        subset = plot_df[plot_df["query_condition"] == condition]
        if subset.empty:
            continue
        fig.add_trace(
            go.Scatter3d(
                x=subset["x"],
                y=subset["y"],
                z=subset["z"],
                mode="markers",
                name=f"query / {condition}",
                marker={
                    "size": 5,
                    "color": subset["catholic_alignment_score"],
                    "colorscale": "RdYlGn",
                    "cmin": -max_abs,
                    "cmax": max_abs,
                    "opacity": 0.88,
                    "symbol": symbols.get(condition, "circle"),
                    "colorbar": {"title": "CAS"} if condition == CONDITION_ORDER[0] else None,
                },
                customdata=subset[["query", "locus", "concept", "query_condition", "catholic_alignment_score"]].to_numpy(),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Locus: %{customdata[1]}<br>"
                    "Concept: %{customdata[2]}<br>"
                    "Condition: %{customdata[3]}<br>"
                    "CAS: %{customdata[4]:.4f}<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title="Global Query-Only 3D UMAP",
        template="plotly_dark",
        height=760,
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
        scene={"xaxis_title": "UMAP 1", "yaxis_title": "UMAP 2", "zaxis_title": "UMAP 3"},
    )
    return apply_opaque_layout(fig, is_3d=True)


def make_locus_umap_figure(points_df: pd.DataFrame, locus: str) -> go.Figure:
    subset = points_df[points_df["locus"] == locus].copy()
    vectors = np.vstack(subset["vector"].to_list())
    coords = compute_umap_coords(vectors)
    subset["x"] = coords[:, 0]
    subset["y"] = coords[:, 1]
    subset["z"] = coords[:, 2]

    role_styles = {
        "query": {"color": "#f8fafc", "symbol": "diamond", "size": 6},
        "catholic descriptor": {"color": "#22c55e", "symbol": "circle", "size": 4},
        "secular descriptor": {"color": "#ef4444", "symbol": "square", "size": 4},
    }

    fig = go.Figure()
    for role, role_df in subset.groupby("role", sort=False):
        style = role_styles.get(role, {"color": "#94a3b8", "symbol": "circle", "size": 4})
        fig.add_trace(
            go.Scatter3d(
                x=role_df["x"],
                y=role_df["y"],
                z=role_df["z"],
                mode="markers",
                name=role,
                marker={
                    "size": style["size"],
                    "color": style["color"],
                    "symbol": style["symbol"],
                    "opacity": 0.85,
                    "line": {"width": 0.5, "color": "#ffffff"},
                },
                customdata=role_df[["phrase", "concept", "condition", "role", "cas"]].to_numpy(),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Concept: %{customdata[1]}<br>"
                    "Condition: %{customdata[2]}<br>"
                    "Role: %{customdata[3]}<br>"
                    "CAS: %{customdata[4]:.4f}<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title=f"Per-Locus 3D UMAP: {locus}",
        template="plotly_dark",
        height=680,
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
        scene={"xaxis_title": "UMAP 1", "yaxis_title": "UMAP 2", "zaxis_title": "UMAP 3"},
    )
    return apply_opaque_layout(fig, is_3d=True)


def format_numeric_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if pd.api.types.is_numeric_dtype(out[col]):
            if "p" in col:
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else ("<0.001" if x < 0.001 else f"{x:.4f}"))
            elif col in {"n", "positive_count", "negative_count", "zero_count"} or col.endswith("_query_count"):
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else f"{int(x)}")
            elif "rate" in col:
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else f"{x:.2%}")
            else:
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else f"{x:.4f}")
    return out


def raw_csv_block(title: str, element_id: str, csv_text: str, download_path: str) -> str:
    escaped = html_lib.escape(csv_text)
    safe_title = html_lib.escape(title)
    safe_id = html_lib.escape(element_id)
    safe_path = html_lib.escape(download_path)
    return f"""
      <details class="raw-block">
        <summary>{safe_title}</summary>
        <p>
          <a href="{safe_path}" download>Download CSV</a>
          <button type="button" onclick="copyRawCsv('{safe_id}')">Copy CSV</button>
        </p>
        <textarea id="{safe_id}" readonly spellcheck="false">{escaped}</textarea>
      </details>
"""


def write_dashboard(
    output_html: Path,
    results_df: pd.DataFrame,
    condition_df: pd.DataFrame,
    concept_df: pd.DataFrame,
    stats_df: pd.DataFrame,
    points_df: pd.DataFrame,
    embeddings: Dict[str, np.ndarray],
    deployment: str,
    api_version: str,
    benchmark_path: Path,
    output_csv: Path,
    output_condition_csv: Path,
    output_concept_csv: Path,
    output_stats_csv: Path,
    skip_umap: bool = False,
) -> None:
    figures = [
        ("Context-Level CAS Distributions", make_distribution_figure(concept_df)),
        ("Catholic Context Shift Distributions", make_shift_distribution_figure(concept_df)),
        ("Four-Context Slope Plot", make_slope_figure(concept_df)),
        ("Locus-Level Comparison", make_locus_figure(concept_df)),
        ("Concept Heatmap", make_heatmap_figure(concept_df)),
    ]

    if not skip_umap:
        figures.append(("Global Query-Only UMAP", make_query_umap_figure(results_df, embeddings)))
        for locus in concept_df["locus"].drop_duplicates().tolist():
            figures.append((f"Per-Locus UMAP: {locus}", make_locus_umap_figure(points_df, locus)))

    figure_html_parts = []
    for idx, (title, fig) in enumerate(figures):
        figure_html_parts.append(
            f"<section><h2>{html_lib.escape(title)}</h2>"
            + pio.to_html(fig, include_plotlyjs="cdn" if idx == 0 else False, full_html=False)
            + "</section>"
        )
    figures_html = "\n".join(figure_html_parts)

    stats_table = format_numeric_df(stats_df).to_html(index=False, classes="scores-table", border=0, escape=True)

    concept_cols = [
        "locus",
        "concept",
        "concept_type",
        "ambiguity_level",
        "bare_cas",
        "ordinary_cas",
        "academic_cas",
        "catholic_cas",
        "ordinary_to_catholic_shift",
        "academic_to_catholic_shift",
        "bare_top_catholic_rate",
        "ordinary_top_catholic_rate",
        "academic_top_catholic_rate",
        "catholic_top_catholic_rate",
    ]
    concept_table = (
        format_numeric_df(concept_df[concept_cols].sort_values("ordinary_to_catholic_shift", ascending=False))
        .to_html(index=False, classes="scores-table", border=0, escape=True)
    )

    n_concepts = int(concept_df["concept"].nunique())
    n_queries = int(len(results_df))
    n_unique_strings = int(len(set(results_df["query"].tolist())))
    bare_mean = float(concept_df["bare_cas"].mean())
    ordinary_mean = float(concept_df["ordinary_cas"].mean())
    academic_mean = float(concept_df["academic_cas"].mean())
    catholic_mean = float(concept_df["catholic_cas"].mean())
    ordinary_shift_mean = float(concept_df["ordinary_to_catholic_shift"].mean())
    academic_shift_mean = float(concept_df["academic_to_catholic_shift"].mean())
    ordinary_top_rate = float(concept_df["ordinary_top_catholic_rate"].mean())
    catholic_top_rate = float(concept_df["catholic_top_catholic_rate"].mean())

    raw_blocks = "\n".join([
        raw_csv_block(
            "Statistical summary CSV",
            "raw-stats-csv",
            stats_df.to_csv(index=False),
            display_path(output_stats_csv).replace("/" + ROOT.name + "/", ""),
        ),
        raw_csv_block(
            "Concept-level summary CSV",
            "raw-concept-csv",
            concept_df.to_csv(index=False),
            display_path(output_concept_csv).replace("/" + ROOT.name + "/", ""),
        ),
        raw_csv_block(
            "Condition-level summary CSV",
            "raw-condition-csv",
            condition_df.to_csv(index=False),
            display_path(output_condition_csv).replace("/" + ROOT.name + "/", ""),
        ),
        raw_csv_block(
            "Raw query-level results CSV",
            "raw-query-csv",
            results_df.to_csv(index=False),
            display_path(output_csv).replace("/" + ROOT.name + "/", ""),
        ),
    ])

    generated = utc_now()
    safe_benchmark = display_path(benchmark_path)

    output_html.parent.mkdir(parents=True, exist_ok=True)

    html_doc = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Vector Space and Theological Meaning</title>
  <meta name="viewport" content="width=device-width, initial-scale=1">
  <style>
    :root {{
      color-scheme: dark;
      --bg: #020617;
      --panel: #0f172a;
      --panel-2: #111827;
      --text: #e5e7eb;
      --muted: #94a3b8;
      --border: #334155;
      --accent: #38bdf8;
      --positive: #22c55e;
      --negative: #ef4444;
      --warning: #f59e0b;
    }}
    * {{
      box-sizing: border-box;
    }}
    html, body {{
      min-height: 100%;
      background: var(--bg);
    }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background: radial-gradient(circle at top, #172554 0, var(--bg) 42rem);
      color: var(--text);
      line-height: 1.6;
    }}
    header {{
      padding: 4rem 1.25rem 2rem;
      border-bottom: 1px solid var(--border);
      background: rgba(2, 6, 23, 0.96);
    }}
    main {{
      max-width: 1380px;
      margin: 0 auto;
      padding: 2rem 1.25rem 4rem;
      background: rgba(2, 6, 23, 0.90);
    }}
    .hero {{
      max-width: 1380px;
      margin: 0 auto;
    }}
    h1 {{
      margin: 0 0 0.5rem;
      font-size: clamp(2rem, 5vw, 4rem);
      line-height: 1.05;
      letter-spacing: -0.04em;
    }}
    h2 {{
      margin-top: 2.5rem;
      font-size: 1.5rem;
    }}
    h3 {{
      margin-top: 1.5rem;
    }}
    p {{
      color: var(--muted);
    }}
    .tagline {{
      max-width: 980px;
      font-size: 1.1rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(4, minmax(0, 1fr));
      gap: 1rem;
      margin: 1.5rem 0;
    }}
    .card {{
      background: rgba(15, 23, 42, 0.98);
      border: 1px solid var(--border);
      border-radius: 1rem;
      padding: 1rem;
      box-shadow: 0 20px 60px rgba(0,0,0,0.24);
    }}
    .metric {{
      font-size: 2rem;
      font-weight: 750;
      color: var(--text);
    }}
    .label {{
      color: var(--muted);
      font-size: 0.9rem;
    }}
    .note {{
      border-left: 4px solid var(--accent);
      padding: 1rem;
      background: rgba(56, 189, 248, 0.10);
      border-radius: 0.75rem;
      margin: 1rem 0;
    }}
    .warning {{
      border-left-color: var(--warning);
      background: rgba(245, 158, 11, 0.10);
    }}
    section {{
      background: rgba(15, 23, 42, 0.38);
      border-radius: 1rem;
      padding: 0.25rem 0.75rem 1rem;
      margin: 1.25rem 0;
    }}
    .scores-table {{
      width: 100%;
      border-collapse: collapse;
      overflow: hidden;
      border-radius: 0.75rem;
      font-size: 0.86rem;
    }}
    .scores-table th,
    .scores-table td {{
      padding: 0.7rem;
      border-bottom: 1px solid var(--border);
      text-align: left;
      vertical-align: top;
    }}
    .scores-table th {{
      background: #1e293b;
      color: var(--text);
      position: sticky;
      top: 0;
    }}
    .scores-table td {{
      color: #cbd5e1;
    }}
    .table-wrap {{
      overflow-x: auto;
      max-height: 760px;
      border: 1px solid var(--border);
      border-radius: 0.75rem;
      background: var(--panel);
    }}
    details {{
      border: 1px solid var(--border);
      border-radius: 0.75rem;
      padding: 1rem;
      background: rgba(15, 23, 42, 0.96);
      margin: 1rem 0;
    }}
    summary {{
      cursor: pointer;
      font-weight: 700;
    }}
    .raw-block textarea {{
      width: 100%;
      min-height: 18rem;
      resize: vertical;
      margin-top: 0.75rem;
      padding: 1rem;
      color: #dbeafe;
      background: #020617;
      border: 1px solid var(--border);
      border-radius: 0.75rem;
      font-family: ui-monospace, SFMono-Regular, Menlo, Monaco, Consolas, "Liberation Mono", monospace;
      font-size: 0.8rem;
      line-height: 1.45;
      white-space: pre;
    }}
    button {{
      margin-left: 0.75rem;
      border: 1px solid var(--border);
      border-radius: 0.5rem;
      padding: 0.45rem 0.75rem;
      color: var(--text);
      background: #1e293b;
      cursor: pointer;
    }}
    button:hover {{
      background: #334155;
    }}
    footer {{
      margin-top: 3rem;
      color: var(--muted);
      font-size: 0.9rem;
    }}
    code {{
      color: #bae6fd;
    }}
    a {{
      color: #7dd3fc;
    }}
    @media (max-width: 980px) {{
      .grid {{
        grid-template-columns: repeat(2, minmax(0, 1fr));
      }}
    }}
    @media (max-width: 640px) {{
      .grid {{
        grid-template-columns: 1fr;
      }}
    }}
  </style>
</head>
<body>
  <header>
    <div class="hero">
      <h1>Vector Space and Theological Meaning</h1>
      <p class="tagline">
        CTSB-100 v2 draft audit of secular semantic priors in large language model embeddings.
        Version 2 compares four query contexts: bare/minimal, ordinary lived usage,
        neutral academic usage, and explicit Catholic/theological usage.
      </p>
    </div>
  </header>

  <main>
    <section class="grid" aria-label="summary metrics">
      <div class="card">
        <div class="metric">{n_concepts}</div>
        <div class="label">Concept-level units</div>
      </div>
      <div class="card">
        <div class="metric">{n_queries}</div>
        <div class="label">Query rows</div>
      </div>
      <div class="card">
        <div class="metric">{bare_mean:.4f}</div>
        <div class="label">Mean bare CAS</div>
      </div>
      <div class="card">
        <div class="metric">{ordinary_mean:.4f}</div>
        <div class="label">Mean ordinary CAS</div>
      </div>
      <div class="card">
        <div class="metric">{academic_mean:.4f}</div>
        <div class="label">Mean academic CAS</div>
      </div>
      <div class="card">
        <div class="metric">{catholic_mean:.4f}</div>
        <div class="label">Mean Catholic CAS</div>
      </div>
      <div class="card">
        <div class="metric">{ordinary_shift_mean:.4f}</div>
        <div class="label">Ordinary → Catholic shift</div>
      </div>
      <div class="card">
        <div class="metric">{academic_shift_mean:.4f}</div>
        <div class="label">Academic → Catholic shift</div>
      </div>
      <div class="card">
        <div class="metric">{ordinary_top_rate:.2%}</div>
        <div class="label">Catholic top-rate: ordinary</div>
      </div>
      <div class="card">
        <div class="metric">{catholic_top_rate:.2%}</div>
        <div class="label">Catholic top-rate: Catholic context</div>
      </div>
      <div class="card">
        <div class="metric">{n_unique_strings}</div>
        <div class="label">Unique query strings</div>
      </div>
    </section>

    <section class="note">
      <strong>Methodological note:</strong>
      Positive CAS means the query is closer to Catholic-magisterial descriptors.
      Negative CAS means the query is closer to secular/common-language descriptors.
      The main v2 shift metric is ordinary lived usage to explicit Catholic context.
      UMAP is illustrative only; substantive interpretation should rely on high-dimensional cosine,
      rank-order metrics, confidence intervals, and effect sizes.
    </section>

    <section class="note warning">
      <strong>Benchmark status:</strong>
      CTSB-100 v2 is a draft benchmark. Version 1 has been archived as an iterative starting point.
      Version 2 is stronger because it separates bare, ordinary, academic, and explicit Catholic query contexts.
      The descriptor sets should still be reviewed before final dissertation claims.
    </section>

    <section>
      <h2>Statistical Summary</h2>
      <div class="table-wrap">
        {stats_table}
      </div>
    </section>

    {figures_html}

    <section>
      <h2>Concept-Level Summary</h2>
      <div class="table-wrap">
        {concept_table}
      </div>
    </section>

    <section>
      <h2>Advanced Raw Data Export</h2>
      <p>
        These blocks are hidden by default. Open them to copy the raw CSV directly for external analysis,
        peer review, or follow-up interpretation.
      </p>
      {raw_blocks}
    </section>

    <footer>
      <p>
        Generated: {html_lib.escape(generated)}<br>
        Azure deployment: <code>{html_lib.escape(deployment)}</code><br>
        API version: <code>{html_lib.escape(api_version)}</code><br>
        Model name: <code>{html_lib.escape(MODEL_METADATA["model_name"])}</code><br>
        Model version: <code>{html_lib.escape(MODEL_METADATA["model_version"])}</code><br>
        Life cycle status: <code>{html_lib.escape(MODEL_METADATA["life_cycle_status"])}</code><br>
        Date created: <code>{html_lib.escape(MODEL_METADATA["date_created"])}</code><br>
        Date updated: <code>{html_lib.escape(MODEL_METADATA["date_updated"])}</code><br>
        Model retirement date: <code>{html_lib.escape(MODEL_METADATA["model_retirement_date"])}</code><br>
        Benchmark: <code>{html_lib.escape(safe_benchmark)}</code>
      </p>
    </footer>
  </main>

  <script>
    async function copyRawCsv(id) {{
      const el = document.getElementById(id);
      if (!el) return;
      try {{
        await navigator.clipboard.writeText(el.value);
        alert("CSV copied to clipboard.");
      }} catch (err) {{
        el.focus();
        el.select();
        document.execCommand("copy");
        alert("CSV selected/copied. If needed, press Command+C.");
      }}
    }}
  </script>
</body>
</html>
"""
    output_html.write_text(html_doc, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit Azure embedding semantic priors against Catholic and secular descriptor sets."
    )
    parser.add_argument("--benchmark", default=str(ROOT / "data" / "benchmarks" / "ctsb_100_v2_contexts_draft.csv"))
    parser.add_argument("--output-csv", default=str(ROOT / "outputs" / "results" / "ctsb_100_v2_results.csv"))
    parser.add_argument("--output-condition-csv", default=str(ROOT / "outputs" / "results" / "ctsb_100_v2_condition_summary.csv"))
    parser.add_argument("--output-concept-csv", default=str(ROOT / "outputs" / "results" / "ctsb_100_v2_concept_summary.csv"))
    parser.add_argument("--output-stats-csv", default=str(ROOT / "outputs" / "results" / "ctsb_100_v2_statistical_summary.csv"))
    parser.add_argument("--output-html", default=str(ROOT / "index.html"))
    parser.add_argument("--cache", default=str(ROOT / "outputs" / "cache" / "azure_embeddings_cache.json"))
    parser.add_argument("--env-file", default=str(ROOT / ".env"))
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--skip-umap", action="store_true", help="Skip UMAP plots for faster dashboard generation.")
    parser.add_argument("--open", action="store_true", help="Open generated dashboard in the default browser.")
    args = parser.parse_args()

    benchmark_path = Path(args.benchmark)
    output_csv = Path(args.output_csv)
    output_condition_csv = Path(args.output_condition_csv)
    output_concept_csv = Path(args.output_concept_csv)
    output_stats_csv = Path(args.output_stats_csv)
    output_html = Path(args.output_html)
    cache_path = Path(args.cache)

    if not benchmark_path.exists():
        raise FileNotFoundError(f"Benchmark file not found: {benchmark_path}")

    load_dotenv(args.env_file)

    api_key = os.getenv("AZURE_OPENAI_API_KEY")
    azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
    deployment = os.getenv("AZURE_OPENAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large-prova1")
    api_version = os.getenv("AZURE_OPENAI_API_VERSION", "2024-02-01")

    if not api_key:
        raise ValueError("AZURE_OPENAI_API_KEY not found. Create a local .env file.")
    if not azure_endpoint:
        raise ValueError("AZURE_OPENAI_ENDPOINT not found. Create a local .env file.")

    client = AzureOpenAI(api_key=api_key, api_version=api_version, azure_endpoint=azure_endpoint)

    df = pd.read_csv(benchmark_path)
    required_cols = {
        "locus",
        "concept",
        "query_condition",
        "query",
        "catholic_descriptors",
        "secular_descriptors",
    }
    missing_cols = required_cols - set(df.columns)
    if missing_cols:
        raise ValueError(f"Benchmark is missing columns: {sorted(missing_cols)}")

    if "concept_type" not in df.columns:
        df["concept_type"] = "unspecified"
    if "ambiguity_level" not in df.columns:
        df["ambiguity_level"] = "unspecified"
    if "query_template_id" not in df.columns:
        df["query_template_id"] = ""

    all_texts = collect_all_texts(df)
    cache = load_cache(cache_path)
    embeddings = embed_texts(
        all_texts,
        client=client,
        deployment=deployment,
        cache=cache,
        cache_path=cache_path,
        batch_size=args.batch_size,
    )
    save_cache(cache_path, cache)

    results_df = evaluate_benchmark(df, embeddings)
    condition_df = make_condition_summary(results_df)
    concept_df = make_concept_summary(condition_df)
    stats_df = make_statistical_summary(concept_df)

    output_csv.parent.mkdir(parents=True, exist_ok=True)
    output_condition_csv.parent.mkdir(parents=True, exist_ok=True)
    output_concept_csv.parent.mkdir(parents=True, exist_ok=True)
    output_stats_csv.parent.mkdir(parents=True, exist_ok=True)

    results_df.to_csv(output_csv, index=False)
    condition_df.to_csv(output_condition_csv, index=False)
    concept_df.to_csv(output_concept_csv, index=False)
    stats_df.to_csv(output_stats_csv, index=False)

    points_df = build_points(df, results_df, embeddings)
    write_dashboard(
        output_html=output_html,
        results_df=results_df,
        condition_df=condition_df,
        concept_df=concept_df,
        stats_df=stats_df,
        points_df=points_df,
        embeddings=embeddings,
        deployment=deployment,
        api_version=api_version,
        benchmark_path=benchmark_path,
        output_csv=output_csv,
        output_condition_csv=output_condition_csv,
        output_concept_csv=output_concept_csv,
        output_stats_csv=output_stats_csv,
        skip_umap=args.skip_umap,
    )

    print("")
    print("Done.")
    print(f"Benchmark rows: {len(df)}")
    print(f"Concepts: {concept_df['concept'].nunique()}")
    print(f"Unique embedded strings: {len(all_texts)}")
    print(f"Results CSV: {output_csv}")
    print(f"Condition summary CSV: {output_condition_csv}")
    print(f"Concept summary CSV: {output_concept_csv}")
    print(f"Statistical summary CSV: {output_stats_csv}")
    print(f"Dashboard HTML: {output_html}")
    print("")
    print("Concept-level means:")
    mean_cols = [
        "bare_cas",
        "ordinary_cas",
        "academic_cas",
        "catholic_cas",
        "bare_to_catholic_shift",
        "ordinary_to_catholic_shift",
        "academic_to_catholic_shift",
    ]
    print(concept_df[mean_cols].mean().round(4).to_string())
    print("")
    print("Main statistical tests:")
    display_cols = [
        "analysis",
        "subset",
        "metric",
        "n",
        "mean",
        "bootstrap_ci_low",
        "bootstrap_ci_high",
        "p_value",
        "practical_effect",
        "interpretation",
    ]
    print(format_numeric_df(stats_df[display_cols]).head(24).to_string(index=False))
    print("")
    print("GitHub Pages can serve the generated dashboard from index.html after commit and push.")

    if args.open:
        webbrowser.open("file://" + str(output_html.resolve()))


if __name__ == "__main__":
    main()
