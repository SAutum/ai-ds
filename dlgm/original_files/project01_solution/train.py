# Code adapted from https://pytorch.org/tutorials/beginner/introyt/trainingyt.html #
####################################################################################

import os
import random
import numpy as np

import torch
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter

import torch.multiprocessing

import hydra
from omegaconf import DictConfig
import logging

import torch
from torch.utils.data import DataLoader

from src.data import HistoDataset, HistoSampler
from src.vae import VariationalAutoencoder, VAELoss 

global dataset, train_sampler, train_loader, val_sampler, val_loader, model, optimizer, loss_function

# Needed to add this for my work station for larger batch sizes
# https://github.com/pytorch/pytorch/issues/11201
torch.multiprocessing.set_sharing_strategy('file_system')

# A logger for this file
log = logging.getLogger(__name__)


def train_one_epoch(epoch_index, tb_writer, log_interval=100, device='cpu'):

    global dataset, train_sampler, train_loader, model, optimizer, loss_function

    running_loss = 0.
    last_loss = 0.

    # Here, we use enumerate(training_loader) instead of
    # iter(training_loader) so that we can track the batch
    # index and do some intra-epoch reporting
    for i, batch in enumerate(train_loader):
        # Zero your gradients for every batch!
        optimizer.zero_grad()

        # Make predictions for this batch
        batch = batch.to(device)
        outputs, mu, log_var = model(batch)

        # Compute the loss and its gradients
        loss = loss_function(batch, outputs, mu, log_var)
        loss.backward()
      # Adjust learning weights
        optimizer.step()
  

        # Gather data and report
        running_loss += loss.item()
        if (i + 1) % log_interval == 0:
            last_loss = running_loss / log_interval # loss per batch
            log.info('  batch {} loss: {}'.format(i + 1, last_loss))
            tb_x = epoch_index * len(train_loader) + i + 1
            if tb_writer is not None:
                tb_writer.add_scalar('Loss/train', last_loss, tb_x)
            running_loss = 0.

    return last_loss


@hydra.main(config_path="configs/", config_name="train.yaml")
def main(config: DictConfig):

    global dataset, train_sampler, train_loader, val_sampler, val_loader, model, optimizer, loss_function

    # Use a common dataset for training and validation
    dataset = HistoDataset(
        file=config.data_path,
        mean=config.mean,
        std=config.std
    )

    # Define train sampling on train brains
    train_sampler = HistoSampler(
        file=config.data_path,
        tile_size=config.tile_size,
        epoch_length=config.train_epoch_size,
        sample_groups=config.train_brains,
    )

    train_loader = DataLoader(
        dataset=dataset,
        batch_size=config.batch_size,
        sampler=train_sampler,
        num_workers=config.num_workers
    )

    # Define validation sampling on validation brain
    val_sampler = HistoSampler(
        file=config.data_path,
        tile_size=config.tile_size,
        epoch_length=config.val_epoch_size,
        sample_groups=config.val_brains,
    )

    val_loader = DataLoader(
        dataset=dataset,
        batch_size=config.batch_size,
        sampler=val_sampler,
        num_workers=config.num_workers
    )

    # Model
    model = VariationalAutoencoder(latent_dim=config.latent_dim)
    model.to(config.device)

    # Optimizers specified in the torch.optim package
    optimizer = torch.optim.Adam(model.parameters(), lr=config.lr, weight_decay=config.weight_decay)

    # Define reconstruction loss function
    loss_function = VAELoss()

    ### TRAIN ###

    log.info(f"Start training from {os.getcwd()}")

    # Create SummaryWriter and tensorboard  dir
    writer = SummaryWriter(".")

    epoch_number = 0
    best_vloss = 1_000_000.
    
    model_path = None
    for epoch in range(config.num_epochs):
        log.info('EPOCH {}:'.format(epoch_number + 1))

        model.train(True)
        avg_loss = train_one_epoch(
            epoch_index=epoch,
            tb_writer=writer,
            log_interval=config.log_interval,
            device=config.device
        )
        model.train(False)

        running_vloss = 0.
        for i, batch in enumerate(val_loader):
            batch = batch.to(config.device)
            outputs, mu, log_var = model(batch)
            vloss = loss_function(batch, outputs, mu, log_var)
            running_vloss += vloss.item()

        avg_vloss = running_vloss / (i + 1)
        log.info('LOSS train {} valid {}'.format(avg_loss, avg_vloss))

        # Log validation loss
        writer.add_scalar('Loss/val', avg_vloss, epoch_number + 1)

        # Track best performance, and save the model's state
        if avg_vloss < best_vloss:
            best_vloss = avg_vloss
            if model_path:
                # Delete old model if exist
                os.remove(model_path)
            model_path = 'model_epoch{:04d}.ckpt'.format(epoch_number)
            log.info(f"New best model! Store at {model_path}")
            torch.save(model.state_dict(), model_path)

        epoch_number += 1

    writer.close()


def set_seed(seed: int):
    # set seed for Numpy
    np.random.seed(seed)

    # Set seed for Python's built-in `random` library
    random.seed(seed)

    # Set seed for PyTorch
    torch.manual_seed(seed)
    torch.cuda.manual_seed_all(seed)
    torch.backends.cudnn.deterministic = True
    torch.backends.cudnn.benchmark = False
    
    
if __name__ == "__main__":
    main()


