"""
Training of DCGAN network on MNIST with Discriminator
and Generator imported from models.py
"""

import torch
import torch.nn as nn
import torch.optim as optim
import torchvision
import torchvision.datasets as datasets
import torchvision.transforms as transforms
from torch.utils.data import DataLoader
from torch.utils.tensorboard import SummaryWriter
from tqdm import tqdm

from models import Discriminator, Generator, initialize_weights


device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
LEARNING_RATE = 2E-4
BATCH_SIZE = 32
IMAGE_SIZE = 64
CHANNELS_IMG = 3
Z_DIM = 100
NUM_EPOCHS = 5
FEATURES_DISC = 64
FEATURES_GEN = 64

transform = transforms.Compose(
    [
        transforms.Resize((IMAGE_SIZE, IMAGE_SIZE)),
        transforms.ToTensor(),
        transforms.Normalize(
            [0.5 for _ in range(CHANNELS_IMG)], [0.5 for _ in range(CHANNELS_IMG)]
        ),
    ]
)

dataset = datasets.MNIST(root="dataset/", train=True, transform=transform, download=True)
dataset = datasets.CelebA(root="dataset_celeb/", split="train", transform=transform, download=True)
loader = DataLoader(dataset, batch_size=BATCH_SIZE, shuffle=True)
gen = Generator(Z_DIM, CHANNELS_IMG, FEATURES_GEN).to(device)
disc = Discriminator(CHANNELS_IMG, FEATURES_DISC).to(device)
initialize_weights(gen)
initialize_weights(disc)

opt_gen = optim.Adam(gen.parameters(), lr=LEARNING_RATE, betas=(0.5, 0.999))
opt_disc = optim.Adam(disc.parameters(), lr=LEARNING_RATE, betas=(0.5, 0.999))
criterion = nn.BCELoss()

fixed_noise = torch.randn(32, Z_DIM, 1, 1).to(device)
writer_real = SummaryWriter(f"logs/celeba_real")
writer_fake = SummaryWriter(f"logs/celeba_fake")

step = 0

gen.train()
disc.train()

for epoch in tqdm(range(NUM_EPOCHS)):
    for batch_idx, (real, _) in enumerate(loader):
        real = real.to(device)
        noise = torch.randn((BATCH_SIZE, Z_DIM, 1, 1)).to(device)
        fake = gen(noise)

        # Train Discriminator
        disc.zero_grad()
        
        disc_real = disc(real).reshape(-1)
        loss_disc_real = criterion(disc_real, torch.ones_like(disc_real))
        loss_disc_real.backward(retain_graph=True)

        disc_fake = disc(fake).reshape(-1)
        loss_disc_fake = criterion(disc_fake, torch.zeros_like(disc_fake))
        loss_disc_fake.backward(retain_graph=True)

        loss_disc = (loss_disc_fake+loss_disc_real)/2

        opt_disc.step()

        # Train Generator
        gen.zero_grad()
        output = disc(fake).reshape(-1)
        loss_gen = criterion(output, torch.ones_like(output))
        loss_gen.backward()
        opt_gen.step()

        # Print losses
        if batch_idx % 100 == 0:
            print(
                f"Epoch [{epoch}/{NUM_EPOCHS}] Batch {batch_idx}/{len(loader)} | Loss D: {loss_disc:.4f} | Loss G: {loss_gen:.4f}"
            )

            with torch.no_grad():
                fake = gen(fixed_noise)
                img_grid_real = torchvision.utils.make_grid(
                    real[:32], normalize=True
                )
                img_grid_fake = torchvision.utils.make_grid(
                    fake[:32], normalize=True
                )

                writer_real.add_image("Real Celeb", img_grid_real, global_step=step)
                writer_fake.add_image("Fake Celeb", img_grid_fake, global_step=step)
            
            step += 1


import matplotlib.pyplot as plt

real.shape
imgs, labels = next(iter(loader))
imgs.shape
plt.imshow(torch.permute(imgs[0], (1,2,0)))

n = torch.randn(1, Z_DIM, 1, 1).to(device)
result = gen(n)

result.shape
plt.imshow(torch.permute(result[0], (1,2,0)).detach().cpu())

torch.save(gen, "generar_caras.pt")