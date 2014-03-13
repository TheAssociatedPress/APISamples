__author__ = 'dalegaspi'

import requests

def main():

    # sign up for developer key at http://developer.ap.org/
    apikey = '** your API key **' 
    
    keyword_search = 'star wars'

    url = 'http://api.ap.org/v2/search/photo'

    payload = requests.get('http://api.ap.org/v2/search/photo',
                           headers={'accept': 'application/json'},
                           params={'apikey': apikey, 'q': keyword_search, 'count': '1'})

    # requests does not automatically handle BOM for UTF-8, hence specifying the encoding
    # with utf-8-sig
    payload.encoding = 'utf-8-sig'
    payload = payload.json()

    suggested_term = payload['suggestedTerm']['title']

    print 'suggested term: "{0}"'.format(suggested_term)
    print 'title of the most recent image about "{0}" is "{1}"'.format(keyword_search, payload['entries'][0]['title'])

    img_url = next(u['href'] for u in payload['entries'][0]['contentLinks'] if u['rel'] == 'thumbnail')

    print 'downloading thumbnail link {0}'.format(img_url)

    img_payload = requests.get(img_url, params={'apikey': apikey})
    if img_payload.status_code == 200:
        f = open('/tmp/thumbnail.jpg', 'wb')
        f.write(img_payload.content)
        f.close()

if __name__ == "__main__":
    main()
