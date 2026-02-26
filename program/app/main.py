import argparse

from processors.processor import Processor
from models.promql_model import *

def main():
  parser = argparse.ArgumentParser(description="Query Prometheus from config file")
  parser.add_argument("-c", "--config", required=True, help="Path to config Yaml file")
  args = parser.parse_args()

  processor = Processor(args.config)
  processor.execute()
 
if __name__ == "__main__":
  main()