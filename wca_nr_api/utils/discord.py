# Python dependencies
import os
import time

# External dependencies
import requests

# Project dependencies
from wca_nr_api.classes.gender import Gender
from wca_nr_api.classes.record import Record
from wca_nr_api.classes.result_type import ResultType
from wca_nr_api.config.logger import logger


def send_record_announcement(record: Record) -> None:
    """
    Sends a message to Discord in the form of an announcement. Tries 3 times in case rate is limited.

    :param record: (Record) The new national record, which is announced.
    """

    webhook_url = os.environ["WEBHOOK_URL"]
    role_id = os.environ["ROLE_ID"]

    # Generate message content based on the record
    content = (f"**<@&{role_id}>**, поздравете "
               f"**[{record.name}](https://www.worldcubeassociation.org/persons/{record.person_id})** :flag_bg:,\n"
               f"{"който" if record.gender == Gender.MALE else "която" } постави нов национален рекорд за "
               f"{"най-добро" if record.result_type == ResultType.SINGLE else "средно"} време "
               f"в дисциплината **{record.event.readable_name()}** - **{record.readable_result()}** 🎉")
    data = {
        "username": "NR Bot",
        "content": content,
        "allowed_mentions": {"roles": [role_id]}
    }

    # Try 3 times
    for _ in range(3):
        response = requests.post(webhook_url, json=data)

        if response.status_code == 204:
            logger.info("Discord message sent successfully!")
            return
        elif response.status_code == 429:  # Rate limited
            retry_after = response.json().get("retry_after", 1)
            logger.warning(f"Rate limited! Retrying in {retry_after} seconds...")
            time.sleep(retry_after)
        else:
            raise Exception(f"Failed to send message: {response.status_code}, {response.text}")
