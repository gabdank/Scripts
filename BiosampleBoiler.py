
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

def boildown_lab(lab_object):
    return lab_object['title']

def is_control_target(target_object):
    for entry in target_object['investigated_as']:
        if entry == 'control':
            return True
    return False

def boildown_references(references_list):
    listToReturn = []
    for publicationObject in references_list:
        listToReturn.append(boildown_publication(publicationObject))
    return listToReturn

def boildown_publication(publication_object):
    return publication_object['identifiers']

def boildown_document(document_object):
    documentDictionary = {}
    if 'attachment' in document_object:
        documentDictionary['attachment']=boildown_attachment(document_object['attachment'])
    if 'urls' in document_object:
        documentDictionary['urls']=document_object['urls']
    if 'references' in document_object:
        documentDictionary['references'] = boildown_references(document_object['references'])
    return documentDictionary

def boildown_attachment(attachment_dict):
    dictionaryToReturn = {}
    for key in attachment_dict:
        if key in attachmentLitOfInterestingValues:
            dictionaryToReturn[key]=attachment_dict[key]
    return dictionaryToReturn

def boildown_documents(documents_list):
    listToReturn = []
    for documentObject in documents_list:
        listToReturn.append(boildown_document(documentObject))
    return listToReturn

# donor object is replaced by limited set of its properties
def boildown_donor(donor_object):
    donorDictionary = {}
    for key in donor_object.keys():
        if key in donorListOfInterestingValues:
            donorDictionary[key]=donor_object[key]
        if key == 'target' or key == 'mutated_gene':
            if is_control_target(donor_object[key]) == False:
                donorDictionary[key] = donor_object[key]['label']
    return donorDictionary

def boildown_constructs(constructs_list):
    listToReturn = []
    for entry in constructs_list:
        listToReturn.append(boildown_construct(entry))
    return listToReturn

def boildown_construct(construct_object):
    construct_dictionary = {}
    for key in construct_object.keys():
        if key in constructListOfInterestingValues:
            construct_dictionary[key]=construct_object[key]
        if key == 'target':
            if is_control_target(construct_object[key]) == False:
                construct_dictionary[key] = construct_object[key]['label']
        if key == 'documents':
            construct_dictionary[key] = boildown_documents(construct_object[key])

    return construct_dictionary

def boildown_protocol_documents(documents_list):
    return boildown_documents(documents_list)

attachmentLitOfInterestingValues = ['md5sum','href','download']
constructListOfInterestingValues = ['construct_type','description','url']
donorListOfInterestingValues = ['accession', 'strain_name', 'strain_background', 'sex', 'life_stage', 'health_status', 'alternate_accessions', 'ethnicity', 'genotype' , 'mutagen']
biosampleListOfSimpleValues = ['dbxrefs','accession','biosample_term_name','biosample_term_id','description','synonyms','alternate_accessions','biosample_type','url']

dispatch = {
    'organism': boildown_organism,
    'award': boildown_award,
    'source': boildown_source,
    'donor': boildown_donor,
    'lab': boildown_lab,
    'references': boildown_references,
    'constructs': boildown_constructs,
    'protocol_documents': boildown_protocol_documents,
}

#with open("/Users/idan/Documents/GEO/example/ENCBS778MKB.json", encoding='utf-8') as data_file:

with open("/Users/idan/Documents/GEO/example/ENCBS823IZS.json", encoding='utf-8') as data_file:
    data = json.loads(data_file.read())

print ("-------------")
for entry in data.keys():
    #print (entry)
    if entry in dispatch:
        print (str(entry)+":"+str(dispatch[entry](data[entry])))
    else:
        if entry in biosampleListOfSimpleValues:
            print (str(entry)+":"+str(data[entry]))
        #else:
        #    print ("NO MATCH: -------------------->"+str(entry))
print ("-------------")


for x in data['donor']:
    print (str(x) + "\t" + str(data['donor'][x]))

'''
print ('^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^')
print ("boiled down award = "+str(boildown_award(data['award'])))
print ("boiled down organism = "+str(boildown_organism(data['organism'])))
print ("boiled down source = "+str(boildown_source(data['source'])))
'''