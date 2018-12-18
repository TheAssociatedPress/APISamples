@prefix rdfs: <http://www.w3.org/2000/01/rdf-schema#> .  
@prefix foaf: <http://xmlns.com/foaf/0.1/> .  
@prefix owl: <http://www.w3.org/2002/07/owl#> .  
@prefix skos: <http://www.w3.org/2004/02/skos/core#> .  
@prefix dc: <http://purl.org/dc/terms/> .  
@prefix xsd: <http://www.w3.org/2001/XMLSchema#> .  
@prefix geo: <http://www.w3.org/2003/01/geo/> .  
@prefix gr: <http://rs.tdwg.org/ontology/voc/GeographicRegion#> .  
@prefix org: <http://www.w3.org/TR/vocab-org/> .  
@prefix vcard: <http://www.w3.org/2006/vcard/ns#> .  
@prefix dbprop: <http://dbpedia.org/property/> .  
@prefix dbpedia-owl: <http://dbpedia.org/ontology/> .  

------

skos:Concept  
  a  owl:Class ;  
  rdfs:subClassOf pub:Terminology_Management ;  
  rdfs:label "Concept"@en .  

skos:exactMatch  
	a owl:DatatypeProperty ;         
	rdfs:label "has exact match"@en ;  
	rdfs:domain skos:Concept ;  
	rdfs:comment "used to link two concepts, indicating a high degree of confidence that the concepts can be used interchangeably across a wide range of information retrieval applications."@en  .  

skos:closeMatch  
	a owl:DatatypeProperty ;  
	rdfs:label "has close match"@en ;  
	rdfs:domain skos:Concept ;  
	rdfs:comment "used to link two concepts that are sufficiently similar that they can be used interchangeably in some information retrieval applications."@en  .  

skos:relatedMatch  
	a owl:DatatypeProperty ;     
	rdfs:label "has related match"@en ;  
	rdfs:domain skos:Concept ;  
	rdfs:comment "used to state an associative mapping link between two conceptual resources in different concept schemes."@en  .  	

skos:broadMatch  
	a owl:DatatypeProperty ;   
	rdfs:label "has broader match"@en ;  
	rdfs:domain skos:Concept ;  
	rdfs:comment "used to state a hierarchical mapping link between two conceptual resources in different concept schemes."@en  .  	

skos:narrowMatch  
	a owl:DatatypeProperty ;  
	rdfs:label "has narrower match"@en ;  
	rdfs:domain skos:Concept ;  
	rdfs:comment "used to state a hierarchical mapping link between two conceptual resources in different concept schemes."@en  .  			
skos:broader  
    a owl:ObjectProperty ;  
    rdfs:label "broader"@en ;  
    rdfs:domain skos:Concept ;  
    rdfs:range skos:Concept  ;   
    rdfs:comment "used to assert a direct hierarchical link between two SKOS concepts."@en  .  
	
skos:related  
    a owl:ObjectProperty ;  
    rdfs:label "related"@en ;  
    rdfs:domain skos:Concept ;  
    rdfs:range skos:Concept  ;  
    rdfs:comment "used to assert an associative link between two SKOS concepts."@en  .  

skos:altLabel  
  a owl:DatatypeProperty ;  
  rdfs:label "alternative label"@en ;  
  rdfs:comment "An alternative lexical label for a resource."@en ;  
  rdfs:domain skos:Concept .  
  
skos:changeNote  
  a owl:DatatypeProperty ;  
  rdfs:label "change note"@en ;  
  rdfs:comment "A note about a modification to a concept."@en ;  
  rdfs:subPropertyOf skos:note ;  
  rdfs:domain skos:Concept .  

rdfs:comment  
  a owl:DatatypeProperty ;  
  rdfs:label "definition"@en ;  
  rdfs:comment "A statement or formal explanation of the meaning of a concept."@en ;  
  rdfs:subPropertyOf skos:note ;  
  rdfs:domain skos:Concept .  

skos:note  
  a owl:DatatypeProperty ;  
  rdfs:label "note"@en ;  
  rdfs:comment "A general note, for any purpose."@en ;  
  rdfs:domain skos:Concept .  
    
skos:inScheme  
  a owl:ObjectProperty ;  
  rdfs:label "in scheme"@en ;  
  rdfs:domain skos:Concept ;  
  rdfs:range ap:Authority  .  
 
dc:created  
  a owl:DatatypeProperty ;  
  rdfs:label "date created"@en ;  
  rdfs:domain ap:Concept .  
  
dc:modified  
  a owl:DatatypeProperty ;  
  rdfs:label "date modified"@en ;  
  rdfs:domain ap:Concept .  
 
foaf:homepage  
  a owl:DatatypeProperty ;  
  rdfs:label "homepage"@en ;  
  rdfs:domain ap:Concept .  
    
org:memberOf  
    a owl:ObjectProperty ;  
    rdfs:label "member of"@en ;  
    rdfs:domain ap:OrganizationOrPerson ;  
    rdfs:range ap:AllOrganizations ;  
    rdfs:comment "property indicating a member of an Organization with no indication of the nature of that membership or the role played."@en .  

vcard:locality  
  a owl:DatatypeProperty ;  
  rdfs:label "locality"@en ;  
  rdfs:domain <http://cv.ap.org/ns#Organization> .  
  
vcard:region  
  a owl:DatatypeProperty ;  
  rdfs:label "region"@en ;  
  rdfs:domain <http://cv.ap.org/ns#Organization> .  
  
vcard:country-name    
  a owl:ObjectProperty ;  
  rdfs:label "country name"@en ;  
  rdfs:domain  <http://cv.ap.org/ns#Organization> ;  
  rdfs:range <http://cv.ap.org/ns#Geography>  .  

geo:lat  
  a owl:DatatypeProperty ;  
  rdfs:label "latitude"@en ;  
  rdfs:domain ap:Geography .  

geo:long  
  a owl:DatatypeProperty ;  
  rdfs:label "longitude"@en ;  
  rdfs:domain ap:Geography .  

gr:iso2Code  
  a owl:DatatypeProperty ;  
  rdfs:label "ISO 3166-1 alpha-2"@en ;  
  rdfs:domain ap:Geography .  
  
gr:iso3Code  
  a owl:DatatypeProperty ;  
  rdfs:label "ISO 3166-1 alpha-3"@en ;  
  rdfs:domain ap:Geography .  
   
dbpedia-owl:birthPlace  
  a owl:DatatypeProperty ;  
  rdfs:label "birth place"@en ;  
  rdfs:domain <http://cv.ap.org/ns#Person> .  
  
dbpedia-owl:birthDate  
  a owl:DatatypeProperty ;  
  rdfs:label "birth date"@en ;  
  rdfs:domain <http://cv.ap.org/ns#Person> .  

dbpedia-owl:deathDate  
  a owl:DatatypeProperty ;  
  rdfs:label "death date"@en ;  
  rdfs:domain <http://cv.ap.org/ns#Person> .  

foaf:gender  
  a owl:DatatypeProperty ;  
  rdfs:label "gender"@en ;  
  rdfs:domain <http://cv.ap.org/ns#Person>  .  

dbpedia-owl:team  
  a owl:ObjectProperty ;  
  rdfs:label "team"@en ;  
  rdfs:domain <http://cv.ap.org/ns#Person> ;  
  rdfs:range <http://cv.ap.org/ns#SportsOrganization>  .    
  
dbpedia-owl:party  
  a owl:ObjectProperty ;  
  rdfs:label "political party"@en ;  
  rdfs:domain <http://cv.ap.org/ns#Person> ;  
  rdfs:range <http://cv.ap.org/ns#Organization>  .    

dbprop:secCik  
  a owl:DatatypeProperty ;  
  rdfs:label "sec cik"@en ;  
  rdfs:domain <http://cv.ap.org/ns#Company> .  
