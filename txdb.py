import build
import query
import filter
import sys

if sys.argv[1] not in set(["build","query","filter"]):
	print("missing argument")
	print("python main.py build or query")
	quit()

if sys.argv[1] == "build":
	build.main(sys.argv[2])

elif sys.argv[1] == "query":
	query.main(sys.argv[2],sys.argv[3])

elif sys.argv[1] == "filter":
	filter.main(sys.argv[2])
