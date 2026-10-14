

from enum import StrEnum
from pathlib import Path

import pandas as pd
from sklearn.preprocessing import LabelEncoder 




# id,filename,subject,body,label



class EmailColumn(StrEnum):
    FILENAME = "filename"
    SUBJECT = "subject"
    BODY = "body"
    LABEL = "label"
    TEXT = "text"
    TARGET = "target"


REQUIRED_COLUMNS = [
    EmailColumn.FILENAME,
    EmailColumn.SUBJECT,
    EmailColumn.BODY,
    EmailColumn.LABEL,
]


def clean_dataset(df : pd.DataFrame) -> pd.DataFrame:
     
    df.head()
    
    
    print(df.columns )
    
    allcols =  df.columns 
    
    
    mssingCols = set(REQUIRED_COLUMNS) - set(allcols) 
    
    
    print("mssingCols : ", mssingCols)
    
    
    
    if mssingCols:
        print("cols missing")
        return
    
    
    
    cleaned_data = df.copy()
    
    
    # Remplace all none subject,body with empty str
    cleaned_data[EmailColumn.SUBJECT] = cleaned_data[EmailColumn.SUBJECT].fillna("").astype(str)
    cleaned_data[EmailColumn.BODY] = cleaned_data[EmailColumn.BODY].fillna("").astype(str)
    
    # make upper case "SPAM" to "spam" and remove spaces
    cleaned_data[EmailColumn.LABEL] = cleaned_data[EmailColumn.LABEL].str.lower().str.strip()
    
    
    
    # duplications
    # print("duplication : ",cleaned_data.duplicated().sum())
    
    email_cols = [EmailColumn.SUBJECT, EmailColumn.BODY]
    
    duplicate_count = cleaned_data.duplicated(subset=email_cols).sum()
    
    conflicting_labels = (
        cleaned_data.groupby(email_cols)[EmailColumn.LABEL]. nunique().gt(1).sum()
        
    
    )
    print("Duplicate emails:", duplicate_count)
    print("Emails with conflicting labels:", conflicting_labels)
    
    if conflicting_labels:
        raise ValueError("Identical emails have different labels.")
    
    cleaned_data = cleaned_data.drop_duplicates(subset=email_cols)

    cleaned_data[EmailColumn.TEXT] = (
    "subject: " + cleaned_data[EmailColumn.SUBJECT]
    + "\nbody: " + cleaned_data[EmailColumn.BODY]
    
    )
    
    
    
    labelEconder = LabelEncoder()
    
    cleaned_data[EmailColumn.TARGET] = labelEconder.fit_transform(cleaned_data[EmailColumn.LABEL])
    
    

    print("Label order:", labelEconder.classes_)
    return cleaned_data.reset_index(drop=True)


def main() -> None:
    data_path = Path("data/processed/emails.csv")
    df = pd.read_csv(data_path)

    cleaned_data = clean_dataset(df)

    print("Before:", len(df))
    print("After:", len(cleaned_data))
    print(cleaned_data[EmailColumn.TARGET].value_counts())


if __name__ == "__main__":
    main()
    
    