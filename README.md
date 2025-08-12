# APISamples

This is a repository of code samples for the Associated Press APIs. For more information about the APIs, visit [AP Developer portal](https://developer.ap.org).

## AP Media API

Contact [AP Customer Support](https://customerzone.ap.org/s/contactsupport) to sign up for an API key required to use the code in the MediaAPI repository.

For the complete documentation of the API methods, refer to the [AP Media API developer's guide](https://api.ap.org/media/v/docs/).

### Concepts demonstrated in the code samples

- Issuing a search request
- Transitioning from /search to /feed
- Issuing a feed request
- Saving a search or feed response payload
- Long polling on a feed request
- Downloading and saving renditions
- Following redirects
- Downloading priced renditions (disabled by default)
- Fetching associations
- Processing associations: saving metadata, fetching and saving renditions
- Basic error handling

### Concepts NOT demonstrated

- Handling quota violations
- Complete handling of pricing exceptions
- Caching concepts with ETags (some mentions in comments)
- Anything with meta {} block; for example, pricing and products
- /account/* calls

## AP Metadata Services (APMS) APIs

Contact [AP Customer Support](https://customerzone.ap.org/s/contactsupport) to sign up for an API key required to use the code in the APMS repository.

For the complete documentation of the API methods, refer to the [APMS developer's guide](https://developer.ap.org/ap-metadata-services/AP_Metadata_Services_Developer_Guide.pdf).