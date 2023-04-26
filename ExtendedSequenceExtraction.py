import pandas as pd
import stanfordnlp
from LodeExtractor import *
nlp = stanfordnlp.Pipeline(processors='tokenize,pos,depparse', models_dir="C:\\Users\\sebas\\stanfordnlp_resources", use_gpu=False, pos_batch_size=1000)


class extendedCQ(object):
    def __init__(self, cq):
        self.cq = cq

    def process(self):
        doc = nlp(self.cq)
        deps = doc.sentences[0].dependencies
        sentence = []
        for dep in deps:
            pos, text, index = dep[2].upos, dep[2].text, int(dep[2].index)
            if text.lower() in ["which", "who", "what", "where", "when"]:
                sentence.append(text)
            if pos == "AUX" and text.lower() != "can":
                if text.lower() in ["are", "is", "was", "were"]: 
                    sentence.append("TO-BE-VERB")
                elif text.lower() in ["has", "have"]:
                    sentence.append("TO-HAVE-AUX")
                elif not sentence[-1].endswith("AUX"): #to avoid "have been" cases to be regarded as "TO-HAVE-AUX" + "TO-BE-VERB"
                    sentence.append("AUX")
            elif pos in ["ADJ","VERB"] and sentence[-1] in ["TO-BE-VERB", "TO-HAVE-AUX"] and (text.lower().endswith("ed") or text.lower().endswith("ing")):
                sentence[-1] = "VERB"
            elif pos == "ADJ" and sentence[:-2] and (text.lower().endswith("ed") or text.lower().endswith("ing")):
                sentence.append("VERB")
            elif pos == "VERB" and dep[1] != "nsubj":
                sentence.append(pos)
            elif (pos in ["NOUN", "PROPN"] or (pos=="VERB" and dep[1] == "nsubj")) and dep[1]!="compound":
                if deps[index-2][2].text.lower() == "of" and len(deps) > index+1:
                    if deps[index][2].text.lower() == "of" and deps[index+1][2].upos == "DET":
                        sentence.pop()
                    else:
                        sentence.append("NOUN")
                else:
                    sentence.append("NOUN")
            elif pos == "ADP":    
                sentence.append(text)
        if "AUX" in sentence and "VERB" not in "sentence": #it means that a verb has been classified as a noun (e.g.: what does this object document?, "document" is regarded as a noun)
            if sentence[-2:] == ["AUX", "NOUN"] :
                sentence.append("VERB") 
        return sentence

""" a_list = [] 
df = pd.read_csv("CQs.csv")
for idx, row in df.iterrows():
    a_list.append(row["Competency question"])
for el in a_list:
    process(el)  """
    
        
            
            