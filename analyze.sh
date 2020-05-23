FOLDER_PATH=$1
FILENAME=$2
INLIER_QUANTITY=$3
OUTLIER_QUANTITY=$4
END=$5

for ((SEED=1;SEED<=END;SEED++))
do

    python simple_plot.py "$FILENAME".g2o_seed_"$SEED"_dcs.g2o
    
    python plot_s_value.py $FOLDER_PATH $FILENAME $INLIER_QUANTITY $OUTLIER_QUANTITY $SEED

done
