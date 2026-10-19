from __future__ import annotations

import csv
import tarfile
from email import policy
from email.parser import BytesParser
from pathlib import Path
from urllib.request import urlretrieve

import pandas as pd

from spam_filter import log


ARCHIVES = {
    "ham": {
        "url": (
            "https://spamassassin.apache.org/old/publiccorpus/"
            "20030228_easy_ham.tar.bz2"
        ),
        "path": Path("data/raw/20030228_easy_ham.tar.bz2"),
    },
    "spam": {
        "url": (
            "https://spamassassin.apache.org/old/publiccorpus/"
            "20030228_spam.tar.bz2"
        ),
        "path": Path("data/raw/20030228_spam.tar.bz2"),
    },
}

ARCHIVE_PATH = Path("data/raw/20030228_easy_ham.tar.bz2")
OUTPUT_PATH = Path("data/processed/emails.csv")


def download_archives() -> None:
    for label, archive_info in ARCHIVES.items():
        archive_path = archive_info["path"]
        archive_path.parent.mkdir(parents=True, exist_ok=True)

        if archive_path.exists():
            log.syslog(f"{label} archive already exists: {archive_path}")
            continue

        log.syslog(f"Downloading {label} archive...")
        urlretrieve(archive_info["url"], archive_path)
        log.syslog(f"Downloaded: {archive_path}")
        
    
def extract_text(message) -> str:
    """Extract plain text from an email."""

    if message.is_multipart():
        parts = []

        for part in message.walk():
            if part.get_content_type() == "text/plain":
                parts.append(part.get_content())

        return "\n".join(parts)

    if message.get_content_type() == "text/plain":
        return message.get_content()

    return ""


def parse_email(email_file) -> dict[str, str]:
    message = BytesParser(policy=policy.default).parse(email_file)

    subject = message["subject"] or ""
    body = extract_text(message)

    return {
        "subject": subject.strip(),
        "body": body.strip(),
    }




def build_dataset() -> list[dict[str, str]]:
    rows = []


    for label, archive_info in ARCHIVES.items():
        archive_path = archive_info["path"]

        with tarfile.open(archive_path, mode="r:bz2") as archive:
            for member in archive.getmembers():
                filename = Path(member.name).name

                if not member.isfile() or not filename[:5].isdigit():
                    continue

                email_file = archive.extractfile(member)

                if email_file is None:
                    continue

                try:
                    email_data = parse_email(email_file)

                    rows.append(
                        {
                            "filename": filename,
                            "subject": email_data["subject"],
                            "body": email_data["body"],
                            "label": label,
                        }
                    )
                except Exception as error:
                    log.syslog(f"Could not parse {member.name}: {error}")

    return rows
          




def save_csv(rows: list[dict[str, str]]) -> None:
    output_path = Path("data/processed/emails.csv")
    output_path.parent.mkdir(parents=True, exist_ok=True)

    dataframe = pd.DataFrame(rows)
    dataframe.to_csv(output_path, index=True, index_label="id")

    log.syslog(f"Saved {len(dataframe)} emails to {output_path}")


def downloadData() -> None:
    download_archives()
    rows = build_dataset()
    save_csv(rows)

    # spam_count = sum(row["label"] == "spam" for row in rows)
    # ham_count = sum(row["label"] == "ham" for row in rows)

    # log.syslog(f"Ham messages: {ham_count}")
    # log.syslog(f"Spam messages: {spam_count}")


# if __name__ == "__main__":
#     main()