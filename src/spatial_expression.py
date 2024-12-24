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

    def save_data(self, data, filename):
        """Save data to JSON file"""
        try:
            output_file = self.data_dir / filename
            with open(output_file, 'w') as f:
                json.dump(data, f, indent=2)
            logger.info(f"Successfully saved data to {output_file}")
        except Exception as e:
            logger.error(f"Failed to save data: {e}")

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
            query = f"data/Gene/query.json?criteria=[acronym$eq'{gene_name}']"
            response = requests.get(self.base_url + query)
            response.raise_for_status()
            data = response.json()

            if not data.get('msg'):
                logger.warning(f"No data found for gene {gene_name}")
                return None

            logger.info(f"Successfully fetched data for gene {gene_name}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch data for gene {gene_name}: {e}")
            return None

    def fetch_expression_data(self, gene_id):
        try:
            query = f"data/SectionDataSet/query.json?criteria=genes[id$eq{gene_id}]"
            response = requests.get(self.base_url + query)
            response.raise_for_status()
            data = response.json()
            
            # Debug print
            print(f"\nDebug - Initial response for gene ID {gene_id}:")
            print(json.dumps(data, indent=2))

            if not data.get('msg') or len(data['msg']) == 0:
                logger.warning(f"No expression data found for gene ID {gene_id}")
                return None

            experiment_id = data['msg'][0]['id']
            logger.info(f"Found experiment ID: {experiment_id}")

            expression_query = f"data/SectionDataSet/{experiment_id}.json"
            expression_response = requests.get(self.base_url + expression_query)
            expression_response.raise_for_status()
            expression_data = expression_response.json()
            
            # Debug print
            print("\nDebug - Expression data response:")
            print(json.dumps(expression_data, indent=2))
            
            return expression_data

        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch expression data: {e}")
            return None
        except (KeyError, IndexError) as e:
            logger.error(f"Error parsing response data: {e}")
            return None        
    def fetch_structure_data(self, structure_id):
        """
        Fetch information about brain structures
        """
        try:
            query = f"data/Structure/{structure_id}.json"
            response = requests.get(self.base_url + query)
            response.raise_for_status()
            data = response.json()
            logger.info(f"Successfully fetched structure data for ID {structure_id}")
            return data
        except requests.exceptions.RequestException as e:
            logger.error(f"Failed to fetch structure data: {e}")
            return None

    def process_expression_data(self, expression_data):
        """
        Process raw expression data into a more usable format
        """
        try:
            if not expression_data or not isinstance(expression_data, dict) or 'msg' not in expression_data:
                logger.warning("Invalid expression data format")
                return None

            # Log the structure of the data for debugging
            logger.debug(f"Expression data structure: {json.dumps(expression_data, indent=2)}")

            # Extract relevant information
            processed_data = {
                'experiment_id': None,
                'gene_name': None,
                'expression_level': None,
                'structures': []
            }

            msg = expression_data.get('msg', {})
            if isinstance(msg, list) and len(msg) > 0:
                msg = msg[0]  # Take the first item if it's a list

            # Update basic information
            processed_data.update({
                'experiment_id': msg.get('id'),
                'gene_name': msg.get('gene'),
                'expression_level': msg.get('expression_level')
            })

            # Process structure-specific expression
            structures = msg.get('structure_unionizes', [])
            for structure in structures:
                if isinstance(structure, dict):
                    structure_info = {
                        'structure_id': structure.get('structure_id'),
                        'expression_density': structure.get('expression_density'),
                        'expression_energy': structure.get('expression_energy'),
                        'volume': structure.get('volume')
                    }
                    processed_data['structures'].append(structure_info)

            return processed_data

        except Exception as e:
            logger.error(f"Failed to process expression data: {e}")
            logger.debug(f"Raw expression data: {expression_data}")
            return None
def main():
    # Initialize API client
    api = AllenBrainAtlasAPI()

    if not api.test_connection():
        logger.error("Exiting due to connection failure")
        return

    test_genes = ['APP', 'MAPT', 'SNCA']

    for gene in test_genes:
        logger.info(f"Fetching data for {gene}...")

        gene_data = api.fetch_gene_info(gene)

        if gene_data and gene_data.get('msg'):
            gene_id = gene_data['msg'][0].get('id')

            expression_data = api.fetch_expression_data(gene_id)

            if expression_data:
                processed_data = api.process_expression_data(expression_data)

                if processed_data:
                    api.save_data(processed_data, f"{gene}_expression.json")

                    print(f"\nGene: {gene}")
                    print(f"Number of brain structures with expression data: {len(processed_data['structures'])}")

                    densities = [s['expression_density'] for s in processed_data['structures'] if s['expression_density']]
                    if densities:
                        avg_density = sum(densities) / len(densities)
                        print(f"Average expression density: {avg_density:.4f}")

if __name__ == "__main__":
    main()
