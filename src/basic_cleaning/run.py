#!/usr/bin/env python
"""
Performs basic cleaning on the data and save the resultsin Weights & Biases
"""
import argparse
import logging
import wandb
import pandas as pd

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    logger.info("Download Artifact")
    run = wandb.init(job_type="basic_cleaning")
    run.config.update(args)

    # Download input artifact. This will also log that this script is using this
    # particular version of the artifact
    # artifact_local_path = run.use_artifact(args.input_artifact).file()

    ######################
    # YOUR CODE HERE     #
    ######################
    logger.info("Load csv file")
    artifact_local_path = run.use_artifact(args.input_artifact).file()
    df = pd.read_csv(artifact_local_path)

    logger.info("Set Price min-max range")
    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    logger.info("Convert data type to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("Convert dataframe to csv format")
    df.to_csv(args.input_artifact, index=False)


    logger.info("Logging artifact")
    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
     )
    run.log_artifact(artifact)

if __name__ == "__main__":

    parser = argparse.ArgumentParser(description="This steps cleans the data")

    parser.add_argument(
        "--input_artifact", 
        type=str, 
        help="Input data to clean",
        required=True
    )

    parser.add_argument(
        "--output_artifact", 
        type=str, 
        help="Output cleaned data",
        required=True
    )

    parser.add_argument(
        "--output_type", 
        type=str, 
        help="Output data type",
        required=False
    )

    parser.add_argument(
        "--output_description", 
        type=str, 
        help="Output data description",
        required=False
    )

    parser.add_argument(
        "--min_price", 
        type=float,
        help="Minimum value of price",
        required=True
    )

    parser.add_argument(
        "--max_price", 
        type=float, 
        help="Max values of price",
        required=True
    )


    args = parser.parse_args()

    go(args)
