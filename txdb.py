import build
import query
import filter
import sys

if len(sys.argv) < 2:
	print("python txdb.py build")
	print("python txdb.py query")
	print("python txdb.py filter")
	print("missing argument")
	quit()

if sys.argv[1] not in set(["build","query","filter"]):
	print("python txdb.py build")
	print("python txdb.py query")
	print("python txdb.py filter")
	print("missing argument")
	quit()

if sys.argv[1] == "build":
	if len(sys.argv) < 3:
		print("missing argument")
		print("python txdb.py build input.txt")
		print("input.txt is a file containing path to stringtie gtf")

	build.main(sys.argv[2])

elif sys.argv[1] == "query":
	if len(sys.argv) < 4:
		print("missing argument")
		print("python txdb.py in.gtf db.gtf")
		print("in.gtf is a stringtie gtf, db.gtf is a database produced through txdb.py build")

	query.main(sys.argv[2],sys.argv[3])

elif sys.argv[1] == "filter":
	filter.main(sys.argv[2])
