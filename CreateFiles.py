import os
from xml.dom import minidom
from lxml import etree


N_SAMPLES = 100
N_FOLDS = 5
#N_BOTS = 9
#N_MALES = 8
#N_FEMALES = 8
N_BOTS = 100
N_MALES = 100
N_FEMALES = 100

def process_author(file_name, auth_no, n_samples=N_SAMPLES, n_folds=N_FOLDS):
    print(file_name)
    with open(file_name) as xfile:
        xdata = xfile.read().replace('\n', '')
    if 'RT' in xdata: # get rid of retweets
        return 0
    root = etree.fromstring(xdata)
    batch_size = n_samples / n_folds
    n = 0
    text = ''
    for doc_text in root.xpath("//documents/document"):
        t = doc_text.text
        if 'http' in t:
            t = t[:t.index('http')]
        text += t.strip() + '\n'
        n += 1
        if (n % batch_size) == 0:
            with open(os.path.join(os.path.pardir,"Data",str(auth_no)+"_"+str(int(n/batch_size))+".txt"), "w") as out_file:
                out_file.write(text)
            text = ''
    return 1


def process_folder(folder, n_bots=N_BOTS, n_males=N_MALES, n_females=N_FEMALES):
    bot_base = 1000
    male_base = bot_base + n_bots
    female_base = male_base + n_males
    bot_count = 0
    male_count = 0
    female_count = 0
    with open(os.path.join(folder,"en.txt")) as list_file:
        for ln in list_file:
            parts = ln.strip().split(":::")
            if parts[2] == "bot" and bot_count < n_bots:
                print("bot")
                bot_count += process_author(os.path.join(folder,"en",parts[0]+".xml"), bot_count+bot_base)
            elif parts[2] == "male" and male_count < n_males:
                print("male")
                male_count += process_author(os.path.join(folder,"en",parts[0]+".xml"), male_count+male_base)
            elif female_count < n_females:
                print("female")
                female_count += process_author(os.path.join(folder,"en",parts[0]+".xml"), female_count+female_base)




'''
for d in os.listdir("."):
    if os.path.isdir(d):
        process_folder(d)
'''
process_folder("pan19-author-profiling-test-2019-04-29")
