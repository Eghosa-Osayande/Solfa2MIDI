
from .note import Note
from .instrument import Instrument


time_markers={ ':': 1, '.': 0.5, ',': 0.25, '|': 1}

class Part():
    '''
    Class representing a part in the music 
    '''
    def __init__(self,**kwargs):
        self.name= kwargs.get('name')
        self.id= kwargs.get('id')
        self.volume= kwargs.get('volume')
        self.instrument= kwargs.get('instrument')
        self.channel= kwargs.get('channel')
        self.conductor=kwargs.get('conductor')
        self.start_time=kwargs.get('start_time',0)
        
        _raw_score= None
        self.notes = None 
    
    def get_solfa(self):
        '''
        returns list containing tuples of solfa, duration and relative pitch
        '''
        return [(n.solfa,n._duration,n.pitch) for n in self.notes]
    
    def make_music(self, conductor):
        '''
       returns the MIDI track of the part
        '''
        return Instrument(self.instrument, self.name,self.volume, self.channel, conductor, self.notes,self.start_time).play()
                    
    
    def read_sheet(self, conductor):
        
        '''
        this function reads the solfa notation and returns list of notes
        
        '''
        key, pitch, bpm, scale = conductor.key, conductor.pitch,conductor.bpm, conductor.scale
        
        notes=[]
        start=''
        _pitch=''
        pitch=0
        solfa=''
        end=''
        songpos=self.start_time
        skip=0

        for index,char in enumerate(self.sheet,0):
            
            if skip:
                skip-=1
                print(skip)
                continue
            if char in '<':
                values=self.sheet[index : self.sheet[index:].index('>')+index]               
                v=values[1:]
                skip=len(values)
                self.conductor.get_dynamic_music_code(v,songpos)
                continue
            if char in time_markers.keys():
                if start != '' :
                    end=char
                    if solfa != '':
                        n=Note(start,end, pitch, solfa,conductor)
                        if n.error:
                            print(n.solfa, start, end, '\n', self.sheet[:index])
                            exit()
                        if solfa=='-':
                            notes[-1].do_extension(n)
                        else:
                            if len(notes)>0:
                                prev=notes[-1]
                                n.prev=prev
                                prev.next=n 
                            notes.append(n)
                            
                        songpos+=n.duration
                        start=''
                        _pitch=''
                        pitch=0
                        solfa=''
                        end=''
                        
                        
                start=char
                continue
            if char.isalpha() or char=='-' or char =='x':
                solfa+=char
                
            if char =="'":
              _pitch+=char
              pitch= len(_pitch)*-1 if solfa == '' else len(_pitch)*1
              
        self.notes= notes      
    
    def set_sheet(self, raw_score):
        '''
        sets the sheet for the part
        and checks if there is any error
        '''
        if raw_score:
            self._raw_score=r=raw_score.splitlines()
            raw_sheet=r= self._get_raw_sheet()
            sheet= self.check_syntax(raw_sheet)
            self.sheet=sheet
            
        else:
            self.sheet=sheet='|x:|'        
        #print(sheet)
        return sheet if sheet else False
        
    def check_syntax(self,score):
        #TODO
        #False means error
        return score #False
    
    def _get_raw_sheet(self):
        
        raw_sheet=''
        for line in self._raw_score:
            line='|'+line
            line=line.replace('\t','').replace(' ','').replace('\n','')
            raw_sheet+=line
            if 0:#line.startswith(self.id):
                line=line.replace(self.id,'')
                raw_sheet+=line
        
        return raw_sheet