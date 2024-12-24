import requests
import pandas as pd
import json
from pathlib import Path
import logging

# Set up logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

class AllenBrainAtlasAPI:
    def __init__(self):
        self.base_url = "https://api.brain-map.org/api/v2/"
        self.data_dir = Path("data/raw")
        self.data_dir.mkdir(parents=True, exist_ok=True)

    def test_connection(self):
        """Test the connection to the Allen Brain Atlas API"""
        try:
            response = requests.get(self.base_url + "structure_graph_download/1.json")
            response.raise_for_status()
            logger.info("Successfully connected to Allen Brain Atlas API")
            return True
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to connect to Allen Brain Atlas API: {e}")
            return False

    def fetch_gene_info(self, gene_name):
        """
        Fetch basic information about a gene
        """
        try:
            # Simplified query for the Gene model
            query = f"data/Gene/query.json?criteria=[acronym$eq'{gene_name}']"
            response = requests.get(self.base_url + query)
            response.raise_for_status()
            data = response.json()

            # Check if 'msg' contains data
            if not data.get('msg'):
                logger.warning(f"No data found for gene {gene_name}")
                return None

            logger.info(f"Successfully fetched data for gene {gene_name}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch data for gene {gene_name}: {e}")
            return None


    def save_data(self, data, filename):
        """Save data to JSON file"""
        try:
            output_file = self.data_dir / filename
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Successfully saved data to {output_file}")
        except Exception as e:
            logger.error(f"Failed to save data: {e}")

def main():
    # Initialize API client
    api = AllenBrainAtlasAPI()

    # Test connection
    if not api.test_connection():
        logger.error("Exiting due to connection failure")
        return

    # Test with a few important genes related to neurodegenerative diseases
    test_genes = ['APP', 'MAPT', 'SNCA']

    for gene in test_genes:
        logger.info(f"Fetching data for {gene}...")
        gene_data = api.fetch_gene_info(gene)

        if gene_data:
            api.save_data(gene_data, f"{gene}_info.json")

            # Print some basic information about the gene
            if gene_data.get('msg'):
                for item in gene_data['msg']:
                    print(f"\nGene: {gene}")
                    print(f"Name: {item.get('gene_symbol', 'N/A')}")
                    print(f"Entrez ID: {item.get('entrez_id', 'N/A')}")
                    print(f"Chromosome: {item.get('chromosome_id', 'N/A')}")

print("'test_connection.py' ran successfully")

if __name__ == "__main__":
    main()
