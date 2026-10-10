1. Spam Email Classifier   [Beginner]
Tech Stack: Python, scikit-learn, NLTK, Pandas
Problem: Email spam costs enterprises $20.5 billion annually in productivity loss (Verizon DBIR, 2024). A classifier trained on the SpamAssassin or Enron dataset filters messages before they reach inboxes.

Approach: Load the SpamAssassin public corpus (6,000 emails). Tokenise using NLTK, remove stopwords, apply TF-IDF vectorization. Train a Naive Bayes, Logistic Regression, and SVM classifier. Compare F1 scores. Deploy as a Flask API that accepts email text and returns spam probability.

Outcome: Achieve 97%+ accuracy on the test set. Document precision, recall, and AUC-ROC curve in the README. Wrap in a Streamlit app for the demo.

GitHub Source Code: https://github.com/topics/spam-detection

Research Paper: Naive Bayes and SVM for Email Spam Classification (IEEE, 2023)