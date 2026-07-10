# Development Log

## 10 July 2026 — CTSB v3.4 methodology redesign

### Status

CTSB-100 v2 has been archived. The active project has entered a methodology-design phase. No v3.4 benchmark results have yet been generated.

### Questions raised during methodological review

The redesign was motivated by several foundational questions:

1. Does negative CAS demonstrate “common language,” and how is that category defined?
2. What model is being audited, and what text is known to have trained it?
3. What can be concluded from the plots, and what cannot?
4. How can a numerical embedding result be identified as Catholic?
5. Does a positive contrast shift represent increased Catholic proximity or only reduced comparison proximity?
6. Are psychological, biological, clinical, legal, social, and theological meanings mutually exclusive?
7. Why audit an embedding model rather than a generative chatbot?
8. How can the method remain useful to theologians without treating cosine similarity as theological authority?

Attribution for externally raised review questions will be added only with the reviewer's permission.

### Main v3.4 decisions

- Rename the metric **Catholic Association Contrast**.
- Treat CAS as a relative association statistic, not a probability or truth score.
- Embed both queries and known natural-language references.
- Interpret vectors through their measured relationships to source-grounded references.
- Preserve the original natural-language text attached to every reference vector.
- Distinguish complementary, partial, conflicting, lexical, and generic-religious relationships.
- Validate the instrument on held-out texts.
- Retain separate Catholic and comparison similarities alongside their difference.
- Decompose every context shift as:
  
  \[
  \Delta CAS=\Delta S_C-\Delta S_R
  \]

- Introduce natural ambiguity and critical-context conditions.
- Keep visualisations secondary to high-dimensional numerical analysis.
- Reserve generative GPT and retrieval-system audits for future work.

### Archived v2 findings

The v2 results remain historical preliminary evidence. They are not automatically carried forward as v3.4 conclusions.

The following patterns will be independently re-tested:

- explicit Catholic wording produced a strong relative shift;
- explicitly doctrinal concepts appeared comparatively stable;
- moral-teleological concepts showed autonomy-, choice-, permission-, and well-being-centred foregrounding;
- anthropological concepts showed biological, functional, economic, and legal foregrounding;
- life/death concepts showed clinical, psychological, biological, legal, and crisis-related foregrounding;
- grief, suicide, euthanasia, chastity, autonomy, shame, and license appeared comparatively resistant.

### Next implementation stage

The next stage will design the v3.4 benchmark schema and source-review workflow.

The v3.4 Python audit must be written separately. The archived v2 script does not implement the v3.4 protocol.
