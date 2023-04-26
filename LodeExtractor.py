import urllib.request
from bs4 import BeautifulSoup

class OntologyExtractor(object):
    def __init__(self, link):
        self.link = link
        base_url = "https://w3id.org/lode/"
        page = urllib.request.urlopen(base_url + link)
        soup = BeautifulSoup(page)
        self.soup = soup

        
    #CLASSES: da aggiungere casi di errore
    def extractClasses(self):
        classes_div = self.soup.find(id="classes").findAll("div", {"class": "entity"})
        classes = {}
        for el in classes_div:
            inner_dict = {}
            dts = el.findAll("dt") 
            dds = el.findAll("dd")
            for idx in range(len(dts)):
                a_list = []
                for a in dds[idx].findAll("a"):
                    a_list.append(a.find(text=True))
                inner_dict[str(dts[idx].find(text=True))] = a_list
            inner_dict["iri"] = el.find("a")['name']
            classes[str((el.find("h3").find(text=True)))] = inner_dict
        return classes
        
    #OBJECT PROPERTIES
    def extractObjProperties(self):
        obj_props_div = self.soup.find(id="objectproperties").findAll("div", {"class": "entity"})
        obj_props = {}
        for el in obj_props_div: 
            sup = el.findAll("dd")
            dts = el.findAll("dt")
            domain_and_range = {}
            for dd in sup:
                if len(domain_and_range) == 0 and dts[0].find(text=True) == "has domain":
                    domain_and_range["domain"] = dd.find(text=True)
                elif len(domain_and_range) == 1 and dts[1].find(text=True) == "has range":
                    domain_and_range["range"] = dd.find(text=True)
            domain_and_range["iri"] = el.find("a")['name']
            obj_props[str((el.find("h3").find(text=True)))] = domain_and_range
        return obj_props

    #DATA PROPERTIES
    def extractDataProperties(self):
        data_props_div = self.soup.find(id="dataproperties").findAll("div", {"class": "entity"})
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
    def extractIndividuals(self):
        individuals_id = self.soup.find(id="namedindividuals")
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
            individuals[str((el.find("h3").find(text=True)))] = a_dict
        return individuals

    #NAMESPACES
    def extractIndividuals(self):
        namespacedeclarations_div = self.soup.find(id="namespacedeclarations")
        namespacedeclarations = {}
        for prefix, ref in zip(namespacedeclarations_div.findAll("dt"), namespacedeclarations_div.findAll("dd")):
            namespacedeclarations[prefix.find(text=True)] = ref.find(text=True)
        return namespacedeclarations

