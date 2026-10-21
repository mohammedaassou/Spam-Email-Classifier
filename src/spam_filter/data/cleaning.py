

from enum import StrEnum
from pathlib import Path
import re
import string

import pandas as pd
from sklearn.preprocessing import LabelEncoder

from spam_filter import log


from nltk.stem import PorterStemmer

import nltk

from nltk.corpus import stopwords


nltk.download("stopwords")


STOP_WORDS = set(stopwords.words("english") )

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


# return dict of Unicode of special caracteres
ponctuations = str.maketrans("", "", string.punctuation)

stemmer = PorterStemmer()

def clean_text(text: str):
    # make the text lowercase
    text = text.lower()
    # remove ponctuations
    text = text.translate( ponctuations )
    # remove numbers 
    text = re.sub(r"\d+" , "" , text)
    # remove stop words
    words = text.split()

    words = [word for word in words if word not in STOP_WORDS]
    # stemming
    textStemmer = [stemmer.stem(word ) for word in words]

    text = " ".join(textStemmer)

    return text







def build_email_text(subject: str, body: str) -> str:
    return f"{subject}\n{body}"

def clean_dataset(df : pd.DataFrame, verbose = False) -> pd.DataFrame:
     
    log.syslog(message="Cleaning dataset...", verbose=verbose)  
    log.syslog(message="First few rows of the dataset:", verbose=verbose)
    # log.syslog(message= df.head(), verbose=verbose)
    
    log.syslog(message= f"Columns: {df.columns}", verbose=verbose)
    
    allcols =  df.columns 
    
    
    mssingCols = set(REQUIRED_COLUMNS) - set(allcols) 
    
    
    log.syslog(message= f"mssingCols : {mssingCols}", verbose=verbose , level=log.WARNING)
    
    
    
    if mssingCols:
        log.syslog(message="cols missing", verbose=verbose , level=log.ERROR)
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
    log.syslog(message= f"Duplicate emails:{duplicate_count}", verbose= verbose)
    log.syslog(message= f"Emails with conflicting labels:{conflicting_labels}", verbose= verbose)
    
    if conflicting_labels :
        log.syslog(message="Identical emails have different labels.", verbose=verbose , level=log.ERROR)
        raise ValueError("Identical emails have different labels.")
    
    cleaned_data = cleaned_data.drop_duplicates(subset=email_cols)

    cleaned_data[EmailColumn.TEXT] = (
    "subject: " + cleaned_data[EmailColumn.SUBJECT]
    + "\nbody: " + cleaned_data[EmailColumn.BODY]
    
    )


    cleaned_data[EmailColumn.TEXT] = cleaned_data[EmailColumn.TEXT].apply(clean_text)



    # short_emails = cleaned_data[cleaned_data[EmailColumn.TEXT].fillna("").str.split().str.len() < 20]

    # print(f"Short emails: {len(short_emails)}")
    # # print(short_emails[[EmailColumn.TEXT, EmailColumn.LABEL]].to_string(index=False))
    # Show the 10 shortest emails by word count
    
    labelEconder = LabelEncoder()
    
    cleaned_data[EmailColumn.TARGET] = labelEconder.fit_transform(cleaned_data[EmailColumn.LABEL])
    
    label_mapping = {
    label: index
    for index, label in enumerate(labelEconder.classes_)
}

    log.syslog(message=f"Label mapping: {label_mapping}", verbose=verbose)

    if label_mapping != {"ham": 0, "spam": 1}:
        raise ValueError(f"Unexpected label mapping: {label_mapping}", verbose)
    
    log.syslog( message= f"Label order: {labelEconder.classes_}", verbose=verbose)
    return cleaned_data.reset_index(drop=True)


def main() -> None:
    data_path = Path("data/processed/emails.csv")
    df = pd.read_csv(data_path)

    cleaned_data = clean_dataset(df, verbose=True)

    # log.syslog(f"cleaned_data.target : {cleaned_data[["text"]]}")

    log.syslog( message= f"Before:{len(df)}"  )
    log.syslog(message= f"After:{len(cleaned_data)}", verbose=True)
    log.syslog(message= f"Target value counts: {cleaned_data[EmailColumn.TARGET].value_counts()}", verbose=True)



if __name__ == "__main__":
    main()
    
    