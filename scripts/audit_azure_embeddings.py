#!/usr/bin/env python3
from __future__ import annotations

import argparse
import hashlib
import json
import os
import webbrowser
from datetime import datetime, timezone
from pathlib import Path
from typing import Dict, List, Tuple
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
    raise RuntimeError(
        "Could not import umap. Install dependencies with: pip install -r requirements.txt"
    ) from exc


ROOT = Path(__file__).resolve().parents[1]


def utc_now() -> str:
    return datetime.now(timezone.utc).isoformat(timespec="seconds")


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

    result = {}
    for text in unique_texts:
        key = cache_key(deployment, text)
        result[text] = np.array(cache[key]["embedding"], dtype=np.float32)

    return result


def rank_descriptors(
    query_vec: np.ndarray,
    catholic_desc: List[str],
    secular_desc: List[str],
    embeddings: Dict[str, np.ndarray],
) -> List[dict]:
    ranked = []
    for descriptor in catholic_desc:
        ranked.append(
            {
                "descriptor": descriptor,
                "descriptor_group": "catholic",
                "similarity": cosine(query_vec, embeddings[descriptor]),
            }
        )
    for descriptor in secular_desc:
        ranked.append(
            {
                "descriptor": descriptor,
                "descriptor_group": "secular",
                "similarity": cosine(query_vec, embeddings[descriptor]),
            }
        )
    ranked.sort(key=lambda row: row["similarity"], reverse=True)
    for idx, row in enumerate(ranked, start=1):
        row["rank"] = idx
    return ranked


def evaluate_benchmark(df: pd.DataFrame, embeddings: Dict[str, np.ndarray]) -> pd.DataFrame:
    records = []

    for _, row in df.iterrows():
        locus = str(row["locus"]).strip()
        concept = str(row["concept"]).strip()
        condition = str(row["query_condition"]).strip()
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

        records.append(
            {
                "locus": locus,
                "concept": concept,
                "query_condition": condition,
                "query": query,
                "catholic_score": catholic_score,
                "secular_score": secular_score,
                "catholic_alignment_score": cas,
                "top_descriptor": top["descriptor"],
                "top_descriptor_group": top["descriptor_group"],
                "top_descriptor_similarity": top["similarity"],
                "nearest_catholic_descriptor": nearest_catholic["descriptor"],
                "nearest_catholic_similarity": nearest_catholic["similarity"],
                "nearest_catholic_rank": nearest_catholic["rank"],
                "nearest_secular_descriptor": nearest_secular["descriptor"],
                "nearest_secular_similarity": nearest_secular["similarity"],
                "nearest_secular_rank": nearest_secular["rank"],
            }
        )

    return pd.DataFrame.from_records(records)


def collect_all_texts(df: pd.DataFrame) -> List[str]:
    texts: List[str] = []
    for _, row in df.iterrows():
        texts.append(str(row["query"]).strip())
        texts.extend(parse_descriptors(row["catholic_descriptors"]))
        texts.extend(parse_descriptors(row["secular_descriptors"]))
    return list(dict.fromkeys([text for text in texts if text]))


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
        condition = str(row["query_condition"]).strip()
        query = str(row["query"]).strip()

        key = (query, locus, concept, condition, "query")
        if key not in seen:
            seen.add(key)
            rr = result_lookup.get((concept, condition, query))
            cas = float(rr["catholic_alignment_score"]) if rr is not None else float("nan")
            points.append(
                {
                    "phrase": query,
                    "locus": locus,
                    "concept": concept,
                    "condition": condition,
                    "role": "query",
                    "cas": cas,
                    "vector": embeddings[query],
                }
            )

        for descriptor in parse_descriptors(row["catholic_descriptors"]):
            key = (descriptor, locus, concept, condition, "catholic descriptor")
            if key not in seen:
                seen.add(key)
                points.append(
                    {
                        "phrase": descriptor,
                        "locus": locus,
                        "concept": concept,
                        "condition": condition,
                        "role": "catholic descriptor",
                        "cas": float("nan"),
                        "vector": embeddings[descriptor],
                    }
                )

        for descriptor in parse_descriptors(row["secular_descriptors"]):
            key = (descriptor, locus, concept, condition, "secular descriptor")
            if key not in seen:
                seen.add(key)
                points.append(
                    {
                        "phrase": descriptor,
                        "locus": locus,
                        "concept": concept,
                        "condition": condition,
                        "role": "secular descriptor",
                        "cas": float("nan"),
                        "vector": embeddings[descriptor],
                    }
                )

    return pd.DataFrame(points)


def make_umap_figure(points_df: pd.DataFrame) -> go.Figure:
    vectors = np.vstack(points_df["vector"].to_list())
    n_points = vectors.shape[0]
    n_neighbors = max(2, min(15, n_points - 1))

    reducer = umap.UMAP(
        n_components=3,
        n_neighbors=n_neighbors,
        min_dist=0.15,
        metric="cosine",
        random_state=42,
    )
    coords = reducer.fit_transform(vectors)

    points_df = points_df.copy()
    points_df["x"] = coords[:, 0]
    points_df["y"] = coords[:, 1]
    points_df["z"] = coords[:, 2]

    locus_colors = {
        "Sin Grace and Redemption": "#ef4444",
        "Love Communion and Sacramentality": "#3b82f6",
        "Human Dignity and Theological Anthropology": "#22c55e",
        "Freedom Truth and Moral Teleology": "#a855f7",
    }
    role_symbols = {
        "query": "diamond",
        "catholic descriptor": "circle",
        "secular descriptor": "square",
    }

    fig = go.Figure()

    for (locus, role), subset in points_df.groupby(["locus", "role"], sort=False):
        fig.add_trace(
            go.Scatter3d(
                x=subset["x"],
                y=subset["y"],
                z=subset["z"],
                mode="markers",
                name=f"{locus} / {role}",
                marker={
                    "size": 7 if role == "query" else 5,
                    "color": locus_colors.get(locus, "#94a3b8"),
                    "symbol": role_symbols.get(role, "circle"),
                    "opacity": 0.86,
                    "line": {"width": 1, "color": "#ffffff"},
                },
                customdata=subset[["phrase", "locus", "concept", "condition", "role", "cas"]].to_numpy(),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Locus: %{customdata[1]}<br>"
                    "Concept: %{customdata[2]}<br>"
                    "Condition: %{customdata[3]}<br>"
                    "Role: %{customdata[4]}<br>"
                    "CAS: %{customdata[5]:.4f}<extra></extra>"
                ),
            )
        )

    fig.update_layout(
        title="3D UMAP Semantic Map",
        template="plotly_dark",
        height=760,
        margin={"l": 0, "r": 0, "t": 50, "b": 0},
        legend={"orientation": "v", "y": 0.98, "x": 0.01},
        scene={
            "xaxis_title": "UMAP 1",
            "yaxis_title": "UMAP 2",
            "zaxis_title": "UMAP 3",
        },
    )
    return fig


def make_bar_figure(results_df: pd.DataFrame) -> go.Figure:
    plot_df = results_df.copy()
    plot_df["label"] = plot_df["concept"] + " / " + plot_df["query_condition"]

    colors = [
        "#16a34a" if value >= 0 else "#dc2626"
        for value in plot_df["catholic_alignment_score"]
    ]

    fig = go.Figure()
    fig.add_trace(
        go.Bar(
            x=plot_df["label"],
            y=plot_df["catholic_alignment_score"],
            marker_color=colors,
            customdata=plot_df[
                [
                    "locus",
                    "query",
                    "catholic_score",
                    "secular_score",
                    "top_descriptor",
                    "top_descriptor_group",
                ]
            ].to_numpy(),
            hovertemplate=(
                "<b>%{x}</b><br>"
                "Locus: %{customdata[0]}<br>"
                "Query: %{customdata[1]}<br>"
                "Catholic score: %{customdata[2]:.4f}<br>"
                "Secular score: %{customdata[3]:.4f}<br>"
                "CAS: %{y:.4f}<br>"
                "Top descriptor: %{customdata[4]} (%{customdata[5]})<extra></extra>"
            ),
        )
    )

    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="#e5e7eb")
    fig.update_layout(
        title="Catholic Alignment Score by Query",
        template="plotly_dark",
        height=520,
        yaxis_title="Catholic Alignment Score",
        xaxis_title="Concept / condition",
        margin={"l": 40, "r": 20, "t": 60, "b": 120},
    )
    fig.update_xaxes(tickangle=35)
    return fig


def write_dashboard(
    output_html: Path,
    results_df: pd.DataFrame,
    points_df: pd.DataFrame,
    deployment: str,
    api_version: str,
    benchmark_path: Path,
) -> None:
    fig_bar = make_bar_figure(results_df)
    fig_umap = make_umap_figure(points_df)

    bar_html = pio.to_html(fig_bar, include_plotlyjs="cdn", full_html=False)
    umap_html = pio.to_html(fig_umap, include_plotlyjs=False, full_html=False)

    table_cols = [
        "locus",
        "concept",
        "query_condition",
        "catholic_score",
        "secular_score",
        "catholic_alignment_score",
        "top_descriptor",
        "top_descriptor_group",
        "nearest_catholic_rank",
        "nearest_secular_rank",
    ]
    table_df = results_df[table_cols].copy()
    numeric_cols = ["catholic_score", "secular_score", "catholic_alignment_score"]
    for col in numeric_cols:
        table_df[col] = table_df[col].map(lambda x: f"{x:.4f}")
    table_html = table_df.to_html(index=False, classes="scores-table", border=0, escape=True)

    mean_cas = float(results_df["catholic_alignment_score"].mean())
    neutral_mean = float(
        results_df.loc[results_df["query_condition"] == "neutral", "catholic_alignment_score"].mean()
    )
    theological_mean = float(
        results_df.loc[results_df["query_condition"] == "theological", "catholic_alignment_score"].mean()
    )

    generated = utc_now()
    output_html.parent.mkdir(parents=True, exist_ok=True)

    html = f"""<!doctype html>
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
    }}
    * {{
      box-sizing: border-box;
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
    }}
    main {{
      max-width: 1200px;
      margin: 0 auto;
      padding: 2rem 1.25rem 4rem;
    }}
    .hero {{
      max-width: 1200px;
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
    p {{
      color: var(--muted);
    }}
    .tagline {{
      max-width: 780px;
      font-size: 1.1rem;
    }}
    .grid {{
      display: grid;
      grid-template-columns: repeat(3, minmax(0, 1fr));
      gap: 1rem;
      margin: 1.5rem 0;
    }}
    .card {{
      background: rgba(15, 23, 42, 0.86);
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
      background: rgba(56, 189, 248, 0.08);
      border-radius: 0.75rem;
    }}
    .scores-table {{
      width: 100%;
      border-collapse: collapse;
      overflow: hidden;
      border-radius: 0.75rem;
      font-size: 0.92rem;
    }}
    .scores-table th,
    .scores-table td {{
      padding: 0.75rem;
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
      border: 1px solid var(--border);
      border-radius: 0.75rem;
      background: var(--panel);
    }}
    footer {{
      margin-top: 3rem;
      color: var(--muted);
      font-size: 0.9rem;
    }}
    code {{
      color: #bae6fd;
    }}
    @media (max-width: 800px) {{
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
        A pilot audit of secular semantic priors in large language model embeddings,
        comparing Catholic-magisterial descriptors with secular/common-language contrast descriptors.
      </p>
    </div>
  </header>

  <main>
    <section class="grid" aria-label="summary metrics">
      <div class="card">
        <div class="metric">{mean_cas:.4f}</div>
        <div class="label">Mean Catholic Alignment Score</div>
      </div>
      <div class="card">
        <div class="metric">{neutral_mean:.4f}</div>
        <div class="label">Mean CAS: neutral queries</div>
      </div>
      <div class="card">
        <div class="metric">{theological_mean:.4f}</div>
        <div class="label">Mean CAS: theological queries</div>
      </div>
    </section>

    <section class="note">
      <strong>Methodological note:</strong>
      Positive CAS means the query is closer to Catholic-magisterial descriptors.
      Negative CAS means the query is closer to secular/common-language descriptors.
      UMAP is illustrative only; substantive interpretation should rely on the high-dimensional cosine and rank-order scores.
    </section>

    <section>
      <h2>Alignment Scores</h2>
      {bar_html}
    </section>

    <section>
      <h2>3D UMAP Semantic Map</h2>
      <p>
        This map projects high-dimensional embeddings into three dimensions for exploration.
        Visual proximity can be distorted by dimensionality reduction.
      </p>
      {umap_html}
    </section>

    <section>
      <h2>Result Table</h2>
      <div class="table-wrap">
        {table_html}
      </div>
    </section>

    <footer>
      <p>
        Generated: {html_lib.escape(generated)}<br>
        Azure deployment: <code>{html_lib.escape(deployment)}</code><br>
        API version: <code>{html_lib.escape(api_version)}</code><br>
        Benchmark: <code>{html_lib.escape(str(benchmark_path))}</code>
      </p>
    </footer>
  </main>
</body>
</html>
"""
    output_html.write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(
        description="Audit Azure embedding semantic priors against Catholic and secular descriptor sets."
    )
    parser.add_argument("--benchmark", default=str(ROOT / "data" / "benchmarks" / "ctsb_pilot.csv"))
    parser.add_argument("--output-csv", default=str(ROOT / "outputs" / "results" / "ctsb_pilot_results.csv"))
    parser.add_argument("--output-html", default=str(ROOT / "index.html"))
    parser.add_argument("--cache", default=str(ROOT / "outputs" / "cache" / "azure_embeddings_cache.json"))
    parser.add_argument("--env-file", default=str(ROOT / ".env"))
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--open", action="store_true", help="Open generated dashboard in the default browser.")
    args = parser.parse_args()

    benchmark_path = Path(args.benchmark)
    output_csv = Path(args.output_csv)
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

    client = AzureOpenAI(
        api_key=api_key,
        api_version=api_version,
        azure_endpoint=azure_endpoint,
    )

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

    all_texts = collect_all_texts(df)
    cache = load_cache(cache_path)
    embeddings = embed_texts(
        all_texts,
        client=client,
        deployment=deployment,
        cache=cache,
        batch_size=args.batch_size,
    )
    save_cache(cache_path, cache)

    results_df = evaluate_benchmark(df, embeddings)
    output_csv.parent.mkdir(parents=True, exist_ok=True)
    results_df.to_csv(output_csv, index=False)

    points_df = build_points(df, results_df, embeddings)
    write_dashboard(
        output_html=output_html,
        results_df=results_df,
        points_df=points_df,
        deployment=deployment,
        api_version=api_version,
        benchmark_path=benchmark_path,
    )

    print("")
    print("Done.")
    print(f"Benchmark rows: {len(df)}")
    print(f"Unique embedded strings: {len(all_texts)}")
    print(f"Results CSV: {output_csv}")
    print(f"Dashboard HTML: {output_html}")
    print("")
    print("Mean Catholic Alignment Score by condition:")
    print(results_df.groupby("query_condition")["catholic_alignment_score"].mean().round(4).to_string())
    print("")
    print("GitHub Pages can serve the generated dashboard from index.html after commit and push.")

    if args.open:
        webbrowser.open("file://" + str(output_html.resolve()))


if __name__ == "__main__":
    main()
