# txdb
Build frequency database of transcripts from gtf

# Build

	python txdb.py build input.txt prefix

input.txt is a file containing file path to stringtie gtf
txdb will generate two files:

	prefix.gtf -> which is used for querying
	prefix.full.gtx -> comprehensive db containing exons, used for visualization in IGV etc.

# Query

	python txdb.py query in.gtf db.gtf > query.gtf

# Filter
