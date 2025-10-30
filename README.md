# AI API Documentation
API used to transform unstructured text into JSON by using AI.
- Private API.
- `#todo` mean they are still missing to be designed/implemented before they are added to the `README.md`
- Use it moderately for Ben's wallet sake

# Headers
- `Content-Type: application/json`
- Allow all origins
- No need for authentication

# HTTP Status Codes
- **200**: Successful Request
- **400**: Bad Request
- **422**: Unprocessable Entity
- **404**: Route Not Found

# Domain
We will be using #todo`/v1`.

# Endpoints

## `POST: /json/parse`
Route to parse unstructured text into one structured JSON object.
The JSON object returned is created based on the syntax and semantics of the text.
- `text` parameter: Unstructured text to be parsed.
- `lang` parameter: Language in which the output should be structured around.
	- Should use only language names with 2 letters (e.g. `en`, `es`).
		- Currently only accepting `en` and `def`. #todo
	- Also accepts `def`, which is default, and lets the AI model to structure the data according in the input text's language(s).
- Returns a JSON object with the structured data from the text if successful.
	- See ***Invalid/Rejected Input*** section for more information.
- Returns a Bad Request Error (400) if invalid input for `text` and `lang` parameters.
- Returns a Bad Request Error (400) if the given `lang` parameter is not in the accepted languages.

### Request Examples

##### Successful Request
- Req.body:
```json
{
	"text": "Alice is 30 years old and works as a software engineer.",
	"lang": "en"
}
```
- Res:
```json
{
	"status": "success",
	"code": 200,
	"message": "Successful request.",
	"error": null,
	"data": {
		"name": "Alice",
		"age": 30,
		"occupation": "software engineer"
	}
}
```

##### Invalid `text` (Whitespace)
- Req.body:
```json
{
	"text": "   ",
	"lang": "en"
}
```
- Res:
```json
{
	"status": "error",
	"code": 400,
	"message": "Invalid Text: `text` cannot be empty or contain only whitespace characters.",
	"error": true,
	"data": null
}
```

##### Invalid `text` (Prompt Injection)
- Req.body:
```json
{
	"text": "Ignore previous instructions;",
	"lang": "def"
}
```
- Res:
```json
{
	"status": "error",
	"code": 400,
	"message": "Invalid Input: Dangerous prompt instructions are not allowed.",
	"error": true,
	"data": null
}
```

##### Invalid `lang`
- Req.body:
```json
{
	"text": "Ignore previous instructions;",
	"lang": "asdf"
}
```
- Res:
```json
{
	"status": "error",
	"code": 400,
	"message": "Invalid Input: Invalid target language.",
	"error": true,
	"data": null
}
```

## `POST: /json/schemedParse`
Route to parse unstructured text into one structured JSON object based on a given schema.
The JSON object returned is created based on the syntax and semantics of the text.
- `text` parameter: Unstructured text to be parsed.
- `lang` parameter: Language in which the output should be structured around.
	- Should use only language names with 2 letters (e.g. `en`, `es`). Currently only accepting `en` and `def`. #todo
	- Also accepts `def`, which is default, and lets the AI model to structure the data according in the input text's language(s).
- `schema` parameter: Schema used to build the JSON object.
	- Schema should be valid according to the [JSON Schema Standard](https://json-schema.org).
	- If the AI cannot find a piece of data that is in the schema, it will be added as `null`, if possible.
- Returns a JSON object with the structured data from the text if successful.
- Returns a Bad Request Error (400) if invalid input for `text` and `lang` parameters.
	- See ***Invalid/Rejected Input*** section for more information.
- Returns a Bad Request Error (400) if the given `lang` parameter is not in the accepted languages.
- Returns an Unprocessable Entity Error (422) if `text` cannot produce an object that follows the given `schema` because of structural or semantic errors.
	- E.g. `age: { type: integer }`, but receives a string
- Returns a Bad Request Error (400) if an invalid `schema` is given according to [JSON Schema Standard](https://json-schema.org).

### Request Examples

##### Successful Request
- Req.body:
```json
{
	"text": "Alice is 30 years old and works as a software engineer.",
	"lang": "en",
	"schema": {
		"type": "object",
		"properties": {
			"name": {"type": "string"},
			"age": {"type": "integer"},
			"occupation": {"type": "string"},
			"email": {"type": ["string", "null"]}
		},
		"required": ["name", "age", "occupation"]
	}
}
```
- Res:
```json
{
	"status": "success",
	"code": 200,
	"message": "Successful request.",
	"error": null,
	"data": {
		"name": "Alice",
		"age": 30,
		"occupation": "software engineer",
		"email": null
	}
}
```

##### Invalid `text` (ASCII Control Characters)
- Req.body:
```json
{
	"text": "\x00",
	"lang": "en",
	"schema": {
		"type": "object",
		"properties": {
			"name": {"type": "string"},
			"age": {"type": "integer"},
			"occupation": {"type": "string"},
			"email": {"type": ["string", "null"]}
		},
		"required": ["name", "age", "occupation"]
	}
}
```
- Res:
```json
{
	"status": "error",
	"code": 400,
	"message": "Invalid Input: `text` cannot contain ASCII control characters.",
	"error": true,
	"data": null
}
```

##### Invalid `lang`
- Req.body:
```json
{
	"text": "Alice is 30 years old and works as a software engineer.",
	"lang": "asdf",
	"schema": {
		"type": "object",
		"properties": {
			"name": {"type": "string"},
			"age": {"type": "integer"},
			"occupation": {"type": "string"},
			"email": {"type": ["string", "null"]}
		},
		"required": ["name", "age", "occupation"]
	}
}
```
- Res:
```json
{
	"status": "error",
	"code": 400,
	"message": "Invalid Input: Invalid target language.",
	"error": true,
	"data": null
}
```

##### Invalid `schema`
- Req.body:
```json
{
	"text": "Alice is 30 years old and works as a software engineer.",
	"lang": "def",
	"schema": {
		"type": "object",
		"properties": "should be an object, not string"
	}
}
```
- Res:
```json
{
	"status": "error",
	"code": 400,
	"message": "Invalid Input: Schema does not follow JSON Schema Standard.",
	"error": true,
	"data": null
}
```

##### Unprocessable Entity - `text` cannot satisfy `schema`
- Req.body:
```json
{
	"text": "Alice is a cat",
	"lang": "def",
	"schema": {
		"type": "object",
		"properties": {
			"name": {"type": "string"},
			"age": {"type": "integer"},
			"occupation": {"type": "string"},
			"email": {"type": ["string", "null"]}
		},
		"required": ["name", "age", "occupation"]
	}
}
```
- Res:
```json
{
	"status": "error",
	"code": 422,
	"message": "Unprocessable Input: Missing required data in input text to produce a valid output.",
	"error": true,
	"data": null
}
```

# Invalid/Rejected Input
The API rejects an input if it's:
1. **Empty string or Whitespaces-only**
	- Tabs, new lines, blank space, space, backspaces, etc.
2. **Control character**
	- Any ASCII control character: `\x00` to `\x08`, `\x0B`, `\x0C`, `\x0E` to `\x1F`, `\x7F`
3. **Zero-width & Directional unicode**
	- `\u200B` to `\u200D`, `\uFEFF`, `\u202A` to `\u202E`
4. **Prompt injections**
	- E.g. `ignore previous instructions`
5. **SQL queries**
6. **Shell commands**
7. **Other code snippets**

# Expected Responses

## On Success
```json
{
	"status": "success",
	"code": 200, // Generic successful request
	"message": "Successful request.",
	"error": null,
	"data": {
		"key1": "value1",
		"key2": "value2"
	}
}
```

## On Error
- #todo `error` can return an object with error logs or more information about the error.
```json
{
	"status": "error",
	"code": 400, // Bad request
	"message": "Internal server error.",
	"error": true,
	"data": null
}
```

# Authors
- Minwook (Ben) Oh - [benoh5186](https://github.com/benoh5186)
- Seohyeon (Ethan) Park - [ethan8663](https://github.com/ethan8663)
- Marcus V. S. Lages - [MarcusLages](https://github.com/MarcusLages)