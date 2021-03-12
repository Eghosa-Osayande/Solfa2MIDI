from .part import Part
import mido
import os

class Cfg():
    '''
    Cfg contains the settings read from the
    solfa score
    '''
    def __init__(self,TITLE, TONIC, TONIC_PITCH, BPM, PARTS, SCORE,MODE, NUMERATOR, DENOMINATOR):
        self.TITLE=TITLE
        self.TONIC=TONIC
        self.TONIC_PITCH=TONIC_PITCH
        self.BPM=BPM
        self.PARTS=PARTS
        self.SCORE=SCORE
        self.MODE=MODE
        self.NUMERATOR=NUMERATOR
        self.DENOMINATOR=DENOMINATOR
        
class Conductor():
    '''
    The conductor is responsible for parsing 
    the contents of the solfa score and retrieving 
    important settings for the song.
    This class also serves as the cordinator for the different parts
    '''
    letters='C C# D D# E F F# G G# A A# B'.replace(' ',',').split(',')
    _scale= None
    _raw_score=None
    
    def __init__(self, config):
        self.config=config
        self.key= self.config.TONIC
        self.pitch= self.config.TONIC_PITCH
        self.bpm= self.config.BPM
        self.song_title = self.config.TITLE
        self.mode= self.config.MODE
        parts= self.config.PARTS
        self.parts=[]
       
        for channel,part in enumerate(parts):
            self.parts.append(Part(
                name=part['name'],
                id= part['id'],
                volume=part['volume'],
                instrument=part['instrument'],
                conductor=self,
                channel=channel,
            ))
            self.next_channel=channel+1
       
    def offset(self,note):
        '''
        function to help correctly match notes to
        their relative pitch
        '''
        ref= self.letters.index(self.key)
        return 1 if note in self.letters[:ref] else 0
        
    
    @property    
    def scale(self,*a):
        '''
        returns dict containing the solfa notes and their corresponding letters
        '''
        if self._scale:
            return self._scale
        ref= self.letters.index(self.key)
        new_scale=t=self.letters[ref:]+self.letters[:ref]
        
        scale ={
            'd':new_scale[0], 'de':new_scale[1],
            'r':new_scale[2], 're':new_scale[3], 
            'm':new_scale[4], 'f':new_scale[5], 
            'fe':new_scale[6], 's':new_scale[7], 
            'se':new_scale[8], 'l':new_scale[9], 
            'le':new_scale[10], 't':new_scale[11],
            'ta':new_scale[10], 'soh':new_scale[6], 
            'ma':new_scale[3], 'ra':new_scale[1],
            '-':'-', 'x':'x' 
        }
        
        self._scale=scale
        return scale
    
    def process_data(self,data):
        '''
        parses the solfa score and returns the Cfg class containing the required settings
        '''
        exec(data, globals())
        c=Cfg(TITLE, TONIC, TONIC_PITCH,BPM, PARTS,SCORE,MODE,NUMERATOR, DENOMINATOR)
        return c
    
    def get_solfa(self):
        '''
        returns list of lists containing notes for respective parts
        '''
        return [p.get_solfa() for p in self.parts]
    
    @property
    def raw_score(self,*a):
        '''
        returns score as a list containing each line
        '''
        if self._raw_score:
            return self._raw_score
        score=self.config.SCORE
        self._raw_score=score.splitlines()
        return self._raw_score 
    
    def get_music_code(self):
        '''
        step 1 
        Conductor asks,       
        'Parts check for errors
        if any raise error
        else set your sheet'
        #TODO
        '''
        results=[]
        for part in self.parts:
            results.append(part.set_sheet(self.config.SCORE.get(part.id)))
        if False in results:
            print('syntax error')
            
        '''
        Step 2
        Conductor says,
        Parts read your sheet
        tell me each note and its duration
        '''
        instructions=[]
        for part in self.parts:
            part.read_sheet(self)
            
    def get_dynamic_music_code(self,a,start_time):
        '''
        handles dynamic creation of music parts
        when parsing music score
        '''
        a=a.split(',')
        self.parts.append(Part(
                name=a[0],
                id= a[1],
                volume=int(a[2]),
                instrument=int(a[3]),
                conductor=self,
                channel=self.next_channel,
                start_time=start_time,
            ))
        self.parts[-1].set_sheet(self.config.SCORE.get(self.parts[-1].id))
        self.next_channel+=1
       
    def produce(self):
        '''saves music to a midi file'''
        mid = mido.MidiFile()
        for part in self.parts:
            mid.tracks.append(part.make_music(self))
        filename=self.config.TITLE+'.mid'
        mid.save(filename)
        
        return os.path.join(os.getcwd(),filename)
             
             
        
            
