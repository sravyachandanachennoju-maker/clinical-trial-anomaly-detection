# Repository Guide

## Start here

1. `README.md` for the research question, locked design, final results, limitations, and reproduction commands.
2. `research_design.md` for the original Stage 1 research architecture.
3. `data/README.md` and `docs/dataset_generation.md` for the synthetic dataset design.
4. `docs/methodology.md` for the end-to-end study design.
5. `docs/rule_dictionary.md` for the deterministic rules.
6. `docs/feature_dictionary.md` for the Isolation Forest feature set.
7. `docs/isolation_forest.md` for the model configuration and interpretation.
8. `docs/reproducibility.md` for execution instructions.
9. `manuscript/research_report.md` for the completed manuscript.
10. `docs/phd_professor_explanation.md` for a concise research explanation.

## Source code

- `src/generate_data.py`: locked synthetic dataset generation.
- `src/rule_based_detection.py`: deterministic detection layer.
- `src/preprocessing.py`: locked feature construction and train-only preprocessing utilities.
- `src/isolation_forest.py`: modular implementation of the refined held-out Isolation Forest experiment.
- `src/evaluation.py`: apples-to-apples evaluation on the same held-out population.
- `src/stage4_refinement.py`: preserved original Stage 4 refinement script and audit outputs.
- `src/stage5_comparative_evaluation.py`: preserved comparative analysis and figure-generation workflow.

## Results organization

The repository keeps the original staged result files under `results/` for traceability. Clean copies of the most important final tables are also available in:

- `results/tables/`
- `results/metrics/`
- `results/figures/`

The manuscript package is in `manuscript/`.

## Locked experiment policy

Stages 1–7 are locked. Do not change the dataset, anomaly injections, seed, split, rules, model configuration, or final evaluation population merely to improve a result. Any future methodological change should be documented as a new experiment with a new analysis version.
