# IPL Cricket Analytics

This project loads the IPL dataset from SQLite, performs a small analytics workflow, and produces the figures and summary report used in the project findings.

## Run the analysis

1. Create or activate a virtual environment.
2. Install the project dependencies:
   `pip install -r requirements.txt`
3. Run:
   `python src/ipl_cricket_analysis.py`

The script creates charts in `reports/figures/` and writes a summary to `reports/analysis_report.md`.