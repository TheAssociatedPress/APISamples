APISamples
==========

This is a repository of code samples for the Associated Press APIs.  

You will need to [sign up for an API key](http://developer.ap.org/) before you can use any of the code in this repository.

#AP Content API

The full developer's guide can be found [here](http://developer.ap.org/files/AP_Content_API_Developer_Guide.pdf).

##Basic Search

Basic search can be achieved using the following HTTP GET call:

```
http://api.ap.org/v2/search/{mediatype}?apikey={apikey}&q={searchterms}
```

`mediatype` can be *photo*, *video*, or *graphic* depending on the media type you are looking for.  `apikey` is your API key and `q` is your search terms.  As an example:

```
http://api.ap.org/v2/search/photo?apikey=your_api_key&q=computer
```

This returns photos about the search term "computer."

###Payload Format Support

The API returns XML (Atom 1.0) by default, but it can return JSON by applying `accept:application/json` in the header and JSONP by passing a `callback` HTTP GET parameter.  Here is an example snippet in Python requesting for a JSON payload:

```python
import requests

apikey = 'my_api_key'
keyword_search = 'star wars'

url = 'http://api.ap.org/v2/search/photo'

payload = requests.get('http://api.ap.org/v2/search/photo',
                       headers={'accept': 'application/json'},
                       params={'apikey': apikey, 'q': keyword_search})
```


