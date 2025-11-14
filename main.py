import flask
import generator

app = flask.Flask(__name__)

@app.route("/")
def hello():
	return "Hello, World!"

@app.route("/generate", methods=["GET"])
def generate():
	args = flask.request.args
	seed = args.get("seed", None)
	tempo = int(args.get("tempo", 200))
	key = args.get("key", "C")
	scale_type = args.get("scale_type", "major")
	segment_length = int(args.get("segment_length", 8))
	song = generator.Song(
		seed=seed,
		tempo=tempo,
		key=key,
		scale_type=scale_type,
		segment_length=segment_length
	)
	song.generate()
	return song.exportSong()

app.run(debug=True, port=5000)
