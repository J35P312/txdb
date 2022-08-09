import time

gtf_meta={"transcript_id":"transcript_id","gene_id":"gene_id","transcript_name":"reference_id","gene_name":"ref_gene_id"}
#gtf_meta={"transcript_id":"transcript_id","gene_id":"gene_id","transcript_name":"cmp_ref","gene_name":"gene_name"}

def generate_tx_str(gtf,transcript):
	tx_str=[gtf["transcripts"][transcript]["chr"],gtf["transcripts"][transcript]["strand"] ]
	for exon in gtf["transcripts"][transcript]["exons"]:
		tx_str.append("{}-{}".format(exon[0],exon[1]))
	return("|".join(tx_str))	

def read_gtf(gtf_path,gft_meta,filter=True):
	gtf={"transcripts":{},"transcripts_to_exon":set([]),"exons":{},"genes":{} }
	t=time.time()
	#print(time.time()-t)
	for line in open(gtf_path):
		if line[0] == "#":
			continue

		content=line.strip().replace("\"","").replace(" ","").split("\t")
		feature=content[2]
		gene=content[-1].split(gtf_meta["gene_id"])[-1].split(";")[0]
		transcript=content[-1].split(gtf_meta["transcript_id"])[-1].split(";")[0]

		if gtf_meta["gene_name"] in content[-1]:
			gene_name=content[-1].split(gtf_meta["gene_name"])[-1].split(";")[0]
		else:
			gene_name="."	

		if gtf_meta["transcript_name"] in content[-1]:
			transcript_name=content[-1].split(gtf_meta["transcript_name"])[-1].split(";")[0]
		else:
			transcript_name="."
		chromosome=content[0]
		strand=content[6]
		start=int(content[3])
		end=int(content[4])

		if feature == "transcript":
			if filter:
				TPM=float(content[-1].split("TPM")[-1].split(";")[0])
				if TPM < 0.10:
					continue
			
			gtf["transcripts"][transcript]={"exons":[],"chr":chromosome,"start":start,"end":end,"strand":strand,"gene":gene,"gene_name":gene_name,"transcript_name":transcript_name}
			if not gene in gtf["genes"]:
				gtf["genes"][gene]=set([])
			gtf["genes"][gene].add(transcript)
		elif feature == "exon":
			if not transcript in gtf["transcripts"]:
				continue

			gtf["transcripts"][transcript]["exons"].append([start,end])

	for transcript in gtf["transcripts"]:
		gtf["transcripts"][transcript]["string"]=generate_tx_str(gtf,transcript)
	return(gtf)

def initiate_db(sample,gtf):
	db={}

	tx_counter=1	
	for transcript in gtf["transcripts"]:
		db[ gtf["transcripts"][transcript]["string"] ]=gtf["transcripts"][transcript]
		db[ gtf["transcripts"][transcript]["string"] ]["samples"]=set([sample])
		db[ gtf["transcripts"][transcript]["string"] ]["transcript"]=str(tx_counter)
		tx_counter+=1

	return(db,tx_counter)

def update_db(sample,gtf,db,counts):
	for transcript in gtf["transcripts"]:
		if gtf["transcripts"][transcript]["string"] in db:
			db[ gtf["transcripts"][transcript]["string"] ]["samples"].add(sample)
		else:
			counts+=1
			db[ gtf["transcripts"][transcript]["string"] ]=gtf["transcripts"][transcript]
			db[ gtf["transcripts"][transcript]["string"] ]["samples"]=set([sample])
			db[ gtf["transcripts"][transcript]["string"] ]["transcript"]=str(counts)

	return(db,counts)

def print_db(samples,db):
	for tx in db:
		chromosome=db[tx]["chr"]
		tx_start=str(db[tx]["start"])
		tx_end=str(db[tx]["end"])
		strand=db[tx]["strand"]
		tx_out=[chromosome,"txmix","transcript",tx_start,tx_end,"1000",strand,"."]
		tx_string=f"transcript_id \"{tx}\""
		gene_name="gene_name \"{}\"".format(db[tx]["gene_name"])
		transcript_name="transcript_name \"{}\"".format(db[tx]["transcript_name"])
		frequency="frequency {}".format(len(db[tx]["samples"])/float(len(samples)) )
		counts="counts {}".format(len(db[tx]["samples"]) )
		s="samples \"{}\"".format("|".join(db[tx]["samples"]) )
		tx_data=[tx_string,gene_name,transcript_name,frequency,counts,s]
		tx_out.append("; ".join(tx_data))
		print("\t".join(tx_out))

		#for exon in db[tx]["exons"]:
		#	exon_out=[chromosome,"txmix","exon",str(exon[0]),str(exon[1]),"1000",strand,".","; ".join(tx_data)]
		#	print("\t".join(exon_out))

	
def main(files):
	in_files={}
	for line in open(files):
		sample=line.split("/")[-1].split(".")[0]
		in_files[sample]=line.strip()

	db={}
	i=0
	total=0
	read=0
	initiate=0
	update=0

	for sample in in_files:
		t=time.time()

		#if i == 20:
		#	break

		gtf=read_gtf(in_files[sample],gtf_meta)
		read+=time.time()-t
		if not db:
			db,counts=initiate_db(sample,gtf)
			continue
		i+=1
		db,counts=update_db(sample,gtf,db,counts)
		total+=time.time()-t

	#print("read",read,"total",total)
	print_db(in_files.keys(),db)
