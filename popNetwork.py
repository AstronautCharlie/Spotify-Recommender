import os 
import sys 
import torch
import pandas as pd 
from torch import nn 
from torch.utils.data import DataLoader 
from dataLoader import SpotifyDataset, SONG_FEATURES

LEARNING_RATE = 0.001
EPOCHS = 100

class PopularityModel(nn.Module):
	def __init__(self):
		super(PopularityModel, self).__init__()
		self.stack = nn.Sequential(
						nn.Linear(9, 256),
						nn.ReLU(),
						nn.Linear(256,512),
						nn.ReLU(),
						nn.Linear(512,256),
						nn.ReLU(),
						nn.Linear(256, 256),
						nn.ReLU(),
						nn.Linear(256,1),
						nn.ReLU())

	def forward(self, x):
		return self.stack(x.float())

def train_loop(dataloader, model, loss_fn, optimizer):
	size = len(dataloader.dataset)
	for batch, (X, y) in enumerate(dataloader):
		prediction = model.forward(X)
		loss = loss_fn(prediction, y)

		loss.backward()
		optimizer.step()
		optimizer.zero_grad() 

		if batch % 10 == 0: 
			loss, current = loss.item(), batch * len(X)
			print(f"loss: {loss:>7f} [{current:>5d}/{size:>5d}]")

def test_loop(dataloader, model, loss_fun):
	loss = 0 
	for X, y in dataloader:
		pred = model.forward(X)
		loss += loss_fun(pred, y)
	print(f"Testing loss: {loss:>7f}")

if __name__ == '__main__':
	# Set device 
	device = 'cuda' if torch.cuda.is_available() else 'cpu'
	print('Using {} device'.format(device))

	# Load data 
	df = pd.read_csv(sys.argv[1])
	df['release_date'] = pd.to_datetime(df['release_date'])
	df = df.loc[df['release_date'].dt.year > 1960]
	df = df.sample(n=10000, replace=False)
	ds = SpotifyDataset(df, 
						feature_columns=SONG_FEATURES, 
						output_columns=['track_popularity'])
	train_size = int(0.7 * len(ds))
	test_size = len(ds) - train_size 
	train_dataset, test_dataset = torch.utils.data.random_split(ds, [train_size, test_size])

	train_dataloader = DataLoader(train_dataset, batch_size=64, shuffle=True)
	test_dataloader = DataLoader(test_dataset, batch_size=len(test_dataset))

	# Create model 
	pop_model = PopularityModel()
	loss_fn = nn.MSELoss()
	optim = torch.optim.SGD(pop_model.parameters(), lr=LEARNING_RATE)

	print('Training now...')
	epochs = EPOCHS 
	for i in range(epochs):
		print(f'Epoch {i+1}\n-------------------------------')
		train_loop(train_dataloader, pop_model, loss_fn, optim)
		print('\n\n')
	print('Training done...')
	test_loop(test_dataloader, pop_model, loss_fn)