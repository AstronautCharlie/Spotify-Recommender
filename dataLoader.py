import torch 
import sys 

from torch.utils.data import Dataset, DataLoader  
from dataReader import * 

class SpotifyDataset(Dataset):
	'''
	Dataset wrapper to the Spotify data. Takes in a pandas Dataframe and 
	two lists, one of feature columns and the other of outputs
	'''
	def __init__(self, df, feature_columns, output_columns):
		self.df = df
		self.features = feature_columns
		self.outputs = output_columns

	def __len__(self):
		return len(self.df[self.features].values)

	def __getitem__(self, idx): 
		features = torch.tensor(self.df[self.features].values)
		features = features.type(torch.FloatTensor)
		outputs = torch.tensor(self.df[self.outputs].values)
		outputs = outputs.type(torch.FloatTensor)
		feature = features[idx]
		output = outputs[idx]
		return feature, output 

if __name__ == '__main__':
	input_file = pd.read_csv(sys.argv[1], index_col=False)
	#print(input_file)
	ds = SpotifyDataset(input_file, 
						feature_columns=SONG_FEATURES, 
						output_columns=['track_popularity'])
	#print(len(ds))
	#print(ds[0])
	train_dataloader = DataLoader(ds, batch_size=2, shuffle=True)
	train_features, train_labels = next(iter(train_dataloader))
	print(train_features, type(train_features))
	print(train_labels, type(train_labels))
