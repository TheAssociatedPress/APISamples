var request = require('request');
var apiKey = ''; // Add your API key here!

exports.index = function(req, res) {
	var keyword = 'bitcoin';
	
	// Read a keyword from the url.
	if (req.query.keyword != null && req.query.keyword.length > 0) {
		keyword = req.query.keyword;
	}

	// Call the AP Content API.
	request({ url: 'http://api.ap.org/v2/search/photo?q=' + keyword + '&count=10&apiKey=' + apiKey, headers: { 'accept' : 'application/json' } }, function(error, response, body) {
		// Strip UTF-8 BOM bytes from response.
		body =  body.replace('\ufeff', '');

		// Render view.
		res.render('index', { results: JSON.parse(body), apiKey: apiKey, keyword: keyword });
	});
};