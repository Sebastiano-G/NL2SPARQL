import stanfordnlp
import spacy
import pandas as pd
nlp = stanfordnlp.Pipeline(processors='tokenize,pos,depparse', models_dir="C:\\Users\\sebas\\stanfordnlp_resources", use_gpu=False, pos_batch_size=1000)

class CQ(object):
    def __init__(self, cq):
        self.cq = cq

    def look_for_dep_NOUN(self, dependency, depencies_list):
        result = ""
        if dependency.upos == "PROPN":
            result = dependency.text
            idx = int(dependency.index)
            for dep in depencies_list:
                if dep[0] == dependency and dep[2].upos == "PROPN":
                    if int(dep[2].index) > idx:
                        result = result + " " + dep[2].text
                    else:
                        result = dep[2].text + " " + result
                elif dep[2] == dependency and dep[0].upos == "PROPN":
                    result = self.look_for_dep_NOUN(dep[0], depencies_list)
                    return (result.strip())
            return ("PROPN,"+result.strip())
        else:
            for dep in depencies_list:
                if dep[0] == dependency:
                    if (dep[2].upos in ["ADJ"] or dep[1] == "compound") and dep[2].text.lower() not in ["which", "who", "what", "where", "when"]:
                        result = result + " " + dep[2].text
                elif dep[2] == dependency:
                    result = result + " " + dep[2].text
            result = result.strip()
            if result.startswith("of "):
                result = result.replace("of ", "")
            return result
    
    def check_entity(self, var, sentence):
        for el in sentence:
            if var == sentence[el]:
                return False
        return True

    def process(self):
        doc = nlp(self.cq)
        deps = doc.sentences[0].dependencies
        sentence = {}
        pred_num, entity_num = 0, 1
        last_verb = ""
        for dep in deps:
            pos, text, governor = dep[2].upos, dep[2].text, dep[2].governor
            if text.lower() in ["which", "who", "what", "where", "when"]:
                sentence["question"] = text
            if (pos in ["AUX", "VERB"] and dep[1] != "nsubj") or (pos=="ADJ" and dep[1]=="root"):
                if last_verb != "AUX" and (pos == "VERB" or (pos =="AUX" and text.lower() != "been")):
                    pred_num += 1
                    sentence[("predicate"+str(pred_num))] = text
                elif last_verb == "AUX" and dep[1] != "acl:relcl" and (text.lower() == "been" or (pos=="ADJ" and dep[1]=="root")):
                    sentence[("predicate"+str(pred_num))] = sentence[("predicate"+str(pred_num))] + " " + text
                elif last_verb == "AUX" and pos == "AUX":
                    pred_num += 1
                    sentence[("predicate"+str(pred_num))] = text
                elif last_verb == "AUX" and pos == "VERB":
                    sentence[("predicate"+str(pred_num))] = sentence[("predicate"+str(pred_num))] + " " + text
                last_verb = pos
                if deps[governor][0].upos in ["NOUN", "PROPN"]:
                    var_and_dep = (self.look_for_dep_NOUN(deps[governor][0], deps)).strip()
                    if self.check_entity(var_and_dep, sentence):
                        sentence[("entity"+str(entity_num))] = var_and_dep
                        entity_num +=1
            elif (pos in ["NOUN", "PROPN"] or (pos=="VERB" and dep[1] == "nsubj")) and dep[1]!="compound":
                if pos == "PROPN":
                    var_and_dep = (self.look_for_dep_NOUN(dep[2], deps))
                else:
                    var_and_dep = (self.look_for_dep_NOUN(dep[2], deps)).strip()
                if self.check_entity(var_and_dep, sentence):
                    sentence[("entity"+str(entity_num))] = var_and_dep
                    entity_num+=1
        return sentence


""" df = pd.read_csv("CQs.csv")
for idx, row in df.iterrows():
    print(CQ(row["Competency question"]).process()) """

