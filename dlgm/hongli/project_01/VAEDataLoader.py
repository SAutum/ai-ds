import numpy as np
import matplotlib.pyplot as plt
import h5py

import torch
import torch.random as random
import torchvision.transforms as T
from torch.utils.data import Dataset
from torch.utils.data import Sampler
from torch.utils.data import DataLoader



class BrainImageDataset(Dataset):
    """
    A dataset for the brain images. The dataset is stored in a h5 file

    attributes:
    - self.h5pyfile: the h5 file object
    - self.brains: a list of all the brains in the dataset
    - self.global_values: a dictionary with the global mean and std of the dataset

    methods:
    - available_images(brain): returns a list of all the available images in a brain
    """

    def __init__(self, img_dir = './cell_data.h5', transform=None, \
        train=True, subset = False):
        self.transform = transform
        self.h5pyfile = h5py.File(img_dir, 'r')
        self.brains = list(self.h5pyfile.keys())

        # If we are training, we want to use all the brains except the last one
        if train:
            self.brains.pop(-1)
        else:
            self.brains = [self.brains[-1]]

        # calculate the global max, min, mean and std of the dataset
        self.global_values = self.global_mean_std()

    # Means and standard deviations for the dataset. See e01
    def global_mean_std(self):
        pixel_values = np.empty((0,5))
        for brain in self.brains:
            for image_name in self.h5pyfile[brain].keys():
                image = self.h5pyfile[brain][image_name][:].astype(np.float32)
                tuple = np.array([[image.size, image.min(), image.max(), image.mean(), (image**2).mean()]])
                pixel_values = np.append(pixel_values, tuple, axis=0)

        global_values = {}
        p = pixel_values[:,0]/np.sum(pixel_values[:,0])
        global_values['min'] = np.min(pixel_values[:,1])
        global_values['max'] = np.max(pixel_values[:,2])
        global_values['mean'] = p @ pixel_values[:,3]
        mean_squared = p @ pixel_values[:,4]
        global_values['std'] = np.sqrt(mean_squared - global_values['mean']**2)
        return global_values

    # Returns a list of all the available images in a brain
    def available_images(self, brain):
        return list(self.h5pyfile[brain].keys())

    def __len__(self):
        length = 0
        for brain in self.brains:
            length += len(self.h5pyfile[brain].keys())
        return length

    def __getitem__(self, input: tuple):
        brain, image_name, row, column, tile_size = input
        # make sure the brain and image are in the dataset
        assert brain in self.brains, f'Brain {brain} not in dataset'
        assert image_name in self.available_images(brain), f'Image {image_name} not in brain {brain}'

        # make sure the tile is in the image
        image = self.h5pyfile[brain][image_name]
        assert row >= 0 and \
            row + tile_size <= image.shape[0], \
            f'Tile row {row} out of bounds'
        assert column >=0 and \
            column + tile_size <= image.shape[1], \
            f'Tile column {column} out of bounds'

        # get the tile
        tile = image[row:row+tile_size, column:column+tile_size]
        # to tensor
        tile = T.ToTensor()(tile)
        # standardize
        tile = T.Normalize(mean=self.global_values['mean'], \
                           std=self.global_values['std'])(tile)
        return tile


class BrainRandomSampler(Sampler):
    def __init__(self, dataset, tile_size, batch_size, num_of_batches):
        self.dataset = dataset
        self.batch_size = batch_size
        self.tile_size = tile_size
        self.length = num_of_batches

        # save a probability distribution for each brain
        self.calculate_probabilities()

        # test using only one tile
        # self.tile = self.sample_tile()

    # for each tile we sample 2 times, one for the brain and one for the image
    def calculate_probabilities(self):
        # the probability of each brain is the number of available images for
        # the brain/total number of images
        self.brain_probabilities = np.array(
            [len(self.dataset.available_images(brain)) for brain in self.dataset.brains]
        )
        self.brain_probabilities = self.brain_probabilities/np.sum(self.brain_probabilities)

        # the probability of each image is the number of available tiles for
        # the image/total number of tiles in the brain
        self.image_probabilites = {}
        for brain in self.dataset.brains:
            image_tiles = np.zeros(len(self.dataset.available_images(brain)))
            for image in self.dataset.available_images(brain):
                image_size = self.dataset.h5pyfile[brain][image].shape
                image_tiles = (image_size[0]-self.tile_size)*(image_size[1]-self.tile_size)
            self.image_probabilites[brain] = image_tiles/np.sum(image_tiles)

    def sample_tile(self):
        # sample the tuple based on the total number available tiles in each
        # brain and image
        brain = torch.randint(len(self.dataset.brains), (1, ))
        brain = self.dataset.brains[brain]
        image_name = torch.randint(len(self.dataset.available_images(brain)), (1,))
        image_name = self.dataset.available_images(brain)[image_name]

        # get the image
        image = self.dataset.h5pyfile[brain][image_name]
        # sample the row and column
        row = torch.randint(image.shape[0]-self.tile_size, (1,))
        column = torch.randint(image.shape[1]-self.tile_size, (1,))
        tile = (brain, image_name, int(row), int(column), self.tile_size)
        return tile

    def __iter__(self):
        # return a batch of samples using sample_tile for each sample
        for j in range(self.length):
            batch = []
            for i in range(self.batch_size):
                batch.append(self.sample_tile())
                # batch.append(self.tile)
            yield batch

    def __len__(self):
        return self.length
