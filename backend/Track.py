class Track():
    def __init__(
        self, 
        id,
        title,
        playDate,
        valence,
        acousticness=None,
        danceability=None,
        energy=None,
        speechiness=None,
        tempo=None):
        
        self.spotifyID = id
        self.title = title
        self.playDate = playDate
        self.valence = valence
        self.acousticness = acousticness
        self.danceability = danceability
        self.energy = energy
        self.speechiness = speechiness
        self.tempo = tempo       
        
    def asJSON(self):
        return self.__dict__