from pathlib import Path

import joblib
from sklearn.pipeline import Pipeline

from spam_filter import log
from spam_filter.data.cleaning import build_email_text


def load_model(model_path: Path):
    return joblib.load(model_path)



def predict_email(modelpath: Path, subject: str, body: str) -> int:
    text = build_email_text(subject, body)

    model: Pipeline = load_model(modelpath)

    # print("Textes différents :", data[EmailColumn.TEXT].nunique())
    # print("Modèle sauvegardé :", type(model.steps[-1][1]).__name__)
    # print(confusion_matrix(y_test, model.predict(X_test)))  

    # log.syslog([type(step).__name__ for _, step in model.steps], )
    # log.syslog(model.classes_)

    return int(model.predict([text])[0])


# def predict_email(modelpath, subject: str, body: str) -> dict:
#     text = build_email_text(subject, body)

#     model : Pipeline= load_model(modelpath)

#     # log.syslog(type(model))

#     result = model.predict([text])

#     # print(result)

#     # spam_index = list(model.classes_).index(1)
#     # spam_probability = float(model.predict([text])[0, spam_index])

#     return {
#         "label" : "spam" if result is 1 else "ham",
#         "spam_probability" : result * 100
#     }

#     # return {
#     #     "label": "spam" if result >= 0.5 else "ham",
#     #     "spam_probability": result,
#     # }


if __name__ == "__main__":
    PROJECT_ROOT = Path(__file__).resolve().parents[3]

    model_path = PROJECT_ROOT / "artifacts" / "spam_classifier.joblib"

    # predict_email(PROJECT_ROOT / "artifacts" / "spam_classifier.joblib", "test" , "give me your bank number")

    # predict_email(PROJECT_ROOT / "artifacts" / "spam_classifier.joblib", "test", "give me your bank number hhhhhh ")

    test_emails = [
    ("spam", "Important notice about your account",
     """Dear customer,

We have noticed unusual activity on your account. For your protection,
access has been temporarily limited. Please confirm your account details
within the next 24 hours to avoid a permanent suspension.

Open the verification page and enter your username, password, and payment
information. Once verification is complete, you will receive a confirmation
message and full access will be restored.

Please do not reply to this email. Our support team cannot process account
verification by email.

Customer Security Department"""),

    ("spam", "Special offer available until Friday",
     """Hello,

You have been selected to receive an exclusive discount on our products.
For a limited time, you can order at 80 percent below the regular price.
This offer is available only to the first customers who respond.

Visit our order page today and provide your delivery and payment details
to reserve your purchase. If you order more than one item, shipping is
free. Do not wait until the end of the week, because the discount will
expire and cannot be renewed.

Best regards,
Sales Team"""),

    ("ham", "Notes from yesterday's project meeting",
     """Hi everyone,

Thank you for joining the project meeting yesterday. We agreed to finish
the data review before Wednesday and to share the revised document with
the team on Thursday. Sarah will update the diagrams, and I will check
the figures in the final section.

I have added my meeting notes to the shared folder. Please read them
when you have time and let me know if I missed any decisions. We can
discuss remaining questions during our regular meeting next Monday.

Thanks,
Alex"""),

    ("ham", "Re: Problem with the search window",
     """Hi Chris,

I tried to reproduce the issue you described with the search window.
The first search completed normally, but the second attempt displayed
an error after I selected several messages. I have attached the command
output and noted the steps I followed.

Could you confirm which version of the application you are using? I
would also like to know whether the error appears when you search a
different folder. I will continue checking the logs this afternoon and
send an update when I find the cause.

Regards,
Martin"""),

    ("ham", "Family visit this weekend",
     """Hi Mom,

I booked my train ticket for Saturday and should arrive at the station
around three in the afternoon. I will call you when the train leaves so
you know whether it is running on time.

I can help with the shopping after I arrive. Please tell me if there is
anything you would like me to bring from the city. On Sunday, we could
have lunch together and visit Grandma before I travel back in the
evening.

See you soon,
Sam"""),
]

    for expected, subject, body in test_emails:
        predicted = predict_email(model_path, subject, body)
        expected_number = 1 if expected == "spam" else 0

        print(f"Expected: {expected_number} | Predicted: {predicted} | {subject}")

    