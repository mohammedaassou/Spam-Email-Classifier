



from sklearn.linear_model import LogisticRegression
from sklearn.metrics import classification_report



from spam_filter import log


from sklearn.dummy import DummyClassifier


from sklearn.naive_bayes import MultinomialNB

# TODO understand MultinomialNB

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.pipeline import make_pipeline

from spam_filter.modeling.split import DataSplits
from spam_filter.modeling.utils import calc_metrics, customer_confusion_matrix, metricsEnum


from sklearn.svm import LinearSVC

def training(splits: DataSplits,  verbose = False):
    
    X_fit = splits.X_fit
    X_val = splits.X_val
    y_fit = splits.y_fit
    y_val = splits.y_val
    # X_train = splits.X_train
    # X_test = splits.X_test

    modelbaseline = DummyClassifier(strategy="most_frequent")
    
    vectorizer = TfidfVectorizer()
    modelNB = make_pipeline(
        vectorizer,
        MultinomialNB()
    )
    modelLogistic_reg = make_pipeline(
            vectorizer,
            LogisticRegression(
                class_weight="balanced" , max_iter=1000
            )
        )

    svm_model = make_pipeline(
        vectorizer,
        LinearSVC(class_weight="balanced" , max_iter=1000)
    )
        

    models = {
        "DummyClassifier" : modelbaseline, 
        "Naive bayes" : modelNB,
        "logistic regression" : modelLogistic_reg,
        "SVM" : svm_model
    
    } 

    result = {}

    for name , model in models.items():


        # log.syslog(f"▶ Training {name}")

        model.fit(X_fit , y_fit)

        predictions = model.predict(X_val)






        metrics = calc_metrics(y_pred=predictions, y_true=y_val)

        result[name] = metrics

        # log.syslog(message=f"{name} - Accuracy: {metrics[metricsEnum.ACCURACY]}", verbose=verbose)
        # log.syslog(message=f"{name} - Precision: {metrics[metricsEnum.PRECISION]}", verbose=verbose)
        # log.syslog(message=f"{name} - Recall: {metrics[metricsEnum.RECALL]}", verbose=verbose)
        # log.syslog(message=f"{name} - F1: {metrics[metricsEnum.F1]}", verbose=verbose)

        log.syslog(
            f"{name} confusion matrix:\n"
            f"{customer_confusion_matrix(y_test=y_val, predictions=predictions, title=f'{name} Confusion Matrix', saveFigure=True)}"
        )


        # log.syslog(
        #     f"{name} classification report:\n"
        #     + classification_report(

        #         y_true=y_val,
        #         y_pred=predictions,
        #         labels=[0, 1],
        #         target_names=["ham", "spam"],
        #         zero_division=0,
        #     )
        #      , verbose)

    return result




def fit_final_model(splits: DataSplits, verbose = False):


    x_train = splits.X_train
    # x_test = splits.X_test
    y_train = splits.y_train
    # y_test = splits.y_test


    # final model is Logistic reg, cuz the recall is higher : does not let spam emails go to ham 
    final_model = make_pipeline(
        TfidfVectorizer(),
        LogisticRegression(
            class_weight="balanced" , max_iter=1000
        )
    )
    final_model.fit(x_train, y_train)

    return final_model


