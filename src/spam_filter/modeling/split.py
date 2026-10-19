
from dataclasses import dataclass
from tkinter import Y

import pandas as pd
from sklearn.model_selection import train_test_split

from spam_filter import log
from spam_filter.data.cleaning import EmailColumn


@dataclass

class DataSplits:

    X_fit: pd.Series
    X_val: pd.Series
    X_train: pd.Series
    X_test: pd.Series

    y_fit: pd.Series
    y_val: pd.Series
    y_train: pd.Series
    y_test: pd.Series




def split_dataset(df: pd.DataFrame, verbose = False) -> DataSplits:

    X = df[EmailColumn.TEXT]
    y = df[EmailColumn.TARGET]

        # TODO : need to understand stratify=y
        
    X_train, X_test , y_train, y_test = train_test_split(X,y , random_state=1, test_size=0.2, stratify=y)
    
    
    X_fit , X_val , y_fit , y_val = train_test_split(X_train, y_train , random_state=1, test_size=0.2, stratify=y_train)
        
    log.syslog(message=f"Training rows: {len(X_train)}", verbose=verbose)
    log.syslog(message=f"Test rows: {len(X_test)}", verbose=verbose)
    log.syslog(message=f"Training labels: {y_train.value_counts()}", verbose=verbose)
    log.syslog(message=f"Test labels: {y_test.value_counts()}", verbose=verbose)
    
    log.syslog(message=f"Fiting rows: {len(X_fit)}", verbose=verbose)
    log.syslog(message=f"Validating rows: {len(X_val)}", verbose=verbose)
    log.syslog(message=f"Validating labels: {y_val.value_counts()}", verbose=verbose)

    return DataSplits( X_fit = X_fit, X_val = X_val, X_train = X_train ,X_test = X_test,   y_fit = y_fit, y_val = y_val,  y_train = y_train, y_test = y_test)
    

