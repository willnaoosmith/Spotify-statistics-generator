from spotipy.oauth2 import SpotifyOAuth
import matplotlib.dates as mdates
import matplotlib.pyplot as plt
import pandas as pd
import spotipy

#https://developer.spotify.com/documentation/web-api
spotifyClient = spotipy.Spotify(
  auth_manager=SpotifyOAuth(
    client_id="",
    client_secret="",
    redirect_uri="",
    scope=""
  )
)

def askDigit(questionMessage, validOptions={}):
	digitAnswer = ""

	while digitAnswer.isdigit() == False:
	    digitAnswer = input(questionMessage)

	    if digitAnswer.isdigit() == False:
	        print("Please, input a valid number.\n")
	    
	    else:
	    	if validOptions:	    		
	    		try:
	    			validOptions[digitAnswer]

	    		except Exception as error:
	    			print("Please, input a valid option.\n")
	    			digitAnswer = ""

	    		else:
	    			return int(digitAnswer)

	    	else:
	    		return int(digitAnswer)

tracksArray = []

TotalTracks = askDigit("How many songs do you have saved on your 'Liked songs' spotify playlist?: ")
    
trackOffset = 0
limit = 49

while trackOffset < TotalTracks:
	try:
		addedTracks = spotifyClient.current_user_saved_tracks(limit=limit, offset=trackOffset)['items']
		addedTracksFeatures = spotifyClient.audio_features([track['track']['id'] for track in addedTracks])	

		for track in addedTracks:
			
			track = {
				"releaseDate": track['track']['album']['release_date'],
				"popularity": track['track']['popularity'],
				"addedDate": track['added_at'],
				"id": track['track']['id']
			}

			trackData = [
				"instrumentalness",
				"acousticness",
				"danceability",
				"speechiness",
				"duration_ms",
				"loudness",
				"liveness",
				"valence",
				"energy",
				"tempo",			
				"key"
			]

			currentTrackFeature = next(filter(lambda item: item["id"] == track['id'], addedTracksFeatures), None)

			trackData = {key:value for key, value in currentTrackFeature.items() if key in trackData}

			track.update(trackData)

			tracksArray.append(track)

	except Exception as error:
		print("An error ocurred while fetching! Continuing with the next batch...")

	finally:
		if (TotalTracks - trackOffset) >= limit:
			trackOffset = trackOffset + limit

		else:		
			limit = (TotalTracks - trackOffset)
			trackOffset = trackOffset + (TotalTracks - trackOffset)

	print(f"{trackOffset} songs of {TotalTracks} fetched.")

df = pd.DataFrame(tracksArray)

df['addedDate'] = pd.to_datetime(df['addedDate'])

df['year'] = df['addedDate'].dt.year
df['month'] = df['addedDate'].dt.month
df['yearMonth'] = df['addedDate'].dt.tz_localize(None).dt.to_period('M').dt.to_timestamp()
df['week'] = df['addedDate'].dt.isocalendar().week
df['yearWeek'] = df.apply(lambda row: pd.to_datetime(f"{row['year']}-W{row['week']}-1", format="%Y-W%W-%w"), axis=1)

numeric_columns = df.select_dtypes(include='number').columns

print("")
generateType = askDigit("""How do you want to group your graph?
	1) By months of the year.
	2) By weeks of the year.

Chosse an option: """, {"1": "month", "2": "weeks"})

if generateType == "week":
	df_grouped = df.groupby('yearWeek')[numeric_columns].median().reset_index()
else:
	df_grouped = df.groupby('yearMonth')[numeric_columns].median().reset_index()

attributes = [
    'popularity', 'danceability', 'energy', 'key', 'loudness', 'speechiness', 
    'acousticness', 'instrumentalness', 'liveness', 'valence', 'tempo', 'duration_ms'
]

for attribute in attributes:
    if attribute in df_grouped.columns:
        plt.figure(figsize=(12, 6))
        
        if generateType == "week":
        	plt.plot(df_grouped['yearWeek'], df_grouped[attribute], marker='o', linestyle='-')
        	plt.xlabel('Year-Week')        
        	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%W'))
        	plt.gca().xaxis.set_major_locator(mdates.WeekdayLocator())

        else:
        	plt.plot(df_grouped['yearMonth'], df_grouped[attribute], marker='o', linestyle='-')
        	plt.xlabel('Year-Month')
        	plt.gca().xaxis.set_major_formatter(mdates.DateFormatter('%Y-%m'))
        	plt.gca().xaxis.set_major_locator(mdates.MonthLocator())

        plt.ylabel(attribute)
        plt.title(f'{attribute} Over Time')        
        plt.xticks(rotation=45)
        plt.tight_layout()
        plt.grid(True)
        plt.show()