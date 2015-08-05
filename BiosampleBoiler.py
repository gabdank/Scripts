
import json

''' script for boiling down biosample json objects
each field deemed as important will stay, while the unimportant fields will be removed '''

# organism object is replaced by organism scientific name
def boildown_organism(organism_object):
    return organism_object['scientific_name']

# award object is replaced by the name of the award
def boildown_award(award_object):
    return award_object['name']

# source object is replaced by the title of the source
def boildown_source(source_object):
    return source_object['title']

def is_control_target(target_object):
    for entry in target_object['investigated_as']:
        if entry == 'control':
            return True
    return False



# donor object is replaced by limited set of its properties
def boildown_donor(donor_object):
    donorDictionary = {}
    for key in donor_object.keys():
        listOfInterestingValues = ['accession', 'strain_name', 'strain_background', 'sex', 'life_stage', 'health_status', 'alternate_accessions', 'ethnicity', 'genotype' , 'mutagen']


        if key in listOfInterestingValues:
            donorDictionary[key]=donor_object[key]
        if key == 'target' or key == 'mutated_gene':
            if is_control_target(donorDictionary[key]) == False:
                donorDictionary[key] = donor_object[key]['label']
    return donorDictionary


dispatch = {
    'organism': boildown_organism,
    'award': boildown_award,
    'source': boildown_source,
    'donor': boildown_donor,
}


with open("/Users/idan/Documents/GEO/example/ENCBS778MKB.json", encoding='utf-8') as data_file:
    data = json.loads(data_file.read())

print ("-------------")
for entry in data.keys():
    #print (entry)
    if entry in dispatch:
        print (str(entry)+"\t"+str(dispatch[entry](data[entry])))
    else:
        print ("NO MATCH:"+str(entry))
print ("-------------")


for x in data['donor']:
    print (str(x) + "\t" + str(data['donor'][x]))


print ('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
print ("boiled down award = "+str(boildown_award(data['award'])))
print ("boiled down organism = "+str(boildown_organism(data['organism'])))
print ("boiled down source = "+str(boildown_source(data['source'])))