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
        query = f"query.json?criteria=model::Gene,rma::criteria,[acronym'{gene_name}'],products[id]"
        response = requests.get(self.base_url + query)
        return response.json()

if __name__ == "__main__":
    print("Data collection module initialized")
