import mido

class Note():
    '''
    class representing a sound to be made 
    by a part
    '''
    def __init__(self, start, end, pitch, solfa, conductor):
        self.start=start
        self.end=end
        self.solfa=solfa
        self.pitch=pitch
        self.conductor=conductor
        self.duration=f=self.get_duration(start,end)
        try:
            self.error=False
            self._duration=self.duration*(self.conductor.bpm/60)
        except:
            self.error=True
        
        self.type= self.get_type(solfa)
        self.note= self.get_letter()
        self.note_number= self.get_note_number()
        self.extensions=[] 
        self.prev=None
        self.next=None
        self.sound=None

    def __str__(self):
        return self.note
            
    @property
    def length(self,*a):
        return self.duration *1000
    
    def do_extension(self,child):
        '''
        extends the note longer than a second
        '''
        self.duration+=child.duration
        self.extensions.append(child)
    
    def is_silent(self):
        return True if self.type == 'silence' else False
        
    def get_type(self,solfa):
           if solfa == 'x':
               return 'silence'
           elif solfa == '-':
               return 'extension'
           else:
               return 'normal'
           
    def get_letter(self):
        ##TODO
        #Edit Later
        
        try:
            return self.conductor.scale[self.solfa]
        except:
            print(self.solfa)
            print(f'error')
     
    def get_note_number(self):
        '''get the midi note number representing this class'''
        if self.type != 'normal':
            return 0
        k= self.conductor.letters
        s={kk:{i:j for i, j in enumerate(range(k.index(kk),128,12))} for kk in k}
        
        n=s.get(self.note).get(self.conductor.pitch+self.pitch+self.conductor.offset(self.note))  
        
        return n
        
    def get_duration(self,start,end):
        '''
        get duration of note based on the mode the tonic solfa was written, either dynamic or static
        Currently I have implementes the feature to switch from dynamic to static,
        Currently set to dynamic
        '''
        if self.conductor.mode=='dynamic':
            dur=end
            if dur in (':'):
                return 60/self.conductor.bpm
            
            if dur in ('.'):
                return (60/self.conductor.bpm)* .5
            
            if dur in (','):
                return (60/self.conductor.bpm)* .25
        else:
            dur=start+end
            if dur in ('::', ':|', '|:', ':|', '||'):
                return 60/self.conductor.bpm
            
            if dur in (':.', '.|', '|.', '.:'):
                return (60/self.conductor.bpm)* .5
            
            if dur in (':,', ',:', ',|', '|,', '.,', ',.'):
                return (60/self.conductor.bpm)* .25

