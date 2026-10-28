# Image coverage

The report uses 12 figures. Ten are copied from `artifacts/`; two validation charts were redrawn from the saved counts with concept labels. Their originals remain in `artifacts/`. The metrics study sketch was excluded at the author's request. Copied filenames remove spaces and special characters so `main.tex` compiles portably. ``Evidence'' means a saved or faithfully redrawn project chart or screenshot; ``illustrative'' means a conceptual graphic.

The report also includes five official technology logos in the technologies table; their sources are listed in `TECH_LOGOS.md`.

| Original under `artifacts/` | Copy under `assets/` | Report section | Figure label | Role |
|---|---|---|---|---|
| `class_distribution_before_cleaning.png` | `class_distribution.png` | Dataset | `fig:class` | Evidence |
| `piplines_flow.png` | `training_flow.png` | Experimental method | `fig:trainflow` | Illustrative |
| `model_comparison.png` | `model_comparison_readable.png` | Validation comparison | `fig:compare` | Evidence; redrawn from saved counts |
| `Validation - DummyClassifier - Confusion Matrix _matrix.png` | `validation_majority_readable.png` | Validation comparison | `fig:dummy` | Evidence; redrawn from saved counts |
| `Validation - Naive bayes - Confusion Matrix _matrix.png` | `validation_nb.png` | Validation comparison | `fig:nb` | Evidence |
| `Validation - logistic regression - Confusion Matrix _matrix.png` | `validation_logreg.png` | Validation comparison | `fig:logreg` | Evidence |
| `Validation - SVM - Confusion Matrix _matrix.png` | `validation_svm.png` | Validation comparison | `fig:svm` | Evidence |
| `Final model Test - logistic regression_matrix.png` | `test_matrix.png` | Held-out evaluation | `fig:test` | Evidence |
| `roc_curve.png` | `roc_curve.png` | Held-out evaluation | `fig:roc` | Evidence, rounded legend |
| `Spam Classifier — Prediction Flow-1.png` | `prediction_flow_a.png` | Application | `fig:predicta` | Illustrative; probability output inaccurate |
| `screen_home.png` | `screen_home.png` | Application | `fig:screen` | Interface screenshot |
| `Predict-to-result workflow infographic-2.png` | `prediction_flow_b.png` | Appendix | `fig:predictb` | Illustrative; probability output inaccurate |
