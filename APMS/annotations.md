# Annotate a Document

Annotate a Document. Requires a valid API Key for authentication.

**URL** : `/annotations/`

**Method** : `POST`

**Auth required** : YES

**Permissions required** : Must be permitted to access one or more annotation features.

**Data constraints**

Required: provide document to be annotated.
Optional: one or more features to apply to the document

```json
{
    "document": "[unicode-encoded document to be annotated]"
}
```

**Data example** "document" is the only required property.

```json
{
    "document": "When a dog bites a man, that is not news, because it happens so often. But if a man bites a dog, that is news."
}
```

Optional: one or more features to apply to the document

```json
{
    "meta":
	{ "features": [ {"name" : "AP"}]},
    "document": "[unicode-encoded document to be annotated]"
}
```

## Success Response

**Condition** : If everything is OK, annotation contains the RDF results of the annotations features applied to the document.

**Code** : `200 OK`

**Content example**

```json
{
	"elapsedtime":995,
	"documentid":"f4fdf9a5fdeb4e98a26c55625e16f743",
	"annotation":"<?xml version=\"1.0\" encoding=\"UTF-8\"?>\n<rdf:RDF\n xmlns:rdf=\"http://www.w3.org/1999/02/22-rdf-syntax-ns#\"\n>\n</rdf:RDF>\n"
}
```

## Error Responses

**Condition** : If API Key is invalid

**Code** : `401 UNAUTHORIZED`

**Content example**

```json
{
	"fault":
		{
			"faultstring":"Invalid ApiKey",
			 "detail":
			{
				"errorcode":"oauth.v2.InvalidApiKey"
			}
		}
}
```

### Or

**Condition** : If fields are missed.

**Code** : `400 BAD REQUEST`

**Content example**

```json
{
	"elapsedtime":1,
	"documentid":"8574ff38a1c442c095628a7646a55ece",
	"message":"Format contains syntax errors or submitted format is invalid"
}
```
