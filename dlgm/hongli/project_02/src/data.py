from collections import namedtuple
from typing import Dict, List, Union
from math import prod

import h5py as h5
import pandas as pd

import os
import yaml

import torch
from torchvision import transforms
from torch.utils.data import Dataset, Sampler

import logging

# A logger for this file
log = logging.getLogger(__name__)

configs = yaml.safe_load(open('./configs/train.yaml'))

Tile = namedtuple('Tile',
                  ['brain', 'section', 'region', 'map_type',
                   'row', 'column', 'patch_size'])


# data path configuration
def get_data_path() -> Union[str, str]:
    data_path = configs['data_path']
    data_fom = os.path.join(data_path, configs['data_fom'])
    data_trans = os.path.join(data_path, configs['data_trans'])
    # expanduser expands the path to the user home directory
    data_path = os.path.expanduser(data_path)
    data_fom = os.path.expanduser(data_fom)
    data_trans = os.path.expanduser(data_trans)
    return data_fom, data_trans


class HistoDataset(Dataset):

    data: Dict

    def __init__(self, train: bool = True):
        super(HistoDataset, self).__init__()

        # Define some data augmentations and normalization
        self.transforms = torch.nn.Sequential(
            transforms.RandomHorizontalFlip(0.5),
            transforms.RandomVerticalFlip(0.5),
        )

        # Load all data to RAM
        log.info("Loading all data to RAM...")

        files = yaml.safe_load(open('./configs/selected_regions.yaml'))
        files = files['train'] if train else files['val']

        self.metadata = {}
        data_fom, data_trans = get_data_path()
        folders = [data_fom, data_trans]
        suffixes = list(configs['suffixes'].values())
        self.init_data(files, folders, suffixes)

    def init_data(self, files: list, folders: list, suffixes: list):
        for file in files:
            brain, section, region = file.split('_')[:3]
            if region not in configs['regions']:
                region = None
                file = file.replace('_None', '')

            for folder, suffix, map_type in \
                    zip(folders, suffixes, ['FOM', 'transmittance']):
                _file = os.path.join(folder, file + "_" + suffix + '.h5')
                key = (brain, section, region, map_type)
                self.metadata[key] = h5.File(_file, 'r')['Image']

    def __getitem__(self, loc: Tile) -> torch.Tensor:
        # Request image from memory
        image = self.metadata[(loc.brain, loc.section, loc.region, loc.map_type)]

        # Extract the requested tile from the image
        tile = image[loc.row:loc.row + loc.patch_size,
                     loc.column:loc.column + loc.patch_size]

        # Add a channel dimension to the tile and perform some data
        # augmentations
        tile = transforms.ToTensor()(tile)
        tile = self.transforms(tile)

        return tile

    def __len__(self) -> int:
        return prod([len(v) for v in self.data.values()])


class HistoSampler(Sampler):

    def __init__(
            self,
            train: bool,
            dataset: HistoDataset,
            tile_size: int,
            epoch_length: int
    ):
        super().__init__(None)

        self.tile_size = tile_size
        self.epoch_length = epoch_length
        self.dataset = dataset

        # Store image metadata to create sample points
        files = yaml.safe_load(open('./configs/selected_regions.yaml'))
        files = files['train'] if train else files['val']

        sizes = []
        shapes = []
        brains = []
        sections = []
        regions = []
        map_types = []
        data_fom, data_trans = get_data_path()
        folders = [data_fom, data_trans]
        suffixes = list(configs['suffixes'].values())

        for file in files:
            brain, section, region = file.split('_')[:3]
            if region not in configs['regions']:
                region = None
                file = file.replace('_None', '')

            for folder, suffix, map_type in \
                    zip(folders, suffixes, ['FOM', 'transmittance']):
                _file = os.path.join(folder, file + "_" + suffix + '.h5')
                img = h5.File(_file, 'r')['Image']
                sizes.append(prod(img.shape))
                shapes.append(img.shape)
                brains.append(brain)
                sections.append(section)
                regions.append(region)
                map_types.append(map_type)

        self.metadata = pd.DataFrame({'brain': brains, 'section': sections,
                                      'region': regions, 'img_shape': shapes,
                                      'img_size': sizes,
                                      'map_type': map_types})

        # Use a sampling strategy that weights probabilities based on image size
        self.sample_probs = list(self.metadata.img_size / self.metadata.img_size.sum())

    def __iter__(self):
        # Call data sampling with a random seed created by PyTorch (there is a bug with numpy which it uses internally)
        #random_state = torch.randint(123456789, (1,))
        #random_state = random_state.numpy()
        random_state = 1234

        # Sample a whole epoch of groups and images in advance
        locs = self.metadata.sample(n=self.epoch_length, replace=True,
                    random_state=random_state, weights=self.sample_probs)

        # Iterate over the images and perform selection of random locations for the Tile
        for _, l in locs.iterrows():
            shape = l.img_shape
            accepted = False
            while not accepted:
                r = torch.randint(shape[0] - self.tile_size, (1,))
                c = torch.randint(shape[1] - self.tile_size, (1,))
                tile = Tile(l.brain, l.section, l.region, l.map_type, r, c,
                            self.tile_size)

                # Check if the tile is valid (avoid black tiles)
                median = self.dataset[tile].median()
                if median > 0.1 and median < 0.9:
                    accepted = True

            yield tile

    def __len__(self):
        # The length does not depend on the number of images or groups but is set manually
        return self.epoch_length


class FomSampler(HistoSampler):
    def __init__(self, train: bool, dataset: HistoDataset, tile_size: int, epoch_length: int):
        super().__init__(train, dataset, tile_size, epoch_length)

        # Filter out transmittance images
        self.metadata = self.metadata[self.metadata.map_type == 'FOM']
        self.sample_probs = list(self.metadata.img_size / self.metadata.img_size.sum())


# main function
if __name__ == '__main__':
    get_data_path()
