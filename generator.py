from enum import Enum, auto
import random
from sound_analysis import *

SCALE_PATTERNS = {
	"major":            [0, 2, 4, 5, 7, 9, 11],
	"natural_minor":    [0, 2, 3, 5, 7, 8, 10],
	"harmonic_minor":   [0, 2, 3, 5, 7, 8, 11],
	"melodic_minor":    [0, 2, 3, 5, 7, 9, 11],
	"dorian":           [0, 2, 3, 5, 7, 9, 10],
	"phrygian":         [0, 1, 3, 5, 7, 8, 10],
	"lydian":           [0, 2, 4, 6, 7, 9, 11],
	"mixolydian":       [0, 2, 4, 5, 7, 9, 10],
	"locrian":          [0, 1, 3, 5, 6, 8, 10],
	"major_pentatonic": [0, 2, 4, 7, 9],
	"minor_pentatonic": [0, 3, 5, 7, 10],
	"blues":            [0, 3, 5, 6, 7, 10],
	"chromatic":        list(range(12))
}

# Common chord progressions (scale degrees)
CHORD_PROGRESSIONS = {
	"major": {
		"pop": [0, 4, 5, 3],      # I-V-vi-IV
		"classic": [0, 3, 4, 0],  # I-IV-V-I
		"sad": [0, 5, 3, 4],      # I-vi-IV-V
	},
	"minor": {
		"emotional": [0, 3, 4, 4],  # i-III-iv-iv
		"dark": [0, 5, 3, 4],       # i-v-III-IV
		"hopeful": [0, 3, 6, 4],    # i-III-VI-IV
	}
}

NOTE_NAMES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

class SegmentPhase(Enum):
	INTRO = auto()
	VERSE = auto()
	CHORUS = auto()
	BRIDGE = auto()
	OUTRO = auto()

STRUCTURE = [SegmentPhase.INTRO, SegmentPhase.VERSE, SegmentPhase.CHORUS]

def getTime(tempo, bars):
	beats_per_bar = 4
	seconds_per_beat = 60 / tempo
	return bars * beats_per_bar * seconds_per_beat

def getScale(key, scale_type):
	root_note = NOTE_NAMES.index(key)
	scale_pattern = SCALE_PATTERNS[scale_type]
	return [(root_note + interval) % 12 for interval in scale_pattern]

def getChordNotes(root_semitone, scale_notes, chord_type="triad"):
	"""Generate notes for a chord based on scale degrees"""
	if chord_type == "triad":
		# Root, third, fifth
		return [
			scale_notes[0] + root_semitone,
			scale_notes[2] + root_semitone,
			scale_notes[4] + root_semitone
		]
	elif chord_type == "seventh":
		# Root, third, fifth, seventh
		return [
			scale_notes[0] + root_semitone,
			scale_notes[2] + root_semitone,
			scale_notes[4] + root_semitone,
			scale_notes[6] + root_semitone
		]

class SongSegment:
	def __init__(self, seed=None, tempo=120, key="C", scale_type="major", length_bars=16, segmentPhase: SegmentPhase = SegmentPhase.VERSE):
		self.seed = seed
		self.tempo = tempo
		self.key = key
		self.scale_type = scale_type
		self.length_bars = length_bars
		self.notes = NoteChain()
		self.segmentPhase = segmentPhase
	
	def generate(self, song: "Song", idx):
		"""Generate music for this segment based on its phase"""
		scale = getScale(self.key, self.scale_type)
		segment_duration = getTime(self.tempo, self.length_bars)
		beat_duration = 60 / self.tempo
		
		# Different generation strategies based on phase
		if self.segmentPhase == SegmentPhase.INTRO:
			self._generateIntro(scale, segment_duration, beat_duration, song)
		elif self.segmentPhase == SegmentPhase.VERSE:
			self._generateVerse(scale, segment_duration, beat_duration, song)
		elif self.segmentPhase == SegmentPhase.CHORUS:
			self._generateChorus(scale, segment_duration, beat_duration, song)
		elif self.segmentPhase == SegmentPhase.BRIDGE:
			self._generateBridge(scale, segment_duration, beat_duration, song)
		elif self.segmentPhase == SegmentPhase.OUTRO:
			self._generateOutro(scale, segment_duration, beat_duration, song)
		
		self.notes.sort(key=lambda x: x.time)
	
	def _generateIntro(self, scale, duration, beat, song):
		"""Sparse, building intro"""
		beats = int(duration / beat)
		notes = []
	
	def _generateVerse(self, scale, duration, beat, song):
		"""Verse with melody and steady rhythm"""
		# Drum pattern
		beats = int(duration / beat)
		for i in range(beats):
			if i % 4 == 0:
				self.notes.append(Note("bd", 0, i * beat))
			if i % 4 == 2:
				self.notes.append(Note("snare", 0, i * beat))
			if i % 2 == 1:
				self.notes.append(Note("hat", 0, i * beat))
		
		# Melody
		melody_instruments = [name for name, inst in INSTRUMENTS.items() if inst.melody]
		if melody_instruments:
			melody_inst = random.choice(melody_instruments)
			for i in range(0, beats, 2):
				note = random.choice(scale) + 12
				self.notes.append(Note(melody_inst, note, i * beat))
	
	def _generateChorus(self, scale, duration, beat, song):
		"""Energetic chorus with more layers"""
		beats = int(duration / beat)
		
		# Stronger drum pattern
		for i in range(beats):
			if i % 2 == 0:
				self.notes.append(Note("bd", 0, i * beat))
			if i % 4 == 2:
				self.notes.append(Note("snare", 0, i * beat))
			self.notes.append(Note("hat", 0, i * beat))
		
		# Lead melody
		melody_instruments = [name for name, inst in INSTRUMENTS.items() if inst.melody]
		if melody_instruments:
			for i in range(0, beats, 1):
				note = random.choice(scale) + 12
				self.notes.append(Note("guitar", note, i * beat))
		
		# Accents for emphasis
		accent_instruments = [name for name, inst in INSTRUMENTS.items() if inst.accents]
		if accent_instruments:
			for i in range(0, beats, 4):
				note = random.choice(scale) + 24  # Higher octave
				self.notes.append(Note(random.choice(accent_instruments), note, i * beat))
	
	def _generateBridge(self, scale, duration, beat, song):
		"""Contrasting bridge section"""
		beats = int(duration / beat)
		
		# Different rhythm pattern
		for i in range(beats):
			if i % 8 == 0:
				self.notes.append(Note("bd", 0, i * beat))
			if i % 8 == 4:
				self.notes.append(Note("snare", 0, i * beat))
		
		# Sparse, different melody
		for i in range(0, beats, 4):
			note = random.choice(scale) + 12
			self.notes.append(Note("flute", note, i * beat))
	
	def _generateOutro(self, scale, duration, beat, song):
		"""Fading outro"""
		beats = int(duration / beat)
		
		# Gradually reducing rhythm
		for i in range(0, beats, 2):
			if i < beats / 2:
				self.notes.append(Note("hat", 0, i * beat))
		
		# Final melody notes
		accent_instruments = [name for name, inst in INSTRUMENTS.items() if inst.accents]
		if accent_instruments:
			for i in range(0, min(beats // 2, 8), 4):
				note = random.choice(scale) + 12
				self.notes.append(Note(random.choice(accent_instruments), note, i * beat))

class Song:
	def __init__(
		self,
		seed=None,
		tempo=120,
		key="C",
		scale_type="major",
		segment_length=16,
		instruments=None,
		chord_progression=None
	):
		self.segments = [
			SongSegment(seed=seed, tempo=tempo, key=key, scale_type=scale_type, 
					   length_bars=segment_length, segmentPhase=phase) 
			for phase in STRUCTURE
		]
		self.seed = seed
		self.tempo = tempo
		self.key = key
		self.scale_type = scale_type
		self.segment_length = segment_length
		self.instruments = instruments
		self.chord_progression = chord_progression or self._getDefaultProgression()
		
		if seed is not None:
			random.seed(seed)
	
	def _getDefaultProgression(self):
		"""Get appropriate chord progression for scale type"""
		if "minor" in self.scale_type:
			return CHORD_PROGRESSIONS["minor"]["emotional"]
		else:
			return CHORD_PROGRESSIONS["major"]["pop"]
	
	def generate(self):
		"""Generate all segments of the song"""
		# Generate base loop (kept across some segments)
		loop = self.generateLoop()
		
		# Generate each segment
		for idx, segment in enumerate(self.segments):
			# Only VERSE and CHORUS inherit the full loop
			if segment.segmentPhase in [SegmentPhase.INTRO, SegmentPhase.VERSE, SegmentPhase.CHORUS]:
				segment.notes = loop.copy()
			
			segment.generate(self, idx)
	
	def generateLoop(self):
		"""Generate base rhythmic loop with variation"""
		loop = NoteChain()
		beat_duration = 60 / self.tempo
		bars = 4  # 4-bar loop
		
		# Pick 3 loop instruments sorted by volume (quietest to loudest)
		chosenInstruments = sorted(random.sample(list(LOOP), k=3), key=lambda inst: INSTRUMENTS[inst].volume)
		
		quietest = chosenInstruments[0]
		secondary = chosenInstruments[1]
		loudest = chosenInstruments[2]
		
		# Generate ONE bar pattern that will repeat 3 times
		bar_pattern = []
		
		# Create random pattern for one bar (4 beats, with half-beat resolution)
		for beat in range(4):
			for halfbeat in [0, 0.5]:  # On-beat and off-beat
				time_in_bar = beat + halfbeat
				
				# Quietest - main steady rhythm
				if halfbeat == 0 or random.random() < 0.3:
					bar_pattern.append((quietest, time_in_bar))
				
				# Secondary - syncopated rhythm
				if (beat % 2 == 1 and halfbeat == 0) or (random.random() < 0.2):
					bar_pattern.append((secondary, time_in_bar))
				
				# Loudest - sparse accents
				if beat == 0 and halfbeat == 0:
					bar_pattern.append((loudest, time_in_bar))
				elif beat == 2 and halfbeat == 0 and random.random() < 0.5:
					bar_pattern.append((loudest, time_in_bar))
		
		# Apply the pattern to all 4 bars
		for bar in range(bars):
			is_spicy = (bar == 3)
			
			# Copy the base pattern
			for instrument, time_in_bar in bar_pattern:
				absolute_time = (bar * 4 + time_in_bar) * beat_duration
				loop.append(Note(instrument, 0, absolute_time))
			
			# Add SPICE to the 4th bar only
			if is_spicy:
				# Add a fill in the last beat
				for subdivision in [3.25, 3.5, 3.75]:
					absolute_time = (bar * 4 + subdivision) * beat_duration
					loop.append(Note(secondary, 0, absolute_time))
				
				# Big accent on the very last hit
				absolute_time = (bar * 4 + 3.75) * beat_duration
				loop.append(Note(loudest, 0, absolute_time))
		
		return loop
	
	def exportSong(self, filename='song.txt'): # export to df
		compiledData = ""
		for segment in self.segments:
			for note in segment.notes:
				compiledData += f"{note.time:.2f}|{note.instrument[0]+note.instrument[-1]+('2' if note.instrument == 'iron_xylophone' else '')}|{note.semitone},"
		return compiledData

