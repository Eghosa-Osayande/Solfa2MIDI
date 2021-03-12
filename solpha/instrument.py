import mido

class Instrument():
    '''class representing midi instrument'''
    letters='C Cs D Ds E F Fs G Gs A As B'.lower().replace(' ',',').split(',')
    programs={1: 'Acoustic', 2: 'Bright', 3: 'Electric', 4: 'Honky-tonk', 5: 'Electric', 6: 'Electric', 7: 'Harpsichord', 8: 'Clavinet', 9: 'Celesta', 10: 'Glockenspiel', 11: 'Music', 12: 'Vibraphone', 13: 'Marimba', 14: 'Xylophone', 15: 'Tubular', 16: 'Dulcimer', 17: 'Drawbar', 18: 'Percussive', 19: 'Rock', 20: 'Church', 21: 'Reed', 22: 'Accordion', 23: 'Harmonica', 24: 'Acoustic', 25: 'Acoustic', 26: 'Electric', 27: 'Electric', 28: 'Electric', 29: 'Overdriven', 30: 'Distortion', 31: 'Guitar', 32: 'Acoustic', 33: 'Electric', 34: 'Electric', 35: 'Fretless', 36: 'Slap', 37: 'Slap', 38: 'Synth', 39: 'Synth', 40: 'Violin', 41: 'Viola', 42: 'Cello', 43: 'Contrabass', 44: 'Tremolo', 45: 'Pizzicato', 46: 'Orchestral', 47: 'Timpani', 48: 'String', 49: 'String', 50: 'Synth', 51: 'Synth', 52: 'Choir', 53: 'Voice', 54: 'Synth', 55: 'Orchestra', 56: 'Trumpet', 57: 'Trombone', 58: 'Tuba', 59: 'Muted', 60: 'French', 61: 'Brass', 62: 'Synth', 63: 'Synth', 64: 'Soprano', 65: 'Alto', 66: 'Tenor', 67: 'Baritone', 68: 'Oboe', 69: 'English', 70: 'Bassoon', 71: 'Clarinet', 72: 'Piccolo', 73: 'Flute', 74: 'Recorder', 75: 'Pan', 76: 'Blown', 77: 'Shakuhachi', 78: 'Whistle', 79: 'Ocarina', 80: 'Lead', 81: 'Lead', 82: 'Lead', 83: 'Lead', 84: 'Lead', 85: 'Lead', 86: 'Lead', 87: 'Lead', 88: 'Pad', 89: 'Pad', 90: 'Pad', 91: 'Pad', 92: 'Pad', 93: 'Pad', 94: 'Pad', 95: 'Pad', 96: 'FX', 97: 'FX', 98: 'FX', 99: 'FX', 100: 'FX', 101: 'FX', 102: 'FX', 103: 'FX', 104: 'Sitar', 105: 'Banjo', 106: 'Shamisen', 107: 'Koto', 108: 'Kalimba', 109: 'Bagpipe', 110: 'Fiddle', 111: 'Shanai', 112: 'Tinkle', 113: 'Agogo', 114: 'Steel', 115: 'Woodblock', 116: 'Taiko', 117: 'Melodic', 118: 'Synth', 119: 'Reverse', 120: 'Guitar', 121: 'Breath', 122: 'Seashore', 123: 'Bird', 124: 'Telephone', 125: 'Helicopter', 126: 'Applause', 127: 'Gunshot'}
    
    def __init__(self,program, name, volume, channel, conductor,notes,start_time):
       self.program= int(program)
       self.conductor= conductor
       self.notes= notes
       self.name=name
       self.volume=int(volume)
       self.channel=int(channel)
       self.start_time=int(mido.second2tick(
                        start_time,
                        480,
                        int(mido.bpm2tempo(self.conductor.bpm))
                        ))
        
    def play(self):
        '''returns midi track from list of notes'''
        track_name=mido.MetaMessage('track_name',name=self.name)
        tempo=mido.MetaMessage('set_tempo',tempo=int(mido.bpm2tempo(self.conductor.bpm)))
        time= mido.MetaMessage('time_signature',numerator=self.conductor.config.NUMERATOR, denominator=self.conductor.config.DENOMINATOR)
        key= mido.MetaMessage('key_signature', key= self.conductor.key)
        program= mido.Message('program_change', program= int(self.program),channel=int(self.channel))
        track=mido.MidiTrack()
        track.append(track_name)
        track.append(tempo)
        track.append(time)
        track.append(key)
        track.append(program)
        for note in self.notes:
            if note.is_silent():
                volume=0
            else:
                volume=self.volume
            
            
            track.append(
                mido.Message(
                    'note_on',
                    channel=self.channel, 
                    note=note.note_number, 
                    velocity= volume, 
                    time= self.start_time,
                    )
                )
            self.start_time=0   
            track.append(
                mido.Message(
                    'note_on',
                    channel=self.channel, 
                    note=note.note_number, 
                    velocity= 0, 
                    time= int(mido.second2tick(
                        note.duration,
                        480,
                        int(mido.bpm2tempo(self.conductor.bpm))
                        ))
                    )
                )   
        return track    