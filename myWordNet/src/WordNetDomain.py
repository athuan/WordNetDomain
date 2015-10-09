

import nltk
from nltk.corpus import wordnet
from nltk.corpus import WordNetCorpusReader
from duplicity.tempdir import default
print('loading wordnet2.0')
wn2 = WordNetCorpusReader(nltk.data.find('corpora/wordnet2.0'), None)
print('done loading')

print('loading wordnet3.0')
wn3 = WordNetCorpusReader(nltk.data.find('corpora/wordnet'), None)
print('done loading')

S2 = wn2.synset
L = wn2.lemma
S3 = wn3.synset


# hash with key is synset_offset of Wordnet 2.0's synset and value is domain
domain_list = {}

# hash with key is synset_offset of Wordnet 2.0's synset and value is synset 2.0
synset2_list = {}

# hash wiht key is synset_offset of WN 3.0's synset and value is synset 3.0
synset3_list = {}
    

def addZero(number):
    numberStr = str(number)
    num = ""
    leng = len(numberStr)
    
    if leng == 0:
        num = "00000000"+numberStr
    elif leng == 1:
        num = "0000000"+numberStr
    elif leng == 2:
        num = "000000"+numberStr
    elif leng == 3:
        num = "00000"+numberStr
    elif leng == 4:
        num = "0000"+numberStr
    elif leng == 5:
        num = "000"+numberStr
    elif leng == 6:
        num = "00"+numberStr
    elif leng == 7:
        num = "0"+numberStr
    else:
        num = numberStr
        
    return num


def getDomainList():
    file_in = open("wn-domains-3.2-20070223", "r")
    for line in file_in:
        line = line.rstrip()
        split = line.split("\t")
        offset = str(split[0])
        domain = split[1]
        domain_list[offset] = domain
        
def getSynset2List():
    synset2 = list(wn2.all_synsets())
    for synset in synset2:
        offset = synset.offset()
        key = str(synset.name())
        value = str(addZero(offset)+"-"+synset.pos())
        synset2_list[key] = value

def getSynset3List():
    synset3 = list(wn3.all_synsets())
    for synset in synset3:
        offset = synset.offset()
        key = str(addZero(offset)+"-"+synset.pos())
        synset3_list[key] = synset

def countDomain(list):
    hashDomain = {}
    for key, domain in list.items():
        # print(key+","+domain)
        if hashDomain.has_key(domain):
            hashDomain[domain] = hashDomain[domain] + 1
        else:
            hashDomain[domain] = 1
    return hashDomain

def writeFile(filename, list):
    file_out = open(filename, "w")

    for key, value in list.items():
        string =""
        string += key + "\t" + str(value)+"\n"
        file_out.write(string)
    file_out.close()

def splitDomain(list):
    hashDomain = {}
    for key, domain in list.items():
        domain_array = domain.strip().split(" ")
        for i in range(0, len(domain_array)):
            keyDomain = key+"-"+str(i)
            hashDomain[keyDomain] = domain_array[i]
    return hashDomain

        
def main():
    getDomainList()
    getSynset2List()
#     getSynset3List()
    
    synset_domain = {}
    
    file_synset = open("danhsachmasynset.txt", "r")
    file_out = open("Synset_With_Domain.txt", "w")
    
    
    for synset in file_synset:
        string = ""
        synset = synset.strip()
        syn = S3(synset)

        if synset2_list.has_key(str(syn.name())):
            offset = synset2_list[str(syn.name())]
            domain = domain_list[offset]
            string += synset + "\t" + domain +"\n"
            synset_domain[synset] = domain
        else:
            string += synset + "\t" + "Not_in_Domain\n" 
            synset_domain[synset] = "Not_in_Domain"
        print(string)

        file_out.write(string)
        
    print("Done compute domain!")

    writeFile("domain_synset_require.txt", synset_domain)
    sDomain = splitDomain(synset_domain)
    writeFile("split_domain.txt", sDomain)
    count_Domain = countDomain(sDomain)
    writeFile("Domain_Frequency.txt", count_Domain)

    print("Done!")

    file_synset.close()
    file_out.close()
        
main()

