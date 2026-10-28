

from enum import StrEnum
from pathlib import Path
from statistics import mode

import joblib
from matplotlib import pyplot as plt
from sklearn.metrics import ConfusionMatrixDisplay, accuracy_score, confusion_matrix, precision_score,recall_score,f1_score, roc_auc_score
from sklearn.pipeline import Pipeline

from spam_filter import log



class metricsEnum( StrEnum):
    ACCURACY = "accuracy"
    PRECISION = "precision"
    RECALL = "recall"
    F1 = "f1"
    ROC_AUC = "ROC-AUC"

def calc_metrics(y_true, y_pred, spam_scores = 0):
    # EN: Calculate spam metrics using the real labels first.
    # FR : Calculer les métriques spam en mettant les vraies étiquettes en premier.
    return {
        metricsEnum.ACCURACY: accuracy_score(y_true, y_pred),
        metricsEnum.PRECISION: precision_score(
            y_true, y_pred, pos_label=1, zero_division=0
        ),
        metricsEnum.RECALL: recall_score(
            y_true, y_pred, pos_label=1, zero_division=0
        ),
        metricsEnum.F1: f1_score(
            y_true, y_pred, pos_label=1, zero_division=0
        ),
        
        metricsEnum.ROC_AUC : roc_auc_score( y_true , spam_scores) if spam_scores is not 0 else "Not calculated" 
    }



def save_model(model : Pipeline, path : Path):

    path.parent.mkdir(parents=True, exist_ok=True)
    log.syslog(message=f"Saving model to {path}", verbose=True)
    
    joblib.dump(model, path)


    return path



def customer_confusion_matrix(predictions, y_test, title, saveFigure = False):
    confusion_matrix_ = confusion_matrix(y_pred=predictions, y_true=y_test , labels=[0, 1])


    ConfusionMatrixDisplay(
    
    confusion_matrix=confusion_matrix_,
    
    display_labels=["ham", "spam"],
).plot()


    plt.title(title)


    PROJECT_ROOT = Path(__file__).resolve().parents[3]
        
    artifactpath = PROJECT_ROOT / "artifacts"

    output_path = Path(f"{artifactpath}/{title}_matrix.png")
    output_path.parent.mkdir(parents=True, exist_ok=True)
    if saveFigure:
        # TODO ; the saving does not work, need to fix it
        # log.syslog(message=f"Saving confusion matrix figure to {output_path}", verbose=True)
        plt.savefig(output_path, dpi=150)
        log.syslog(message=f"Saved confusion matrix figure to {output_path}", verbose=True)

    # plt.show()
    
    return confusion_matrix_





def format_run_summary(result: dict) -> str:
    columns = [
        (metricsEnum.ACCURACY, "Accuracy"),
        (metricsEnum.PRECISION, "Precision"),
        (metricsEnum.RECALL, "Recall"),
        (metricsEnum.F1, "F1"),
        (metricsEnum.ROC_AUC, "ROC-AUC"),
    ]

    def format_value(value) -> str:
        if isinstance(value, (int, float)):
            return f"{value:.2%}"
        return "—" if value in (None, "Not calculated") else str(value)

    def format_row(name: str, metrics: dict) -> str:
        values = [
            f"{format_value(metrics.get(key)):>11}"
            for key, _ in columns
        ]
        return f"{name:<22}" + "".join(values)

    header = f"{'Model':<22}" + "".join(
        f"{label:>11}" for _, label in columns
    )
    separator = "─" * len(header)

    lines = [
        "",
        "▶ VALIDATION — model comparison",
        header,
        separator,
    ]

    for name, metrics in result["validation_results"].items():
        lines.append(format_row(name, metrics))

    lines.extend([
        "",
        "▶ FINAL TEST — Logistic Regression",
        header,
        separator,
        format_row("Logistic Regression", result["test_results"]),
        "",
        f"✓ Saved model: {result['model_path']}",
    ])

    return "\n".join(lines)



def saveComparisonResultsGraph(comparison: dict):

    ax = comparison.plot(
        kind="bar",
        figsize=(10, 5),
        color=["steelblue", "coral", "seagreen"],
        rot=0,
    )

    ax.set_title("Model comparison on the validation set")
    ax.set_xlabel("Model")
    ax.set_ylabel("Score")
    ax.set_ylim(0, 1.15)
    ax.legend(title="Spam metrics")

    for container in ax.containers:
        ax.bar_label(container, fmt="%.3f", padding=3)

    fig = ax.figure
    fig.tight_layout()

    project_root = Path(__file__).resolve().parents[3]
    output_dir = project_root / "artifacts"
    output_dir.mkdir(parents=True, exist_ok=True)

    fig.savefig(
        output_dir / "model_comparison.png",
        dpi=300,
        bbox_inches="tight",
    )

    plt.close(fig)

