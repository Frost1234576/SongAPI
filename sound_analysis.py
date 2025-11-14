from dataclasses import dataclass

@dataclass
class Instrument:
	volume: float
	loop: bool = False   # background rhythm layer
	melody: bool = False # main tune layer
	accents: bool = False # decorative layer

INSTRUMENT_VOLUME = {
	"banjo": 1,
	"bass": 1.2,
	"bd": 0.9,
	"bell": 1.1,
	"bit": 1.3,
	"cow_bell": 1.3,
	"didgeridoo": 1.1,
	"flute":1.3,
	"guitar": 0.8,
	"harp": 0.7,
	"hat": 0.6,
	"icechime": 0.8,
	"iron_xylophone": 1.1,
	"pling": 1.2,
	"snare": 1,
	"xylobone": 0.8
}

# Define groups once, cleanly:
LOOP = {"bd", "hat", "snare"}
MELODY = {"bass", "guitar", "flute", "harp"}
ACCENTS = {"bell", "pling", "icechime", "xylobone", "iron_xylophone"}

# Build unified structure:
INSTRUMENTS = {
	name: Instrument(
		volume=vol,
		loop=name in LOOP,
		melody=name in MELODY,
		accents=name in ACCENTS
	)
	for name, vol in INSTRUMENT_VOLUME.items()
}


class Note:
	def __init__(self, instrument:str, semitone: int, time: float):
		self.semitone: int = semitone
		self.time: float = time
		self.instrument: str = instrument

class NoteChain(list):
	def __init__(self, *args):
		super().__init__(*args)
		self.sort(key=lambda x: x.time)

	def append(self, note: Note):
		super().append(note)
		self.sort(key=lambda x: x.time)
	
	@property
	def tempo(self):
		if len(self) < 2:
			return None
		return (self[-1].time - self[0].time) / (len(self) - 1)

	@property
	def length(self):
		return self[-1].time
	
	@property
	def volume(self):
		return sum(INSTRUMENTS[n.instrument].volume for n in self) / len(self) if self else 0

	def copy(self): return NoteChain(super().copy())