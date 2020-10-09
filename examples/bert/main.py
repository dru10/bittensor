"""BERT Next Sentence Prediction Neuron.

This file demonstrates training the BERT neuron with next sentence prediction.

Example:
        $ python examples/bert/main.py

"""
import bittensor
from bittensor.synapses.bert.model import BertNSPSynapse

import argparse
from datasets import load_dataset, list_metrics, load_metric
from loguru import logger
import os, sys
import math
import random
import time
import transformers
import torch

def nsp_batch(data, batch_size):
    """ Returns a random batch from text dataset with 50 percent NSP.

        Args:
            data: (List[dict{'text': str}]): Dataset of text inputs.
            batch_size: size of batch to create.
        
        Returns:
            batch_inputs List[str]: List of sentences.
            batch_next List[str]: List of (potential) next sentences 
            batch_labels torch.Tensor(batch_size): 1 if random next sentence, otherwise 0.
    """
    batch_inputs = []
    batch_next = []
    batch_labels = []
    for _ in range(batch_size):
        if random.random() > 0.5:
            pos = random.randint(0, len(data))
            batch_inputs.append(data[pos]['text'])
            batch_next.append(data[pos + 1]['text'])
            batch_labels.append(0)
        else:
            while True:
                pos_1 = random.randint(0, len(data))
                pos_2 = random.randint(0, len(data))
                batch_inputs.append(data[pos_1]['text'])
                batch_next.append(data[pos_2]['text'])
                batch_labels.append(1)
                if (pos_1 != pos_2) and (pos_1 != pos_2 - 1):
                    break
    return batch_inputs, batch_next, torch.tensor(batch_labels, dtype=torch.long)
            
def main(hparams):
    # Args
    config = bittensor.Config( hparams )
    learning_rate = 0.01 
    batch_size = 100
    epoch_size = 50
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")

    # Dataset: 74 million sentences pulled from books.
    dataset = load_dataset('bookcorpus')

    # collator accepts a list [ dict{'input_ids, ...; } ] where the internal dict 
    # is produced by the tokenizer.
    data_collator = DataCollatorForLanguageModeling(
        tokenizer=bittensor.__tokenizer__, mlm=True, mlm_probability=0.15
    )

    # Tokenize the list of strings.
    train_tokenized = tokenizer(train_batch)

    # Tokenizer returns a dict { 'input_ids': list[], 'attention': list[] }
    # but we need to convert to List [ dict ['input_ids': ..., 'attention': ... ]]
    # annoying hack
    train_tokenized = [dict(zip(train_tokenized,t)) for t in zip(*train_tokenized.values())]

    # Produces the masked language model inputs aw dictionary dict {'inputs': tensor_batch, 'labels': tensor_batch}
    # which can be used with the Bert Language model. 
    print (data_collator(train_tokenized))


    # Build Synapse
    model_config = transformers.modeling_bert.BertConfig(hidden_size=bittensor.__network_dim__, num_hidden_layers=2, num_attention_heads=2, intermediate_size=512, is_decoder=False)
    model = BertNSPSynapse(model_config)
    model.to(device)

    # Setup Bittensor.
    # Create background objects.
    # Connect the metagraph.
    # Start the axon server.
    bittensor.init( config )
    bittensor.serve( model )
    bittensor.start()
  
    # Optimizer.
    optimizer = torch.optim.SGD(model.parameters(), lr=learning_rate)
    scheduler = torch.optim.lr_scheduler.StepLR(optimizer, step_size=5, gamma=0.1)
    
    def train(dataset, model, epoch):
        model.train()  # Turn on the train mode.
        optimizer.zero_grad() # Zero out lingering gradients.

        step = 0
        while step < epoch_size:
            # Next batch.
            sentences, next_sentences, next_sentence_labels = nsp_batch(dataset['train'], batch_size)
            
            # Compute full pass and get loss with a network query.
            output = model(sentences, next_sentences, next_sentence_labels, query=True)
            
            loss = output['loss']
            loss.backward()
            optimizer.step()
            scheduler.step()

            step += 1
            logger.info('Train Step: {} [{}/{} ({:.1f}%)]\t Network Loss: {:.6f}\t Local Loss: {:.6f}\t Distilation Loss: {:.6f}'.format(
                epoch, step, epoch_size, float(step * 100)/float(epoch_size), output['network_target_loss'].item(), output['local_target_loss'].item(), output['distillation_loss'].item()))
      
    epoch = 0
    try:
        while True:
            train(dataset, model, epoch)
            epoch += 1
    except Exception as e:
        logger.exception(e)
        bittensor.stop()
        


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    hparams = bittensor.Config.add_args(parser)
    hparams = parser.parse_args()
    main(hparams)