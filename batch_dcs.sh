INPUT=$1
FILENAME=$2
KERNELWIDTH=$3
END=$4

for ((SEED=1;SEED<=END;SEED++))
do

    ./run_dcs.sh "$INPUT""$FILENAME".g2o_seed_"$SEED"_del0.g2o "$FILENAME".g2o_seed_"$SEED"_dcs.g2o $KERNELWIDTH >&1 | tee s_value_seed_"$SEED".txt


done
