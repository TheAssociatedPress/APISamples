#!/usr/bin/perl
$| = 1;
use XML::Simple;
use Data::Dumper;
use LWP::UserAgent;

# Content API key provided by The Associated Press
my $apiKey = "Your AP Content API key goes here";

# Search terms passed in on the command line as a parameter to the script
my $searchTerms = $ARGV[0];
$searchTerms =~ s/ /\%20/g;

# Number of results, defaults to 10
my $numResults = 10;
if($ARGV[1]){
	$numResults = $ARGV[1];
}

# Content API URL
my $apiBaseUrl = "http://api.ap.org/v2/search";
my $apiUrlArgs = "?count=" . $numResults . "&apikey=" . $apiKey . "&q=" . $searchTerms;
my $apiUrl = $apiBaseUrl . $apiUrlArgs;

#### Make the Content API Request ####
my $userAgent = new LWP::UserAgent;
$userAgent->agent("APContentAPIFetcher/1.0");

print "Making AP Content API request...\n";
print "   APIUrl: " . $apiBaseUrl . "\n";
print "   APIKey: " . $apiKey . "\n";
print "   Query : " . $searchTerms . "\n";
print "   Count : " . $numResults . "\n";
my $startTime = time;
my $request = new HTTP::Request("GET", $apiUrl);
my $response = $userAgent->request($request);
my $requestTime = time - $startTime;
print "Got AP Content API response...\n";
print "   HTTP " . $response->code . " - " . length($response->content) . " bytes in " . $requestTime . " seconds.\n";

#### Parse the Content API Response into XML ####
my $xmlResponse = new XML::Simple(KeyAttr=>[]);
my $xmlData = $xmlResponse -> XMLin($response->content);

#### Loop through each feed item ####
print "   Feed Items...\n";
foreach my $entry(@{$xmlData->{entry}}){
	my $entryId = $entry->{id};
	$entryId =~ s/.*\///g;
	$entryId =~ s/\?.*//g;
	print "      id: " . $entryId . "\n";
	
	#### Loop through each item's link and save all 3 photo sizes ####
	foreach my $link(@{$entry->{link}}){
		my $rel = $link->{rel};
		print "         link: " . $rel . "\n";
		if($rel =~ /thumbnail/i || $rel =~ /preview/i || $rel =~ /main/i){
			my $href = $link->{href};
			$href =~ s/\&amp\;/\&/g;
			$href .= "&apikey=" . $apiKey;
			my $fileExt = $href;
			$fileExt =~ s/.*\.//;
			$fileExt =~ s/\&.*//;
			my $fileName = $entryId . "." . $rel . "." . $fileExt;
			my $fileStartTime = time;
			print "            Making AP Content API request for $fileName...\n";
			my $fileRequest = new HTTP::Request("GET", $href);
			my $fileResponse = $userAgent->request($fileRequest);
			my $fileRequestTime = time - $fileStartTime;
			print "            Got AP Content API response...\n";
			print "               HTTP " . $fileResponse->code . " - " . length($fileResponse->content) . " bytes in " . $fileRequestTime . " seconds.\n";
			open(FILE, ">$fileName");
			binmode(FILE);
			print FILE $fileResponse->content;
			close(FILE);
			print "               Wrote " . $fileName . "\n";
		}
	}
}
