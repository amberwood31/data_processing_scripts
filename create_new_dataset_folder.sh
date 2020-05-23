#!/bin/bash


prefix=`dirname "$BASH_SOURCE"`
dataset=$1
outlier_strategy=$2
# create new dir

mkdir "$prefix"/"$dataset"_"$outlier_strategy"

# copy scripts into new dir
cp "$prefix"/generateDataset.py "$prefix"/generate_dataset.sh "$prefix"/sort.py "$prefix"/uniquify.py "$prefix"/"$dataset"_"$outlier_strategy"
cp "$prefix"/"$dataset".g2o "$prefix"/"$dataset"_"$outlier_strategy"
