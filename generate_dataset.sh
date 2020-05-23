#!/bin/bash

# i.e. random outliers
#./generate_dataset.sh <input.g2o> <sample_size> <n_outlier> 
# i.e. random outliers, linkdown
#./generate_dataset.sh <input.g2o> <sample_size> <n_outlier> 0
# i.e  group outliers
#./generate_dataset.sh <input.g2o> <sample_size> <n_outlier> <group_size>
# i.e group outliers, linkdown
#./generate_dataset.sh <input.g2o> <sample_size> <n_outlier> 0 <group_size>


prefix=`dirname "$BASH_SOURCE"`


END=$2
INPUT=$1
N_OUTLIER=$3
DIMENSION=2


for ((SEED=1;SEED<=END;SEED++))
do
    #echo $SEED
    # delete pose 0
    if [[ $DIMENSION -eq 2 ]] ; then
        sed '/VERTEX_SE2 0 /d' "$prefix"/$INPUT > "$prefix"/"$INPUT"_del0.g2o
    elif [[ $DIMENSION -eq 3 ]] ; then
        sed '/VERTEX_SE3:QUAT 0 /d' "$prefix"/$INPUT > "$prefix"/"$INPUT"_del0.g2o
    fi

    if [[ $# -eq 3 ]] ; then
    # add outliers (resulting file doesn't include pose 0 , but edge 0-1)
        "$prefix"/./generateDataset.py -i "$prefix"/"$INPUT"_del0.g2o -o "$prefix"/"$INPUT"_seed_"$SEED"_del0.g2o --seed=$SEED -n $N_OUTLIER

    elif [[ $# -eq 4 ]] ; then
    	if [[ $4 -eq 0 ]] ; then
    		"$prefix"/./generateDataset.py -i "$prefix"/"$INPUT"_del0.g2o -o "$prefix"/"$INPUT"_seed_"$SEED"_del0.g2o --seed=$SEED -n $N_OUTLIER --linkdown
    	else
    		"$prefix"/./generateDataset.py -i "$prefix"/"$INPUT"_del0.g2o -o "$prefix"/"$INPUT"_seed_"$SEED"_del0.g2o --seed=$SEED -n $N_OUTLIER -g $4
    	fi

    elif [[ $# -eq 5 ]] ; then
    	"$prefix"/./generateDataset.py -i "$prefix"/"$INPUT"_del0.g2o -o "$prefix"/"$INPUT"_seed_"$SEED"_del0.g2o --seed=$SEED -n $N_OUTLIER -g $5 --linkdown

    fi

    # sort incrementally (resulting file doesn't have any vertexs, but contains edge 0-1
    python "$prefix"/sort.py "$prefix"/"$INPUT"_seed_"$SEED"_del0.g2o "$prefix"/"$INPUT"_seed_"$SEED"_sorted.g2o $DIMENSION

    # delete edge 0-1

    if [[ $DIMENSION -eq 2 ]] ; then
	    sed -i '/EDGE_SE2 0 1 /d' "$prefix"/"$INPUT"_seed_"$SEED"_del0.g2o
            sed -i '/EDGE_SE2 0 1.000000 /d' "$prefix"/"$INPUT"_seed_"$SEED"_del0.g2o
	    sed -i '/EDGE_SE2 0 /d' "$prefix"/"$INPUT"_del0.g2o
	elif [[ $DIMENSION -eq 3 ]] ; then
	    sed -i '/EDGE_SE3:QUAT 0 1 /d' "$prefix"/"$INPUT"_seed_"$SEED"_del0.g2o
            sed -i '/EDGE_SE3:QUAT 0 1.000000 /d' "$prefix"/"$INPUT"_seed_"$SEED"_del0.g2o
	    sed -i '/EDGE_SE3:QUAT 0 /d' "$prefix"/"$INPUT"_del0.g2o
	fi
	    
    

    
    
done
