"https://www.biostars.org/p/221662/"

import os
from Bio import Entrez

leere_liste = []
information = []
" Read the accessions from a file"
print("Current working directory: {0}".format(os.getcwd()))
os.chdir("C:/Users/phh20/Desktop/16S rRNA Genomsuche/NCBI_16S_nr_database_BLAST/gbk_files")
print("Changing to new working directory: {0}".format(os.getcwd()), "\n")

accessions_file = "accessions.txt"
with open(accessions_file) as f:
    ids = f.read().split('\n')



" Fetch the entries from Entrez"
Entrez.email = 'halamaflipp@gmail.com'  # Insert your email here
handle = Entrez.efetch('nuccore', id=ids, retmode='xml')
response = Entrez.read(handle)



" Parse the entries to get the country"
def extract_countries(entry):
    sources = [feature for feature in entry['GBSeq_feature-table']
               if feature['GBFeature_key'] == 'source']

    for source in sources:
        qualifiers = [qual for qual in source['GBFeature_quals']
                      if qual['GBQualifier_name'] == 'country']
        
        for qualifier in qualifiers:
            yield qualifier['GBQualifier_value']

for entry in response:
    accession = entry['GBSeq_primary-accession']
    for country in extract_countries(entry):
        print(accession, country, sep=',')
        information.append(accession)
        information.append(country)


    leere_liste.append(information)
    information = []


"Safe as csv-file"
output_handle = open("C:/Users/phh20/Desktop/16S rRNA Genomsuche/NCBI_16S_nr_database_BLAST/gbk_files/Countries.csv", "w")

for line in leere_liste:
    output_line = "" #convert int into strings
    
    for n in line:
        output_line += str(n) + ","
    
    output_line = output_line.rsplit(",", 1)[0]
    output_line += "\n"    
    output_handle.write(output_line)

output_handle.close()

print("\n Extraktion abgeschlossen") 

