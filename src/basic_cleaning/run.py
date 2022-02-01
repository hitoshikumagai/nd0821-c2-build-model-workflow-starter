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
    min_price = 10
    max_price = 350
    idx = df['price'].between(min_price, max_price)
    df = df[idx].copy()

    logger.info("Convert data type to datetime")
    df['last_review'] = pd.to_datetime(df['last_review'])

    logger.info("Convert dataframe to csv format")
    df.to_csv("clean_sample.csv", index=False)


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
        "--parameter1", 
        type=str ## INSERT TYPE HERE: str, float or int,
        help="Input date to clean" ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--parameter2", 
        type=float ## INSERT TYPE HERE: str, float or int,
        help="Minimum value of price" ## INSERT DESCRIPTION HERE,
        required=True
    )

    parser.add_argument(
        "--parameter3", 
        type=float ## INSERT TYPE HERE: str, float or int,
        help="Max values of price" ## INSERT DESCRIPTION HERE,
        required=True
    )


    args = parser.parse_args()

    go(args)
