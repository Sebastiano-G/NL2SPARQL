# NL2SPARQL
Natural Language to Sparql Query Language

Competency questions analysis available at this [link](https://docs.google.com/spreadsheets/d/1KJ0Jx0Jem_frTjoJt80ZCkbYefHMMwLnNWUb-pid3Ys/edit#gid=0)

The SequenceExtract.py script attempts to isolate the predicates and entities that make up questions, while ExtendedSequenceExtract.py provides meaningful grammatical and syntactic analysis. 

## Scripts organization

Let's consider the following question "What are the topics of a song?". This question will processed to produce the following outputs:

| **File**   | **Output**                                                                                 |
| ---------- | ------------------------------------------------------------------------------------------ |
| [SequenceExtraction.py](https://github.com/Sebastiano-G/NL2SPARQL/blob/main/SequenceExtraction.py) |{'question': 'Which', 'predicate1': 'are', 'entity1': 'topics', 'entity2': 'song'}|
| [ExtendedSequenceExtract.py](https://github.com/Sebastiano-G/NL2SPARQL/blob/main/ExtendedSequenceExtract.py) |['Which', 'TO-BE-VERB', 'NOUN', 'of', 'NOUN'] |            
| [LodeExtractor.py](https://github.com/Sebastiano-G/NL2SPARQL/blob/main/LodeExtractor.py)| [example notebook](https://github.com/Sebastiano-G/NL2SPARQL/blob/main/Parsing%20OWL%20ontology.ipynb)|
| [ToSPARQL.py](https://github.com/Sebastiano-G/NL2SPARQL/blob/main/ToSPARQL.py) |  <code> SELECT ?topics WHERE { </code><br><code> ?topics <https://songstopoems.github.io/STOP/stopfinal.owl#appears_in> ?song . </code><br><code> ?topics hasType <https://songstopoems.github.io/STOP/stopfinal.owl#Topic> . </code><br><code> ?song hasType <https://songstopoems.github.io/STOP/stopfinal.owl#Song> . } </code>|
