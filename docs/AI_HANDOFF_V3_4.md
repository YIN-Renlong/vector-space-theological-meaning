# AI Handoff: CTSB v3.4

## Purpose of this document
This document transfers the methodological and implementation context of the project to a new AI thread.
The active project is no longer the CTSB-100 v2 implementation. It is now in the CTSB v3.4 methodology and implementation stage.
The archived v2 Python files are included in the generated AI context only as historical implementation references. They must not be treated as the active methodological specification or copied unchanged.

## 1. Project identity
Project: Vector Space and Theological Meaning
Active methodological version: CTSB v3.4
Direct object of study: Azure/OpenAI text-embedding-3-large
Primary intellectual orientation: A Catholic theological audit of semantic behaviour in a commercial embedding model, especially under moral ambiguity, anthropological complexity, pastoral sensitivity, and critical or crisis contexts.

## 2. Current repository state
The active root contains the v3.4 methodology README and development files. A lean, non-evidential synthetic prototype now tests five audit units using four CSV files and one integrated Python script. This prototype validates data flow and mathematics only. The next substantive task is source-grounded benchmark construction and review. Visualisation and dashboard development are not the next primary task.

## 3. Historical v2 status
The v2 findings are preliminary observations to be re-tested, not assumptions that v3.4 must reproduce. The v2 comparison category was too broad. A negative v2 CAS must therefore not be interpreted simply as secularism or opposition to Catholic theology.

## 4. Primary v3.4 research orientation
The project investigates recurring semantic behaviours such as stable theological legibility, general-use foregrounding, theological recoverability, register differentiation, and persistent theological attenuation. It is a computational semantic autopsy.

## 5. Important theological distinction
Catholic theology is not always opposed to psychological, biological, medical, legal, social, or economic descriptions. These descriptions may have different relationships to Catholic theology (Complementary levels, Valid but partial, Normatively conflicting, Alternative lexical senses).

## 6. How the embedding method actually works
An embedding model outputs numerical vectors, not natural-language explanations. The method works by embedding both the query text and known natural-language reference texts, then comparing them using cosine similarity.

## 7. Catholic Association Contrast
The active full name of CAS is Catholic Association Contrast.
CAS(q; C, R) = mean(cosine(q, C)) - mean(cosine(q, R))
A negative CAS does not automatically mean secular ideology; it is a relative contrast.

## 8. Mathematical foundation
The CAS formula adapts the differential cosine-association function introduced in the Word Embedding Association Test (WEAT) and SEAT. v3.4 emphasizes empirical reference construction and held-out validation.

## 9. How a result is identified as Catholic
A numerical vector cannot be read directly as Catholic. The category is defined externally through the provenance of the natural-language references (Catechism, encyclicals, etc.).

## 10. Held-out validation
Reference review is necessary but insufficient. The metric must also be validated numerically on natural-language passages that were not used to build the reference sets (Stage A, B, and C validation).

## 11. Shift decomposition
For two matched contexts, ΔCAS = ΔSc - ΔSr. A positive CAS shift may arise because Catholic similarity increased, comparison similarity decreased, or both. We must track the component shifts.

## 12. Theological loci
1. Freedom, truth, and moral teleology
2. Human dignity and theological anthropology
3. Love, communion, and sacramentality
4. Sin, grace, and redemption

## 13. Life and Death critical-context module
How does the model reorganise semantic salience when life, death, grief, suicide, and euthanasia are expressed as natural existential, pastoral, or crisis-language utterances?

## 14. Planned benchmark structure
The active v3.4 benchmark should use several linked registries rather than one overloaded CSV: Concept registry, Reference registry, Query registry, and Validation registry.

## 15. Planned query conditions
Conditions include bare concepts, ordinary usage, ambiguous contexts, crisis contexts, and explicit Catholic contexts.

## 16. Planned output structure
Required numerical outputs: Model-run manifest, Descriptor/reference-level similarities, Query-level scores, Concept-context summaries, Held-out validation results, Component-shift decomposition, and Statistical summaries.

## 17. Minimum robustness requirements
Essential checks: held-out validity, theological review, source provenance, leave-one-out sensitivity, component-level shift decomposition, and a frozen benchmark before final evaluation.

## 18. Data-first implementation order
Phase 1: benchmark schema
Phase 2: small development fixture
Phase 3: computational engine
Phase 4: tests
Phase 5: benchmark construction and review
Phase 6: freeze and final run
Phase 7: analysis
Phase 8: visualisation (Only after numerical analysis is stable)

## 19. What may be reused from v2
Use v2 for API access, caching, and cosine calculations. Do NOT copy the assumption of a single broad secular category or mix computation with HTML generation.

## 20. Visualisation policy
Numerical analysis establishes the result; visualisation diagnoses and communicates it. Produce stable machine-readable outputs first.

## 21. Cross-model work
Raw CAS values from different models must not be compared directly. Cross-model comparisons should use within-model standardised effects and rank correlation.

## 22. Instructions for the next AI thread
Treat this handoff as the controlling specification. The immediate task is defining the benchmark schemas and building the modular pipeline. Do not fabricate theological sources.

## 23. User workflow preferences
The user works primarily through macOS Terminal. Provide concise, deterministic Bash commands using HTTPS GitHub remotes.
