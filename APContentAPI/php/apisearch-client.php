<?php
$apikey = "";       ### Place your private ApiKey value here
$keyword_search = "star wars";

$apiSearch = "http://api.ap.org/v2/search/photo";

$searchRequest = $apiSearch . "?apikey={$apikey}&q=" . urlencode($keyword_search) . "&count=3";       ## Always encode your query

$contextOpts = array('http' =>
    array ( 'method' => 'GET',
            'header' => 'Accept: application/json' ) );
$context = stream_context_create($contextOpts);

print "Invoking AP Content API Search : " . $searchRequest . "\n";

$jsonResponse = file_get_contents($searchRequest, false, $context );

if ( $jsonResponse === false || strpos($http_response_header[0], ' 200 ' ) === false ) {
    print "Error response: " . $http_response_header[0] . "\n";
    exit;
}

print "HTTP Response: " . $http_response_header[0] . "\n";
print "\n";

$bomHead = substr($jsonResponse,0,2);
if ( $bomHead == "\xef\xbb" ) {               #  strip BOM if present
    $jsonResponse = substr($jsonResponse,3);
}

$jsonResults = json_decode($jsonResponse, true );

print "API Search Hits: " . $jsonResults['totalResults'] . "\n";
print "Hits on this page:\n\n";

$hitNo=0;
foreach ($jsonResults['entries'] as $searchHit ) {
    $imgUrl = "n/a";
    if ( count($searchHit['contentLinks']) > 1 )
      if ( $searchHit['contentLinks'][0]['rel'] == "thumbnail" )
        $imgUrl = $searchHit['contentLinks'][0]['href'];
      else if ( $searchHit['contentLinks'][1]['rel'] == "thumbnail" )
        $imgUrl = $searchHit['contentLinks'][1]['href'];
    ### IMPORTANT: To request $imgUrl you must add your apiKey parameter, i.e. $imgUrl .= "&apiKey={$apiKey}"
    print "#{$hitNo} Title: " . $searchHit['title'] . "\n";
    print "Thumbnail: " . $imgUrl . "\n";
    print "Full Metadata: " . $searchHit['id'] . "\n";          ### always provide your apiKey parameter on requests
    print "\n";
    $hitNo++;
}

if ( isset($jsonResults['nextpage']) )
     print "End of page. Request next page: " . $jsonResults['nextpage'] . "\n";
    ### IMPORTANT: To request nextpage you must provide your apiKey parameter
else
    print "End of results\n";



