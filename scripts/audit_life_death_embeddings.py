#!/usr/bin/env python3
from __future__ import annotations

import argparse
import html as html_lib
import os
import webbrowser
from pathlib import Path

import numpy as np
import pandas as pd
import plotly.graph_objects as go
import plotly.io as pio
from dotenv import load_dotenv
from openai import AzureOpenAI

from audit_azure_embeddings import (
    ROOT,
    MODEL_METADATA,
    collect_all_texts,
    display_path,
    embed_texts,
    evaluate_benchmark,
    load_cache,
    make_concept_summary,
    make_condition_summary,
    make_statistical_summary,
    save_cache,
    utc_now,
)

CONDITION_ORDER = ["bare", "ordinary", "academic", "catholic"]
CONDITION_COLORS = {
    "bare": "#94a3b8",
    "ordinary": "#f97316",
    "academic": "#38bdf8",
    "catholic": "#22c55e",
}
LOCUS_COLORS = {
    "Life and Death / Created Life": "#22c55e",
    "Life and Death / Mortality": "#ef4444",
    "Life and Death / Eschatology": "#a855f7",
    "Life and Death / Pastoral Ethics": "#f59e0b",
}


def repo_href(path: Path) -> str:
    return path.resolve().relative_to(ROOT.resolve()).as_posix()


def format_df(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    for col in out.columns:
        if pd.api.types.is_numeric_dtype(out[col]):
            if col in {"p_value", "wilcoxon_p"}:
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else ("<0.001" if x < 0.001 else f"{x:.4f}"))
            elif col in {"n", "positive_count", "negative_count", "zero_count"} or col.endswith("_query_count"):
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else f"{int(x)}")
            elif "rate" in col:
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else f"{x:.2%}")
            else:
                out[col] = out[col].map(lambda x: "" if pd.isna(x) else f"{x:.4f}")
    return out


def apply_opaque(fig: go.Figure) -> go.Figure:
    fig.update_layout(
        template="plotly_dark",
        paper_bgcolor="#111827",
        plot_bgcolor="#111827",
        font={"color": "#e5e7eb"},
    )
    return fig


def make_context_distribution(concept_df: pd.DataFrame) -> go.Figure:
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
        title="Life and Death: CAS by Query Context",
        height=540,
        yaxis_title="Catholic Alignment Score",
        margin={"l": 40, "r": 20, "t": 60, "b": 60},
    )
    return apply_opaque(fig)


def make_quadrant_scatter(concept_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for locus, subset in concept_df.groupby("locus", sort=False):
        fig.add_trace(
            go.Scatter(
                x=subset["ordinary_cas"],
                y=subset["catholic_cas"],
                mode="markers+text",
                name=locus,
                text=subset["concept"],
                textposition="top center",
                marker={
                    "size": 12,
                    "color": LOCUS_COLORS.get(locus, "#94a3b8"),
                    "line": {"width": 1, "color": "#ffffff"},
                    "opacity": 0.9,
                },
                customdata=subset[["concept", "bare_cas", "ordinary_cas", "academic_cas", "catholic_cas", "ordinary_to_catholic_shift"]].to_numpy(),
                hovertemplate=(
                    "<b>%{customdata[0]}</b><br>"
                    "Bare CAS: %{customdata[1]:.4f}<br>"
                    "Ordinary CAS: %{customdata[2]:.4f}<br>"
                    "Academic CAS: %{customdata[3]:.4f}<br>"
                    "Catholic CAS: %{customdata[4]:.4f}<br>"
                    "Ordinary → Catholic shift: %{customdata[5]:.4f}<extra></extra>"
                ),
            )
        )
    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="#e5e7eb")
    fig.add_vline(x=0, line_width=1, line_dash="dash", line_color="#e5e7eb")
    fig.update_layout(
        title="Ordinary Usage vs Catholic Context",
        height=720,
        xaxis_title="Ordinary CAS",
        yaxis_title="Catholic CAS",
        margin={"l": 40, "r": 20, "t": 60, "b": 60},
    )
    return apply_opaque(fig)


def make_life_death_heatmap(concept_df: pd.DataFrame) -> go.Figure:
    plot_df = concept_df.sort_values("ordinary_to_catholic_shift", ascending=True).copy()
    plot_df["label"] = plot_df["locus"] + " — " + plot_df["concept"]
    cols = [
        "bare_cas",
        "ordinary_cas",
        "academic_cas",
        "catholic_cas",
        "ordinary_to_catholic_shift",
        "academic_to_catholic_shift",
    ]
    z = plot_df[cols].to_numpy()
    z_abs = max(0.1, float(np.nanmax(np.abs(z)))) if np.isfinite(z).any() else 0.1
    fig = go.Figure(
        data=go.Heatmap(
            z=z,
            x=[c.replace("_", " ") for c in cols],
            y=plot_df["label"],
            zmin=-z_abs,
            zmax=z_abs,
            colorscale=[[0.0, "#991b1b"], [0.5, "#f8fafc"], [1.0, "#166534"]],
            colorbar={"title": "Score"},
            hovertemplate="<b>%{y}</b><br>%{x}: %{z:.4f}<extra></extra>",
        )
    )
    fig.update_layout(
        title="Life and Death Concept Heatmap",
        height=max(680, int(len(plot_df) * 28)),
        margin={"l": 330, "r": 20, "t": 60, "b": 80},
    )
    return apply_opaque(fig)


def make_slope(concept_df: pd.DataFrame) -> go.Figure:
    fig = go.Figure()
    for locus, subset in concept_df.groupby("locus", sort=False):
        x_values = []
        y_values = []
        hover_values = []
        for _, row in subset.iterrows():
            values = [row[f"{c}_cas"] for c in CONDITION_ORDER]
            x_values.extend(CONDITION_ORDER + [None])
            y_values.extend(values + [None])
            hover = (
                f"{row['concept']}<br>"
                f"Bare: {row['bare_cas']:.4f}<br>"
                f"Ordinary: {row['ordinary_cas']:.4f}<br>"
                f"Academic: {row['academic_cas']:.4f}<br>"
                f"Catholic: {row['catholic_cas']:.4f}<br>"
                f"Ordinary → Catholic: {row['ordinary_to_catholic_shift']:.4f}"
            )
            hover_values.extend([hover] * len(CONDITION_ORDER) + [None])
        fig.add_trace(
            go.Scatter(
                x=x_values,
                y=y_values,
                mode="lines+markers",
                name=locus,
                line={"width": 1.8, "color": LOCUS_COLORS.get(locus, "#94a3b8")},
                marker={"size": 7, "color": LOCUS_COLORS.get(locus, "#94a3b8")},
                hovertext=hover_values,
                hoverinfo="text",
            )
        )
    fig.add_hline(y=0, line_width=1, line_dash="dash", line_color="#e5e7eb")
    fig.update_layout(
        title="Life and Death Context Trajectories",
        height=650,
        xaxis_title="Query context",
        yaxis_title="Catholic Alignment Score",
        margin={"l": 40, "r": 20, "t": 60, "b": 60},
    )
    return apply_opaque(fig)


def raw_block(files: list[Path]) -> str:
    parts = []
    for file in files:
        label = display_path(file)
        content = file.read_text(encoding="utf-8", errors="replace").strip() if file.exists() else "FILE NOT FOUND"
        parts.append(f"===== FILE: {label} =====\n{content}\n")
    combined = "\n".join(parts).strip() + "\n"
    return html_lib.escape(combined)


def write_life_dashboard(
    output_html: Path,
    benchmark_path: Path,
    output_csv: Path,
    output_condition_csv: Path,
    output_concept_csv: Path,
    output_stats_csv: Path,
    results_df: pd.DataFrame,
    condition_df: pd.DataFrame,
    concept_df: pd.DataFrame,
    stats_df: pd.DataFrame,
    deployment: str,
    api_version: str,
) -> None:
    fig1 = pio.to_html(make_context_distribution(concept_df), include_plotlyjs="cdn", full_html=False)
    fig2 = pio.to_html(make_quadrant_scatter(concept_df), include_plotlyjs=False, full_html=False)
    fig3 = pio.to_html(make_slope(concept_df), include_plotlyjs=False, full_html=False)
    fig4 = pio.to_html(make_life_death_heatmap(concept_df), include_plotlyjs=False, full_html=False)

    stats_table = format_df(stats_df).to_html(index=False, classes="scores-table", border=0, escape=True)
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
    concept_table = format_df(concept_df[concept_cols].sort_values("ordinary_to_catholic_shift", ascending=False)).to_html(index=False, classes="scores-table", border=0, escape=True)

    raw_text = raw_block([output_stats_csv, output_concept_csv, output_condition_csv, output_csv])

    n_concepts = int(concept_df["concept"].nunique())
    n_queries = int(len(results_df))
    means = concept_df[["bare_cas", "ordinary_cas", "academic_cas", "catholic_cas", "ordinary_to_catholic_shift"]].mean()
    generated = utc_now()

    html = f"""<!doctype html>
<html lang="en">
<head>
  <meta charset="utf-8">
  <title>Life and Death Semantic Audit</title>
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
      --accent: #f59e0b;
    }}
    * {{ box-sizing: border-box; }}
    html, body {{ min-height: 100%; background: var(--bg); }}
    body {{
      margin: 0;
      font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif;
      background:
        radial-gradient(circle at 20% 0%, rgba(34, 197, 94, 0.20), transparent 28rem),
        radial-gradient(circle at 80% 0%, rgba(239, 68, 68, 0.18), transparent 28rem),
        var(--bg);
      color: var(--text);
      line-height: 1.6;
    }}
    header {{
      padding: 4rem 1.25rem 2rem;
      border-bottom: 1px solid var(--border);
      background: rgba(2, 6, 23, 0.94);
    }}
    main {{ max-width: 1380px; margin: 0 auto; padding: 2rem 1.25rem 4rem; }}
    .hero {{ max-width: 1380px; margin: 0 auto; }}
    h1 {{
      margin: 0 0 0.5rem;
      font-size: clamp(2rem, 5vw, 4rem);
      line-height: 1.05;
      letter-spacing: -0.04em;
    }}
    p {{ color: var(--muted); }}
    .tagline {{ max-width: 980px; font-size: 1.1rem; }}
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
    .metric {{ font-size: 2rem; font-weight: 750; color: var(--text); }}
    .label {{ color: var(--muted); font-size: 0.9rem; }}
    section {{
      background: rgba(15, 23, 42, 0.50);
      border: 1px solid rgba(51, 65, 85, 0.55);
      border-radius: 1rem;
      padding: 0.25rem 0.75rem 1rem;
      margin: 1.25rem 0;
    }}
    .note {{
      border-left: 4px solid var(--accent);
      padding: 1rem;
      background: rgba(245, 158, 11, 0.10);
      border-radius: 0.75rem;
      margin: 1rem 0;
    }}
    .scores-table {{
      width: 100%;
      border-collapse: collapse;
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
    .scores-table td {{ color: #cbd5e1; }}
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
    summary {{ cursor: pointer; font-weight: 700; }}
    textarea {{
      width: 100%;
      min-height: 22rem;
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
      border: 1px solid var(--border);
      border-radius: 0.5rem;
      padding: 0.45rem 0.75rem;
      color: var(--text);
      background: #1e293b;
      cursor: pointer;
    }}
    button:hover {{ background: #334155; }}
    code {{ color: #bae6fd; }}
    a {{ color: #7dd3fc; }}
    footer {{ margin-top: 3rem; color: var(--muted); font-size: 0.9rem; }}
    @media (max-width: 980px) {{ .grid {{ grid-template-columns: repeat(2, minmax(0, 1fr)); }} }}
    @media (max-width: 640px) {{ .grid {{ grid-template-columns: 1fr; }} }}
  </style>
</head>
<body>
  <header>
    <div class="hero">
      <h1>Life and Death Semantic Audit</h1>
      <p class="tagline">
        A focused supplement to CTSB-100, testing concepts where secular, medical, existential,
        and Catholic eschatological meanings strongly overlap.
      </p>
      <p><a href="index.html">Back to main CTSB-100 dashboard</a></p>
    </div>
  </header>
  <main>
    <section class="grid" aria-label="summary metrics">
      <div class="card"><div class="metric">{n_concepts}</div><div class="label">Life/death concepts</div></div>
      <div class="card"><div class="metric">{n_queries}</div><div class="label">Query rows</div></div>
      <div class="card"><div class="metric">{means['bare_cas']:.4f}</div><div class="label">Mean bare CAS</div></div>
      <div class="card"><div class="metric">{means['ordinary_cas']:.4f}</div><div class="label">Mean ordinary CAS</div></div>
      <div class="card"><div class="metric">{means['academic_cas']:.4f}</div><div class="label">Mean academic CAS</div></div>
      <div class="card"><div class="metric">{means['catholic_cas']:.4f}</div><div class="label">Mean Catholic CAS</div></div>
      <div class="card"><div class="metric">{means['ordinary_to_catholic_shift']:.4f}</div><div class="label">Ordinary → Catholic shift</div></div>
    </section>

    <section class="note">
      <strong>Interpretive note:</strong>
      Life and death concepts are intentionally ambiguous: they are biological, medical,
      existential, pastoral, and eschatological at once. The primary question is whether explicit
      Catholic context shifts these concepts toward Catholic descriptors such as resurrection,
      created life, dignity, hope, judgment, and eternal communion with God.
    </section>

    <section><h2>Context Distribution</h2>{fig1}</section>
    <section><h2>Ordinary vs Catholic Quadrant Map</h2>{fig2}</section>
    <section><h2>Context Trajectories</h2>{fig3}</section>
    <section><h2>Concept Heatmap</h2>{fig4}</section>

    <section>
      <h2>Statistical Summary</h2>
      <div class="table-wrap">{stats_table}</div>
    </section>

    <section>
      <h2>Concept-Level Summary</h2>
      <div class="table-wrap">{concept_table}</div>
    </section>

    <section>
      <h2>Advanced Raw Data Export: Life and Death Only</h2>
      <p>This block is hidden by default. Open it and copy only the life/death supplement data.</p>
      <details>
        <summary>Combined life/death raw CSV export</summary>
        <p><button type="button" onclick="copyRawCsv('raw-life-death-csv')">Copy life/death raw CSV export</button></p>
        <textarea id="raw-life-death-csv" readonly spellcheck="false">{raw_text}</textarea>
      </details>
    </section>

    <footer>
      <p>
        Generated: {html_lib.escape(generated)}<br>
        Azure deployment: <code>{html_lib.escape(deployment)}</code><br>
        API version: <code>{html_lib.escape(api_version)}</code><br>
        Model name: <code>{html_lib.escape(MODEL_METADATA["model_name"])}</code><br>
        Model version: <code>{html_lib.escape(MODEL_METADATA["model_version"])}</code><br>
        Life cycle status: <code>{html_lib.escape(MODEL_METADATA["life_cycle_status"])}</code><br>
        Model retirement date: <code>{html_lib.escape(MODEL_METADATA["model_retirement_date"])}</code><br>
        Benchmark: <code>{html_lib.escape(display_path(benchmark_path))}</code>
      </p>
    </footer>
  </main>
  <script>
    async function copyRawCsv(id) {{
      const el = document.getElementById(id);
      if (!el) return;
      try {{
        await navigator.clipboard.writeText(el.value);
        alert("Life/death CSV export copied to clipboard.");
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
    output_html.write_text(html, encoding="utf-8")


def main() -> None:
    parser = argparse.ArgumentParser(description="Focused life/death semantic audit.")
    parser.add_argument("--benchmark", default=str(ROOT / "data" / "benchmarks" / "life_death_v1_draft.csv"))
    parser.add_argument("--output-csv", default=str(ROOT / "outputs" / "results" / "life_death_v1_results.csv"))
    parser.add_argument("--output-condition-csv", default=str(ROOT / "outputs" / "results" / "life_death_v1_condition_summary.csv"))
    parser.add_argument("--output-concept-csv", default=str(ROOT / "outputs" / "results" / "life_death_v1_concept_summary.csv"))
    parser.add_argument("--output-stats-csv", default=str(ROOT / "outputs" / "results" / "life_death_v1_statistical_summary.csv"))
    parser.add_argument("--output-html", default=str(ROOT / "life_death.html"))
    parser.add_argument("--cache", default=str(ROOT / "outputs" / "cache" / "azure_embeddings_cache.json"))
    parser.add_argument("--env-file", default=str(ROOT / ".env"))
    parser.add_argument("--batch-size", type=int, default=64)
    parser.add_argument("--open", action="store_true")
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

    write_life_dashboard(
        output_html=output_html,
        benchmark_path=benchmark_path,
        output_csv=output_csv,
        output_condition_csv=output_condition_csv,
        output_concept_csv=output_concept_csv,
        output_stats_csv=output_stats_csv,
        results_df=results_df,
        condition_df=condition_df,
        concept_df=concept_df,
        stats_df=stats_df,
        deployment=deployment,
        api_version=api_version,
    )

    print("")
    print("Done.")
    print(f"Life/death benchmark rows: {len(df)}")
    print(f"Life/death concepts: {concept_df['concept'].nunique()}")
    print(f"Unique embedded strings: {len(all_texts)}")
    print(f"Results CSV: {output_csv}")
    print(f"Condition summary CSV: {output_condition_csv}")
    print(f"Concept summary CSV: {output_concept_csv}")
    print(f"Statistical summary CSV: {output_stats_csv}")
    print(f"Dashboard HTML: {output_html}")
    print("")
    print("Life/death concept-level means:")
    print(concept_df[["bare_cas", "ordinary_cas", "academic_cas", "catholic_cas", "ordinary_to_catholic_shift"]].mean().round(4).to_string())

    if args.open:
        webbrowser.open("file://" + str(output_html.resolve()))


if __name__ == "__main__":
    main()
