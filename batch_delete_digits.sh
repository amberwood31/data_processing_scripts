for dataset in csail 
do
    for configuration in 14 32 54 85 127
    do
        
        cp delete_digits.py "$dataset"_random"$configuration"
        cd "$dataset"_random"$configuration"
        python delete_digits.py $dataset
        cd ../

    done

done


for dataset in manhattan
do
    for configuration in 217 488 837 1301 1952
    do
        
        cp delete_digits.py "$dataset"_random"$configuration"
        cd "$dataset"_random"$configuration"
        python delete_digits.py $dataset
        cd ../

    done

done

