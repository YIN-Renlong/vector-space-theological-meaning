"use strict";

/* ==========================================================
   CTSB v3.5-alpha dashboard
   Part 1: data access, shared utilities, condition charts,
   and matched shift decomposition
   ========================================================== */

(() => {
  const RUN_BASE =
    "../../outputs/v3_5_alpha/runs/" +
    "v3_5_alpha_azure_20260713-010232";

  const BENCHMARK_BASE =
    "../../data/benchmarks/v3_5_alpha/generated_100";

  const FILES = Object.freeze({
    conditionStatistics: `${RUN_BASE}/alpha_condition_statistics.csv`,
    shiftStatistics: `${RUN_BASE}/alpha_shift_statistics.csv`,
    conditionSummary: `${RUN_BASE}/condition_summary.csv`,
    queryScores: `${RUN_BASE}/query_scores.csv`,
    shifts: `${RUN_BASE}/shifts.csv`,
    referenceSensitivity:
      `${RUN_BASE}/leave_one_reference_out_summary.csv`,
    paraphraseCondition:
      `${RUN_BASE}/paraphrase_condition_sensitivity.csv`,
    paraphraseShift:
      `${RUN_BASE}/paraphrase_shift_sensitivity.csv`,
    validationMetrics: `${RUN_BASE}/validation_metrics.csv`,
    embeddingIndex: `${RUN_BASE}/embedding_index.csv`,
    umapCoordinates: `${RUN_BASE}/umap_3d_coordinates.csv`,
    umapManifest: `${RUN_BASE}/umap_3d_manifest.json`,
    comparisons: `${BENCHMARK_BASE}/comparisons.csv`,
    references: `${BENCHMARK_BASE}/references.csv`,
    validation: `${BENCHMARK_BASE}/validation.csv`
  });

  const COLORS = Object.freeze({
    catholic: "#173f6f",
    catholicLight: "#7d9fc3",
    comparison: "#a36f16",
    comparisonLight: "#d0ac65",
    cas: "#675184",
    casLight: "#ad9bc0",
    integrative: "#187b78",
    critical: "#7a3045",
    neutral: "#667486",
    neutralLight: "#dce1e7",
    grid: "#e4e8ed",
    ink: "#182130",
    muted: "#657083",
    white: "#ffffff",
    transparent: "rgba(0,0,0,0)"
  });

  const LOCUS_COLORS = Object.freeze({
    "Freedom Truth and Moral Teleology": "#24598a",
    "Human Dignity and Theological Anthropology": "#7a3045",
    "Love Communion and Sacramentality": "#187b78",
    "Sin Grace and Redemption": "#675184"
  });

  const RELATIONSHIP_SYMBOLS = Object.freeze({
    complementary_levels: "circle",
    valid_but_partial: "square",
    normatively_conflicting: "diamond",
    alternative_lexical_senses: "triangle-up",
    generic_religious_vs_catholic_specific: "cross"
  });

  const CONDITION_ORDER = Object.freeze([
    "bare",
    "natural_general",
    "natural_ambiguous",
    "label_free_theological",
    "explicit_catholic",
    "integrative",
    "critical"
  ]);

  const CONDITION_LABELS = Object.freeze({
    bare: "Bare",
    natural_general: "Natural general",
    natural_ambiguous: "Natural ambiguous",
    label_free_theological: "Label-free theological",
    explicit_catholic: "Explicit Catholic",
    integrative: "Integrative",
    critical: "Critical"
  });

  const SHIFT_ORDER = Object.freeze([
    "bare_to_general",
    "general_to_ambiguous",
    "general_to_label_free_theological",
    "label_free_to_explicit_catholic",
    "general_to_integrative",
    "general_to_critical"
  ]);

  const SHIFT_LABELS = Object.freeze({
    bare_to_general: "Bare → general",
    general_to_ambiguous: "General → ambiguous",
    general_to_label_free_theological:
      "General → label-free theological",
    label_free_to_explicit_catholic:
      "Label-free → explicit Catholic",
    general_to_integrative: "General → integrative",
    general_to_critical: "General → critical"
  });

  const state = {
    data: null,
    points: [],
    textMetadata: new Map(),
    comparisonsByAudit: new Map(),
    coordinatesById: new Map(),
    selectedAuditId: "",
    selectedQueryId: "",
    defaultCamera: {
      eye: { x: 1.45, y: 1.45, z: 1.18 },
      center: { x: 0, y: 0, z: 0 },
      up: { x: 0, y: 0, z: 1 }
    }
  };

  const plotConfig = Object.freeze({
    responsive: true,
    displaylogo: false,
    scrollZoom: true,
    doubleClick: "reset",
    modeBarButtonsToRemove: [
      "lasso2d",
      "select2d",
      "autoScale2d",
      "toggleSpikelines"
    ],
    toImageButtonOptions: {
      format: "png",
      filename: "ctsb_v3_5_alpha_chart",
      height: 900,
      width: 1400,
      scale: 2
    }
  });

  function byId(id) {
    return document.getElementById(id);
  }

  function assertLibrary(name, value) {
    if (!value) {
      throw new Error(
        `${name} did not load. Check the network connection and Content Security Policy.`
      );
    }
  }

  function number(value, fallback = 0) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed : fallback;
  }

  function boolean(value) {
    if (typeof value === "boolean") {
      return value;
    }
    return String(value).trim().toLowerCase() === "true";
  }

  function formatNumber(value, digits = 3) {
    const parsed = Number(value);
    return Number.isFinite(parsed) ? parsed.toFixed(digits) : "—";
  }

  function formatSigned(value, digits = 3) {
    const parsed = Number(value);
    if (!Number.isFinite(parsed)) {
      return "—";
    }
    if (Math.abs(parsed) < 0.5 * 10 ** -digits) {
      return (0).toFixed(digits);
    }
    return `${parsed > 0 ? "+" : "−"}${Math.abs(parsed).toFixed(digits)}`;
  }

  function formatPercent(value, digits = 1) {
    const parsed = Number(value);
    return Number.isFinite(parsed)
      ? `${(parsed * 100).toFixed(digits)}%`
      : "—";
  }

  function formatInteger(value) {
    const parsed = Number(value);
    return Number.isFinite(parsed)
      ? new Intl.NumberFormat("en").format(parsed)
      : "—";
  }

  function humanise(value) {
    return String(value ?? "")
      .replaceAll("_", " ")
      .replace(/\b\w/g, character => character.toUpperCase());
  }

  function truncate(value, length = 150) {
    const text = String(value ?? "");
    return text.length > length
      ? `${text.slice(0, length - 1).trimEnd()}…`
      : text;
  }

  function escapeHtml(value) {
    return String(value ?? "")
      .replaceAll("&", "&amp;")
      .replaceAll("<", "&lt;")
      .replaceAll(">", "&gt;")
      .replaceAll('"', "&quot;")
      .replaceAll("'", "&#039;");
  }

  function uniqueSorted(values) {
    return [...new Set(values.filter(Boolean))]
      .sort((left, right) =>
        String(left).localeCompare(String(right), "en", {
          sensitivity: "base"
        })
      );
  }

  function mean(values) {
    const finite = values.map(Number).filter(Number.isFinite);
    if (!finite.length) {
      return Number.NaN;
    }
    return finite.reduce((total, value) => total + value, 0) / finite.length;
  }

  function median(values) {
    const finite = values
      .map(Number)
      .filter(Number.isFinite)
      .sort((left, right) => left - right);

    if (!finite.length) {
      return Number.NaN;
    }

    const middle = Math.floor(finite.length / 2);
    return finite.length % 2
      ? finite[middle]
      : (finite[middle - 1] + finite[middle]) / 2;
  }

  function sum(values) {
    return values
      .map(Number)
      .filter(Number.isFinite)
      .reduce((total, value) => total + value, 0);
  }

  function setStatus(message, type = "loading") {
    const element = byId("app-status");
    if (!element) {
      return;
    }

    element.textContent = message;
    element.classList.toggle("is-ready", type === "ready");
    element.classList.toggle("is-error", type === "error");
  }

  function setText(id, value) {
    const element = byId(id);
    if (element) {
      element.textContent = value;
    }
  }

  function createElement(tag, attributes = {}, text = null) {
    const element = document.createElement(tag);

    Object.entries(attributes).forEach(([name, value]) => {
      if (name === "className") {
        element.className = value;
      } else if (name === "dataset") {
        Object.entries(value).forEach(([key, item]) => {
          element.dataset[key] = item;
        });
      } else {
        element.setAttribute(name, value);
      }
    });

    if (text !== null) {
      element.textContent = text;
    }

    return element;
  }

  function replaceChildren(element, children) {
    if (!element) {
      return;
    }
    element.replaceChildren(...children);
  }

  function populateSelect(
    select,
    values,
    {
      allLabel = null,
      selectedValue = null,
      labelFunction = humanise
    } = {}
  ) {
    if (!select) {
      return;
    }

    const options = [];

    if (allLabel !== null) {
      options.push(createElement("option", { value: "all" }, allLabel));
    }

    values.forEach(value => {
      options.push(
        createElement(
          "option",
          { value: String(value) },
          labelFunction(value)
        )
      );
    });

    replaceChildren(select, options);

    if (
      selectedValue !== null &&
      [...select.options].some(option => option.value === selectedValue)
    ) {
      select.value = selectedValue;
    }
  }

  function baseLayout(overrides = {}) {
    return {
      autosize: true,
      margin: { l: 70, r: 30, t: 25, b: 60 },
      paper_bgcolor: COLORS.transparent,
      plot_bgcolor: COLORS.white,
      font: {
        family:
          'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
        size: 12,
        color: COLORS.ink
      },
      hoverlabel: {
        bgcolor: COLORS.white,
        bordercolor: "#c5ccd5",
        font: {
          family:
            'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
          size: 12,
          color: COLORS.ink
        },
        align: "left"
      },
      legend: {
        orientation: "h",
        x: 0,
        xanchor: "left",
        y: 1.08,
        yanchor: "bottom",
        font: { size: 11 }
      },
      xaxis: {
        showgrid: true,
        gridcolor: COLORS.grid,
        zerolinecolor: "#9ba5b1",
        tickfont: { size: 11 },
        titlefont: { size: 12 }
      },
      yaxis: {
        showgrid: false,
        tickfont: { size: 11 },
        titlefont: { size: 12 }
      },
      ...overrides
    };
  }

  function darkLayout(overrides = {}) {
    const layout = baseLayout(overrides);
    return {
      ...layout,
      paper_bgcolor: COLORS.transparent,
      plot_bgcolor: "#192434",
      font: {
        ...layout.font,
        color: "#e8edf4"
      },
      hoverlabel: {
        ...layout.hoverlabel,
        bgcolor: "#ffffff",
        font: {
          ...layout.hoverlabel.font,
          color: COLORS.ink
        }
      },
      legend: {
        ...layout.legend,
        font: { size: 11, color: "#d7dfe8" }
      },
      xaxis: {
        ...layout.xaxis,
        gridcolor: "rgba(255,255,255,0.11)",
        zerolinecolor: "rgba(255,255,255,0.48)",
        tickfont: { size: 11, color: "#d7dfe8" },
        titlefont: { size: 12, color: "#d7dfe8" }
      },
      yaxis: {
        ...layout.yaxis,
        tickfont: { size: 11, color: "#d7dfe8" },
        titlefont: { size: 12, color: "#d7dfe8" }
      }
    };
  }

  async function fetchText(path) {
    const url = new URL(path, window.location.href);
    const response = await fetch(url, { cache: "no-store" });

    if (!response.ok) {
      throw new Error(
        `Could not load ${url.pathname}: HTTP ${response.status}`
      );
    }

    return response.text();
  }

  async function fetchJson(path) {
    const url = new URL(path, window.location.href);
    const response = await fetch(url, { cache: "no-store" });

    if (!response.ok) {
      throw new Error(
        `Could not load ${url.pathname}: HTTP ${response.status}`
      );
    }

    return response.json();
  }

  async function fetchCsv(path) {
    const text = await fetchText(path);

    return new Promise((resolve, reject) => {
      window.Papa.parse(text, {
        header: true,
        dynamicTyping: true,
        skipEmptyLines: "greedy",
        transformHeader: header => header.trim(),
        complete(result) {
          const seriousErrors = result.errors.filter(
            error => error.code !== "TooFewFields"
          );

          if (seriousErrors.length) {
            reject(
              new Error(
                `CSV parsing failed for ${path}: ` +
                seriousErrors
                  .slice(0, 3)
                  .map(error => error.message)
                  .join("; ")
              )
            );
            return;
          }

          resolve(result.data);
        },
        error(error) {
          reject(error);
        }
      });
    });
  }

  function validateColumns(name, rows, columns) {
    if (!Array.isArray(rows) || !rows.length) {
      throw new Error(`${name} is empty.`);
    }

    const actual = new Set(Object.keys(rows[0]));
    const missing = columns.filter(column => !actual.has(column));

    if (missing.length) {
      throw new Error(
        `${name} is missing required columns: ${missing.join(", ")}`
      );
    }
  }

  function validateLoadedData(data) {
    const definitions = [
      [
        "condition statistics",
        data.conditionStatistics,
        [
          "condition",
          "concept_count",
          "mean_s_c",
          "mean_s_r",
          "mean_cas",
          "cas_bootstrap_95_low",
          "cas_bootstrap_95_high",
          "positive_cas_proportion"
        ]
      ],
      [
        "shift statistics",
        data.shiftStatistics,
        [
          "contrast_type",
          "concept_count",
          "mean_delta_s_c",
          "mean_delta_s_r",
          "mean_delta_cas"
        ]
      ],
      [
        "condition summary",
        data.conditionSummary,
        [
          "audit_id",
          "concept",
          "condition",
          "mean_s_c",
          "mean_s_r",
          "mean_cas"
        ]
      ],
      [
        "query scores",
        data.queryScores,
        [
          "query_id",
          "audit_id",
          "condition",
          "query_text",
          "s_c",
          "s_r",
          "cas"
        ]
      ],
      [
        "shifts",
        data.shifts,
        [
          "audit_id",
          "contrast_type",
          "delta_s_c",
          "delta_s_r",
          "delta_cas"
        ]
      ],
      [
        "reference sensitivity",
        data.referenceSensitivity,
        [
          "query_id",
          "sign_stability_proportion",
          "max_absolute_cas_change"
        ]
      ],
      [
        "paraphrase condition sensitivity",
        data.paraphraseCondition,
        [
          "audit_id",
          "condition",
          "min_cas",
          "max_cas",
          "cas_standard_deviation"
        ]
      ],
      [
        "comparisons",
        data.comparisons,
        [
          "audit_id",
          "concept",
          "primary_locus",
          "comparison_register",
          "relationship_type"
        ]
      ],
      [
        "embedding index",
        data.embeddingIndex,
        ["embedding_id", "text", "roles", "dimensions"]
      ],
      [
        "UMAP coordinates",
        data.umapCoordinates,
        ["embedding_id", "umap_x", "umap_y", "umap_z"]
      ]
    ];

    definitions.forEach(([name, rows, columns]) => {
      validateColumns(name, rows, columns);
    });

    if (data.conditionStatistics.length !== 7) {
      throw new Error(
        `Expected 7 condition-statistic rows; found ` +
        `${data.conditionStatistics.length}.`
      );
    }

    if (data.shiftStatistics.length !== 6) {
      throw new Error(
        `Expected 6 shift-statistic rows; found ` +
        `${data.shiftStatistics.length}.`
      );
    }

    if (data.queryScores.length !== 1624) {
      throw new Error(
        `Expected 1,624 query-score rows; found ${data.queryScores.length}.`
      );
    }

    if (data.embeddingIndex.length !== 3032) {
      throw new Error(
        `Expected 3,032 embedding-index rows; found ` +
        `${data.embeddingIndex.length}.`
      );
    }

    if (data.umapCoordinates.length !== 3032) {
      throw new Error(
        `Expected 3,032 UMAP rows; found ${data.umapCoordinates.length}.`
      );
    }

    const maximumCasError = Math.max(
      ...data.queryScores.map(row =>
        Math.abs(number(row.cas) - (number(row.s_c) - number(row.s_r)))
      )
    );

    if (maximumCasError > 1e-8) {
      throw new Error(
        `CAS reconstruction failed; maximum error was ${maximumCasError}.`
      );
    }

    const maximumShiftError = Math.max(
      ...data.shifts.map(row =>
        Math.abs(
          number(row.delta_cas) -
          (number(row.delta_s_c) - number(row.delta_s_r))
        )
      )
    );

    if (maximumShiftError > 1e-8) {
      throw new Error(
        `Shift decomposition failed; maximum error was ${maximumShiftError}.`
      );
    }
  }

  async function loadAllData() {
    const [
      conditionStatistics,
      shiftStatistics,
      conditionSummary,
      queryScores,
      shifts,
      referenceSensitivity,
      paraphraseCondition,
      paraphraseShift,
      validationMetrics,
      embeddingIndex,
      umapCoordinates,
      umapManifest,
      comparisons,
      references,
      validation
    ] = await Promise.all([
      fetchCsv(FILES.conditionStatistics),
      fetchCsv(FILES.shiftStatistics),
      fetchCsv(FILES.conditionSummary),
      fetchCsv(FILES.queryScores),
      fetchCsv(FILES.shifts),
      fetchCsv(FILES.referenceSensitivity),
      fetchCsv(FILES.paraphraseCondition),
      fetchCsv(FILES.paraphraseShift),
      fetchCsv(FILES.validationMetrics),
      fetchCsv(FILES.embeddingIndex),
      fetchCsv(FILES.umapCoordinates),
      fetchJson(FILES.umapManifest),
      fetchCsv(FILES.comparisons),
      fetchCsv(FILES.references),
      fetchCsv(FILES.validation)
    ]);

    const data = {
      conditionStatistics,
      shiftStatistics,
      conditionSummary,
      queryScores,
      shifts,
      referenceSensitivity,
      paraphraseCondition,
      paraphraseShift,
      validationMetrics,
      embeddingIndex,
      umapCoordinates,
      umapManifest,
      comparisons,
      references,
      validation
    };

    validateLoadedData(data);
    return data;
  }

  function renderConditionTable(rows) {
    const body = byId("condition-table-body");
    if (!body) {
      return;
    }

    const tableRows = rows.map(row => {
      const tr = createElement("tr");

      [
        CONDITION_LABELS[row.condition] ?? humanise(row.condition),
        formatInteger(row.concept_count),
        formatNumber(row.mean_s_c),
        formatNumber(row.mean_s_r),
        formatSigned(row.mean_cas),
        `${formatSigned(row.cas_bootstrap_95_low)} to ` +
          `${formatSigned(row.cas_bootstrap_95_high)}`,
        formatPercent(row.positive_cas_proportion)
      ].forEach(value => {
        tr.append(createElement("td", {}, value));
      });

      return tr;
    });

    replaceChildren(body, tableRows);
  }

  function renderConditionCharts() {
    const rows = [...state.data.conditionStatistics]
      .sort(
        (left, right) =>
          CONDITION_ORDER.indexOf(left.condition) -
          CONDITION_ORDER.indexOf(right.condition)
      );

    const labels = rows.map(
      row => CONDITION_LABELS[row.condition] ?? humanise(row.condition)
    );

    const lineX = [];
    const lineY = [];

    rows.forEach((row, index) => {
      lineX.push(number(row.mean_s_c), number(row.mean_s_r), null);
      lineY.push(labels[index], labels[index], null);
    });

    const componentTraces = [
      {
        type: "scatter",
        mode: "lines",
        x: lineX,
        y: lineY,
        line: {
          color: "#c7ced7",
          width: 3
        },
        hoverinfo: "skip",
        showlegend: false
      },
      {
        type: "scatter",
        mode: "markers",
        name: "Catholic-reference similarity (S_C)",
        x: rows.map(row => number(row.mean_s_c)),
        y: labels,
        customdata: rows.map(row => [
          CONDITION_LABELS[row.condition],
          number(row.concept_count),
          number(row.mean_cas)
        ]),
        marker: {
          color: COLORS.catholic,
          size: 11,
          symbol: "circle",
          line: { color: COLORS.white, width: 1 }
        },
        hovertemplate:
          "<b>%{customdata[0]}</b><br>" +
          "S<sub>C</sub>: %{x:.4f}<br>" +
          "CAS: %{customdata[2]:+.4f}<br>" +
          "Concepts: %{customdata[1]}<extra></extra>"
      },
      {
        type: "scatter",
        mode: "markers",
        name: "Comparison-reference similarity (S_R)",
        x: rows.map(row => number(row.mean_s_r)),
        y: labels,
        customdata: rows.map(row => [
          CONDITION_LABELS[row.condition],
          number(row.concept_count),
          number(row.mean_cas)
        ]),
        marker: {
          color: COLORS.comparison,
          size: 11,
          symbol: "square",
          line: { color: COLORS.white, width: 1 }
        },
        hovertemplate:
          "<b>%{customdata[0]}</b><br>" +
          "S<sub>R</sub>: %{x:.4f}<br>" +
          "CAS: %{customdata[2]:+.4f}<br>" +
          "Concepts: %{customdata[1]}<extra></extra>"
      }
    ];

    const componentLayout = baseLayout({
      height: 460,
      margin: { l: 155, r: 25, t: 45, b: 55 },
      xaxis: {
        ...baseLayout().xaxis,
        title: "Mean cosine similarity",
        range: [0.3, 0.95],
        tickformat: ".2f"
      },
      yaxis: {
        ...baseLayout().yaxis,
        autorange: "reversed",
        categoryorder: "array",
        categoryarray: labels
      }
    });

    window.Plotly.newPlot(
      "condition-components-chart",
      componentTraces,
      componentLayout,
      plotConfig
    );

    const casTrace = {
      type: "scatter",
      mode: "markers+text",
      name: "Mean CAS",
      x: rows.map(row => number(row.mean_cas)),
      y: labels,
      text: rows.map(row => formatSigned(row.mean_cas)),
      textposition: rows.map(row =>
        number(row.mean_cas) >= 0 ? "middle right" : "middle left"
      ),
      textfont: {
        color: COLORS.cas,
        size: 10
      },
      customdata: rows.map(row => [
        CONDITION_LABELS[row.condition],
        number(row.cas_bootstrap_95_low),
        number(row.cas_bootstrap_95_high),
        number(row.positive_cas_proportion),
        number(row.concept_count)
      ]),
      error_x: {
        type: "data",
        symmetric: false,
        array: rows.map(
          row =>
            number(row.cas_bootstrap_95_high) -
            number(row.mean_cas)
        ),
        arrayminus: rows.map(
          row =>
            number(row.mean_cas) -
            number(row.cas_bootstrap_95_low)
        ),
        color: COLORS.casLight,
        thickness: 2,
        width: 6
      },
      marker: {
        color: COLORS.cas,
        size: 11,
        symbol: "diamond",
        line: { color: COLORS.white, width: 1 }
      },
      cliponaxis: false,
      hovertemplate:
        "<b>%{customdata[0]}</b><br>" +
        "Mean CAS: %{x:+.4f}<br>" +
        "95% interval: %{customdata[1]:+.4f} to " +
        "%{customdata[2]:+.4f}<br>" +
        "Positive CAS: %{customdata[3]:.1%}<br>" +
        "Concepts: %{customdata[4]}<extra></extra>"
    };

    const casLayout = baseLayout({
      height: 460,
      showlegend: false,
      margin: { l: 155, r: 55, t: 45, b: 55 },
      xaxis: {
        ...baseLayout().xaxis,
        title: "Mean Catholic Association Contrast (CAS)",
        range: [-0.32, 0.52],
        tickformat: "+.2f",
        zeroline: true,
        zerolinewidth: 2
      },
      yaxis: {
        ...baseLayout().yaxis,
        autorange: "reversed",
        categoryorder: "array",
        categoryarray: labels
      }
    });

    window.Plotly.newPlot(
      "condition-cas-chart",
      [casTrace],
      casLayout,
      plotConfig
    );

    const general = rows.find(row => row.condition === "natural_general");
    const ambiguous = rows.find(
      row => row.condition === "natural_ambiguous"
    );
    const integrative = rows.find(row => row.condition === "integrative");

    setText(
      "condition-components-summary",
      `Natural-general wording had mean S_C ` +
        `${formatNumber(general.mean_s_c)} and S_R ` +
        `${formatNumber(general.mean_s_r)}. Integrative wording retained ` +
        `higher proximity to both fields: S_C ` +
        `${formatNumber(integrative.mean_s_c)} and S_R ` +
        `${formatNumber(integrative.mean_s_r)}.`
    );

    setText(
      "condition-cas-summary",
      `Natural-ambiguous wording had mean CAS ` +
        `${formatSigned(ambiguous.mean_cas)} with a 95% interval from ` +
        `${formatSigned(ambiguous.cas_bootstrap_95_low)} to ` +
        `${formatSigned(ambiguous.cas_bootstrap_95_high)}.`
    );

    renderConditionTable(rows);
  }

  function renderShiftTable(rows) {
    const body = byId("shift-table-body");
    if (!body) {
      return;
    }

    const tableRows = rows.map(row => {
      const tr = createElement("tr");

      [
        SHIFT_LABELS[row.contrast_type] ?? humanise(row.contrast_type),
        formatInteger(row.concept_count),
        formatSigned(row.mean_delta_s_c),
        formatSigned(row.mean_delta_s_r),
        formatSigned(row.mean_delta_cas),
        `${formatSigned(row.delta_cas_bootstrap_95_low)} to ` +
          `${formatSigned(row.delta_cas_bootstrap_95_high)}`,
        formatPercent(row.positive_delta_cas_proportion)
      ].forEach(value => {
        tr.append(createElement("td", {}, value));
      });

      return tr;
    });

    replaceChildren(body, tableRows);
  }

  function renderShiftChart() {
    const rows = [...state.data.shiftStatistics]
      .sort(
        (left, right) =>
          SHIFT_ORDER.indexOf(left.contrast_type) -
          SHIFT_ORDER.indexOf(right.contrast_type)
      );

    const labels = rows.map(
      row => SHIFT_LABELS[row.contrast_type] ?? humanise(row.contrast_type)
    );

    const traceDefinitions = [
      {
        key: "mean_delta_s_c",
        name: "ΔS_C",
        color: COLORS.catholic,
        symbol: "circle"
      },
      {
        key: "mean_delta_s_r",
        name: "ΔS_R",
        color: COLORS.comparison,
        symbol: "square"
      },
      {
        key: "mean_delta_cas",
        name: "ΔCAS",
        color: "#a98bc4",
        symbol: "diamond"
      }
    ];

    const traces = traceDefinitions.map(definition => ({
      type: "scatter",
      mode: "markers+text",
      name: definition.name,
      x: rows.map(row => number(row[definition.key])),
      y: labels,
      text: rows.map(row => formatSigned(row[definition.key])),
      textposition: rows.map(row =>
        number(row[definition.key]) >= 0 ? "middle right" : "middle left"
      ),
      textfont: {
        color: definition.color,
        size: 10
      },
      customdata: rows.map(row => [
        SHIFT_LABELS[row.contrast_type],
        number(row.concept_count),
        row.contrast_type === "general_to_ambiguous" ||
        row.contrast_type === "general_to_critical"
          ? "Positive ΔCAS with negative ΔS_C"
          : ""
      ]),
      marker: {
        color: definition.color,
        size: definition.name === "ΔCAS" ? 13 : 11,
        symbol: definition.symbol,
        line: {
          color: "#192434",
          width: 1
        }
      },
      cliponaxis: false,
      hovertemplate:
        "<b>%{customdata[0]}</b><br>" +
        `${definition.name}: %{x:+.4f}<br>` +
        "Concepts: %{customdata[1]}<br>" +
        "%{customdata[2]}<extra></extra>"
    }));

    const annotations = [
      {
        x: 0.61,
        y: "General → ambiguous",
        xref: "x",
        yref: "y",
        text: "Apparent relative recovery",
        showarrow: false,
        xanchor: "right",
        font: { color: "#d5c1e7", size: 10 }
      },
      {
        x: 0.61,
        y: "General → critical",
        xref: "x",
        yref: "y",
        text: "Apparent relative recovery",
        showarrow: false,
        xanchor: "right",
        font: { color: "#d5c1e7", size: 10 }
      }
    ];

    const layout = darkLayout({
      height: 590,
      margin: { l: 210, r: 145, t: 65, b: 65 },
      showlegend: true,
      legend: {
        ...darkLayout().legend,
        y: 1.04,
        font: { size: 11, color: "#d7dfe8" }
      },
      xaxis: {
        ...darkLayout().xaxis,
        title: "Mean matched change",
        range: [-0.4, 0.65],
        tickformat: "+.2f",
        zeroline: true,
        zerolinewidth: 2
      },
      yaxis: {
        ...darkLayout().yaxis,
        autorange: "reversed",
        categoryorder: "array",
        categoryarray: labels
      },
      annotations
    });

    window.Plotly.newPlot(
      "shift-chart",
      traces,
      layout,
      plotConfig
    );

    const ambiguous = rows.find(
      row => row.contrast_type === "general_to_ambiguous"
    );
    const critical = rows.find(
      row => row.contrast_type === "general_to_critical"
    );

    setText(
      "shift-summary",
      `General → ambiguous: ΔS_C ` +
        `${formatSigned(ambiguous.mean_delta_s_c)}, ΔS_R ` +
        `${formatSigned(ambiguous.mean_delta_s_r)}, and ΔCAS ` +
        `${formatSigned(ambiguous.mean_delta_cas)}. General → critical: ` +
        `ΔS_C ${formatSigned(critical.mean_delta_s_c)}, ΔS_R ` +
        `${formatSigned(critical.mean_delta_s_r)}, and ΔCAS ` +
        `${formatSigned(critical.mean_delta_cas)}.`
    );

    renderShiftTable(rows);
  }

  function renderAccessibilityTable(rows) {
    const body = byId("accessibility-table-body");
    if (!body) {
      return;
    }

    const tableRows = rows.map(row => {
      const tr = createElement("tr");

      [
        row.concept,
        row.primary_locus,
        row.comparison_register,
        formatNumber(row.mean_s_c),
        formatNumber(row.mean_s_r),
        formatSigned(row.mean_cas)
      ].forEach(value => {
        tr.append(createElement("td", {}, value));
      });

      return tr;
    });

    replaceChildren(body, tableRows);
  }

  function updateAccessibilityChart() {
    const condition =
      byId("accessibility-condition")?.value || "integrative";
    const locus = byId("accessibility-locus")?.value || "all";

    const rows = state.data.conditionSummary
      .filter(row => row.condition === condition)
      .filter(row => locus === "all" || row.primary_locus === locus)
      .sort((left, right) =>
        String(left.concept).localeCompare(String(right.concept))
      );

    const loci = uniqueSorted(rows.map(row => row.primary_locus));

    const traces = loci.map(currentLocus => {
      const subset = rows.filter(
        row => row.primary_locus === currentLocus
      );

      return {
        type: "scatter",
        mode: "markers",
        name: currentLocus,
        x: subset.map(row => number(row.mean_s_r)),
        y: subset.map(row => number(row.mean_s_c)),
        customdata: subset.map(row => [
          row.concept,
          row.comparison_register,
          humanise(row.relationship_type),
          number(row.mean_cas),
          number(row.query_count)
        ]),
        marker: {
          color: LOCUS_COLORS[currentLocus] || COLORS.neutral,
          size: 10,
          opacity: 0.86,
          symbol: subset.map(
            row =>
              RELATIONSHIP_SYMBOLS[row.relationship_type] ||
              "circle"
          ),
          line: {
            color: COLORS.white,
            width: 1
          }
        },
        hovertemplate:
          "<b>%{customdata[0]}</b><br>" +
          "Comparison register: %{customdata[1]}<br>" +
          "Relationship: %{customdata[2]}<br>" +
          "S<sub>R</sub>: %{x:.4f}<br>" +
          "S<sub>C</sub>: %{y:.4f}<br>" +
          "CAS: %{customdata[3]:+.4f}<br>" +
          "Queries: %{customdata[4]}<extra></extra>"
      };
    });

    const layout = baseLayout({
      height: 580,
      margin: { l: 75, r: 30, t: 65, b: 70 },
      xaxis: {
        ...baseLayout().xaxis,
        title: "Comparison-reference similarity (S_R)",
        range: [0.2, 0.95],
        tickformat: ".2f"
      },
      yaxis: {
        ...baseLayout().yaxis,
        title: "Catholic-reference similarity (S_C)",
        range: [0.2, 0.95],
        tickformat: ".2f",
        scaleanchor: "x",
        scaleratio: 1
      },
      shapes: [
        {
          type: "line",
          x0: 0.2,
          x1: 0.95,
          y0: 0.2,
          y1: 0.95,
          line: {
            color: "#8791a0",
            width: 1.5,
            dash: "dash"
          },
          layer: "below"
        }
      ],
      annotations: [
        {
          x: 0.88,
          y: 0.89,
          text: "CAS = 0",
          showarrow: false,
          font: {
            color: COLORS.muted,
            size: 10
          }
        }
      ]
    });

    window.Plotly.react(
      "accessibility-chart",
      traces,
      layout,
      plotConfig
    );

    const meanSC = mean(rows.map(row => row.mean_s_c));
    const meanSR = mean(rows.map(row => row.mean_s_r));
    const meanCas = mean(rows.map(row => row.mean_cas));

    setText(
      "accessibility-count",
      `${formatInteger(rows.length)} visible concepts`
    );

    setText(
      "accessibility-summary",
      `${CONDITION_LABELS[condition] || humanise(condition)}: ` +
        `${formatInteger(rows.length)} concept means, mean S_C ` +
        `${formatNumber(meanSC)}, mean S_R ${formatNumber(meanSR)}, ` +
        `and mean CAS ${formatSigned(meanCas)}. The diagonal marks ` +
        `equal component similarity, not a success threshold.`
    );

    renderAccessibilityTable(rows);
  }

  function renderCriticalTable(rows) {
    const body = byId("critical-table-body");
    if (!body) {
      return;
    }

    const tableRows = rows.map(row => {
      const tr = createElement("tr");
      const crossesZero =
        number(row.min_cas) <= 0 && number(row.max_cas) >= 0;

      [
        row.concept,
        formatNumber(row.mean_s_c),
        formatNumber(row.mean_s_r),
        formatSigned(row.mean_cas),
        `${formatSigned(row.min_cas)} to ${formatSigned(row.max_cas)}`,
        crossesZero ? "Yes" : "No"
      ].forEach(value => {
        tr.append(createElement("td", {}, value));
      });

      return tr;
    });

    replaceChildren(body, tableRows);
  }

  function renderCriticalChart() {
    const conceptOrder = [
      "death",
      "dying",
      "euthanasia",
      "grief",
      "illness",
      "palliative care",
      "suffering",
      "suicide"
    ];

    const summaryRows = state.data.conditionSummary
      .filter(row => row.condition === "critical")
      .sort(
        (left, right) =>
          conceptOrder.indexOf(String(left.concept).toLowerCase()) -
          conceptOrder.indexOf(String(right.concept).toLowerCase())
      );

    const sensitivityMap = new Map(
      state.data.paraphraseCondition
        .filter(row => row.condition === "critical")
        .map(row => [row.audit_id, row])
    );

    const rows = summaryRows.map(row => ({
      ...row,
      ...(sensitivityMap.get(row.audit_id) || {
        min_cas: row.mean_cas,
        max_cas: row.mean_cas,
        cas_standard_deviation: 0
      })
    }));

    const labels = rows.map(row => row.concept);

    const componentLineX = [];
    const componentLineY = [];
    const casRangeX = [];
    const casRangeY = [];

    rows.forEach(row => {
      componentLineX.push(
        number(row.mean_s_c),
        number(row.mean_s_r),
        null
      );
      componentLineY.push(row.concept, row.concept, null);

      casRangeX.push(
        number(row.min_cas),
        number(row.max_cas),
        null
      );
      casRangeY.push(row.concept, row.concept, null);
    });

    const traces = [
      {
        type: "scatter",
        mode: "lines",
        x: componentLineX,
        y: componentLineY,
        line: {
          color: "#c8ced6",
          width: 3
        },
        hoverinfo: "skip",
        showlegend: false
      },
      {
        type: "scatter",
        mode: "markers",
        name: "S_C",
        x: rows.map(row => number(row.mean_s_c)),
        y: labels,
        customdata: rows.map(row => [
          row.concept,
          number(row.mean_cas)
        ]),
        marker: {
          color: COLORS.catholic,
          size: 11,
          symbol: "circle",
          line: {
            color: COLORS.white,
            width: 1
          }
        },
        hovertemplate:
          "<b>%{customdata[0]}</b><br>" +
          "Mean S<sub>C</sub>: %{x:.4f}<br>" +
          "Mean CAS: %{customdata[1]:+.4f}<extra></extra>"
      },
      {
        type: "scatter",
        mode: "markers",
        name: "S_R",
        x: rows.map(row => number(row.mean_s_r)),
        y: labels,
        customdata: rows.map(row => [
          row.concept,
          number(row.mean_cas)
        ]),
        marker: {
          color: COLORS.comparison,
          size: 11,
          symbol: "square",
          line: {
            color: COLORS.white,
            width: 1
          }
        },
        hovertemplate:
          "<b>%{customdata[0]}</b><br>" +
          "Mean S<sub>R</sub>: %{x:.4f}<br>" +
          "Mean CAS: %{customdata[1]:+.4f}<extra></extra>"
      },
      {
        type: "scatter",
        mode: "lines",
        name: "Paraphrase CAS range",
        xaxis: "x2",
        x: casRangeX,
        y: casRangeY,
        line: {
          color: COLORS.casLight,
          width: 5
        },
        hoverinfo: "skip"
      },
      {
        type: "scatter",
        mode: "markers",
        name: "Mean CAS",
        xaxis: "x2",
        x: rows.map(row => number(row.mean_cas)),
        y: labels,
        customdata: rows.map(row => [
          row.concept,
          number(row.min_cas),
          number(row.max_cas),
          number(row.cas_standard_deviation),
          number(row.min_cas) <= 0 && number(row.max_cas) >= 0
            ? "Crosses CAS zero"
            : "Does not cross CAS zero"
        ]),
        marker: {
          color: COLORS.critical,
          size: 10,
          symbol: "diamond",
          line: {
            color: COLORS.white,
            width: 1
          }
        },
        hovertemplate:
          "<b>%{customdata[0]}</b><br>" +
          "Mean CAS: %{x:+.4f}<br>" +
          "Paraphrase range: %{customdata[1]:+.4f} to " +
          "%{customdata[2]:+.4f}<br>" +
          "CAS SD: %{customdata[3]:.4f}<br>" +
          "%{customdata[4]}<extra></extra>"
      }
    ];

    const layout = baseLayout({
      height: 570,
      margin: {
        l: 130,
        r: 35,
        t: 65,
        b: 70
      },
      legend: {
        ...baseLayout().legend,
        y: 1.04
      },
      xaxis: {
        ...baseLayout().xaxis,
        domain: [0, 0.66],
        title: "Mean component similarity",
        range: [0.25, 0.58],
        tickformat: ".2f"
      },
      xaxis2: {
        domain: [0.75, 1],
        anchor: "y",
        title: "CAS and paraphrase range",
        range: [-0.22, 0.12],
        showgrid: true,
        gridcolor: COLORS.grid,
        zeroline: true,
        zerolinecolor: "#9ba5b1",
        zerolinewidth: 2,
        tickformat: "+.2f",
        tickfont: {
          size: 11,
          color: COLORS.ink
        },
        titlefont: {
          size: 11,
          color: COLORS.ink
        }
      },
      yaxis: {
        ...baseLayout().yaxis,
        autorange: "reversed",
        categoryorder: "array",
        categoryarray: labels
      },
      annotations: [
        {
          x: 0.705,
          y: 1.06,
          xref: "paper",
          yref: "paper",
          text: "Component means",
          showarrow: false,
          font: {
            color: COLORS.muted,
            size: 10
          }
        },
        {
          x: 0.87,
          y: 1.06,
          xref: "paper",
          yref: "paper",
          text: "Relative contrast",
          showarrow: false,
          font: {
            color: COLORS.muted,
            size: 10
          }
        }
      ]
    });

    window.Plotly.newPlot(
      "critical-chart",
      traces,
      layout,
      plotConfig
    );

    const lowest = [...rows].sort(
      (left, right) =>
        number(left.mean_cas) - number(right.mean_cas)
    )[0];

    const highest = [...rows].sort(
      (left, right) =>
        number(right.mean_cas) - number(left.mean_cas)
    )[0];

    const crossingCount = rows.filter(
      row =>
        number(row.min_cas) <= 0 &&
        number(row.max_cas) >= 0
    ).length;

    setText(
      "critical-summary",
      `Across eight critical audits, mean CAS ranged from ` +
        `${formatSigned(lowest.mean_cas)} for ${lowest.concept} to ` +
        `${formatSigned(highest.mean_cas)} for ${highest.concept}. ` +
        `${crossingCount} paraphrase ranges crossed CAS zero. ` +
        `Negative CAS is a relative reference-field result, not a failure label.`
    );

    renderCriticalTable(rows);
  }

  function renderLabelEffectChart() {
    const labelFree = state.data.conditionStatistics.find(
      row => row.condition === "label_free_theological"
    );
    const explicit = state.data.conditionStatistics.find(
      row => row.condition === "explicit_catholic"
    );

    if (!labelFree || !explicit) {
      throw new Error(
        "Label-free or explicit-Catholic condition statistics are missing."
      );
    }

    const xLabels = [
      "Label-free theological",
      "Explicit Catholic"
    ];

    const definitions = [
      {
        name: "S_C",
        color: COLORS.catholic,
        symbol: "circle",
        values: [
          number(labelFree.mean_s_c),
          number(explicit.mean_s_c)
        ],
        textPosition: "top center"
      },
      {
        name: "S_R",
        color: COLORS.comparison,
        symbol: "square",
        values: [
          number(labelFree.mean_s_r),
          number(explicit.mean_s_r)
        ],
        textPosition: "bottom center"
      },
      {
        name: "CAS",
        color: COLORS.cas,
        symbol: "diamond",
        values: [
          number(labelFree.mean_cas),
          number(explicit.mean_cas)
        ],
        textPosition: "top center"
      }
    ];

    const traces = definitions.map(definition => ({
      type: "scatter",
      mode: "lines+markers+text",
      name: definition.name,
      x: xLabels,
      y: definition.values,
      text: definition.values.map(value => formatSigned(value)),
      textposition: definition.textPosition,
      textfont: {
        color: definition.color,
        size: 10
      },
      line: {
        color: definition.color,
        width: 3
      },
      marker: {
        color: definition.color,
        size: 12,
        symbol: definition.symbol,
        line: {
          color: COLORS.white,
          width: 1
        }
      },
      cliponaxis: false,
      hovertemplate:
        `<b>${definition.name}</b><br>` +
        "%{x}<br>" +
        "Value: %{y:+.4f}<extra></extra>"
    }));

    const layout = baseLayout({
      height: 430,
      margin: {
        l: 70,
        r: 45,
        t: 65,
        b: 80
      },
      xaxis: {
        ...baseLayout().xaxis,
        showgrid: false,
        title: ""
      },
      yaxis: {
        ...baseLayout().yaxis,
        title: "Mean component or contrast value",
        range: [0.2, 0.96],
        tickformat: ".2f",
        showgrid: true,
        gridcolor: COLORS.grid
      },
      legend: {
        ...baseLayout().legend,
        y: 1.04
      }
    });

    window.Plotly.newPlot(
      "label-effect-chart",
      traces,
      layout,
      plotConfig
    );

    const deltaSC =
      number(explicit.mean_s_c) -
      number(labelFree.mean_s_c);

    const deltaSR =
      number(explicit.mean_s_r) -
      number(labelFree.mean_s_r);

    const deltaCas =
      number(explicit.mean_cas) -
      number(labelFree.mean_cas);

    setText(
      "label-effect-summary",
      `From label-free theological to explicit Catholic wording, ` +
        `mean S_C changed by ${formatSigned(deltaSC)}, mean S_R by ` +
        `${formatSigned(deltaSR)}, and mean CAS by ` +
        `${formatSigned(deltaCas)}. The generated references contain ` +
        `repeated Catholic-identifying language, so this is a ` +
        `construction-sensitive diagnostic.`
    );
  }

  function stabilityDistribution(rows) {
    const groups = new Map();

    rows.forEach(row => {
      const value = number(row.sign_stability_proportion);
      const key = value.toFixed(3);
      groups.set(key, (groups.get(key) || 0) + 1);
    });

    return [...groups.entries()]
      .map(([value, count]) => ({
        value: Number(value),
        label: formatPercent(Number(value), 1),
        count
      }))
      .sort((left, right) => right.value - left.value);
  }

  function renderReferenceStabilityChart() {
    const rows = state.data.referenceSensitivity;
    const distribution = stabilityDistribution(rows);

    const trace = {
      type: "bar",
      orientation: "h",
      x: distribution.map(item => item.count),
      y: distribution.map(item => item.label),
      text: distribution.map(item => formatInteger(item.count)),
      textposition: "outside",
      cliponaxis: false,
      marker: {
        color: distribution.map(item =>
          item.value === 1
            ? COLORS.catholic
            : COLORS.catholicLight
        ),
        line: {
          color: COLORS.white,
          width: 1
        }
      },
      customdata: distribution.map(item => item.value),
      hovertemplate:
        "<b>Sign stability %{y}</b><br>" +
        "Queries: %{x:,}<br>" +
        "Proportion: %{customdata:.3f}<extra></extra>"
    };

    const layout = baseLayout({
      height: 390,
      showlegend: false,
      margin: {
        l: 80,
        r: 70,
        t: 25,
        b: 60
      },
      xaxis: {
        ...baseLayout().xaxis,
        title: "Number of queries",
        rangemode: "tozero",
        tickformat: ",d"
      },
      yaxis: {
        ...baseLayout().yaxis,
        title: "Sign stability across six omissions",
        autorange: "reversed"
      }
    });

    window.Plotly.newPlot(
      "robustness-stability-chart",
      [trace],
      layout,
      plotConfig
    );

    const fullyStable = rows.filter(
      row =>
        Math.abs(
          number(row.sign_stability_proportion) - 1
        ) < 1e-10
    ).length;

    const averageStability = mean(
      rows.map(row => row.sign_stability_proportion)
    );

    setText(
      "robustness-stability-summary",
      `${formatInteger(fullyStable)} of ` +
        `${formatInteger(rows.length)} queries retained the same CAS sign ` +
        `under every individual reference omission. Mean sign stability ` +
        `was ${formatNumber(averageStability, 4)}.`
    );
  }

  function conditionColour(condition) {
    const colours = {
      natural_general: COLORS.neutral,
      natural_ambiguous: "#7c8796",
      label_free_theological: COLORS.catholic,
      explicit_catholic: COLORS.cas,
      integrative: COLORS.integrative,
      critical: COLORS.critical
    };

    return colours[condition] || COLORS.neutral;
  }

  function renderParaphraseChart() {
    const rows = state.data.paraphraseCondition;

    const availableConditions = CONDITION_ORDER.filter(condition =>
      rows.some(row => row.condition === condition)
    );

    const traces = availableConditions.map(condition => {
      const subset = rows.filter(
        row => row.condition === condition
      );

      return {
        type: "box",
        name:
          CONDITION_LABELS[condition] ||
          humanise(condition),
        y: subset.map(
          row => number(row.cas_standard_deviation)
        ),
        customdata: subset.map(row => [
          row.concept,
          number(row.mean_cas),
          number(row.min_cas),
          number(row.max_cas),
          number(row.positive_cas_proportion)
        ]),
        marker: {
          color: conditionColour(condition),
          size: 5,
          opacity: 0.7
        },
        line: {
          color: conditionColour(condition),
          width: 1.5
        },
        fillcolor: `${conditionColour(condition)}22`,
        boxpoints: "outliers",
        jitter: 0.25,
        pointpos: 0,
        hovertemplate:
          "<b>%{customdata[0]}</b><br>" +
          `${CONDITION_LABELS[condition] || humanise(condition)}<br>` +
          "CAS SD: %{y:.4f}<br>" +
          "Mean CAS: %{customdata[1]:+.4f}<br>" +
          "Range: %{customdata[2]:+.4f} to " +
          "%{customdata[3]:+.4f}<br>" +
          "Positive proportion: %{customdata[4]:.1%}" +
          "<extra></extra>"
      };
    });

    const layout = baseLayout({
      height: 390,
      showlegend: false,
      margin: {
        l: 70,
        r: 25,
        t: 25,
        b: 105
      },
      xaxis: {
        ...baseLayout().xaxis,
        showgrid: false,
        tickangle: -28
      },
      yaxis: {
        ...baseLayout().yaxis,
        title: "Paraphrase CAS standard deviation",
        rangemode: "tozero",
        tickformat: ".02f",
        showgrid: true,
        gridcolor: COLORS.grid
      }
    });

    window.Plotly.newPlot(
      "robustness-paraphrase-chart",
      traces,
      layout,
      plotConfig
    );

    const mixedCount = rows.filter(row => {
      const positive = number(row.positive_cas_proportion);
      return positive > 0 && positive < 1;
    }).length;

    const medianSd = median(
      rows.map(row => row.cas_standard_deviation)
    );

    const maximumSd = Math.max(
      ...rows.map(row =>
        number(row.cas_standard_deviation)
      )
    );

    setText(
      "robustness-paraphrase-summary",
      `${formatInteger(mixedCount)} of ` +
        `${formatInteger(rows.length)} audit-condition groups contained ` +
        `both positive and negative CAS paraphrases. Median CAS SD was ` +
        `${formatNumber(medianSd, 4)} and the maximum was ` +
        `${formatNumber(maximumSd, 4)}.`
    );
  }

  function makeRankedItem({
    title,
    details,
    value
  }) {
    const item = createElement("li");
    const strong = createElement(
      "strong",
      {},
      title
    );
    const detail = createElement(
      "span",
      {},
      `${details} · ${value}`
    );

    item.append(strong, detail);
    return item;
  }

  function renderSensitivityRankings() {
    const referenceRows = [
      ...state.data.referenceSensitivity
    ]
      .sort(
        (left, right) =>
          number(right.max_absolute_cas_change) -
          number(left.max_absolute_cas_change)
      )
      .slice(0, 5);

    const referenceItems = referenceRows.map(row =>
      makeRankedItem({
        title: row.concept,
        details:
          `${CONDITION_LABELS[row.condition] || humanise(row.condition)} · ` +
          `${row.query_id}`,
        value:
          `max |ΔCAS| ${formatNumber(row.max_absolute_cas_change, 4)}`
      })
    );

    replaceChildren(
      byId("reference-sensitive-list"),
      referenceItems
    );

    const wordingRows = [
      ...state.data.paraphraseCondition
    ]
      .sort(
        (left, right) =>
          number(right.cas_standard_deviation) -
          number(left.cas_standard_deviation)
      )
      .slice(0, 5);

    const wordingItems = wordingRows.map(row =>
      makeRankedItem({
        title: row.concept,
        details:
          CONDITION_LABELS[row.condition] ||
          humanise(row.condition),
        value:
          `CAS SD ${formatNumber(row.cas_standard_deviation, 4)}`
      })
    );

    replaceChildren(
      byId("wording-sensitive-list"),
      wordingItems
    );
  }

  function renderValidationMetrics() {
    const aggregate = state.data.validationMetrics.find(
      row => String(row.scope) === "ALL_AUDITS"
    );

    if (!aggregate) {
      throw new Error(
        "The ALL_AUDITS validation-metrics row is missing."
      );
    }

    setText(
      "validation-balanced",
      formatNumber(aggregate.balanced_accuracy)
    );

    setText(
      "validation-catholic-recall",
      formatNumber(aggregate.catholic_recall)
    );

    setText(
      "validation-comparison-recall",
      formatNumber(aggregate.comparison_recall)
    );

    setText(
      "validation-macro-f1",
      formatNumber(aggregate.macro_f1)
    );
  }

  function renderRobustnessHeadline() {
    const referenceRows = state.data.referenceSensitivity;
    const paraphraseRows = state.data.paraphraseCondition;

    const fullyStable = referenceRows.filter(
      row =>
        Math.abs(
          number(row.sign_stability_proportion) - 1
        ) < 1e-10
    ).length;

    const mixedCount = paraphraseRows.filter(row => {
      const positive = number(row.positive_cas_proportion);
      return positive > 0 && positive < 1;
    }).length;

    const maximumChange = Math.max(
      ...referenceRows.map(row =>
        number(row.max_absolute_cas_change)
      )
    );

    setText(
      "stable-query-count",
      `${formatInteger(fullyStable)} / ` +
        `${formatInteger(referenceRows.length)}`
    );

    setText(
      "mixed-paraphrase-count",
      `${formatInteger(mixedCount)} / ` +
        `${formatInteger(paraphraseRows.length)}`
    );

    setText(
      "max-reference-change",
      formatNumber(maximumChange, 4)
    );
  }

  function renderRobustness() {
    renderRobustnessHeadline();
    renderReferenceStabilityChart();
    renderParaphraseChart();
    renderSensitivityRankings();
    renderValidationMetrics();
  }

  const ROLE_STYLES = Object.freeze({
    "reference:catholic": {
      label: "Catholic references",
      color: COLORS.catholic,
      symbol: "circle",
      size: 5.5,
      opacity: 0.9
    },
    "reference:comparison": {
      label: "Comparison references",
      color: COLORS.comparison,
      symbol: "circle",
      size: 5.5,
      opacity: 0.9
    },
    "query:bare": {
      label: "Bare queries",
      color: "#8791a0",
      symbol: "cross",
      size: 4,
      opacity: 0.62
    },
    "query:natural_general": {
      label: "Natural-general queries",
      color: "#667486",
      symbol: "circle",
      size: 4,
      opacity: 0.62
    },
    "query:natural_ambiguous": {
      label: "Natural-ambiguous queries",
      color: "#9aa3af",
      symbol: "diamond",
      size: 4.5,
      opacity: 0.68
    },
    "query:label_free_theological": {
      label: "Label-free theological queries",
      color: "#3974a7",
      symbol: "diamond",
      size: 4.5,
      opacity: 0.72
    },
    "query:explicit_catholic": {
      label: "Explicit-Catholic queries",
      color: COLORS.cas,
      symbol: "diamond",
      size: 4.5,
      opacity: 0.72
    },
    "query:integrative": {
      label: "Integrative queries",
      color: COLORS.integrative,
      symbol: "square",
      size: 4.5,
      opacity: 0.75
    },
    "query:critical": {
      label: "Critical queries",
      color: COLORS.critical,
      symbol: "diamond",
      size: 5,
      opacity: 0.82
    },
    "validation:clear_register:catholic": {
      label: "Catholic validation passages",
      color: COLORS.catholicLight,
      symbol: "circle-open",
      size: 4.5,
      opacity: 0.55
    },
    "validation:clear_register:comparison": {
      label: "Comparison validation passages",
      color: COLORS.comparisonLight,
      symbol: "circle-open",
      size: 4.5,
      opacity: 0.55
    },
    "validation:integrative:integrative": {
      label: "Integrative validation passages",
      color: "#6aa7a4",
      symbol: "square-open",
      size: 4.5,
      opacity: 0.55
    },
    "validation:critical:critical_review": {
      label: "Critical validation passages",
      color: "#b37888",
      symbol: "diamond-open",
      size: 4.5,
      opacity: 0.55
    }
  });

  const RELATIONSHIP_3D_SYMBOLS = Object.freeze({
    complementary_levels: "circle",
    valid_but_partial: "square",
    normatively_conflicting: "diamond",
    alternative_lexical_senses: "cross",
    generic_religious_vs_catholic_specific: "x"
  });

  function metadataForAudit(auditId) {
    return state.comparisonsByAudit.get(auditId) || {};
  }

  function registerTextMetadata(text, metadata) {
    const key = String(text ?? "");

    if (!key) {
      throw new Error("A benchmark item has empty text.");
    }

    if (state.textMetadata.has(key)) {
      throw new Error(
        `Duplicate embedded text prevented an unambiguous UMAP join: ` +
        `${truncate(key, 100)}`
      );
    }

    state.textMetadata.set(key, metadata);
  }

  function prepareUmapMetadata() {
    state.comparisonsByAudit = new Map(
      state.data.comparisons.map(row => [
        row.audit_id,
        row
      ])
    );

    state.textMetadata = new Map();

    state.data.references.forEach(row => {
      const audit = metadataForAudit(row.audit_id);

      registerTextMetadata(row.reference_text, {
        itemId: row.reference_id,
        itemType: "reference",
        auditId: row.audit_id,
        concept: audit.concept || row.audit_id,
        primaryLocus: audit.primary_locus || "",
        comparisonRegister: audit.comparison_register || "",
        relationshipType: audit.relationship_type || "",
        referenceGroup: row.reference_group,
        sourceStatus: row.text_status || "",
        reviewStatus: row.review_status || ""
      });
    });

    state.data.queryScores.forEach(row => {
      registerTextMetadata(row.query_text, {
        itemId: row.query_id,
        itemType: "query",
        auditId: row.audit_id,
        concept: row.concept,
        primaryLocus: row.primary_locus,
        comparisonRegister: row.comparison_register,
        relationshipType: row.relationship_type,
        condition: row.condition,
        reviewStatus: row.review_status || ""
      });
    });

    state.data.validation.forEach(row => {
      const audit = metadataForAudit(row.audit_id);

      registerTextMetadata(row.validation_text, {
        itemId: row.validation_id,
        itemType: "validation",
        auditId: row.audit_id,
        concept: audit.concept || row.audit_id,
        primaryLocus: audit.primary_locus || "",
        comparisonRegister: audit.comparison_register || "",
        relationshipType: audit.relationship_type || "",
        validationStage: row.validation_stage,
        targetClass: row.target_class,
        sourceStatus: row.ethical_review_status || "",
        reviewStatus: row.review_status || ""
      });
    });

    state.coordinatesById = new Map();

    state.data.umapCoordinates.forEach(row => {
      if (state.coordinatesById.has(row.embedding_id)) {
        throw new Error(
          `Duplicate UMAP embedding ID: ${row.embedding_id}`
        );
      }

      const coordinate = {
        x: number(row.umap_x, Number.NaN),
        y: number(row.umap_y, Number.NaN),
        z: number(row.umap_z, Number.NaN)
      };

      if (
        !Number.isFinite(coordinate.x) ||
        !Number.isFinite(coordinate.y) ||
        !Number.isFinite(coordinate.z)
      ) {
        throw new Error(
          `Non-finite UMAP coordinate for ${row.embedding_id}.`
        );
      }

      state.coordinatesById.set(
        row.embedding_id,
        coordinate
      );
    });

    const missingCoordinates = [];
    const missingMetadata = [];

    state.points = state.data.embeddingIndex.map(row => {
      const coordinate =
        state.coordinatesById.get(row.embedding_id);

      if (!coordinate) {
        missingCoordinates.push(row.embedding_id);
      }

      const metadata =
        state.textMetadata.get(String(row.text));

      if (!metadata) {
        missingMetadata.push(row.embedding_id);
      }

      return {
        embeddingId: row.embedding_id,
        text: String(row.text),
        role: String(row.roles),
        dimensions: number(row.dimensions),
        x: coordinate?.x,
        y: coordinate?.y,
        z: coordinate?.z,
        itemId: metadata?.itemId || "",
        itemType: metadata?.itemType || "",
        auditId: metadata?.auditId || "",
        concept: metadata?.concept || "Unmapped item",
        primaryLocus: metadata?.primaryLocus || "",
        comparisonRegister:
          metadata?.comparisonRegister || "",
        relationshipType:
          metadata?.relationshipType || "",
        referenceGroup:
          metadata?.referenceGroup || "",
        condition: metadata?.condition || "",
        validationStage:
          metadata?.validationStage || "",
        targetClass: metadata?.targetClass || "",
        sourceStatus:
          metadata?.sourceStatus || "",
        reviewStatus:
          metadata?.reviewStatus || ""
      };
    });

    if (missingCoordinates.length) {
      throw new Error(
        `${missingCoordinates.length} embedding-index rows have no ` +
        `UMAP coordinate.`
      );
    }

    if (missingMetadata.length) {
      throw new Error(
        `${missingMetadata.length} embedded texts could not be joined ` +
        `to benchmark metadata.`
      );
    }

    if (state.points.length !== 3032) {
      throw new Error(
        `Expected 3,032 joined UMAP points; found ` +
        `${state.points.length}.`
      );
    }

    const uniqueIds = new Set(
      state.points.map(point => point.embeddingId)
    );

    if (uniqueIds.size !== state.points.length) {
      throw new Error(
        "Joined UMAP points contain duplicate embedding IDs."
      );
    }
  }

  function renderUmapManifest() {
    const manifest = state.data.umapManifest;
    const software = manifest.software || {};

    setText(
      "umap-source-hash",
      manifest.source_embedding_sha256 || "Not recorded"
    );

    setText(
      "umap-coordinate-hash",
      manifest.coordinate_file_sha256 || "Not recorded"
    );

    setText(
      "umap-version",
      software["umap-learn"] || "Not recorded"
    );

    setText(
      "umap-generated",
      manifest.generated_at_utc || "Not recorded"
    );
  }

  function roleStyle(role) {
    return ROLE_STYLES[role] || {
      label: humanise(role),
      color: COLORS.neutral,
      symbol: "circle",
      size: 4,
      opacity: 0.58
    };
  }

  function sceneLayout() {
    const axis = title => ({
      title: {
        text: title,
        font: {
          size: 11,
          color: COLORS.muted
        }
      },
      showbackground: true,
      backgroundcolor: "#f7f8fa",
      gridcolor: "#dfe4e9",
      zerolinecolor: "#c5ccd5",
      showspikes: false,
      tickfont: {
        size: 9,
        color: COLORS.muted
      }
    });

    return {
      xaxis: axis("UMAP 1"),
      yaxis: axis("UMAP 2"),
      zaxis: axis("UMAP 3"),
      bgcolor: COLORS.white,
      aspectmode: "cube",
      camera: state.defaultCamera,
      dragmode: "orbit"
    };
  }

  function umapLayout({
    height = 660,
    showLegend = true
  } = {}) {
    return {
      autosize: true,
      height,
      margin: {
        l: 0,
        r: 0,
        t: showLegend ? 55 : 10,
        b: 0
      },
      paper_bgcolor: COLORS.transparent,
      plot_bgcolor: COLORS.white,
      font: {
        family:
          'Inter, -apple-system, BlinkMacSystemFont, "Segoe UI", sans-serif',
        size: 11,
        color: COLORS.ink
      },
      hoverlabel: {
        bgcolor: COLORS.white,
        bordercolor: "#c5ccd5",
        font: {
          size: 11,
          color: COLORS.ink
        },
        align: "left"
      },
      scene: sceneLayout(),
      showlegend: showLegend,
      legend: {
        orientation: "h",
        x: 0,
        xanchor: "left",
        y: 1.02,
        yanchor: "bottom",
        font: {
          size: 10,
          color: COLORS.ink
        },
        bgcolor: "rgba(255,255,255,0.85)"
      }
    };
  }

  function pointsToTrace(points, role, {
    name = null,
    style = null,
    showLegend = true,
    hover = true
  } = {}) {
    const currentStyle = style || roleStyle(role);

    return {
      type: "scatter3d",
      mode: "markers",
      name: name || currentStyle.label,
      x: points.map(point => point.x),
      y: points.map(point => point.y),
      z: points.map(point => point.z),
      customdata: points.map(point => [
        escapeHtml(point.concept),
        escapeHtml(currentStyle.label),
        escapeHtml(point.primaryLocus),
        escapeHtml(point.comparisonRegister),
        escapeHtml(truncate(point.text, 220)),
        escapeHtml(point.auditId)
      ]),
      marker: {
        color: currentStyle.color,
        size: currentStyle.size,
        opacity: currentStyle.opacity,
        symbol: currentStyle.symbol,
        line: {
          color: currentStyle.color,
          width: 0.4
        }
      },
      showlegend: showLegend,
      hoverinfo: hover ? undefined : "skip",
      hovertemplate: hover
        ? "<b>%{customdata[0]}</b><br>" +
          "%{customdata[1]}<br>" +
          "Locus: %{customdata[2]}<br>" +
          "Comparison register: %{customdata[3]}<br><br>" +
          "%{customdata[4]}<br>" +
          "<span style='color:#657083'>Audit: " +
          "%{customdata[5]}</span><extra></extra>"
        : undefined
    };
  }

  function populateAtlasControls() {
    const roles = uniqueSorted(
      state.points.map(point => point.role)
    );

    populateSelect(
      byId("atlas-role-filter"),
      roles,
      {
        allLabel: "All roles",
        selectedValue: "all",
        labelFunction: role =>
          roleStyle(role).label
      }
    );

    const loci = uniqueSorted(
      state.data.comparisons.map(
        row => row.primary_locus
      )
    );

    populateSelect(
      byId("atlas-locus-filter"),
      loci,
      {
        allLabel: "All loci",
        selectedValue: "all",
        labelFunction: value => value
      }
    );
  }

  function updateGlobalAtlas() {
    const selectedRole =
      byId("atlas-role-filter")?.value || "all";

    const selectedLocus =
      byId("atlas-locus-filter")?.value || "all";

    const visiblePoints = state.points
      .filter(
        point =>
          selectedRole === "all" ||
          point.role === selectedRole
      )
      .filter(
        point =>
          selectedLocus === "all" ||
          point.primaryLocus === selectedLocus
      );

    const roles = uniqueSorted(
      visiblePoints.map(point => point.role)
    );

    const traces = roles.map(role =>
      pointsToTrace(
        visiblePoints.filter(
          point => point.role === role
        ),
        role
      )
    );

    window.Plotly.react(
      "atlas-chart",
      traces,
      umapLayout({
        height: 660,
        showLegend: roles.length > 1
      }),
      plotConfig
    );

    setText(
      "atlas-count",
      `${formatInteger(visiblePoints.length)} of ` +
        `${formatInteger(state.points.length)} points visible`
    );

    const roleDescription =
      selectedRole === "all"
        ? "all text roles"
        : roleStyle(selectedRole).label.toLowerCase();

    const locusDescription =
      selectedLocus === "all"
        ? "all four theological loci"
        : selectedLocus;

    setText(
      "atlas-summary",
      `Showing ${formatInteger(visiblePoints.length)} embedded texts ` +
        `across ${roleDescription} and ${locusDescription}. ` +
        `The coordinates provide exploratory orientation only; ` +
        `component cosine scores remain primary.`
    );
  }

  function bindGlobalAtlasControls() {
    byId("atlas-role-filter")?.addEventListener(
      "change",
      updateGlobalAtlas
    );

    byId("atlas-locus-filter")?.addEventListener(
      "change",
      updateGlobalAtlas
    );

    byId("atlas-reset-camera")?.addEventListener(
      "click",
      () => {
        window.Plotly.relayout(
          "atlas-chart",
          {
            "scene.camera": state.defaultCamera
          }
        );
      }
    );
  }

  function initialiseGlobalAtlas() {
    prepareUmapMetadata();
    renderUmapManifest();
    populateAtlasControls();
    bindGlobalAtlasControls();
    updateGlobalAtlas();
  }

  function referenceTrace(
    points,
    referenceGroup,
    relationshipType
  ) {
    const isCatholic =
      referenceGroup === "catholic";

    const fieldLabel = isCatholic
      ? "Catholic"
      : "Comparison";

    const relationshipLabel =
      humanise(relationshipType);

    const colour = isCatholic
      ? COLORS.catholic
      : COLORS.comparison;

    const symbol =
      RELATIONSHIP_3D_SYMBOLS[relationshipType] ||
      "circle";

    return {
      type: "scatter3d",
      mode: "markers",
      name: `${fieldLabel} · ${relationshipLabel}`,
      x: points.map(point => point.x),
      y: points.map(point => point.y),
      z: points.map(point => point.z),
      customdata: points.map(point => [
        escapeHtml(point.concept),
        escapeHtml(fieldLabel),
        escapeHtml(relationshipLabel),
        escapeHtml(point.primaryLocus),
        escapeHtml(point.comparisonRegister),
        escapeHtml(truncate(point.text, 240)),
        escapeHtml(humanise(point.sourceStatus)),
        escapeHtml(humanise(point.reviewStatus)),
        escapeHtml(point.auditId)
      ]),
      marker: {
        color: colour,
        size: 5.5,
        opacity: 0.88,
        symbol,
        line: {
          color: colour,
          width: 0.5
        }
      },
      hovertemplate:
        "<b>%{customdata[0]}</b><br>" +
        "%{customdata[1]} reference<br>" +
        "Relationship: %{customdata[2]}<br>" +
        "Locus: %{customdata[3]}<br>" +
        "Comparison register: %{customdata[4]}<br><br>" +
        "%{customdata[5]}<br><br>" +
        "Source status: %{customdata[6]}<br>" +
        "Review status: %{customdata[7]}<br>" +
        "<span style='color:#657083'>Audit: " +
        "%{customdata[8]}</span><extra></extra>"
    };
  }

  function populateReferenceMapControls() {
    const loci = uniqueSorted(
      state.data.comparisons.map(
        row => row.primary_locus
      )
    );

    const relationships = uniqueSorted(
      state.data.comparisons.map(
        row => row.relationship_type
      )
    );

    populateSelect(
      byId("reference-locus-filter"),
      loci,
      {
        allLabel: "All loci",
        selectedValue: "all",
        labelFunction: value => value
      }
    );

    populateSelect(
      byId("reference-relationship-filter"),
      relationships,
      {
        allLabel: "All relationships",
        selectedValue: "all",
        labelFunction: humanise
      }
    );
  }

  function updateReferenceMap() {
    const selectedLocus =
      byId("reference-locus-filter")?.value ||
      "all";

    const selectedRelationship =
      byId("reference-relationship-filter")?.value ||
      "all";

    const referencePoints = state.points
      .filter(point => point.itemType === "reference")
      .filter(
        point =>
          selectedLocus === "all" ||
          point.primaryLocus === selectedLocus
      )
      .filter(
        point =>
          selectedRelationship === "all" ||
          point.relationshipType ===
            selectedRelationship
      );

    const groups = new Map();

    referencePoints.forEach(point => {
      const key =
        `${point.referenceGroup}::` +
        `${point.relationshipType}`;

      if (!groups.has(key)) {
        groups.set(key, []);
      }

      groups.get(key).push(point);
    });

    const traces = [...groups.entries()]
      .sort(([left], [right]) =>
        left.localeCompare(right)
      )
      .map(([key, points]) => {
        const [
          referenceGroup,
          relationshipType
        ] = key.split("::");

        return referenceTrace(
          points,
          referenceGroup,
          relationshipType
        );
      });

    window.Plotly.react(
      "reference-map-chart",
      traces,
      umapLayout({
        height: 640,
        showLegend: true
      }),
      plotConfig
    );

    const catholicCount = referencePoints.filter(
      point =>
        point.referenceGroup === "catholic"
    ).length;

    const comparisonCount = referencePoints.filter(
      point =>
        point.referenceGroup === "comparison"
    ).length;

    setText(
      "reference-map-count",
      `${formatInteger(referencePoints.length)} of 600 anchors`
    );

    setText(
      "reference-map-summary",
      `Showing ${formatInteger(catholicCount)} Catholic and ` +
        `${formatInteger(comparisonCount)} comparison references. ` +
        `Colour identifies the generated reference field; marker shape ` +
        `identifies the pre-assigned theological relationship type.`
    );
  }

  function bindReferenceMapControls() {
    byId("reference-locus-filter")
      ?.addEventListener(
        "change",
        updateReferenceMap
      );

    byId("reference-relationship-filter")
      ?.addEventListener(
        "change",
        updateReferenceMap
      );

    byId("reference-reset-camera")
      ?.addEventListener(
        "click",
        () => {
          window.Plotly.relayout(
            "reference-map-chart",
            {
              "scene.camera":
                state.defaultCamera
            }
          );
        }
      );
  }

  function populateConstellationControl() {
    const select =
      byId("constellation-concept");

    if (!select) {
      return;
    }

    const comparisons = [
      ...state.data.comparisons
    ].sort((left, right) =>
      String(left.concept).localeCompare(
        String(right.concept),
        "en",
        {
          sensitivity: "base"
        }
      )
    );

    const options = comparisons.map(row =>
      createElement(
        "option",
        {
          value: row.audit_id
        },
        `${row.concept} — ${row.comparison_register}`
      )
    );

    replaceChildren(select, options);

    const preferredAudit =
      comparisons.some(
        row =>
          row.audit_id ===
          "death_biological"
      )
        ? "death_biological"
        : comparisons[0]?.audit_id || "";

    select.value = preferredAudit;
    state.selectedAuditId = preferredAudit;
  }

  function constellationTrace(
    points,
    role
  ) {
    const baseStyle = roleStyle(role);

    const selectedStyle = {
      ...baseStyle,
      size: Math.max(
        number(baseStyle.size) + 3.5,
        8
      ),
      opacity: 1
    };

    return pointsToTrace(
      points,
      role,
      {
        style: selectedStyle,
        name: baseStyle.label,
        showLegend: true,
        hover: true
      }
    );
  }

  function updateConstellation() {
    const select =
      byId("constellation-concept");

    const auditId =
      select?.value ||
      state.selectedAuditId;

    if (!auditId) {
      return;
    }

    state.selectedAuditId = auditId;

    const audit =
      metadataForAudit(auditId);

    const selectedPoints = state.points.filter(
      point =>
        point.auditId === auditId
    );

    const backgroundPoints = state.points.filter(
      point =>
        point.auditId !== auditId
    );

    const backgroundTrace = pointsToTrace(
      backgroundPoints,
      "background",
      {
        name: "Other benchmark texts",
        style: {
          label: "Other benchmark texts",
          color: "#9ba5b1",
          symbol: "circle",
          size: 2,
          opacity: 0.075
        },
        showLegend: false,
        hover: false
      }
    );

    const roleOrder = [
      "reference:catholic",
      "reference:comparison",
      "query:bare",
      "query:natural_general",
      "query:natural_ambiguous",
      "query:label_free_theological",
      "query:explicit_catholic",
      "query:integrative",
      "query:critical",
      "validation:clear_register:catholic",
      "validation:clear_register:comparison",
      "validation:integrative:integrative",
      "validation:critical:critical_review"
    ];

    const selectedRoles = uniqueSorted(
      selectedPoints.map(point => point.role)
    ).sort((left, right) => {
      const leftIndex =
        roleOrder.indexOf(left);

      const rightIndex =
        roleOrder.indexOf(right);

      return (
        (leftIndex === -1 ? 999 : leftIndex) -
        (rightIndex === -1 ? 999 : rightIndex)
      );
    });

    const selectedTraces =
      selectedRoles.map(role =>
        constellationTrace(
          selectedPoints.filter(
            point => point.role === role
          ),
          role
        )
      );

    window.Plotly.react(
      "constellation-chart",
      [
        backgroundTrace,
        ...selectedTraces
      ],
      umapLayout({
        height: 640,
        showLegend: true
      }),
      plotConfig
    );

    const referenceCount =
      selectedPoints.filter(
        point =>
          point.itemType === "reference"
      ).length;

    const queryCount =
      selectedPoints.filter(
        point =>
          point.itemType === "query"
      ).length;

    const validationCount =
      selectedPoints.filter(
        point =>
          point.itemType === "validation"
      ).length;

    setText(
      "constellation-summary",
      `${audit.concept || auditId}: ` +
        `${formatInteger(referenceCount)} references, ` +
        `${formatInteger(queryCount)} queries, and ` +
        `${formatInteger(validationCount)} validation passages are ` +
        `highlighted against ${formatInteger(backgroundPoints.length)} ` +
        `dimmed benchmark texts. UMAP distance is not used to identify ` +
        `nearest references.`
    );
  }

  function bindConstellationControls() {
    byId("constellation-concept")
      ?.addEventListener(
        "change",
        updateConstellation
      );

    byId("constellation-reset-camera")
      ?.addEventListener(
        "click",
        () => {
          window.Plotly.relayout(
            "constellation-chart",
            {
              "scene.camera":
                state.defaultCamera
            }
          );
        }
      );
  }

  function initialiseAdditionalUmapViews() {
    populateReferenceMapControls();
    bindReferenceMapControls();
    updateReferenceMap();

    populateConstellationControl();
    bindConstellationControls();
    updateConstellation();
  }

  function explorerFilterValues() {
    return {
      locus:
        byId("explorer-locus-filter")?.value ||
        "all",
      register:
        byId("explorer-register-filter")?.value ||
        "all",
      relationship:
        byId("explorer-relationship-filter")?.value ||
        "all",
      lifeDeath:
        byId("explorer-life-death-filter")?.value ||
        "all",
      critical:
        byId("explorer-critical-filter")?.value ||
        "all"
    };
  }

  function auditMatchesExplorerFilters(
    audit,
    filters
  ) {
    return (
      (
        filters.locus === "all" ||
        audit.primary_locus === filters.locus
      ) &&
      (
        filters.register === "all" ||
        audit.comparison_register ===
          filters.register
      ) &&
      (
        filters.relationship === "all" ||
        audit.relationship_type ===
          filters.relationship
      ) &&
      (
        filters.lifeDeath === "all" ||
        boolean(audit.life_death_module) ===
          (filters.lifeDeath === "true")
      ) &&
      (
        filters.critical === "all" ||
        boolean(
          audit.critical_context_applicable
        ) ===
          (filters.critical === "true")
      )
    );
  }

  function populateExplorerStaticFilters() {
    const audits = state.data.comparisons;

    populateSelect(
      byId("explorer-locus-filter"),
      uniqueSorted(
        audits.map(row => row.primary_locus)
      ),
      {
        allLabel: "All loci",
        selectedValue: "all",
        labelFunction: value => value
      }
    );

    populateSelect(
      byId("explorer-register-filter"),
      uniqueSorted(
        audits.map(
          row => row.comparison_register
        )
      ),
      {
        allLabel: "All registers",
        selectedValue: "all",
        labelFunction: value => value
      }
    );

    populateSelect(
      byId("explorer-relationship-filter"),
      uniqueSorted(
        audits.map(
          row => row.relationship_type
        )
      ),
      {
        allLabel: "All relationships",
        selectedValue: "all",
        labelFunction: humanise
      }
    );
  }

  function clearExplorer() {
    setText(
      "explorer-concept-title",
      "No audits match these filters"
    );

    setText(
      "explorer-register",
      "Reset or broaden the filters to continue."
    );

    replaceChildren(
      byId("explorer-tags"),
      []
    );

    setText(
      "explorer-query-text",
      "No query is selected."
    );

    setText(
      "explorer-review-status",
      ""
    );

    [
      "explorer-s-c",
      "explorer-s-r",
      "explorer-cas",
      "explorer-nearest-catholic",
      "explorer-nearest-comparison",
      "explorer-nearest-overall",
      "explorer-nearest-catholic-score",
      "explorer-nearest-comparison-score",
      "explorer-nearest-overall-score",
      "explorer-sign-stability",
      "explorer-max-change",
      "explorer-paraphrase-range",
      "explorer-paraphrase-sd"
    ].forEach(id => setText(id, "—"));

    replaceChildren(
      byId("explorer-shift-table-body"),
      []
    );
  }

  function updateExplorerConceptOptions() {
    const filters = explorerFilterValues();

    const audits = [
      ...state.data.comparisons
    ]
      .filter(audit =>
        auditMatchesExplorerFilters(
          audit,
          filters
        )
      )
      .sort((left, right) =>
        String(left.concept).localeCompare(
          String(right.concept),
          "en",
          {
            sensitivity: "base"
          }
        )
      );

    const select =
      byId("explorer-concept-filter");

    const previousValue =
      select?.value ||
      state.selectedAuditId;

    if (!audits.length) {
      replaceChildren(
        select,
        [
          createElement(
            "option",
            { value: "" },
            "No matching concepts"
          )
        ]
      );

      setText(
        "explorer-filter-count",
        "0 of 100 audits match the active filters."
      );

      clearExplorer();
      return;
    }

    const options = audits.map(audit =>
      createElement(
        "option",
        { value: audit.audit_id },
        `${audit.concept} — ` +
          `${audit.comparison_register}`
      )
    );

    replaceChildren(select, options);

    if (
      audits.some(
        audit =>
          audit.audit_id === previousValue
      )
    ) {
      select.value = previousValue;
    } else if (
      audits.some(
        audit =>
          audit.audit_id ===
          "death_biological"
      )
    ) {
      select.value = "death_biological";
    } else {
      select.value = audits[0].audit_id;
    }

    state.selectedAuditId = select.value;

    setText(
      "explorer-filter-count",
      `${formatInteger(audits.length)} of 100 audits ` +
        `match the active filters.`
    );

    updateExplorerForAudit();
  }

  function renderExplorerHeader(audit) {
    setText(
      "explorer-concept-title",
      audit.concept
    );

    setText(
      "explorer-register",
      `Compared with: ` +
        `${audit.comparison_register}`
    );

    const tagValues = [
      audit.primary_locus,
      humanise(audit.relationship_type),
      boolean(audit.life_death_module)
        ? "Life and Death module"
        : null,
      boolean(
        audit.critical_context_applicable
      )
        ? "Critical context applicable"
        : null
    ].filter(Boolean);

    const tags = tagValues.map(value =>
      createElement(
        "span",
        {
          className: "concept-tag"
        },
        value
      )
    );

    replaceChildren(
      byId("explorer-tags"),
      tags
    );
  }

  function availableConditionsForAudit(auditId) {
    const conditions = uniqueSorted(
      state.data.queryScores
        .filter(
          row => row.audit_id === auditId
        )
        .map(row => row.condition)
    );

    return CONDITION_ORDER.filter(condition =>
      conditions.includes(condition)
    );
  }

  function updateExplorerConditionOptions() {
    const auditId =
      byId("explorer-concept-filter")?.value;

    if (!auditId) {
      clearExplorer();
      return;
    }

    state.selectedAuditId = auditId;

    const audit =
      metadataForAudit(auditId);

    renderExplorerHeader(audit);

    const select =
      byId("explorer-condition-filter");

    const previousCondition =
      select?.value;

    const conditions =
      availableConditionsForAudit(auditId);

    const preferredCondition =
      conditions.includes(previousCondition)
        ? previousCondition
        : conditions.includes("integrative")
          ? "integrative"
          : conditions[0];

    populateSelect(
      select,
      conditions,
      {
        selectedValue: preferredCondition,
        labelFunction: condition =>
          CONDITION_LABELS[condition] ||
          humanise(condition)
      }
    );

    syncExplorerWithConstellation(auditId);
    updateExplorerQueryOptions();
  }

  function updateExplorerQueryOptions() {
    const auditId =
      byId("explorer-concept-filter")?.value;

    const condition =
      byId("explorer-condition-filter")?.value;

    if (!auditId || !condition) {
      clearExplorer();
      return;
    }

    const rows = state.data.queryScores
      .filter(
        row =>
          row.audit_id === auditId &&
          row.condition === condition
      )
      .sort((left, right) =>
        String(left.paraphrase_id)
          .localeCompare(
            String(right.paraphrase_id),
            "en",
            {
              numeric: true
            }
          )
      );

    const select =
      byId("explorer-query-filter");

    const previousQuery =
      select?.value ||
      state.selectedQueryId;

    const options = rows.map(row =>
      createElement(
        "option",
        { value: row.query_id },
        `${String(
          row.paraphrase_id
        ).toUpperCase()} · ` +
          `${truncate(row.query_text, 90)}`
      )
    );

    replaceChildren(select, options);

    if (
      rows.some(
        row =>
          row.query_id === previousQuery
      )
    ) {
      select.value = previousQuery;
    } else {
      select.value =
        rows[0]?.query_id || "";
    }

    state.selectedQueryId = select.value;
    renderExplorerSelection();
  }

  function nearestScoreText({
    similarity,
    referenceId,
    rank = null,
    group = null
  }) {
    const parts = [
      `Similarity ${formatNumber(
        similarity,
        4
      )}`
    ];

    if (rank !== null) {
      parts.push(`rank ${rank} of 6`);
    }

    if (group) {
      parts.push(`${humanise(group)} field`);
    }

    if (referenceId) {
      parts.push(referenceId);
    }

    return parts.join(" · ");
  }

  function renderExplorerScores(query) {
    setText(
      "explorer-query-text",
      query.query_text
    );

    setText(
      "explorer-review-status",
      `Query status: ${humanise(
        query.review_status
      )}. Exact wording is displayed as generated.`
    );

    setText(
      "explorer-s-c",
      formatNumber(query.s_c, 4)
    );

    setText(
      "explorer-s-r",
      formatNumber(query.s_r, 4)
    );

    setText(
      "explorer-cas",
      formatSigned(query.cas, 4)
    );

    setText(
      "explorer-nearest-catholic",
      query.nearest_catholic_reference_text
    );

    setText(
      "explorer-nearest-catholic-score",
      nearestScoreText({
        similarity:
          query.nearest_catholic_similarity,
        referenceId:
          query.nearest_catholic_reference_id,
        rank:
          query.nearest_catholic_rank
      })
    );

    setText(
      "explorer-nearest-comparison",
      query.nearest_comparison_reference_text
    );

    setText(
      "explorer-nearest-comparison-score",
      nearestScoreText({
        similarity:
          query.nearest_comparison_similarity,
        referenceId:
          query.nearest_comparison_reference_id,
        rank:
          query.nearest_comparison_rank
      })
    );

    setText(
      "explorer-nearest-overall",
      query.top_reference_text
    );

    setText(
      "explorer-nearest-overall-score",
      nearestScoreText({
        similarity:
          query.top_reference_similarity,
        referenceId:
          query.top_reference_id,
        group:
          query.top_reference_group
      })
    );
  }

  function aggregateAuditShifts(auditId) {
    const grouped = new Map();

    state.data.shifts
      .filter(
        row => row.audit_id === auditId
      )
      .forEach(row => {
        if (
          !grouped.has(row.contrast_type)
        ) {
          grouped.set(
            row.contrast_type,
            {
              deltaSC: [],
              deltaSR: [],
              deltaCas: []
            }
          );
        }

        const values =
          grouped.get(row.contrast_type);

        values.deltaSC.push(
          number(row.delta_s_c)
        );

        values.deltaSR.push(
          number(row.delta_s_r)
        );

        values.deltaCas.push(
          number(row.delta_cas)
        );
      });

    return SHIFT_ORDER
      .filter(contrast =>
        grouped.has(contrast)
      )
      .map(contrast => {
        const values =
          grouped.get(contrast);

        return {
          contrast,
          deltaSC: mean(values.deltaSC),
          deltaSR: mean(values.deltaSR),
          deltaCas: mean(values.deltaCas)
        };
      });
  }

  function renderExplorerShiftTable(auditId) {
    const body =
      byId("explorer-shift-table-body");

    const rows =
      aggregateAuditShifts(auditId);

    const tableRows = rows.map(row => {
      const tr = createElement("tr");

      [
        SHIFT_LABELS[row.contrast] ||
          humanise(row.contrast),
        formatSigned(row.deltaSC),
        formatSigned(row.deltaSR),
        formatSigned(row.deltaCas)
      ].forEach(value => {
        tr.append(
          createElement("td", {}, value)
        );
      });

      return tr;
    });

    replaceChildren(body, tableRows);
  }

  function renderExplorerRobustness(query) {
    const reference =
      state.data.referenceSensitivity.find(
        row =>
          row.query_id === query.query_id
      );

    const paraphrase =
      state.data.paraphraseCondition.find(
        row =>
          row.audit_id === query.audit_id &&
          row.condition === query.condition
      );

    setText(
      "explorer-sign-stability",
      reference
        ? formatPercent(
            reference.sign_stability_proportion
          )
        : "Not available"
    );

    setText(
      "explorer-max-change",
      reference
        ? formatNumber(
            reference.max_absolute_cas_change,
            4
          )
        : "Not available"
    );

    setText(
      "explorer-paraphrase-range",
      paraphrase
        ? `${formatSigned(
            paraphrase.min_cas
          )} to ${formatSigned(
            paraphrase.max_cas
          )}`
        : "Single wording"
    );

    setText(
      "explorer-paraphrase-sd",
      paraphrase
        ? formatNumber(
            paraphrase.cas_standard_deviation,
            4
          )
        : "Not applicable"
    );
  }

  function renderExplorerSelection() {
    const queryId =
      byId("explorer-query-filter")?.value;

    if (!queryId) {
      clearExplorer();
      return;
    }

    const query =
      state.data.queryScores.find(
        row =>
          row.query_id === queryId
      );

    if (!query) {
      throw new Error(
        `Selected query was not found: ${queryId}`
      );
    }

    state.selectedQueryId = queryId;

    renderExplorerScores(query);
    renderExplorerShiftTable(
      query.audit_id
    );
    renderExplorerRobustness(query);
  }

  function updateExplorerForAudit() {
    const auditId =
      byId("explorer-concept-filter")?.value;

    if (!auditId) {
      clearExplorer();
      return;
    }

    state.selectedAuditId = auditId;
    updateExplorerConditionOptions();
  }

  function syncExplorerWithConstellation(
    auditId
  ) {
    const constellation =
      byId("constellation-concept");

    if (
      constellation &&
      [...constellation.options].some(
        option =>
          option.value === auditId
      )
    ) {
      constellation.value = auditId;
      updateConstellation();
    }
  }

  function resetExplorerFilters() {
    [
      "explorer-locus-filter",
      "explorer-register-filter",
      "explorer-relationship-filter",
      "explorer-life-death-filter",
      "explorer-critical-filter"
    ].forEach(id => {
      const select = byId(id);

      if (select) {
        select.value = "all";
      }
    });

    state.selectedAuditId =
      "death_biological";

    state.selectedQueryId = "";

    updateExplorerConceptOptions();
  }

  function bindExplorerControls() {
    [
      "explorer-locus-filter",
      "explorer-register-filter",
      "explorer-relationship-filter",
      "explorer-life-death-filter",
      "explorer-critical-filter"
    ].forEach(id => {
      byId(id)?.addEventListener(
        "change",
        updateExplorerConceptOptions
      );
    });

    byId("explorer-concept-filter")
      ?.addEventListener(
        "change",
        () => {
          state.selectedQueryId = "";
          updateExplorerForAudit();
        }
      );

    byId("explorer-condition-filter")
      ?.addEventListener(
        "change",
        () => {
          state.selectedQueryId = "";
          updateExplorerQueryOptions();
        }
      );

    byId("explorer-query-filter")
      ?.addEventListener(
        "change",
        renderExplorerSelection
      );

    byId("explorer-reset-filters")
      ?.addEventListener(
        "click",
        resetExplorerFilters
      );
  }

  function initialiseExplorer() {
    populateExplorerStaticFilters();
    bindExplorerControls();
    updateExplorerConceptOptions();
  }

  function initialiseAccessibilityControls() {
    const loci = uniqueSorted(
      state.data.conditionSummary.map(
        row => row.primary_locus
      )
    );

    populateSelect(
      byId("accessibility-locus"),
      loci,
      {
        allLabel: "All loci",
        selectedValue: "all",
        labelFunction: value => value
      }
    );

    byId("accessibility-condition")
      ?.addEventListener(
        "change",
        updateAccessibilityChart
      );

    byId("accessibility-locus")
      ?.addEventListener(
        "change",
        updateAccessibilityChart
      );

    updateAccessibilityChart();
  }

  function showFatalDashboardError(error) {
    console.error(error);

    const message =
      error instanceof Error
        ? error.message
        : String(error);

    setStatus(
      `Dashboard could not load: ${message}`,
      "error"
    );

    document.documentElement.dataset.dashboardState =
      "error";

    document
      .querySelectorAll(".chart-loading")
      .forEach(element => {
        element.textContent =
          "This chart could not be loaded. " +
          "Check the local server, network connection, and browser console.";
      });
  }

  async function initialiseApplication() {
    try {
      setStatus(
        "Loading committed result tables…"
      );

      assertLibrary(
        "Plotly.js",
        window.Plotly
      );

      assertLibrary(
        "Papa Parse",
        window.Papa
      );

      if (window.location.protocol === "file:") {
        throw new Error(
          "Serve the repository through an HTTP server; " +
          "browser data loading is not supported from file://."
        );
      }

      state.data = await loadAllData();

      setStatus(
        "Rendering high-dimensional numerical analyses…"
      );

      renderConditionCharts();
      renderShiftChart();
      initialiseAccessibilityControls();
      renderCriticalChart();
      renderLabelEffectChart();
      renderRobustness();

      setStatus(
        "Rendering the shared exploratory UMAP views…"
      );

      initialiseGlobalAtlas();
      initialiseAdditionalUmapViews();

      setStatus(
        "Preparing the concept explorer…"
      );

      initialiseExplorer();

      document.documentElement.dataset.dashboardState =
        "ready";

      setStatus(
        "Dashboard ready.",
        "ready"
      );
    } catch (error) {
      showFatalDashboardError(error);
    }
  }

  if (document.readyState === "loading") {
    document.addEventListener(
      "DOMContentLoaded",
      initialiseApplication,
      {
        once: true
      }
    );
  } else {
    initialiseApplication();
  }
})();
