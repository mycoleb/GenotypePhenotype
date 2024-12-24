import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import json
from pathlib import Path
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class ExpressionVisualizer:
    def __init__(self):
        self.results_dir = Path("results/figures")
        self.results_dir.mkdir(parents=True, exist_ok=True)
        
    def load_expression_data(self, gene_name):
        """Load processed expression data for a gene"""
        try:
            data_path = Path(f"data/raw/{gene_name}_expression.json")
            with open(data_path, 'r') as f:
                return json.load(f)
        except Exception as e:
            logger.error(f"Failed to load data for {gene_name}: {e}")
            return None

    def plot_expression_density(self, gene_name):
        """Create a bar plot of expression density across brain structures"""
        data = self.load_expression_data(gene_name)
        if not data:
            return

        # Extract structure data
        structures_df = pd.DataFrame(data['structures'])
        
        # Sort by expression density
        structures_df = structures_df.sort_values('expression_density', ascending=False)
        
        # Create the plot
        plt.figure(figsize=(12, 6))
        sns.barplot(data=structures_df.head(20), 
                   y='structure_id',
                   x='expression_density')
        
        plt.title(f"Expression Density of {gene_name} Across Brain Structures")
        plt.xlabel("Expression Density")
        plt.ylabel("Structure ID")
        
        # Save the plot
        plt.tight_layout()
        plt.savefig(self.results_dir / f"{gene_name}_expression_density.png")
        plt.close()
        
    def plot_expression_comparison(self, gene_names):
        """Create a comparison plot of expression patterns between genes"""
        plt.figure(figsize=(12, 8))
        
        for gene in gene_names:
            data = self.load_expression_data(gene)
            if data:
                structures_df = pd.DataFrame(data['structures'])
                densities = structures_df['expression_density'].sort_values(ascending=False)
                plt.plot(densities.head(20), label=gene)
        
        plt.title("Expression Density Comparison Across Genes")
        plt.xlabel("Structure Rank")
        plt.ylabel("Expression Density")
        plt.legend()
        
        plt.tight_layout()
        plt.savefig(self.results_dir / "gene_expression_comparison.png")
        plt.close()

def main():
    visualizer = ExpressionVisualizer()
    
    # Test genes
    test_genes = ['APP', 'MAPT', 'SNCA']
    
    # Create individual plots
    for gene in test_genes:
        visualizer.plot_expression_density(gene)
        
    # Create comparison plot
    visualizer.plot_expression_comparison(test_genes)

if __name__ == "__main__":
    main()