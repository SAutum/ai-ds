import data
import numpy as np
from matplotlib import pyplot as plt
from torch.utils.data import DataLoader
from PIL import Image


def test_get_data_path():
    data_fom, data_trans = data.get_data_path()
    print(data_fom)
    print(data_trans)


def test_dataset():
    dataset = data.HistoDataset()
    print("Printing train data")
    for key in dataset.metadata:
        print(key)
        print(dataset.metadata[key])
    print("Printing test data")
    dataset = data.HistoDataset(train=False)
    for key in dataset.metadata:
        print(key)
        print(dataset.metadata[key])


def plot_data():
    dataset = data.HistoDataset()
    idx = data.Tile('Vervet1818', 's0850', 'left', 'transmittance',
                    11526, 19258, 512)
    print(idx.brain, idx.section, idx.region, idx.map_type, idx.row,
          idx.column, idx.patch_size)
    sample = dataset[idx].permute(1, 2, 0)
    print("check min and max of sample, should be between 0 and 1")
    assert sample.min() >= 0 and sample.max() <= 1
    plt.imshow(sample.numpy(), cmap='gray')
    plt.savefig('test_data_loader.png')


def test_data_sampler():
    tile_size = 128
    dataset = data.HistoDataset()
    data_sampler = data.FomSampler(train=True, epoch_length=80000,
                                   tile_size=tile_size, dataset=dataset)
    dataloader = DataLoader(dataset, sampler=data_sampler)
    print("The length of the dataloader is", len(dataloader))
    for i, img in enumerate(dataloader):
        # save all the images as png with same resolution
        img = img.squeeze(0)
        img = img.permute(1, 2, 0)
        img = (img * 255).numpy().astype(np.uint8)
        img = Image.fromarray(img)
        img.save('./data/test_data_sampler_{}.png'.format(i))



if __name__ == '__main__':
    print("print current working directory")
    print(data.os.getcwd())

    print("testing get_data_path")
    test_get_data_path()

    print("testing dataset")
    test_dataset()

    print("testing plot_data")
    plot_data()

    print("testing data_sampler")
    test_data_sampler()
