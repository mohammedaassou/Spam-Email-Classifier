from pathlib import Path

import joblib
from matplotlib import pyplot as plt
import pandas as pd

from sklearn.metrics import RocCurveDisplay
from sklearn.pipeline import Pipeline

from spam_filter import log
# from spam_filter.modeling.split import DataSplits
from spam_filter.modeling.utils import calc_metrics, customer_confusion_matrix, metricsEnum


def evaluate_model(modelpath : Path, X_test: pd.Series, y_test:  pd.Series,  artifactpath : Path , verbose  = True) :

    model : Pipeline= joblib.load(modelpath)

    # print(confusion_matrix(y_test, model.predict(X_test)))
    predictions = model.predict(X_test)

    spam_column = list(model.classes_).index(1)
    spam_probabilities = model.predict_proba(X_test)[:, spam_column]

    metrics = calc_metrics(y_pred=predictions , y_true=y_test, spam_scores=spam_probabilities)


    log.syslog(message=f"Accuracy: {metrics[metricsEnum.ACCURACY]}", verbose =verbose )
    log.syslog(message=f"Precision: {metrics[metricsEnum.PRECISION]}", verbose = verbose)
    log.syslog(message=f"Recall: {metrics[metricsEnum.RECALL]}", verbose = verbose)
    log.syslog(message=f"F1: {metrics[metricsEnum.F1]}", verbose = verbose)
    



    log.syslog(f"Confusion matrix{customer_confusion_matrix(predictions= predictions, y_test= y_test, title="Final model Test - logistic regression", saveFigure=True)}",)


    artifactpath.mkdir(parents=True, exist_ok=True)
    figure, axis = plt.subplots()
    RocCurveDisplay.from_predictions(
        y_test,
        spam_probabilities,
        pos_label=1,
        ax=axis,
        name="Logistic Regression",
    )
    figure.savefig(artifactpath / "roc_curve.png", bbox_inches="tight")
    plt.close(figure)

    return metrics


