import numpy as np
import torch
import torchvision
import torch.nn as nn
import torch.nn.functional as F


class Block(nn.Module):
    def __init__(self, in_ch, out_ch, dilation=1):
        super().__init__()
        self.conv1 = nn.Conv2d(in_ch, out_ch, 3, padding="same", dilation=dilation)
        self.bn1 = nn.BatchNorm2d(out_ch)
        self.relu = nn.ReLU()
        self.conv2 = nn.Conv2d(out_ch, out_ch, 3, padding="same", dilation=dilation)

    def forward(self, x):
        return self.conv2(self.relu(self.bn1(self.conv1(x))))


class Encoder(nn.Module):
    def __init__(self, chs=(1, 64, 128, 256, 512, 1024), max_pool=True, features=True):
        super().__init__()
        self.enc_blocks = nn.ModuleList([Block(chs[i], chs[i + 1]) for i in range(len(chs) - 1)])
        self.pool = nn.MaxPool2d(2) if max_pool else nn.Identity()
        self.features = features
        
    def forward(self, x):
        ftrs = []
        for block in self.enc_blocks:
            x = block(x)
            ftrs.append(x)
            x = self.pool(x)
         
        if self.features:
            return ftrs
        else:
            return ftrs[-1]


class Decoder(nn.Module):
    def __init__(self, chs=(1024, 512, 256, 128, 64)):
        super().__init__()
        self.chs = chs
        self.upconvs = nn.ModuleList([nn.ConvTranspose2d(chs[i], chs[i + 1], 2, 2) for i in range(len(chs) - 1)])
        self.dec_blocks = nn.ModuleList([Block(chs[i], chs[i + 1]) for i in range(len(chs) - 1)])

    def forward(self, x, encoder_features):
        for i in range(len(self.chs) - 1):
            x = self.upconvs[i](x)
            enc_ftrs = self.crop(encoder_features[i], x)
            x = torch.cat([x, enc_ftrs], dim=1)
            x = self.dec_blocks[i](x)
        return x

    def crop(self, enc_ftrs, x):
        _, _, H, W = x.shape
        enc_ftrs = torchvision.transforms.CenterCrop([H, W])(enc_ftrs)
        return enc_ftrs


class UNet(nn.Module):
    def __init__(self, enc_chs=(1, 64, 128, 256, 512, 1024), dec_chs=(1024, 512, 256, 128, 64), num_class=1, max_pool=True):
        super().__init__()
        self.encoder = Encoder(enc_chs, max_pool=max_pool)
        self.decoder = Decoder(dec_chs)
        self.head = nn.Conv2d(dec_chs[-1] + enc_chs[0], num_class, kernel_size=3, padding="same")

    def forward(self, x, condition=None):
        # run the model
        enc_ftrs = self.encoder(x)
        out = self.decoder(enc_ftrs[::-1][0], enc_ftrs[::-1][1:])
        out = self.head(torch.cat((out, x), dim=1))

        return F.softmax(out, dim=1)
