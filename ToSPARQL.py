from LodeExtractor import *
from SequenceExtraction import *
from ExtendedSequenceExtraction import *
import spacy
nlp = spacy.load('en_core_web_lg')


my_questions = [
    "Which are the topics of the song?",
]

#ontology_link = "https://raw.githubusercontent.com/polifonia-project/organs-ontology/main/organs-ontology.owl"
ontology_link = "https://raw.githubusercontent.com/SongsTOPoems/STOP/main/WIDOCOFINAL/stop.rdf"

def remove_stop_words(expression):
        if "PROPN," in expression:
            return expression
        else:
            result = ""
            for el in expression.split(" "):
                if el not in ["the", "a", "of", "in"]:
                    result = result + " " + el
            return result.strip()

def bestClass(cls, classes):
    classes_labels = list(classes.keys())
    ref_vec = nlp(cls)
    sims = [nlp(c).similarity(ref_vec) for c in classes_labels]
    sorted_vect = classes_labels[sims.index(max(sims))]
    return [sorted_vect, classes[sorted_vect]["iri"]]

def bestPred(pred, e1, e2, classes, predicates):
    ref_vec = nlp(pred)
    set_value = False
    while set_value == False:
        for dict in predicates:
            if "domain" in list(predicates[dict].keys()):
                set_value = True
    if set_value:
        possible_domains = [e1]
        possible_ranges = [e2] 
        if "has sub-classes" in list(classes[e1].keys()):
            for el in classes[e1]["has sub-classes"]:
                possible_domains.append(el) 
        if "has sub-classes" in list(classes[e2].keys()):
            for el in classes[e2]["has sub-classes"]:
                possible_ranges.append(el)
        pred_labels = []
        for predicate in predicates:
            if "domain" in list(predicates[predicate].keys()) and "range" in list(predicates[predicate].keys()):
                if predicates[predicate]["domain"] in possible_domains and predicates[predicate]["range"] in possible_ranges:
                    pred_labels.append(predicate)
    else:
        pred_labels = list(predicates.keys())
    if len(pred_labels) == 0:
        return "None"
    sims = [nlp(c).similarity(ref_vec) for c in pred_labels]
    sorted_vect = pred_labels[sims.index(max(sims))]
    return predicates[sorted_vect]["iri"]

for cq in my_questions:
    cq_sequence = CQ(cq).process()
    print(cq_sequence)
    cq_extended_sequence = extendedCQ(cq).process()
    print(cq_extended_sequence)
    cq_extended_sequence_to_string = ", ".join(cq_extended_sequence[1:])
    lode_exctractor = OntologyExtractor(ontology_link)
    classes = lode_exctractor.extractClasses()
    predicates = lode_exctractor.extractObjProperties()
    if cq_extended_sequence_to_string.startswith("TO-BE-VERB"):
        if cq_extended_sequence_to_string in ["TO-BE-VERB, NOUN, of, NOUN", "TO-BE-VERB, NOUN, for, NOUN"]:
            best_e1, best_e2 = bestClass(remove_stop_words(cq_sequence["entity1"]), classes), bestClass(remove_stop_words(cq_sequence["entity2"]), classes)
            e1, e2, e1_Class, e2_Class  = cq_sequence["entity1"], cq_sequence["entity2"], best_e1[1], best_e2[1]
            temporary_pred = "is " + cq_extended_sequence[3]
            p1_ref = bestPred(remove_stop_words(temporary_pred), best_e1[0], best_e2[0], classes, predicates)
            query = """
            SELECT ?{0}
            WHERE {{
            ?{0} <{2}> ?{1} .
            ?{0} hasType <{3}> .
            ?{1} hasType <{4}> .
            }}
            """
            print(query.format(e1, e2, p1_ref, e1_Class, e2_Class))




