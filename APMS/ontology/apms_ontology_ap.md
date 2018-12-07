@prefix ap: <http://cv.ap.org/ns#> .

ap:Concept
  a owl:Class ;
  rdfs:label "AP Concept"@en ;
  rdfs:subClassOf skos:Concept .

ap:Authority
  a owl:Class ;
  rdfs:label "AP Authority"@en ;
  rdfs:subClassOf ap:Concept .
    
ap:Classification
  a owl:Class ;
  rdfs:label "Classification"@en ;
  rdfs:subClassOf ap:Concept , 
  [
    a owl:Restriction ;
    owl:onProperty <http://cv.ap.org/ns#isPlaceholder> ;
    owl:maxCardinality "1"^^xsd:nonNegativeInteger 
  ].
    
ap:Event
  a owl:Class ;
  rdfs:label "Event"@en ;
  rdfs:subClassOf ap:Classification .

ap:Geography
  a owl:Class ;
  rdfs:label "Geography"@en ;
  rdfs:subClassOf ap:Classification  .
  
ap:PhysicalFeature
  a owl:Class ;
  rdfs:label "Physical feature"@en ;
  rdfs:subClassOf ap:Geography .
  
ap:PointOfInterest
  a owl:Class ;
  rdfs:label "Point of interest"@en ;
  rdfs:subClassOf ap:Geography .
  
ap:Industry
  a owl:Class ;
  rdfs:label "Industry"@en ;
  rdfs:subClassOf ap:Classification .
  
ap:Organization
  a owl:Class ;
  rdfs:label "Organization"@en ;
  rdfs:subClassOf ap:Classification, ap:OrganizationOrPerson, ap:AllOrganizations .
  
ap:Company
  a owl:Class ;
  rdfs:label "Company"@en ;
  rdfs:subClassOf ap:Organization .  

ap:SportsOrganization
  a owl:Class ;
  rdfs:label "Sports organization"@en ;
  rdfs:subClassOf ap:Organization .  

ap:Person
  a owl:Class ;
  rdfs:label "Person"@en ;
  rdfs:subClassOf ap:Classification, ap:OrganizationOrPerson .

ap:BusinessLeader
  a owl:Class ;
  rdfs:label "Business leader"@en ;
  rdfs:subClassOf ap:Person ;
  rdfs:comment "A Company executive or other newsmaker in the business world."@en .  
  		
ap:Politician
  a owl:Class ;
  rdfs:label "Politician"@en ;
  rdfs:subClassOf ap:Person ;
  rdfs:comment "A person in a policy-making or decision-making role in the government of a geopolitical entity, such as a senator, congress person, governor, or president."@en.  
  
ap:SportsFigure
  a owl:Class ;
  rdfs:label "Sports figure"@en ;
  rdfs:subClassOf ap:Person ;
  rdfs:comment "An athlete participating in professional or collegiate sports, or in major amateur events."@en.  

ap:Subject
  a owl:Class ;
  rdfs:label "Subject"@en ;
  rdfs:subClassOf ap:Classification . 

ap:USState
  a owl:Class ;
  rdfs:label "US State"@en ;
  rdfs:subClassOf ap:Geography .    

ap:Sport
  a owl:Class ;
  rdfs:label "Sport"@en ;
  rdfs:subClassOf ap:Subject .  

ap:LocationType
  a owl:Class ;
  rdfs:label "Location type"@en ;
  rdfs:subClassOf ap:Concept .
  
ap:OrganizationType
  a owl:Class ;
  rdfs:label "Organization type"@en ;
  itm:param "searchable" ;	
  rdfs:subClassOf ap:Concept .

ap:EventType
  a owl:Class ;
  rdfs:label "Event type"@en ;
  rdfs:subClassOf ap:Concept .
  
ap:PersonType
  a owl:Class ;
  rdfs:label "Person type"@en ;
  rdfs:subClassOf ap:Concept . 
   
ap:OrganizationOrPerson
  a owl:Class ;
  rdfs:label "Organization OR Person"@en ;
  rdfs:comment "Abstract class used for Membership Association"@en .
  
ap:AllOrganizations
  a owl:Class ;
  rdfs:label "Organization OR SportsOrganization"@en ;
  rdfs:comment "Abstract class used for Membership Association"@en .

ap:displayLabel
  a owl:DatatypeProperty ;
  rdfs:label "display label"@en ;
  rdfs:domain ap:Concept ;
  rdfs:comment "property representing a lexical label to be used for various end-user displays, for example ones where an element of label disambiguation is needed."@en .
 
ap:inGroup
  a owl:DatatypeProperty ;
  rdfs:label "in group"@en ;
  rdfs:domain ap:Concept ;
  rdfs:comment "property representing the group membership of a term."@en .
 
ap:isPlaceholder
  a owl:ObjectProperty ;
  rdfs:label "placeholder"@en ;
  rdfs:domain ap:Classification ;
  rdfs:range xsd:boolean ;
  rdfs:comment "used to indicate if a term is used only for grouping other terms in hierarchical representations"@en .
  
ap:isReference
  a owl:ObjectProperty ;
  rdfs:label "reference"@en ;
  rdfs:domain ap:Classification ;
  rdfs:range xsd:boolean ;
  rdfs:comment "used to indicate a term available as part of the AP News Taxonomy, but not used by the AP Tagging Service."@en .
  
ap:eventType
  a owl:DatatypeProperty ;
  rdfs:label "event type"@en ;
  rdfs:domain ap:Event ;
  rdfs:comment "property representing a relationship between an event and its generic type (e.g., Entertainment event, Sports event)."@en .
  
ap:location
  a owl:ObjectProperty ;
  rdfs:label "location"@en ;
  rdfs:domain ap:Event ;
  rdfs:range ap:Geography ;
  rdfs:comment "property representing the location of an event or organization."@en .  

ap:associatedEventOf
  a owl:ObjectProperty ;
  rdfs:label "associated event of"@en ;
  rdfs:domain ap:Event ;
  rdfs:range ap:Person ;
  rdfs:comment "property representing a relationship between a person and a current event, typically, the person’s participation in or some significant contribution to the event. See ap:associatedEvent for the reciprocal property"@en . 

ap:location
  a owl:ObjectProperty ;
  rdfs:label "location"@en ;
  rdfs:domain ap:Organization ;
  rdfs:range ap:Geography ;
  rdfs:comment "property representing the location of an event or organization."@en .
  
ap:organizationType
  a owl:DatatypeProperty ;
  rdfs:label "organization type"@en ;
  rdfs:domain ap:Organization ;
  rdfs:comment "property representing a relationship between an organization and its generic type (e.g. Sports team, Sports league)."@en .
  
 ap:competitiveLevel
  a owl:DatatypeProperty ;
  rdfs:label "competitive level"@en ;
  rdfs:domain ap:SportsOrganization ;
  rdfs:comment "property used to indicate the competitive level of a sports team (e.g. Professional, College)."@en .

ap:sport
  a owl:ObjectProperty ;
  rdfs:label "sport"@en ;
  rdfs:domain ap:SportsOrganization ;
  rdfs:range ap:Sport ;
  rdfs:comment "property representing a relationship between an athlete or an organization and the sport they play or represent."@en .
   
ap:locationType
  a owl:DatatypeProperty ;
  rdfs:label "location type"@en ;
  rdfs:domain ap:Geography ;
  rdfs:comment "property used to indicate the generic type of a geographic entity, such as City, Province, Continent, etc."@en .  

ap:dependencyOf
  a owl:ObjectProperty ;
  rdfs:label "dependency of"@en ;
  rdfs:domain ap:Geography ;
  rdfs:range ap:Geography ;
  rdfs:comment "property used to indicate a political dependency between one geographic entity and another. See ap:hasDependency for reciprocal relationship."@en .

ap:hasDependency
  a owl:ObjectProperty ;
  rdfs:label "has dependency"@en ;
  rdfs:domain ap:Geography ;
  rdfs:range ap:Geography ;
  rdfs:comment "property used to indicate a political dependency between one geographic entity and another. See ap:dependencyOf for reciprocal relationship."@en .  
  
ap:locatedIn
  a owl:ObjectProperty ;
  rdfs:label "located in"@en ;
  rdfs:domain ap:PhysicalFeature ;
  rdfs:range ap:Geography ;
  rdfs:comment "property used to indicate a relationship between a physcal feature and its geographic location"@en .  
  
ap:personType
  a owl:DatatypeProperty ;
  rdfs:label "person type"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person>  ;
  rdfs:comment "property representing a relationship between a named person and their generic type (e.g., Artist, Athlete)."@en .
  
ap:associatedCountry
  a owl:ObjectProperty ;
  rdfs:label "associated country"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person> ;
  rdfs:range <http://cv.ap.org/ns#Geography>  ;
  rdfs:comment "property representing a relationship between a person and a related country."@en .

ap:associatedState
  a owl:ObjectProperty ;
  rdfs:label "associated state"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person> ;
  rdfs:range <http://cv.ap.org/ns#USState>  ;
  rdfs:comment "property representing a relationship between a person and a related U.S. state."@en .

ap:hometown
  a owl:DatatypeProperty ;
  rdfs:label "hometown"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person> ;
  rdfs:comment "property used to describe an athlete's hometown."@en .

ap:league
  a owl:ObjectProperty ;
  rdfs:label "league"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person> ;
  rdfs:range <http://cv.ap.org/ns#SportsOrganization>  ;
  rdfs:comment "property representing a relationship between an athlete and the sports league in which they play."@en .
  
ap:associatedEvent
  a owl:ObjectProperty ;
  rdfs:label "associated event"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person> ;
  rdfs:range <http://cv.ap.org/ns#Event>  ;
  rdfs:comment "property representing a relationship between a person and a current event, typically, the person’s participation in or some significant contribution to the event."@en .
  
ap:associatedCompany
  a owl:ObjectProperty ;
  rdfs:label "associated company"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person> ;
  rdfs:range <http://cv.ap.org/ns#Company>  ;
  rdfs:comment "property representing a relationship between a person and a company, typically, the person’s role in the operation of the company or corporate entity."@en .

ap:sport
  a owl:ObjectProperty ;
  rdfs:label "sport"@en ;
  rdfs:domain <http://cv.ap.org/ns#SportsFigure> ;
  rdfs:range <http://cv.ap.org/ns#Sport>  ;
  rdfs:comment "property representing a relationship between an athlete or an organization and the sport they play or represent."@en .
  
 ap:playerNumber
  a owl:DatatypeProperty ;
  rdfs:label "player number"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person> ;
  rdfs:comment "property used to describe an athlete's uniform number."@en .
   
ap:significantOther
  a owl:ObjectProperty ;
  rdfs:label "significant other"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person> ;
  rdfs:range <http://cv.ap.org/ns#Person> ;
  rdfs:comment "property representing a relationship between a person and his or her spouse or romantic partner"@en .
  
ap:formerSignificantOther
  a owl:ObjectProperty ;
  rdfs:label "former significant other"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person> ;
  rdfs:range <http://cv.ap.org/ns#Person> ;
  rdfs:comment "property representing a relationship between a person and his or her former spouse or romantic partner"@en .
  
ap:relative
  a owl:ObjectProperty ;
  rdfs:label "relative"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person> ;
  rdfs:range <http://cv.ap.org/ns#Person> ;
  rdfs:comment "property representing a relationship between a person and a member of his or her extended family, including grandparents, uncles, aunts, cousins, nephews or nieces."@en .	
  					
ap:siblingOf
  a owl:ObjectProperty ;
  rdfs:label "sibling of"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person> ;
  rdfs:range <http://cv.ap.org/ns#Person> ;
  rdfs:comment "property representing a relationship between a person and his or her sibling."@en .
  
ap:hasParent
  a owl:ObjectProperty ;
  rdfs:label "has parent"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person> ;
  rdfs:range <http://cv.ap.org/ns#Person> ;
  rdfs:comment "property representing a relationship between a person and his or her parent."@en .
  
ap:hasChild
  a owl:ObjectProperty ;
  rdfs:label "has child"@en ;
  rdfs:domain <http://cv.ap.org/ns#Person> ;
  rdfs:range <http://cv.ap.org/ns#Person> ;
  rdfs:comment "property representing a relationship between a person and his or her child."@en .

ap:associatedCompanyOf
  a owl:ObjectProperty ;
  rdfs:label "associated company of"@en ;
  rdfs:domain <http://cv.ap.org/ns#Company> ;
  rdfs:range <http://cv.ap.org/ns#Person>  ;
  rdfs:comment "property representing a relationship between a person and a company, typically, the company's associated members or governing figures."@en .
  
ap:industry
  a owl:ObjectProperty ;
  rdfs:label "industry"@en ;
  rdfs:domain <http://cv.ap.org/ns#Company> ;
  rdfs:range <http://cv.ap.org/ns#Industry> ;
  rdfs:comment "property representing a relationship between a company and a related Industry subject term."@en .

ap:instrument
  a owl:DatatypeProperty ;
  rdfs:label "instrument"@en ;
  rdfs:domain <http://cv.ap.org/ns#Company> ;
  rdfs:comment "property used to describe a company's ticker symbol and the stock exchange that it trades on, expressed as [Exchange]:[Ticker]. There can be multiple occurrences of ap:instrument for any single company."@en .

ap:shortName
  a owl:DatatypeProperty ;
  rdfs:label "short name"@en ;
  rdfs:domain <http://cv.ap.org/ns#Concept> ;
  rdfs:comment "property representing an equivalence relationship between a preferred term and a shorter, more common variant."@en .