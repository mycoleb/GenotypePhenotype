

# Create Python files in src
touch src/__init__.py
touch src/data_collection.py
touch src/preprocessing.py
touch src/analysis.py
touch src/visualization.py

# Create Jupyter notebook for exploratory analysis
touch notebooks/exploratory_analysis.ipynb

# Create requirements.txt
cat > requirements.txt << EOF
numpy
pandas
matplotlib
seaborn
nibabel
nilearn
statsmodels
scipy
requests
jupyter
EOF

# Create README.md with project structure and description
cat > README.md << EOF
# Spatial Gene Expression and Disease Susceptibility Analysis

## Project Overview
This project analyzes the relationship between spatial patterns of gene expression and disease susceptibility in the brain using Allen Brain Atlas data.

## Project Structure
\`\`\`
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
\`\`\`

## Setup
1. Create and activate conda environment:
   \`\`\`bash
   conda create -n brain_expr python=3.10
   conda activate brain_expr
   \`\`\`

2. Install requirements:
   \`\`\`bash
   pip install -r requirements.txt
   \`\`\`

## Usage
[Add usage instructions here]
EOF

# Initialize git repository
git init

# Create .gitignore
cat > .gitignore << EOF
# Python
__pycache__/
*.py[cod]
*$py.class
.Python
*.so

# Distribution / packaging
dist/
build/
*.egg-info/

# Virtual environments
venv/
ENV/

# Jupyter Notebook
.ipynb_checkpoints

# Data files
data/

# IDE specific files
.idea/
.vscode/
*.swp
*.swo

# OS specific files
.DS_Store
Thumbs.db
EOF

# Add initial data collection script
cat > src/data_collection.py << EOF
import requests
import pandas as pd
import json
from pathlib import Path

class AllenBrainAtlasAPI:
    def __init__(self):
        self.base_url = "https://api.brain-map.org/api/v2/"
        self.data_dir = Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def fetch_gene_expression(self, gene_name):
        """
        Fetch gene expression data for a specific gene
        """
        query = f"query.json?criteria=model::Gene,rma::criteria,[acronym$eq'{gene_name}'],products[id$eq1]"
        response = requests.get(self.base_url + query)
        return response.json()

if __name__ == "__main__":
    print("Data collection module initialized")
EOF

# Make the script executable
chmod +x src/*.py

echo "Project structure created successfully!"
echo "Next steps:"
echo "1. Create and activate conda environment: conda create -n brain_expr python=3.10"
echo "2. Install requirements: pip install -r requirements.txt"
echo "3. Begin development!"