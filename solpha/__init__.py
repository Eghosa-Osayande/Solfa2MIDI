import json
import mido
import os


time_markers = {":": 1, ".": 0.5, ",": 0.25, "|": 1}


class Instrument:
    """class representing midi instrument"""

    letters = "C Cs D Ds E F Fs G Gs A As B".lower().replace(" ", ",").split(",")
    programs = {
        1: "Acoustic",
        2: "Bright",
        3: "Electric",
        4: "Honky-tonk",
        5: "Electric",
        6: "Electric",
        7: "Harpsichord",
        8: "Clavinet",
        9: "Celesta",
        10: "Glockenspiel",
        11: "Music",
        12: "Vibraphone",
        13: "Marimba",
        14: "Xylophone",
        15: "Tubular",
        16: "Dulcimer",
        17: "Drawbar",
        18: "Percussive",
        19: "Rock",
        20: "Church",
        21: "Reed",
        22: "Accordion",
        23: "Harmonica",
        24: "Acoustic",
        25: "Acoustic",
        26: "Electric",
        27: "Electric",
        28: "Electric",
        29: "Overdriven",
        30: "Distortion",
        31: "Guitar",
        32: "Acoustic",
        33: "Electric",
        34: "Electric",
        35: "Fretless",
        36: "Slap",
        37: "Slap",
        38: "Synth",
        39: "Synth",
        40: "Violin",
        41: "Viola",
        42: "Cello",
        43: "Contrabass",
        44: "Tremolo",
        45: "Pizzicato",
        46: "Orchestral",
        47: "Timpani",
        48: "String",
        49: "String",
        50: "Synth",
        51: "Synth",
        52: "Choir",
        53: "Voice",
        54: "Synth",
        55: "Orchestra",
        56: "Trumpet",
        57: "Trombone",
        58: "Tuba",
        59: "Muted",
        60: "French",
        61: "Brass",
        62: "Synth",
        63: "Synth",
        64: "Soprano",
        65: "Alto",
        66: "Tenor",
        67: "Baritone",
        68: "Oboe",
        69: "English",
        70: "Bassoon",
        71: "Clarinet",
        72: "Piccolo",
        73: "Flute",
        74: "Recorder",
        75: "Pan",
        76: "Blown",
        77: "Shakuhachi",
        78: "Whistle",
        79: "Ocarina",
        80: "Lead",
        81: "Lead",
        82: "Lead",
        83: "Lead",
        84: "Lead",
        85: "Lead",
        86: "Lead",
        87: "Lead",
        88: "Pad",
        89: "Pad",
        90: "Pad",
        91: "Pad",
        92: "Pad",
        93: "Pad",
        94: "Pad",
        95: "Pad",
        96: "FX",
        97: "FX",
        98: "FX",
        99: "FX",
        100: "FX",
        101: "FX",
        102: "FX",
        103: "FX",
        104: "Sitar",
        105: "Banjo",
        106: "Shamisen",
        107: "Koto",
        108: "Kalimba",
        109: "Bagpipe",
        110: "Fiddle",
        111: "Shanai",
        112: "Tinkle",
        113: "Agogo",
        114: "Steel",
        115: "Woodblock",
        116: "Taiko",
        117: "Melodic",
        118: "Synth",
        119: "Reverse",
        120: "Guitar",
        121: "Breath",
        122: "Seashore",
        123: "Bird",
        124: "Telephone",
        125: "Helicopter",
        126: "Applause",
        127: "Gunshot",
    }

    def __init__(self, program, name, volume, channel, conductor, notes, start_time):
        self.program = int(program)
        self.conductor = conductor
        self.notes = notes
        self.name = name
        self.volume = int(volume)
        self.channel = int(channel)
        self.start_time = int(
            mido.second2tick(start_time, 480, int(mido.bpm2tempo(self.conductor.bpm)))
        )

    def play(self):
        """returns midi track from list of notes"""
        track_name = mido.MetaMessage("track_name", name=self.name)
        tempo = mido.MetaMessage(
            "set_tempo", tempo=int(mido.bpm2tempo(self.conductor.bpm))
        )
        time = mido.MetaMessage(
            "time_signature",
            numerator=self.conductor.config.NUMERATOR,
            denominator=self.conductor.config.DENOMINATOR,
        )
        key = mido.MetaMessage("key_signature", key=self.conductor.key)
        program = mido.Message(
            "program_change", program=int(self.program), channel=int(self.channel)
        )
        track = mido.MidiTrack()
        track.append(track_name)
        track.append(tempo)
        track.append(time)
        track.append(key)
        track.append(program)
        for note in self.notes:
            if note.is_silent():
                volume = 0
            else:
                volume = self.volume

            track.append(
                mido.Message(
                    "note_on",
                    channel=self.channel,
                    note=note.note_number,
                    velocity=volume,
                    time=self.start_time,
                )
            )
            self.start_time = 0
            track.append(
                mido.Message(
                    "note_on",
                    channel=self.channel,
                    note=note.note_number,
                    velocity=0,
                    time=int(
                        mido.second2tick(
                            note.duration, 480, int(mido.bpm2tempo(self.conductor.bpm))
                        )
                    ),
                )
            )
        return track

class Note:
    """
    class representing a sound to be made
    by a part
    """

    def __init__(self, start, end, pitch, solfa, part):
        self.start = start
        self.end = end
        self.solfa = solfa
        self.pitch = pitch
        self.part = part
        self.conductor = part.conductor
        self.duration = f = self.get_duration(start, end)
        try:
            self.error = False
            self._duration = self.duration * (self.conductor.bpm / 60)
        except:
            self.error = True

        self.type = self.get_type(solfa)
        self.note = self.get_letter()
        self.note_number = self.get_note_number()
        self.extensions = []
        self.prev = None
        self.next = None
        self.sound = None

    def __str__(self):
        return self.note

    @property
    def length(self, *a):
        return self.duration * 1000

    def do_extension(self, child):
        """
        extends the note longer than a second
        """
        self.duration += child.duration
        self.extensions.append(child)

    def is_silent(self):
        return True if self.type == "silence" else False

    def get_type(self, solfa):
        if solfa == "x" or solfa.strip() == "":
            return "silence"
        elif solfa == "-":
            return "extension"
        else:
            return "normal"

    def get_letter(self):
        ##TODO
        # Edit Later

        try:
            return self.conductor.scale[self.solfa]
        except:
            print(self.solfa)
            print(f"error")

    def get_note_number(self):
        """get the midi note number representing this class"""
        if self.type != "normal":
            return 0
        k = self.conductor.letters
        s = {kk: {i: j for i, j in enumerate(range(k.index(kk), 128, 12))} for kk in k}

        n = s.get(self.note).get(
            self.conductor.pitch + self.pitch + self.conductor.offset(self.note)
        )

        return n

    def get_duration(self, start, end):
        """
        get duration of note based on the mode the tonic solfa was written, either dynamic or static
        Currently I have implementes the feature to switch from dynamic to static,
        Currently set to dynamic
        """
        if self.part.mode == "dynamic":
            dur = end
            if dur in (":"):
                return 60 / self.conductor.bpm

            if dur in ("."):
                return (60 / self.conductor.bpm) * 0.5

            if dur in (","):
                return (60 / self.conductor.bpm) * 0.25
        else:
            dur = start + end
            if dur in ("::", ":|", "|:", ":|", "||"):
                return 60 / self.conductor.bpm

            if dur in (":.", ".:", "|.", ".|"):
                return (60 / self.conductor.bpm) * 0.5

            if dur in (":,", ",:", ",.", ".,", "|,", ",|"):
                return (60 / self.conductor.bpm) * 0.25

class Part:
    """
    Class representing a part in the music
    """

    def __init__(self, **kwargs):
        self.name = kwargs.get("name")
        self.volume = kwargs.get("volume")
        self.instrument = kwargs.get("instrument")
        self.channel = kwargs.get("channel")
        self.conductor = kwargs.get("conductor")
        self.start_time = kwargs.get("start_time", 0)
        self.mode = kwargs.get("mode")
        self._data = kwargs.get("score")

        _raw_score = None
        self.notes = None

    def get_solfa(self):
        """
        returns list containing tuples of solfa, duration and relative pitch
        """
        return [(n.solfa, n._duration, n.pitch) for n in self.notes]

    def make_music(self, conductor):
        """
        returns the MIDI track of the part
        """
        return Instrument(
            self.instrument,
            self.name,
            self.volume,
            self.channel,
            conductor,
            self.notes,
            self.start_time,
        ).play()

    def read_sheet(self, conductor):
        """
        this function reads the solfa notation and returns list of notes

        """
        key, pitch, bpm, scale = (
            conductor.key,
            conductor.pitch,
            conductor.bpm,
            conductor.scale,
        )

        notes = []
        start = ""
        _pitch = ""
        pitch = 0
        solfa = ""
        end = ""
        songpos = self.start_time
        skip = 0

        for index, char in enumerate(self.sheet, 0):

            if skip:
                skip -= 1
                print(skip)
                continue
            if char in time_markers.keys():
                if start != "":
                    end = char

                    n = Note(start, end, pitch, solfa, self)
                    if n.error:
                        print(n.solfa, start, end, "\n", self.sheet[:index])
                        exit()
                    if solfa == "-":
                        notes[-1].do_extension(n)
                    else:
                        if len(notes) > 0:
                            prev = notes[-1]
                            n.prev = prev
                            prev.next = n
                        notes.append(n)

                    songpos += n.duration
                    start = ""
                    _pitch = ""
                    pitch = 0
                    solfa = ""
                    end = ""

                start = char
                continue
            if char.isalpha() or char == "-" or char == "x":
                solfa += char

            if char == "'":
                _pitch += char
                pitch = len(_pitch) * -1 if solfa == "" else len(_pitch) * 1

        self.notes = notes

    def set_sheet(self):
        """
        sets the sheet for the part
        and checks if there is any error
        """

        self._raw_score = r = self._data.splitlines()
        raw_sheet = r = self._get_raw_sheet()
        sheet = self.check_syntax(raw_sheet)
        self.sheet = sheet

        return sheet if sheet else False

    def check_syntax(self, score):
        # TODO
        # False means error
        return score  # False

    def _get_raw_sheet(self):

        raw_sheet = ""
        for line in self._raw_score:
            line = "|" + line
            line = line.replace("\t", "").replace(" ", "").replace("\n", "")
            raw_sheet += line

        return raw_sheet

class Config:
    """
    Cfg contains the settings read from the
    solfa score
    """

    def __init__(
        self,
        title,
        tonic,
        tonic_pitch,
        bpm,
        parts,
        numerator,
        denominator,
    ):
        self.TITLE = title
        self.TONIC = tonic
        self.TONIC_PITCH = tonic_pitch
        self.BPM = bpm
        self.PARTS = parts
        self.NUMERATOR = numerator
        self.DENOMINATOR = denominator

class Score:
    """
    The conductor is responsible for parsing
    the contents of the solfa score and retrieving
    important settings for the song.
    This class also serves as the cordinator for the different parts
    """

    letters = "C C# D D# E F F# G G# A A# B".replace(" ", ",").split(",")
    _scale = None
    _raw_score = None

    def __init__(self, config):
        self.config = config
        self.key = self.config.TONIC
        self.pitch = self.config.TONIC_PITCH
        self.bpm = self.config.BPM
        self.song_title = self.config.TITLE
        parts = self.config.PARTS
        self.parts = []

        for channel, part in enumerate(parts):
            self.parts.append(
                Part(
                    name=part["name"],
                    volume=part["volume"],
                    instrument=part["instrument"],
                    conductor=self,
                    channel=channel,
                    mode=part["mode"],
                    score=part["score"],
                )
            )
            self.next_channel = channel + 1

    def offset(self, note):
        """
        function to help correctly match notes to
        their relative pitch
        """
        ref = self.letters.index(self.key)
        return 1 if note in self.letters[:ref] else 0

    @property
    def scale(self, *a):
        """
        returns dict containing the solfa notes and their corresponding letters
        """
        if self._scale:
            return self._scale
        ref = self.letters.index(self.key)
        new_scale = t = self.letters[ref:] + self.letters[:ref]

        scale = {
            "d": new_scale[0],
            "de": new_scale[1],
            "r": new_scale[2],
            "re": new_scale[3],
            "m": new_scale[4],
            "f": new_scale[5],
            "fe": new_scale[6],
            "s": new_scale[7],
            "se": new_scale[8],
            "l": new_scale[9],
            "le": new_scale[10],
            "t": new_scale[11],
            "ta": new_scale[10],
            "soh": new_scale[6],
            "ma": new_scale[3],
            "ra": new_scale[1],
            "-": "-",
            "x": "x",
            "": "x",
        }

        self._scale = scale
        return scale

    def get_solfa(self):
        """
        returns list of lists containing notes for respective parts
        """
        return [p.get_solfa() for p in self.parts]

    def get_music_code(self):
        """
        step 1
        Conductor asks,
        'Parts check for errors
        if any raise error
        else set your sheet'
        #TODO
        """
        results = []
        for part in self.parts:
            results.append(part.set_sheet())
        if False in results:
            print("syntax error")

        """
        Step 2
        Conductor says,
        Parts read your sheet
        tell me each note and its duration
        """
        instructions = []
        for part in self.parts:
            part.read_sheet(self)

    def produce(self):
        """saves music to a midi file"""
        mid = mido.MidiFile()
        for part in self.parts:
            mid.tracks.append(part.make_music(self))
        filename = self.config.TITLE + ".mid"
        mid.save(filename)

        return os.path.join(os.getcwd(), filename)


def create_score(filename):
    """
    parses the solfa score and returns the Cfg class containing the required settings
    """
    # exec(data, globals())
    fd = open(filename, "r")
    json_data = json.loads(fd.read())
    fd.close()

    # Bind the JSON values to the Cfg class
    c = Config(
        title=json_data["TITLE"],
        tonic=json_data["TONIC"],
        tonic_pitch=json_data["TONIC_PITCH"],
        bpm=json_data["BPM"],
        parts=json_data["PARTS"],
        numerator=json_data["NUMERATOR"],
        denominator=json_data["DENOMINATOR"],
    )

    score = Score(config=c)

    return score
