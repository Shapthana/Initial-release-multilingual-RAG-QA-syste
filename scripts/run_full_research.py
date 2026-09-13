from pathlib import Path
import subprocess,sys
ROOT=Path(__file__).resolve().parents[1]
def run(script,*args):
    cmd=[sys.executable,str(ROOT/"scripts"/script),*args]; print("\n>>>"," ".join(cmd)); subprocess.run(cmd,cwd=ROOT,check=True)
if __name__=="__main__":
    run("ingest.py")
    run("validate_evaluation.py")
    run("enrich_evaluation.py")
    run("evaluate.py","--output","data/results/retrieval_benchmark.json")
    run("failure_analysis.py")
    print("\nCore retrieval research pipeline completed. Generation evaluation is optional and requires an LLM endpoint:")
    print("python scripts/evaluate_generation.py")
