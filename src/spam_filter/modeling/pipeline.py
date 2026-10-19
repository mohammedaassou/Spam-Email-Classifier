
from pathlib import Path
import pandas as pd

from spam_filter import log
from spam_filter.data.cleaning import EmailColumn, clean_dataset
from spam_filter.data.download import downloadData
from spam_filter.modeling.evaluate import evaluate_model
from spam_filter.modeling.split import split_dataset
from spam_filter.modeling.train import fit_final_model, training
from spam_filter.modeling.utils import format_run_summary, save_model


def run_pipeline(
    csv_path: Path,
    artifacts_dir: Path,
) -> dict:

    downloadData()
    
    raw_data = pd.read_csv(csv_path)

    data = clean_dataset(raw_data)
    # texts = data[EmailColumn.TEXT]

    # print("Nombre de textes :", len(texts))
    # print("Textes différents :", texts.nunique())

    # for text in texts.head(3):
    #     print(repr(text[:200]))

    # print("Textes différents :", data[EmailColumn.TEXT].nunique())
    # print("Modèle sauvegardé :", type(model.steps[-1][1]).__name__)
    # print(confusion_matrix(y_test, model.predict(X_test)))  

    splits = split_dataset(data)

    validation_results = training(splits)


    # Notre choix actuel, basé sur la validation : Logistic Regression.
    final_model = fit_final_model(splits)

    model_path = save_model(
        final_model,
        artifacts_dir / "spam_classifier.joblib",
    )

    test_results = evaluate_model(
        model_path,
        splits.X_test,
        splits.y_test,
        artifacts_dir,
    )

    return {
        "model_path": model_path,
        "validation_results": validation_results,
        "test_results": test_results,
    }


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parents[3]
        
    DATA_PATH = PROJECT_ROOT / "data" / "processed" / "emails.csv"

    artifactpath = PROJECT_ROOT / "artifacts"
    # raw_data = pd.read_csv(DATA_PATH)
    result = run_pipeline(DATA_PATH, artifactpath)
    log.syslog(format_run_summary(result))