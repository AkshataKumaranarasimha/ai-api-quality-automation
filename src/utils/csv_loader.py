import csv
from pathlib import Path

def load_csv_test_cases(path: str) -> list[dict]:
    p = Path(path)
    with p.open("r", newline="", encoding="utf-8") as f:
        return list(csv.DictReader(f))

'''
print("CSV test cases loaded successfully.")
path = "data/test_cases.csv"
test_cases = load_csv_test_cases(path)
for i, test_case in enumerate(test_cases, start=1):
    print(f"Test Case {i}: {test_case}")
print(f"Loaded {len(test_cases)} test cases from {path}.")  

'''