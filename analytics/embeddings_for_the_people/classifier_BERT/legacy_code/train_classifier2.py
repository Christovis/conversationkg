import torch

from transformers import DistilBertTokenizer, DistilBertModel#, DistilBertConfig
# from transformers import BertTokenizer, BertModel
# BERTTokenizer = DistilBertTokenizer
# BERT = DistilBertModel

import torch

import pickle
from tqdm import tqdm

import numpy as np

# import logging
# logging.getLogger("transformers.tokenization_utils").setLevel(logging.ERROR)


from defs_classifier import CosineSimilarityClassifierCell, Classifier


def gen_X(train_X, tknsd_emails):
    for i1, i2 in train_X:
        yield tknsd_emails[i1], tknsd_emails[i2]
        
#         yield torch.tensor(tknsd_emails[i1], dtype=torch.long),\
#               torch.tensor(tknsd_emails[i2], dtype=torch.long)
        
def gen_Y(train_Y, tknsd_emails):
    return iter(torch.tensor(train_Y, dtype=torch.float))

def generate_forever(iter_func, iter_args):
    iter_instance = iter_func(*iter_args)
    while True:
        yield from finite_iter
        iter_instance = iter_func(*iter_args)

def data_to_gen():
    with open("data/train_inds.pkl", "rb") as handle:
        train_data = pickle.load(handle)
    pairs = train_data[:, :-1]
    true = train_data[:, -1:]
    
    with open("data/emails_token_ids.pkl", "rb") as handle:
        emails = pickle.load(handle)
        
    return gen_X(pairs, emails), gen_Y(true, emails)

def data_to_ls():
    pair_gen, true_gen = data_to_gen()
    return list(pair_gen), list(true_gen)
    

def train_val_sets(pairs, labels, train_ratio=0.8):
    permutation_inds = np.random.permutation(len(pairs))
    permuted_pairs = [pairs[i] for i permutation_inds]
    permuted_labels = [labels[i] for i permutation_inds]
    
    train = (permuted_pairs[:train_ratio], permuted_labels[:train_ratio])
    val = (permuted_pairs[train_ratio:], permuted_labels[train_ratio:])
    return train, val
    
    
import argparse

def parse_args():
    p = argparse.ArgumentParser()
    
    p.add_argument("--save_dir", type=str)
    
    args = p.parse_args()
    return args.save_dir

    
if __name__ == "__main__":
    save_dir = parse_args() 
    
    """
        data
    
    """
    pairs, true_labels = data_to_ls()
    
    
    """
        parameters
    """
    epochs = 20
    checkpoints = 10
    
    sentence_vector_len = int(2**9)
    
    
    print("SENTENCE VECOR LENGTH ", sentence_vector_len)
    

    
    """
        initialisation 
    """
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    
    bert = DistilBertModel.from_pretrained("distilbert-base-uncased")
    bert.eval()

    for param in bert.parameters():
        param.requires_grad = False

    bert.to(device)

    
    c = Classifier(bert, word_emb_size=bert.config.dim, rnn_hidden_size=sentence_vector_len, rnn_num_layers=2, 
               clssfr_cell_type=CosineSimilarityClassifierCell, clssfr_hidden_size=0)
    c.to(device)

    
    
    """
        training
    """
    
    preds, losses = c.fit(pairs, true_labels, epochs=epochs, num_checkpoints=checkpoints, save_to=save_dir)
    
    
    with open(c.checkpoint_folder + "train_predictions.pkl") as handle:
        pickle.dump(preds)
                    
    with open(c.checkpoint_folder + "train_losses.pkl") as handle:
        pickle.dump(losses)
                    
    
    
    
        
    


