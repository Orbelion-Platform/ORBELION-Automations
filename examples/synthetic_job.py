"""Standalone synthetic illustration; no external systems."""
import json


def count_records(records: int = 3) -> dict:
    if type(records) is not int or not 0 <= records <= 10000:
        raise ValueError("records must be an integer between 0 and 10000")
    return {"status": "success", "records_processed": records}


if __name__ == "__main__":
    print(json.dumps(count_records()))
