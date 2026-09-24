# Reproducibility Guide

This repository preserves the locked outputs from the completed experiment. The scripts implement the methodological pipeline and the saved result files provide an audit trail for the manuscript.

## 1. Create an environment

```bash
python -m venv .venv
```

Windows:

```bash
.venv\Scripts\activate
```

macOS/Linux:

```bash
source .venv/bin/activate
```

Install dependencies:

```bash
pip install -r requirements.txt
```

## 2. Generate the synthetic dataset

```bash
python src/generate_data.py
```

This uses the locked seed `20260924` and writes the synthetic dataset to `data/`.

## 3. Run deterministic rule-based detection

```bash
python src/rule_based_detection.py
```

This produces the rule-level record flags and full-dataset summary outputs in `results/`.

## 4. Run the locked Isolation Forest experiment

```bash
python src/isolation_forest.py
```

This performs the 80/20 stratified split, fits preprocessing only on training data, fits Isolation Forest on the transformed training data, evaluates the held-out set at contamination 0.05, 0.08, and 0.10, and writes the locked Stage 4-style outputs.

## 5. Run the final comparison

```bash
python src/evaluation.py
```

This evaluates both methods on the same held-out population and writes final comparison tables.

## 6. Generate publication-oriented figures

```bash
python src/stage5_comparative_evaluation.py
```

The repository also preserves the audited Stage 6 figures under `results/figures/stage6/`.

## Exact-reproduction note

The manuscript's final numbers are traceable to the locked Stage 5/6 result files. The repository does **not** use the final metrics as inputs to manufacture predictions. Reproduction means rerunning the data generator and analysis pipeline, then checking the outputs against the saved audit files.

Because software versions and platform-level numerical behavior can differ, small implementation-level differences should be treated as a reproducibility issue to investigate rather than silently corrected by changing the experiment.
