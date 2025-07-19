import csv
import requests

API_URL = "http://localhost:8000/event"
CSV_FILE = "C:/Users/91913/Downloads/archive/eventos.csv"

with open(CSV_FILE, encoding="utf-8") as f:
    reader = csv.DictReader(f)
    for idx, row in enumerate(reader):
        status = "fail" if row["Nível"].lower().startswith("erro") else "success"
        event = {
            "job_id": row.get("Identificação do Evento", idx + 1),
            "status": status,
            "event_type": "job_issue",
            "details": {
                "timestamp": row.get("Data e Hora"),
                "source": row.get("Fonte"),
                "description": row.get("Description1", "")
            }
        }
        r = requests.post(API_URL, json=event)
        print(f"Posted event {event['job_id']}: {r.status_code}") 