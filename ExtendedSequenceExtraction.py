import stanfordnlp
nlp = stanfordnlp.Pipeline(processors='tokenize,pos,depparse', models_dir="C:\\Users\\sebas\\stanfordnlp_resources", use_gpu=False, pos_batch_size=1000)

def process(question):
    doc = nlp(question)
    deps = doc.sentences[0].dependencies
    sentence = []
    for dep in deps:
        pos, text, index = dep[2].upos, dep[2].text, int(dep[2].index)
        if text.lower() in ["which", "who", "what", "where", "when"]:
            sentence.append(text)
        if pos == "AUX" and text.lower() != "can":
            if text.lower() in ["are", "is", "was", "were"]: 
                sentence.append("TO-BE-VERB") 
            elif sentence[-1] != "AUX": #to avoid "have been" cases to be regarded as "AUX" + "AUX"
                sentence.append("AUX")
        elif pos in ["ADJ","VERB"] and sentence[-1] == "TO-BE-VERB" and (text.lower().endswith("ed") or text.lower().endswith("ing")):
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
    print(question, sentence)

a_list = ["What role does this object play?", #
"Which objects do play that role?", #
"What is this entity part of?", 
"What are the parts of this entity?", #
"Which is the strength of an Affordance?", #
"Which agent does play this role?", #
"Which algorithm is implemented by this implementation?", #
"Which implementation is executed?", #
"What bag is this item an element of?", #
"Who is taking the course?", #
"Who was involved as bias source in a bias event?", #
"What type of bias is documented?", #
"Who are the bias recipient agents that do not have a bias source agent?", 
"Who is the creator of an archive?", #
"When did this communication event take place?",  
"What is the course name?", 
"What are the descriptions related to a particular entity?", #
"What types of codecs exist?", #
"Who were involved in the 1990 World Chess Championship Match?", #
"Which are the topics of the songs?", #
"Where was a musical composition performed?", #
"Which is the medium of performance of a musical composition?", #
"Which was the first medium of performance of a musical composition?", #
"Which instruments are involved in a musical composition?", #
"Which is the composer of a musical composition?", #
"When was a musical composition performed?", #
"Which performers have performed a musical composition?", #
"What was the country of origin of a piece of music?", 
"Which is the occupation of the creator of a source?", #
"What event objects is this complex event object an abstraction of?", #
"What are the parts of this composite event object?", #
"What actual event does this event object document?", #
"What are the dietary features of the ingredient?", #
"What is the objective of ingredient substitution?", #
"What type of fishing gear can catch what aquatic species?", #
"What vessel type can equip what gear type?", #
"What object is exposed to a hazard?", #
"Which hazardous events are associated with a hazardous situation?", #
"What is the cause of a hazardous event?", #
"What are the physical realizations of this information object?", #
"What information objects are realized by this physical object?", #
"What is the meaning of an information object?", #
"What information objects express this meaning?", #
"What is the order this invoice is referring to?", #
"What is the line item for this invoice?", #
"What is the location of an activity?", #
"What are the items in this list?", #
"What is the length of this list?", #
"What is the first/last item in this list?", #
"What resource does this list item contain?", #
"What is the next/previous item in the list?", #
"What material resources were required to produce a product?", #
"Where did the transformation take place?", 
"What was the time necessary for the transformation?", #
"What are the observations performed by a procedure?", #given removed from the sentence (useless)
"What are the observations performed by a actuator?", #given removed from the sentence (useless)
"What are the procedures implemented by a actuator?", #given removed from the sentence (useless)
"What is the fundamental frequency of a musical object?", #
"What is the duration in seconds of a musical object?", #
"Where did musician X and performer Y met?", #
"When did musician X and performer Y meet?", #
"Which is the employer of a musician?", #
"What objects have been observed?",
"What are the observations of this object?",
"What is the role of this object in this event?",
"What is the object holding this role in this event?",
] 

for el in a_list:
    process(el) 