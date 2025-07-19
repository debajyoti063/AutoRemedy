import csv
from agentic.base import Sensor

def map_status(level):
    level = level.lower()
    # Portuguese log levels and mappings with escalation
    if level.startswith("fatal") or level.startswith("emergência") or level.startswith("emergencia") or level.startswith("crítico") or level.startswith("critico"):
        return "escalate"
    elif level.startswith("erro"):
        return "fail"
    elif level.startswith("alerta"):
        return "warning"
    elif level.startswith("aviso"):
        return "warning"
    elif level.startswith("debug"):
        return "debug"
    elif level.startswith("trace"):
        return "trace"
    elif level.startswith("informações"):
        return "success"
    else:
        return "info"

class KaggleCSVSensor(Sensor):
    def __init__(self, csv_file):
        self.rows = list(csv.DictReader(open(csv_file, encoding="utf-8")))
        self.index = 0

    def get_event(self):
        if self.index < len(self.rows):
            row = self.rows[self.index]
            self.index += 1
            status = map_status(row["Nível"])
            event = {
                "job_id": row.get("Identificação do Evento", self.index),
                "status": status,
                "event_type": "job_issue",
                "details": {
                    "timestamp": row.get("Data e Hora"),
                    "source": row.get("Fonte"),
                    "description": row.get("Description1", "")
                }
            }
            # Add escalation flag for critical/fatal/emergency
            if status == "escalate":
                event["escalate"] = True
            return event
        return None 