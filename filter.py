import sys

def main(gtf_path,min_tpm=0.2,min_coverage=3):
	ok_transcript=set([])
	for line in open(gtf_path):
		if line[0] == "#":
			print(line.strip())
			continue
		content=line.strip().replace("\"","").replace(" ","").split("\t")
		feature=content[2]
		transcript=content[-1].split("transcript_id")[-1].split(";")[0]

		if feature == "transcript":
			TPM=float(content[-1].split("TPM")[-1].split(";")[0])
			coverage=float(content[-1].split("cov")[-1].split(";")[0])
			#print(TPM)
			if coverage > min_coverage and min_tpm < TPM:
				ok_transcript.add(transcript)


		
	for line in open(gtf_path):
		if line[0] == "#":
			continue
		content=line.strip().replace("\"","").replace(" ","").split("\t")
		feature=content[2]
		transcript=content[-1].split("transcript_id")[-1].split(";")[0]
		if transcript in ok_transcript:
			print(line.strip())
