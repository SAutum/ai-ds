from collections import namedtuple
from typing import Dict, List, Union
from math import prod

import h5py as h5
import pandas as pd

import torch
from torchvision import transforms
from torch.utils.data import Dataset, Sampler

import logging

# A logger for this file
log = logging.getLogger(__name__)


Tile = namedtuple('Tile', ['brain', 'image', 'row', 'column', 'tile_size'])


class HistoDataset(Dataset):

    data: Dict

    def __init__(
            self,
            file: str,
            mean: float = 153.84,
            std: float = 49.132
    ):
        super(HistoDataset, self).__init__()

        # Define some data augmentations and normalization
        self.transforms = torch.nn.Sequential(
            transforms.RandomHorizontalFlip(0.5),
            transforms.RandomVerticalFlip(0.5),
            transforms.Normalize(mean, std),
        )

        # Load all data to RAM
        log.info("Loading all data to RAM...")
        self.data = {}
        with h5.File(file, 'r') as f:
            for brain in f.keys():
                for image in f[brain].keys():
                    self.data[(brain, image)] = f[brain][image][:]

    def __getitem__(self, loc: Tile) -> torch.Tensor:
        # Request image from memory
        image = self.data[(loc.brain, loc.image)]

        # Extract the requested tile from the image
        tile = image[loc.row:loc.row + loc.tile_size, loc.column:loc.column + loc.tile_size]

        # Add a channel dimension to the tile and perform some data augmentations and normalization to it
        tile = self.transforms(torch.tensor(tile, dtype=torch.float32)[None])

        return tile


class HistoSampler(Sampler):

    def __init__(
            self,
            file: str,
            tile_size: int,
            epoch_length: int,
            sample_groups: List[str],
            sample_images: Union[List[str], None] = None

    ):
        super().__init__(None)

        self.tile_size = tile_size
        self.epoch_length = epoch_length

        # Store image metadata to create sample points
        sizes = []
        shapes = []
        brain_keys = []
        image_keys = []
        with h5.File(file, 'r') as f:
            for b in sample_groups:
                for i, img in f[b].items():  # "image", dataset
                    if sample_images is None or i in sample_images:
                        shapes.append(img.shape)
                        sizes.append(prod(img.shape))
                        brain_keys.append(b)
                        image_keys.append(i)
        self.metadata = pd.DataFrame({'brain': brain_keys, 'image': image_keys, 'img_shape': shapes, 'img_size': sizes})

        # Use a sampling strategy that weights probabilities based on image size
        self.sample_probs = list(self.metadata.img_size / self.metadata.img_size.sum())

    def __iter__(self):
        # Call data sampling with a random seed created by PyTorch (there is a bug with numpy which it uses internally)
        #random_state = torch.randint(123456789, (1,))
        #random_state = random_state.numpy()
        random_state = 1234

        # Sample a whole epoch of groups and images in advance
        locs = self.metadata.sample(n=self.epoch_length, replace=True, random_state=random_state, weights=self.sample_probs)

        # Iterate over the images and perform selection of random locations for the Tile
        for _, l in locs.iterrows():
            shape = l.img_shape
            r = torch.randint(shape[0] - self.tile_size, (1,))
            c = torch.randint(shape[1] - self.tile_size, (1,))
            yield Tile(l.brain, l.image, r, c, self.tile_size)

    def __len__(self):
        # The length does not depend on the number of images or groups but is set manually
        return self.epoch_length
