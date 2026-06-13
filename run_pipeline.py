
"""
Master execution pipeline for Bluestock Mutual Fund Analytics Project
Runs all steps: data cleaning, EDA, performance analytics, advanced analytics
"""
import subprocess
import sys
from pathlib import Path


def run_step(step_name: str, script_path: Path, cwd: Path = None):
    """Run a single pipeline step"""
    print(f"\n{'='*60}")
    print(f"Running: {step_name}")
    print(f"{'='*60}")
    try:
        result = subprocess.run(
            [sys.executable, str(script_path)],
            cwd=str(cwd) if cwd else None,
            check=True,
            capture_output=False,
            text=True
        )
        print(f"\n✅ {step_name} completed successfully!")
        return True
    except subprocess.CalledProcessError as e:
        print(f"\n❌ {step_name} failed with error: {e}")
        return False


def main():
    project_root = Path(__file__).resolve().parent
    notebooks_dir = project_root / "notebooks"

    print("\n" + "="*60)
    print("Bluestock Mutual Fund Analytics - Pipeline")
    print("="*60)

    # Step 1: Clean and load data
    if not run_step("Data Cleaning & DB Loading", project_root / "clean_and_load_data.py"):
        return

    # Step 2: Build EDA notebook
    if not run_step("Build EDA Notebook", notebooks_dir / "build_eda_notebook.py"):
        return

    # Step 3: Run EDA analysis
    if not run_step("Run EDA Analysis", notebooks_dir / "run_eda.py", cwd=notebooks_dir):
        return

    # Step 4: Build Performance Analytics notebook
    if not run_step("Build Performance Analytics Notebook", notebooks_dir / "build_performance_notebook.py"):
        return

    # Step 5: Run Performance Analytics
    if not run_step("Run Performance Analytics", notebooks_dir / "run_performance.py", cwd=notebooks_dir):
        return

    # Step 6: Build Advanced Analytics notebook
    if not run_step("Build Advanced Analytics Notebook", notebooks_dir / "build_advanced_notebook.py"):
        return

    # Step 7: Run Advanced Analytics
    if not run_step("Run Advanced Analytics", notebooks_dir / "run_advanced.py", cwd=notebooks_dir):
        return

    print("\n" + "="*60)
    print("✅ All pipeline steps completed successfully!")
    print("="*60)
    print("\nDeliverables Summary:")
    print("- Cleaned data in data/processed/")
    print("- SQLite database: bluestock_mf.db")
    print("- EDA charts in reports/eda_charts/")
    print("- Notebooks: notebooks/EDA_Analytics.ipynb, notebooks/Performance_Analytics.ipynb, notebooks/Advanced_Analytics.ipynb")
    print("- Fund scorecard: fund_scorecard.csv")
    print("- Alpha/beta data: alpha_beta.csv")
    print("- VaR/CVaR report: var_cvar_report.csv")


if __name__ == "__main__":
    main()
