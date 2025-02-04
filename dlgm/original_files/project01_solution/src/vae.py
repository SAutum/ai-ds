import torch
import torch.nn as nn
import torch.nn.functional as F
import logging

# A logger for this file
log = logging.getLogger(__name__)


def reparameterize(mu, log_var):
    """
    Reparameterization trick to sample z from a normal distribution.
    """
    std = torch.exp(0.5 * log_var)
    eps = torch.randn_like(std)
    return mu + eps * std


class DownSampler(nn.Module):
    """
    Down sampling module, halving width and height
    """

    def __init__(self, in_c, out_c):
        super(DownSampler, self).__init__()
        self.layers = nn.Sequential(
            nn.Conv2d(in_c, out_c, kernel_size=3, stride=2, padding=1),
            nn.ReLU()
        )

    def forward(self, x):
        return self.layers(x)


class UpSampler(nn.Module):
    """
    Upscaling by factor 2
    """

    def __init__(self, in_c, out_c, use_activation=True):
        super(UpSampler, self).__init__()

        self.layers = nn.Sequential(
            nn.ConvTranspose2d(in_c, out_c, kernel_size=3, stride=2, padding=1, output_padding=1),
        )
        
        if use_activation:
            self.layers.append(nn.ReLU())

    def forward(self, x):
        return self.layers(x)


class Encoder(nn.Module):
    def __init__(self, latent_dim):
        super(Encoder, self).__init__()
        
        self.layers = nn.Sequential(DownSampler(1, 32),     # [b,32,64,64]
                                    DownSampler(32, 64),    # [b,64,32,32]
                                    DownSampler(64, 128),   # [b,128,16,16]
                                    DownSampler(128, 256),  # [b,256,8,8] 
                                    DownSampler(256, 512))  # [b,512,4,4]
        self.fc_mu = nn.Linear(512 * 4 * 4, latent_dim)  # [b,8192]
        self.fc_log_var = nn.Linear(512 * 4 * 4, latent_dim)

    def forward(self, x):
        x = self.layers(x)

        x = torch.flatten(x, start_dim=1)

        mu = self.fc_mu(x)
        log_var = self.fc_log_var(x)
        
        return mu, log_var
    

class Decoder(nn.Module):
    """
    Deterministic decoder for real valued signals
    """

    def __init__(self, latent_dim):
        super(Decoder, self).__init__()
        self.fc = nn.Linear(latent_dim, 512 * 4 * 4)
        self.layers = nn.Sequential(
            UpSampler(512, 256),  # 256 x 8 x 8
            UpSampler(256, 128),  # 128 x 16 x 16
            UpSampler(128, 64),   # 128 x 16 x 16
            UpSampler(64, 32),    # 64 x 32 x 32
            UpSampler(32, 1, use_activation=False)  # 1 x 128 x 128
        )

    def forward(self, z):
        x = F.relu(self.fc(z))
        x = x.view(-1, 512, 4, 4)
        
        x = self.layers(x) # No activation for continuous outputs
        return x


class VariationalAutoencoder(nn.Module):
    """
    A simple VariationalAutoencoder
    """

    def __init__(self, latent_dim):
        super(VariationalAutoencoder, self).__init__()
        
        print("Use latent dim of", latent_dim)

        self.encoder = Encoder(latent_dim=latent_dim)
        self.decoder = Decoder(latent_dim=latent_dim)

    def forward(self, x):
        mu, log_var = self.encoder(x)
        z = reparameterize(mu, log_var)
        
        x_out = self.decoder(z)
        
        return x_out, mu, log_var
    

class VAELoss(nn.Module):
    def __init__(self, reduction='sum'):
        super(VAELoss, self).__init__()
        self.reconstruction_loss = nn.MSELoss(reduction=reduction)
        
    def forward(self, x_in, x_out, mu, logvar):
        recon_loss = self.reconstruction_loss(x_out, x_in)
        kl_loss = -0.5 * torch.sum(1 + logvar - mu.pow(2) - logvar.exp())
        
        return recon_loss + kl_loss
