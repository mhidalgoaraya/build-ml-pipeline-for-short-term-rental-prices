#!/usr/bin/env python
"""
Download data from W&B, clean data, upload new artifact
"""
import argparse
import logging

import pandas as pd
import wandb

logging.basicConfig(level=logging.INFO, format="%(asctime)-15s %(message)s")
logger = logging.getLogger()


def go(args):
    run = wandb.init(project="nyc_airbnb", group="eda", job_type="basic_cleaning", save_code=True)
    run.config.update(args)
    directory = wandb.use_artifact(args.input_artifact).file()
    df = pd.read_csv(directory)

    idx = df['price'].between(args.min_price, args.max_price)
    df = df[idx].copy()

    df['last_review'] = pd.to_datetime(df['last_review'])

    #df.drop(['id', 'name', 'host_name', 'host_id',
    #         'neighbourhood', 'neighbourhood_group', 'number_of_reviews',
    #         'reviews_per_month', 'last_review',
    #         'calculated_host_listings_count'], axis=1, inplace=True)

    #dataset = pd.get_dummies(df, columns=['room_type'])
    idx = df['longitude'].between(-74.25, -73.50) & df['latitude'].between(
        40.5, 41.2)
    df = df[idx].copy()
    df.to_csv(args.output_artifact, index=False)

    artifact = wandb.Artifact(
        args.output_artifact,
        type=args.output_type,
        description=args.output_description,
    )
    artifact.add_file("clean_sample.csv")
    run.log_artifact(artifact)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Basic data cleaning")

    parser.add_argument(
        "--input_artifact",
        type=str,
        help="Name for input artifact",
        required=True
    )

    parser.add_argument(
        "--output_artifact",
        type=str,
        help="Name for output artifact",
        required=True
    )

    parser.add_argument(
        "--output_type",
        type=str,
        help="CSV",
        required=True
    )

    parser.add_argument(
        "--output_description",
        type=str,
        help="Clean data",
        required=True
    )

    parser.add_argument(
        "--min_price",
        type=float,
        help="Minimum price willing to pay",
        required=True
    )

    parser.add_argument(
        "--max_price",
        type=float,
        help="Maximum proce willing to pay",
        required=True
    )

    args = parser.parse_args()

    go(args)
