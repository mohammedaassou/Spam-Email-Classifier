# Evidence and implementation gaps

- This is documented as a personal project. The author name comes from `pyproject.toml`; no institution, supervisor or submission date is claimed.
- The checked CSV has 2,998 rows (2,500 ham, 498 spam), 49 duplicate extras by exact subject/body pair, two blank subjects and 212 blank bodies. Cleaning leaves 2,949 unique subject/body pairs. These are file-inspection counts; a rerun of the downloader may differ.
- Saved validation figures show Logistic Regression and SVM tied: 395 true ham, one false positive, six missed spam and 70 detected spam each. The code comment describing higher Logistic Regression recall is inconsistent with the figures; selection is hard-coded. The report redraws the model comparison and majority-choice charts from these saved counts so the visible labels use concepts rather than class names.
- The final test matrix shows 493 true ham, two false positives, two false negatives and 93 detected spam. The ROC image displays AUC rounded to 1.00; the unrounded value and run metadata are not recorded here.
- `predict_email` calls `predict_proba`, but `/predict` returns only `{ "label": ... }`. Both prediction infographics incorrectly show a spam-probability output.
- Training text includes `subject:` and `body:` markers before `clean_text`; prediction uses `build_email_text` without those markers before the same cleaning function.
- The repository does not provide an external validation set, latency benchmark, deployment record, message-level error analysis or a documented run manifest for the charts. Hand-written demonstration emails are not treated as measured evaluation.
- The metrics study image contains illustrative and ambiguous arithmetic and is excluded from the report at the author's request.
