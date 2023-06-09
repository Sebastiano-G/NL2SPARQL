$(document).ready(function() {
    // Funzione per estrarre concetti e URI
    function extractConceptsAndURIs(data) {
      const parser = new DOMParser();
      const xmlDoc = parser.parseFromString(data, 'application/xml');
  
      const concepts = Array.from(xmlDoc.querySelectorAll('skos\\:Concept, Concept')).map(conceptNode => {
        const uri = conceptNode.getAttribute('rdf:about') || conceptNode.getAttribute('about');
        const prefLabel = conceptNode.querySelector('skos\\:prefLabel, prefLabel').textContent;
  
        return { uri, prefLabel };
      });
  
      const conceptURIs = concepts.map(concept => concept.uri);
  
      return { concepts, conceptURIs };
    }
  
    // Esempio di utilizzo
    fetch('https://op.europa.eu/o/opportal-service/euvoc-download-handler?cellarURI=http%3A%2F%2Fpublications.europa.eu%2Fresource%2Fcellar%2F17ed98cb-c33a-11ed-a05c-01aa75ed71a1.0001.04%2FDOC_1&fileName=filetypes-skos.rdf')
      .then(response => response.text())
      .then(data => {
        const { concepts, conceptURIs } = extractConceptsAndURIs(data);
  
        // Log dei concetti
        console.log('Concetti:');
        concepts.forEach(concept => {
          console.log('Etichetta preferita:', concept.prefLabel);
          console.log('URI:', concept.uri);
          console.log('---');
        });
  
        // Log degli URI dei concetti
        console.log('URI dei concetti:');
        conceptURIs.forEach(uri => {
          console.log(uri);
        });
      })
      .catch(error => {
        console.error('Errore durante il caricamento del file RDF:', error);
      });
  });
  