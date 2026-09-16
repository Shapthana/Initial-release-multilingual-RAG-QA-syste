from pathlib import Path
import csv, json, datetime

ROOT=Path(__file__).resolve().parents[1]
OUT=ROOT.parent/"experiments"/"experiment_log.csv"

def save_experiment(experiment_name, model, method, metrics, parameters=None):
    OUT.parent.mkdir(parents=True,exist_ok=True)
    exists=OUT.exists()
    with OUT.open("a",newline="",encoding="utf-8") as f:
        fields=["timestamp","experiment_name","model","method","parameters","metrics"]
        w=csv.DictWriter(f,fieldnames=fields)
        if not exists:w.writeheader()
        w.writerow({"timestamp":datetime.datetime.now(datetime.timezone.utc).isoformat(),"experiment_name":experiment_name,"model":model,"method":method,"parameters":json.dumps(parameters or {},ensure_ascii=False),"metrics":json.dumps(metrics,ensure_ascii=False)})
    print(f"Saved measured experiment to {OUT}")

if __name__=="__main__":
    print("This helper records measured results only. It intentionally contains no example benchmark numbers.")
    print("Run scripts/evaluate.py first, then record its generated values explicitly if you need a separate experiment log.")
