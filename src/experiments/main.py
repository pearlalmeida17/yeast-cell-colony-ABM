from src.simulation.engine import run

if __name__ == "__main__":
    cells, lineage, run_id = run(seed=1, checkpoint_interval=60.0)
    print(f"Run ID: {run_id}")
    print(f"Final cell count: {len(cells)}")
