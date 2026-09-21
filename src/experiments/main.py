from src.simulation.engine import run

if __name__ == "__main__":
    cells, lineage = run()
    print(f"Final cell count: {len(cells)}")
