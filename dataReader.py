'''
This script handles getting and manipulating data. 

Defines a Table/Field classes, main data type for storing 
spotify data. Table is a modified pandas Dataframe. 

Data is stored as csvs 
'''
import spotipy
import pandas as pd 
import numpy as np 
import sys 
import torch 

from spotipy import SpotifyOAuth

SONG_FEATURES = ['danceability', 
				 'energy',
				 #'key', 
				 'loudness', 
				 'mode', 
				 'speechiness', 
				 'acousticness', 
				 'liveness', 
				 'valence', 
				 'tempo']#, 
				 #'duration_ms', 
				 #'time_signature']

class DataReader():
	'''
	Takes a spotipy.Spotify object 
	'''
	def __init__(self, spotifyObject):
		self._sp = spotifyObject 
		self.df = None 
		self.csv_file = None 

	def read_csv(self, csv_file): 
		'''
		Read in csv file and set self.df to result 
		'''
		df = pd.read_csv(csv_file, header=0)
		df = df.astype(str)
		for row in df: 
			df[row] = df[row].astype(str)
		self.df = df 

	def search_id(self, column, overwrite=False):
		if column + '_id' in self.df.columns and not overwrite:
			raise ValueError('DataReader already has id dataframe. Set overwrite=True to delete old id column')
		#print('search')
		
		if column not in self.df.columns:
			raise ValueError('self.df is not defined')

		if column not in self.df.columns:
			raise ValueError('Cannot search ' + kwargs['type'] + '; column matching type is not in df')

		def apply_id_lookup(row):
			q = row[column]
			return_name = column + 's'
			results = self._sp.search(q=q, type=column)
			try:
				return results[return_name]['items'][0]['id']
			except: 
				print(f'Lookup failed for {row}')
				return None 
		def apply_name_lookup(row):
			q = row[column]
			return_name = column + 's'
			results = self._sp.search(q=q, type=column)
			return results[return_name]['items'][0]['name']

		self.df[column+'_uri'] = self.df.apply(apply_id_lookup, axis=1)
		self.df['matched_'+column+'_name'] = self.df.apply(apply_name_lookup, axis=1)

	def artist_to_albums(self, limit=10):
		'''
		Expand the 'artist' column - adds one row per album to the df 
		'''
		if 'artist_id' not in self.df.columns: 
			raise ValueError('Error in artist_to_albums: no "artist_id" column')
		
		# Look up given number of albums per artist 
		def apply_artist_to_album(row):
			results = self._sp.artist_albums(row['artist_id'], limit=limit, offset=offset)
			album_names = [] 
			album_uris = [] 
			print('Num returned albums for', row['artist'], len(results['items']))
			for i in range(len(results['items'])):
				album_names.append(results['items'][i]['name'])
				album_uris.append(results['items'][i]['uri'])
			return album_names, album_uris
		
		# Add columns to df 
		self.df['results'] = self.df.apply(apply_artist_to_album, axis=1)
		self.df[['album', 'album_uri']] = pd.DataFrame(self.df['results'].to_list(), index=self.df.index)
		self.df = self.df.drop(labels='results', axis=1)
		
		# Explode lists into rows 
		idx = self.df.index.repeat(self.df[['album', 'album_uri'][0]].str.len())
		temp_df = pd.concat([pd.DataFrame({x: np.concatenate(self.df[x].values)}) for x in ['album', 'album_uri']], axis=1)
		temp_df.index = idx 
		self.df = self.df.join(temp_df, how='left', lsuffix='_', rsuffix='')
		self.df = self.df.drop(['album_', 'album_uri_'], axis=1)
		self.df = self.df.set_index(pd.Series([i for i in range(len(self.df))]))

	def album_to_tracks(self):
		'''
		Expand self.df from album to track level
		'''
		if 'album_uri' not in self.df.columns: 
			raise ValueError('Error in albums_to_tracks: no "album_uri" column')

		def apply_album_to_tracks(row):
			results = '1' 
			offset = 0 
			song_names = [] 
			song_uris = [] 
			while True: 
				results = self._sp.album_tracks(row['album_uri'], limit=50, offset=offset)
				if len(results['items']) == 0:
					break 

				for i in range(len(results['items'])):
					song_names.append(results['items'][i]['name'])
					song_uris.append(results['items'][i]['uri'])
				offset += 50

			return song_names, song_uris 

		# Add columns to df 
		self.df['results'] = self.df.apply(apply_album_to_tracks, axis=1)
		self.df[['track', 'track_uri']] = pd.DataFrame(self.df['results'].to_list(), index=self.df.index)
		self.df = self.df.drop(labels='results', axis=1)

		# Explode lists into rows
		idx = self.df.index.repeat(self.df[['track', 'track_uri'][0]].str.len())
		temp_df = pd.concat([pd.DataFrame({x: np.concatenate(self.df[x].values)}) for x in ['track', 'track_uri']], axis=1)
		temp_df.index = idx 
		self.df = self.df.join(temp_df, how='left', lsuffix='_', rsuffix='')
		self.df = self.df.drop(['track_', 'track_uri_'], axis=1)
		self.df = self.df.set_index(pd.Series([i for i in range(len(self.df))]))

	def get_popularity(self, column):
		'''
		Get the popularity metric for the given column 
		'''
		column_uri_string = str(column) + '_uri'

		if column + '_uri' not in self.df.columns:
			raise ValueError('Error in get_popularity: no ' + str(column) + ' column')

		def apply_popularity_lookup(row):
			if column == 'artist':
				results = self._sp.artist(row[column_uri_string])
			elif column == 'album':
				results = self._sp.album(row[column_uri_string])
			elif column == 'track':
				results = self._sp.track(row[column_uri_string])
			else: 
				raise ValueError('Error in get_popularity: ' + str(column) + ' not a supported query')
			return results['popularity']

		self.df[str(column) + '_popularity'] = self.df.apply(apply_popularity_lookup, axis=1)

	def get_track_features(self):
		'''
		Get the properties for the track column. Update self.df to add 1 column per property 
		'''
		if 'track' not in self.df.columns: 
			raise ValueError('Error in get_track_properties: no track column')

		def apply_feature_lookup(row): 
			results = self._sp.audio_features([row['track_uri']])
			return results[0]

		temp_df = self.df.apply(apply_feature_lookup, axis=1)
		temp_df = pd.DataFrame(list(temp_df))
		#print(temp_df.columns)
		temp_df = temp_df.drop(['id', 'type', 'track_href', 'analysis_url'], axis=1)
		#print(temp_df.columns)
		#print(temp_df.dtypes)
		#print(self.df.columns)
		#print(self.df.dtypes)
		#print(self.df.columns)
		self.df = self.df.merge(temp_df, left_on='track_uri', right_on='uri', suffixes=('', '_'))
		self.df = self.df.reset_index()
		#print(self.df.columns)

	def data_to_tensor(self, feature_columns=[], output_columns=[]):
		'''
		Return 2 tensors, the first containing feature data and the 
		second containing the expected outputs 
		'''
		inputs = torch.tensor(self.df[feature_columns].values)
		outputs = torch.tensor(self.df[output_columns].values)
		return inputs, outputs 

if __name__ == '__main__': 
	sp = spotipy.Spotify(auth_manager=SpotifyOAuth())
	dr = DataReader(sp)
	dr.read_csv(sys.argv[1])
	print(dr.df)

	dr.search_id('album')
	#dr.artist_to_albums(limit=5)
	dr.album_to_tracks()
	#print(dr.df.to_string())
	dr.get_popularity('track')
	#print(dr.df.loc[dr.df['album'] == '69 Love Songs'])
	dr.get_track_features()
	dr.data_to_tensor(feature_columns=SONG_FEATURES)
	file_name = sys.argv[1].replace('.csv', '')
	dr.df.to_csv(file_name + '_transformed.csv')
	#print(dr.df[['artist', 'album']].drop_duplicates())#.to_string())
	#print(dr.df.to_string())
