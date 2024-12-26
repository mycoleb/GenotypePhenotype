# Spatial Gene Expression and Disease Susceptibility Analysis

## There are issues involving the API and other things out of my control (12/25/2024). I'll have to come back to this
## Project Overview
This project analyzes the relationship between spatial patterns of gene expression and disease susceptibility in the brain using Allen Brain Atlas data.

## Project Structure
```
brain_expression_project/
├── data/
│   ├── raw/          # For Allen Brain Atlas data
│   └── processed/    # For cleaned and processed data
├── src/
│   ├── __init__.py
│   ├── data_collection.py
│   ├── preprocessing.py
│   ├── analysis.py
│   └── visualization.py
├── notebooks/
│   └── exploratory_analysis.ipynb
├── results/
│   ├── figures/
│   └── tables/
├── requirements.txt
└── README.md
```

## Setup
1. Create and activate conda environment:
   ```bash
   conda create -n brain_expr python=3.10
   conda activate brain_expr
   ```

2. Install requirements:
   ```bash
   pip install -r requirements.txt
   ```

## Usage
[Add usage instructions here]
