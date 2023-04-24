import sys
sys.path.append("c:/users/sebas/appdata/roaming/python/python310/site-packages")
import urllib.request
from bs4 import BeautifulSoup
link = "https://raw.githubusercontent.com/polifonia-project/organs-ontology/main/organs-ontology.owl"
base_url = "https://w3id.org/lode/"
page = urllib.request.urlopen(base_url + link)
soup = BeautifulSoup(page)

#CLASSES: da aggiungere casi di errore
def extractClasses(soup):
    classes_div = soup.find(id="classes").findAll("div", {"class": "entity"})
    classes = {}
    for el in classes_div: 
        sup = el.find("dd").find(text=True) if el.find("dd") != None else None
        iri = el.find("a")
        classes[(el.find("h3").find(text=True))] = [sup, iri['name']]
    return classes
    


#OBJECT PROPERTIES
def extractObjProperties(soup):
    obj_props_div = soup.find(id="objectproperties").findAll("div", {"class": "entity"})
    obj_props = {}
    for el in obj_props_div: 
        sup = el.findAll("dd")
        domain_and_range = {}
        for dd in sup:
            if len(domain_and_range) == 0:
                domain_and_range["domain"] = dd.find(text=True)
            elif len(domain_and_range) == 1:
                domain_and_range["range"] = dd.find(text=True)
        domain_and_range["iri"] = el.find("a")['name']
        obj_props[(el.find("h3").find(text=True))] = domain_and_range
    return obj_props

#DATA PROPERTIES
def extractDataProperties(soup):
    data_props_div = soup.find(id="dataproperties").findAll("div", {"class": "entity"})
    data_props = {}
    for el in data_props_div: 
        sup = el.findAll("dd")
        domain_and_range = {}
        for dd in sup:
            if len(domain_and_range) == 0:
                domain_and_range["domain"] = dd.find(text=True)
            elif len(domain_and_range) == 1:
                domain_and_range["range"] = dd.find(text=True)
        domain_and_range["iri"] = el.find("a")['name']
        data_props[(el.find("h3").find(text=True))] = domain_and_range
    return data_props


#NAMED INDIVIDUALS
def extractIndividuals(soup):
    individuals_id = soup.find(id="namedindividuals")
    individuals_div = individuals_id.findAll("div", {"class": "entity"}) if individuals_id != None else []
    individuals = {}
    for el in individuals_div:
        a_list = []
        sup = el.findAll("dd")
        a_dict = {}
        for dd in sup:
            if len(a_dict) == 0:
                a_dict["belongs_to"] = dd.find(text=True)
            elif len(a_dict) > 0:
                temporary_list = []
                facts = dd.findAll("a") + dd.findAll("span", {"class": "literal"})
                for fact in facts:
                    temporary_list.append(fact.find(text=True))
                a_list.append(temporary_list)
                a_dict["facts"] = a_list
            a_dict["iri"] = el.find("a")['name']
        individuals[(el.find("h3").find(text=True))] = a_dict
    return individuals

#NAMESPACES
def extractIndividuals(soup):
    namespacedeclarations_div = soup.find(id="namespacedeclarations")
    namespacedeclarations = {}
    for prefix, ref in zip(namespacedeclarations_div.findAll("dt"), namespacedeclarations_div.findAll("dd")):
        namespacedeclarations[prefix.find(text=True)] = ref.find(text=True)
    return namespacedeclarations

classes = extractClasses(soup)
obj_props = extractObjProperties(soup)
data_props = extractDataProperties(soup)
individuals = extractIndividuals(soup)
namespaces = extractIndividuals(soup)
