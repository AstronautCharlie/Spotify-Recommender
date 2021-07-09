Files of interest: 
- dataReader.py 
- dataLoader.py 
- popNetwork.py 

dataReader.py: 
- Takes in a csv of artists or albums, looks up all the relevant songs, and queries the API for the track features. Columns must be labelled. Right now, the file looks up based on album name. The functionality to take in artists and look up all the albums for that artists exists in the code (just use the method 'artists_to_albums' by searching for 'artist' in line 207 and uncommenting out line 208 and maybe remove the 5 album limit), but that is not part of the main method right now. It will save the results into a csv file with the name '[original file name]_transformed.csv'
- To run it, enter 'python dataReader.py [csv file name]' into the command line. 
- CSV file should have one column and look like this: 
'album'
album1
album2
album3
...

dataLoader.py:
- Defines a PyTorch Dataset used in the neural network. PyTorch requires a Dataset object. No need to run this

popNetwork.py: 
- Defines the architecture for the popularity predictor and trains the network. Takes in the file rendered by dataReader.py. As it's set up right now, it filters out all songs from before 1960. To remove this, comment out line 59. It also randomly samples 10,000 tracks from the file. To remove this, comment out line 60. It divides the tracks into a 70/30 split, where the 70% is used to train and 30% used to test. See lines 64-66 for details. 
- To run it, enter 'python popNetwork.py [csv file name]' into the command line. 
