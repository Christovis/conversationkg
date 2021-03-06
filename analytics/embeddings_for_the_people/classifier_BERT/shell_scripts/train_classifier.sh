#!/bin/bash


#SBATCH --job-name=train_classifier_BERT

#SBATCH --time=42:00:00
#SBATCH --mem=60G

#SBATCH --nodes=1
# #SBATCH --partition=gpu
#SBATCH --partition=gpu_shared
#SBATCH --gres=gpu:1


##SBATCH --ntasks=1
##SBATCH --cpus-per-task=6
##SBATCH --ntasks-per-node=1



module load pre2019
module load Python/3.6.3-foss-2017b

module load CUDA/10.0.130 
module load cuDNN/7.3.1-CUDA-10.0.130


echo "Job EXPERIMENTAL train_classifier_BERT $PBS_JOBID STARTED at `date`"



cp -r $HOME/conversationkg/embeddings_for_the_people $TMPDIR

mkdir $HOME/classifier_BERT

cd $TMPDIR/embeddings_for_the_people/classifier_BERT/

python3 train_classifier.py --save_dir="$HOME/classifier_BERT/"


# for j in 0 1 2 3; do
#     echo "SH: call with i=$j"
#     python3 BERT_on_emails2.py --k=4 --i=$j
    
    
#     echo "FILE SIZE: " $(du -hcs emails_vectors_$j.pkl)
    
#     cp emails_vectors_$j.pkl $HOME/classifier_BERT
# done



# cp -r $TMPDIR/embeddings_for_the_people/classifier_BERT/ $HOME


echo "Job BERT_on_emails $PBS_JOBID ENDED at `date`"