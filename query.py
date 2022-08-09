import build
gtf_meta={"transcript_id":"transcript_id","gene_id":"gene_id","transcript_name":"reference_id","gene_name":"ref_gene_id"}

def read_db(db_path):
	db={}
	for line in open(db_path):
		content=line.replace("\"","").replace(" ","").split("\t")
		
		transcript=content[-1].split("transcript_id")[-1].split(";")[0]
		frequency=content[-1].split("frequency")[-1].split(";")[0]
		counts=content[-1].split("counts")[-1].split(";")[0]

		db[transcript]=[frequency,counts]
		
	return(db)

def main(gtf_path,db_path):
	db=read_db(db_path)
	gtf=build.read_gtf(gtf_path,gtf_meta,False)

	for line in open(gtf_path):
		if line[0] == "#":
			print(line.strip())
			continue
		content=line.replace("\"","").replace(" ","").split("\t")		
		transcript=content[-1].split("transcript_id")[-1].split(";")[0]
		transcript_string=gtf["transcripts"][transcript]["string"]
		if transcript_string in db:
			print(line.strip().strip(";") + "; Frequency \"{}\";".format(db[transcript_string][0])+ " Counts \"{}\";".format(db[transcript_string][1]))
		else:
			print(line.strip().strip(";") + "; Frequency \"0.0\"; Counts \"0\";")


