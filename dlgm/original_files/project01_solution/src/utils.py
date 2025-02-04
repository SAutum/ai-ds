import matplotlib.pyplot as plt
import numpy as np
from torch import Tensor
import torch
from math import ceil, sqrt


def show_tiles(x: Tensor, mean=153.84, std=49.132, min_val=0, max_val=255):
    x = np.array(x)
    if len(x.shape) == 4:
        x = [a for a in x]
    else:
        x = [x]
    nrows = ceil(sqrt(len(x)))
    ncols = nrows
    fig, axs = plt.subplots(nrows, ncols, figsize=(nrows * 2, ncols * 2))
    if nrows == 1:
        axs = np.array([axs])
    for i, ax in enumerate(axs.flatten()):
        if i < len(x):
            img = x[i]
            if len(img.shape) == 3:
                img = img.transpose((1, 2, 0))
            ax.imshow(img * std + mean, vmin=min_val, vmax=max_val, cmap='gray')
        ax.set_axis_off()
    plt.subplots_adjust(top=1, bottom=0, right=1, left=0, hspace=0.05, wspace=0.05)
    plt.show()


def debug_stats(model, batch, loss_function, device):
    with torch.no_grad():
        debug_batch = batch.to(device)
        outputs, mu, log_var = model(debug_batch)

        # Compute the loss and its gradients
        loss = loss_function(debug_batch, outputs, mu, log_var)

    print(f"Loss of {loss.item()}")
    flat_outputs = outputs.cpu().numpy().flatten()
    flat_batch = debug_batch.cpu().numpy().flatten()

    print("Output mean:", flat_outputs.mean(), "Output std:", flat_outputs.std())
    print("Target mean:", flat_batch.mean(), "Target std:", flat_batch.std())

    plt.hist(flat_outputs, bins=64, label='Output distribution')
    plt.hist(flat_batch, bins=64, label='Target distribution')
    plt.legend()
    plt.show()

    return outputs
