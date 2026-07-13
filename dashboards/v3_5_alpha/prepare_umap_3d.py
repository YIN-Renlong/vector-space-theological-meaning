#!/usr/bin/env python3
"""Create one reproducible three-dimensional UMAP for CTSB v3.5-alpha.

The browser receives only embedding IDs and derived coordinates. Raw vectors
remain local and are never copied into the dashboard.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import importlib.metadata
import json
import os
import platform
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

import numpy as np
import umap
from scipy.spatial import procrustes
from scipy.spatial.distance import pdist
from scipy.stats import spearmanr
from sklearn.neighbors import NearestNeighbors


EXPECTED_VECTOR_COUNT = 3032
EXPECTED_DIMENSIONS = 3072
EXPECTED_SOURCE_SHA256 = (
    "f66fea014d64213fe874f61ca1545d36f4ab37664401824944a101bd7080abf6"
)
CANONICAL_PARAMETERS = {
    "metric": "cosine",
    "n_neighbors": 30,
    "min_dist": 0.15,
    "n_components": 3,
    "random_state": 42,
    "transform_seed": 42,
    "n_jobs": 1,
    "low_memory": True,
}


def find_repository(start: Path) -> Path:
    for candidate in (start, *start.parents):
        if (candidate / ".git").exists() and (candidate / "docs").exists():
            return candidate
    raise RuntimeError("Could not locate the repository root.")


def sha256_file(path: Path) -> str:
    digest = hashlib.sha256()
    with path.open("rb") as handle:
        for block in iter(lambda: handle.read(1024 * 1024), b""):
            digest.update(block)
    return digest.hexdigest()


def read_index(path: Path) -> list[dict[str, str]]:
    with path.open("r", encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle))

    required = {
        "embedding_id",
        "text_sha256",
        "text",
        "roles",
        "dimensions",
        "l2_norm",
    }
    if not rows:
        raise ValueError("embedding_index.csv is empty.")
    missing = required - set(rows[0])
    if missing:
        raise ValueError(f"embedding_index.csv is missing columns: {sorted(missing)}")
    if len(rows) != EXPECTED_VECTOR_COUNT:
        raise ValueError(
            f"Expected {EXPECTED_VECTOR_COUNT} index rows; found {len(rows)}."
        )

    embedding_ids = [row["embedding_id"] for row in rows]
    text_hashes = [row["text_sha256"] for row in rows]
    if len(set(embedding_ids)) != len(embedding_ids):
        raise ValueError("embedding_id values are not unique.")
    if len(set(text_hashes)) != len(text_hashes):
        raise ValueError("text_sha256 values are not unique.")
    if any(int(row["dimensions"]) != EXPECTED_DIMENSIONS for row in rows):
        raise ValueError("The index contains an unexpected embedding dimension.")
    return rows


def load_matrix(npz_path: Path, index_rows: list[dict[str, str]]) -> tuple[np.ndarray, str]:
    embedding_ids = [row["embedding_id"] for row in index_rows]
    text_hashes = [row["text_sha256"] for row in index_rows]

    with np.load(npz_path, allow_pickle=False) as archive:
        keys = list(archive.files)
        key_set = set(keys)

        if len(keys) == 1:
            candidate = np.asarray(archive[keys[0]])
            if candidate.shape == (EXPECTED_VECTOR_COUNT, EXPECTED_DIMENSIONS):
                matrix = candidate.astype(np.float32, copy=False)
                mapping = "single_matrix_in_embedding_index_row_order"
            else:
                raise ValueError(
                    f"Unexpected single-array shape {candidate.shape}; "
                    f"expected {(EXPECTED_VECTOR_COUNT, EXPECTED_DIMENSIONS)}."
                )
        elif set(embedding_ids).issubset(key_set):
            matrix = np.vstack(
                [np.asarray(archive[embedding_id]) for embedding_id in embedding_ids]
            ).astype(np.float32, copy=False)
            mapping = "npz_keys_match_embedding_id"
        elif set(text_hashes).issubset(key_set):
            matrix = np.vstack(
                [np.asarray(archive[text_hash]) for text_hash in text_hashes]
            ).astype(np.float32, copy=False)
            mapping = "npz_keys_match_text_sha256"
        elif set(f"v_{value}" for value in text_hashes).issubset(key_set):
            matrix = np.vstack(
                [np.asarray(archive[f"v_{text_hash}"]) for text_hash in text_hashes]
            ).astype(np.float32, copy=False)
            mapping = "npz_keys_match_prefixed_text_sha256"
        else:
            sample = ", ".join(keys[:5])
            raise ValueError(
                "Could not prove the mapping between NPZ arrays and embedding_index.csv. "
                f"NPZ array count: {len(keys)}; sample keys: {sample}"
            )

    if matrix.shape != (EXPECTED_VECTOR_COUNT, EXPECTED_DIMENSIONS):
        raise ValueError(
            f"Unexpected matrix shape {matrix.shape}; "
            f"expected {(EXPECTED_VECTOR_COUNT, EXPECTED_DIMENSIONS)}."
        )
    if not np.isfinite(matrix).all():
        raise ValueError("The vector matrix contains non-finite values.")
    return np.ascontiguousarray(matrix, dtype=np.float32), mapping


def fit_projection(
    matrix: np.ndarray,
    *,
    n_neighbors: int,
    min_dist: float,
) -> np.ndarray:
    reducer = umap.UMAP(
        metric="cosine",
        n_neighbors=n_neighbors,
        min_dist=min_dist,
        n_components=3,
        random_state=42,
        transform_seed=42,
        n_jobs=1,
        low_memory=True,
        verbose=False,
    )
    coordinates = reducer.fit_transform(matrix)
    coordinates = np.asarray(coordinates, dtype=np.float32)
    if coordinates.shape != (EXPECTED_VECTOR_COUNT, 3):
        raise ValueError(f"Unexpected UMAP output shape: {coordinates.shape}")
    if not np.isfinite(coordinates).all():
        raise ValueError("UMAP generated non-finite coordinates.")
    return coordinates


def neighbour_overlap(first: np.ndarray, second: np.ndarray, k: int = 15) -> float:
    first_nn = NearestNeighbors(n_neighbors=k + 1).fit(first)
    second_nn = NearestNeighbors(n_neighbors=k + 1).fit(second)
    first_indices = first_nn.kneighbors(return_distance=False)[:, 1:]
    second_indices = second_nn.kneighbors(return_distance=False)[:, 1:]
    overlaps = [
        len(set(a.tolist()).intersection(b.tolist())) / k
        for a, b in zip(first_indices, second_indices)
    ]
    return float(np.mean(overlaps))


def projection_comparison(
    canonical: np.ndarray,
    alternate: np.ndarray,
    sample_indices: np.ndarray,
) -> dict[str, float]:
    _, _, disparity = procrustes(canonical, alternate)
    canonical_distances = pdist(canonical[sample_indices], metric="euclidean")
    alternate_distances = pdist(alternate[sample_indices], metric="euclidean")
    correlation = spearmanr(canonical_distances, alternate_distances).statistic
    return {
        "procrustes_disparity": round(float(disparity), 8),
        "sampled_pairwise_distance_spearman": round(float(correlation), 6),
        "mean_k15_neighbour_overlap": round(
            neighbour_overlap(canonical, alternate, k=15), 6
        ),
    }


def write_coordinates(
    path: Path,
    index_rows: list[dict[str, str]],
    coordinates: np.ndarray,
) -> None:
    temporary = path.with_suffix(path.suffix + ".tmp")
    with temporary.open("w", encoding="utf-8", newline="") as handle:
        writer = csv.writer(handle, lineterminator="\n")
        writer.writerow(["embedding_id", "umap_x", "umap_y", "umap_z"])
        for row, point in zip(index_rows, coordinates):
            writer.writerow(
                [
                    row["embedding_id"],
                    f"{float(point[0]):.9f}",
                    f"{float(point[1]):.9f}",
                    f"{float(point[2]):.9f}",
                ]
            )
    os.replace(temporary, path)


def package_version(name: str) -> str:
    try:
        return importlib.metadata.version(name)
    except importlib.metadata.PackageNotFoundError:
        return "unknown"


def existing_generation_timestamp(
    manifest_path: Path,
    source_hash: str,
    coordinate_hash: str,
) -> str | None:
    if not manifest_path.exists():
        return None
    try:
        existing = json.loads(manifest_path.read_text(encoding="utf-8"))
    except (OSError, json.JSONDecodeError):
        return None
    if (
        existing.get("source_embedding_sha256") == source_hash
        and existing.get("coordinate_file_sha256") == coordinate_hash
        and existing.get("parameters") == CANONICAL_PARAMETERS
        and existing.get("software", {}).get("umap-learn")
        == package_version("umap-learn")
    ):
        return existing.get("generated_at_utc")
    return None


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "--diagnostics",
        action="store_true",
        help="Run two non-published nearby-parameter sensitivity projections.",
    )
    parser.add_argument(
        "--allow-source-hash-mismatch",
        action="store_true",
        help="Allow preprocessing when the local NPZ hash differs from the recorded run.",
    )
    args = parser.parse_args()

    repository = find_repository(Path(__file__).resolve())
    run_relative = Path(
        "outputs/v3_5_alpha/runs/v3_5_alpha_azure_20260713-010232"
    )
    run_dir = repository / run_relative
    npz_path = run_dir / "embeddings.npz"
    index_path = run_dir / "embedding_index.csv"
    coordinate_path = run_dir / "umap_3d_coordinates.csv"
    manifest_path = run_dir / "umap_3d_manifest.json"

    for source in (npz_path, index_path):
        if not source.is_file():
            raise FileNotFoundError(f"Required source file not found: {source.name}")

    source_hash = sha256_file(npz_path)
    if source_hash != EXPECTED_SOURCE_SHA256 and not args.allow_source_hash_mismatch:
        raise ValueError(
            "embeddings.npz does not match the recorded source hash. "
            "Use --allow-source-hash-mismatch only after investigating the run."
        )

    index_rows = read_index(index_path)
    matrix, mapping = load_matrix(npz_path, index_rows)

    print("Fitting canonical 3D UMAP...")
    canonical = fit_projection(matrix, n_neighbors=30, min_dist=0.15)
    write_coordinates(coordinate_path, index_rows, canonical)
    coordinate_hash = sha256_file(coordinate_path)

    sensitivity: list[dict[str, Any]] = []
    if args.diagnostics:
        rng = np.random.default_rng(42)
        sample_indices = np.sort(
            rng.choice(EXPECTED_VECTOR_COUNT, size=600, replace=False)
        )
        for setting in (
            {"n_neighbors": 15, "min_dist": 0.10},
            {"n_neighbors": 45, "min_dist": 0.25},
        ):
            print(
                "Running non-published sensitivity fit: "
                f"n_neighbors={setting['n_neighbors']}, "
                f"min_dist={setting['min_dist']}"
            )
            alternate = fit_projection(matrix, **setting)
            comparison = projection_comparison(
                canonical, alternate, sample_indices
            )
            sensitivity.append(
                {
                    "parameters": {
                        "metric": "cosine",
                        "n_components": 3,
                        "random_state": 42,
                        **setting,
                    },
                    **comparison,
                }
            )
            del alternate

    generated_at = existing_generation_timestamp(
        manifest_path, source_hash, coordinate_hash
    )
    if not generated_at:
        generated_at = datetime.now(timezone.utc).replace(microsecond=0).isoformat()

    manifest = {
        "schema_version": 1,
        "source_run_id": "v3_5_alpha_azure_20260713-010232",
        "source_embedding_file": str(run_relative / "embeddings.npz"),
        "source_embedding_sha256": source_hash,
        "source_embedding_index_file": str(run_relative / "embedding_index.csv"),
        "source_embedding_index_sha256": sha256_file(index_path),
        "vector_count": EXPECTED_VECTOR_COUNT,
        "original_dimensions": EXPECTED_DIMENSIONS,
        "coordinate_file": str(run_relative / coordinate_path.name),
        "coordinate_file_sha256": coordinate_hash,
        "coordinate_columns": ["embedding_id", "umap_x", "umap_y", "umap_z"],
        "mapping_verification": mapping,
        "parameters": CANONICAL_PARAMETERS,
        "software": {
            "python": platform.python_version(),
            "numpy": package_version("numpy"),
            "scipy": package_version("scipy"),
            "scikit-learn": package_version("scikit-learn"),
            "numba": package_version("numba"),
            "pynndescent": package_version("pynndescent"),
            "umap-learn": package_version("umap-learn"),
        },
        "sensitivity_diagnostics": sensitivity,
        "sensitivity_note": (
            "Alternate fits are diagnostics only and are not published as coordinates. "
            "All dashboard UMAP views reuse the canonical coordinate file."
        ),
        "interpretive_status": (
            "Exploratory projection only. Numerical cosine analysis in the original "
            "3072-dimensional space remains primary."
        ),
        "generated_at_utc": generated_at,
    }

    temporary_manifest = manifest_path.with_suffix(".json.tmp")
    temporary_manifest.write_text(
        json.dumps(manifest, indent=2, sort_keys=True) + "\n",
        encoding="utf-8",
    )
    os.replace(temporary_manifest, manifest_path)

    print("")
    print("UMAP preparation complete.")
    print(f"Vectors:       {EXPECTED_VECTOR_COUNT}")
    print(f"Dimensions:    {EXPECTED_DIMENSIONS}")
    print(f"Coordinates:   {coordinate_path.relative_to(repository)}")
    print(f"Manifest:      {manifest_path.relative_to(repository)}")
    print(f"Source SHA256: {source_hash}")
    print(f"Output SHA256: {coordinate_hash}")


if __name__ == "__main__":
    main()
