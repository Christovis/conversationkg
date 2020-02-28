#!/bin/bash


#SBATCH --job-name=W3CGPT2

#SBATCH --time=1:00:00
#SBATCH --mem=10G

#SBATCH --ntasks=1
##SBATCH --cpus-per-task=6
#SBATCH --ntasks-per-node=1

##SBATCH --partition=gpu_shared
##SBATCH --gres=gpu:1


module load pre2019
module load Python/3.6.3-foss-2017b

module load CUDA/10.0.130 
module load cuDNN/7.3.1-CUDA-10.0.130


echo "Job W3CGPT2 $PBS_JOBID STARTED at `date`"


cp -r $HOME/work/conversationkg/embeddings_for_the_people $TMPDIR

cd $TMPDIR/embeddings_for_the_people/personalised_GPT2


if ! test -f "W3CGPT2/full.train.all"; then
    echo "W3CGPT2/full.train.all exist"
    cat W3CGPT2/full.train.raw.* > full.train.all
fi

if ! test -f "W3CGPT2/full.test.all"; then
    echo "W3CGPT2/full.test.all exist"
    cat W3CGPT2/full.test.raw.* > full.test.all
fi


python3 run_language_modeling.py \
            --output_dir=W3CGPT2 \ 
            --model_type=gpt2  \
            --model_name_or_path=gpt2 \
            --do_train \
            --train_data_file=W3CGPT2/full.train.raw \
            --line_by_line
            --num_train_epochs=2

cp -r $TMPDIR/embeddings_for_the_people/personalised_GPT2 $HOME


echo "Job W3CGPT2 $PBS_JOBID ENDED at `date`"
