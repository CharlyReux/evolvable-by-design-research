# Pivo documentation

The main idea of Pivo is that any resource you receive from the API are mapped to a "Semantic Resource", a semantic resource contains all the data that can be inferred from the openAPI specification.  


## Use-case documentation
This part of the documentation is centered on use-cases, i.e. it provides examples of how to use the library when you want to implement certain behaviors, Based on an existing annotated OpenAPI specification file.

Each of the use-cases depend on each others, from the top to the bottom.
```yml
openapi: 3.0.3
info:
  version: 1.0.0
  title: Object rest API
  contact:
    name: John Smith
    email: john.smith@mail.com
servers:
  - url: http://example.com:8080/rest
    description: example server
paths:
  /my_objects:
    get:
      parameters:
        - name: objectAttribute
          in: query
          description: The attribute of the objects to get
          x-@id: http://vocabulary.io/myVoc#objectAttribute
          schema: 
            $ref: '#/components/schemas/objectAttribute'
            default: false

      operationId: getAllObjects
      responses:
        '200':
          description: list of objects
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/objectList'
          links:
            createObject:
              operationId: createObject
              x-@relation: http://vocabulary.io/myVoc/rel#Create
    post:
      operationId: createObject
      x-@id: http://vocabulary.io/myVoc#CreateObject
      requestBody:
        content:
          application/json:
            schema:
              $ref: '#/components/schemas/object'
      responses:
        '201':
          description: The created todo
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/object'
          links:
            delete:
              operationId: deleteObject
              x-@relation: http://vocabulary.io/myVoc/rel#Delete
              parameters:
                id: '$response.body#/id'
            get:
              operationId: deleteObject
              x-@relation: http://vocabulary.io/myVoc/rel#GetObject
              parameters:
                id: '$response.body#/id'
  /my_object/{id}:
    parameters:
      - name: id
        in: path
        description: The id of the object to get
        x-@id: http://vocabulary.io/myVoc#objectId
        required: true
        schema: 
          $ref: '#/components/schemas/objectId'
    get:
      responses:
        '200':
          description: object with the id
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/object'
          links:
            getAll:
              operationId: getAllObjects
              x-@relation: http://vocabulary.io/myVoc/rel#GetAll
            delete:
              operationId: deleteObject
              x-@relation: http://vocabulary.io/myVoc/rel#Delete
              parameters:
                id: '$response.body#/id'
    delete:
      operationId: deleteObject
      responses:
        '204':
          description: confirmation
          links:
            getAll:
              operationId: getAllObjects
              x-@relation: http://vocabulary.io/myVoc/rel#GetAll

components:
  schemas:
    objectList:
      type: object
      x-@type: http://vocabulary.io/myVoc#objectList
      properties:
        objects:
          type: array
          items:
            $ref: '#/components/schemas/object'
    object:
      type: object
      x-@type: http://vocabulary.io/myVoc#objectType
      properties:
        id:
          $ref: '#/components/schemas/objectId'
        name:
          type: string
          x-@id: http://schema.org/name
        attribute:
          $ref: '#/components/schemas/objectAttribute'

    objectId:
      type: string
      x-@id: http://vocabulary.io/myVoc#objectId
    objectAttribute:
      type: boolean
      x-@id: http://vocabulary.io/myVoc#objectAttribute  


```



<table>
	<thead>
		<tr>
			<th>Use-case</th>
			<th>OpenApi file</th>
			<th>Pivo Usage</th>
		</tr>
	</thead>
	<tbody>
<tr>
<td><b>Instantiating a pivo object based on an openapi specification from an endpoint</b></td>
<td>

```js
import Pivo from '@evolvable-by-design/pivo'
...
const response = await axios.get(url)
const specString = await response.data
const pivo = new Pivo(documentation)

```
Or
```js
const pivo = Pivo.fetchDocumentationAndCreate(url)
```
</td>
</tr>
<tr>
<td><b>Getting a operation based on the return type</b></td>
<td>

```js
const myObjectOperation = pivo
.get("http://vocabulary.io/myVoc#objectList")
.getOrThrow(() => new Error('REST API operation not available'))
```

</td>
</tr>
<tr>
<td><b>Invoking an operation with a parameter</b></td>
<td>

```javascript
const objectAttribute = true
const myObjectResponse = await myObjectOperation.invoke({["http://vocabulary.io/myVoc#objectAttribute"]:objectAttribute})
```

</td>

</tr>
<tr>
<td><b>Getting an operation from a relation</b></td>
<td>

```javascript
const creationOperation = myObjectResponse.data
  .getRelation("http://vocabulary.io/myVoc/rel#Create")
  .map(relation => {
    return relation[0].operation
  })
  .getOrThrow(()=>new Error("no relation available to create an object"))
```

</td>

</tr>
<tr>
<td><b>Calling an operation with multiple parameters</b></td>
<td>

```javascript
const objectToCreate = { 
  ["http://schema.org/name"]: "the_object_name" ,
  ["http://vocabulary.io/myVoc#objectAttribute"]:false
  }
const creationResponse = await creationOperation.invoke(objectToCreate) 
```

</td>

</tr>
<tr>
<td><b>Getting a value in an object, based on a semantic key</b></td>
<td>

```javascript
const objectId = await user.getOneValue("http://vocabulary.io/myVoc#objectId")
```

</td>

</tr>
<tr>
<tr>
<td><b>Verifying that a relation is available</b></td>
<td>

```javascript
  if(creationResponse.data.isRelationAvailable("http://vocabulary.io/myVoc/rel#Delete")){
    ...
  }
```

</td>

</tr>
<tr>

<td><b>Getting an operation from a relation, and inferring parameters automatically</b></td>
<td>

```javascript
  const deleteOperation = creationResponse.data
  .getRelation("http://vocabulary.io/myVoc/rel#Delete")
  .map(relation => {
    return relation[0].operation
  }).getOrThrow(()=>new Error("no relation available to delete an object"))

  await deleteOperation.invoke()
```

</td>

</tr>

</tbody>
</table>


## In depth documentation

### Definitions
- **SemanticKey**: An identifier for a certain resource, defined by `x-@id` in the OpenAPI specification file.
- **SemanticRelation**: An identifier for a certain relation, defined by `x-@relation` in the OpenAPI specification file.
- **DataSemantics**: The type of a certain resource, defined by `x-@type` in the OpenAPI specification file.

### Pivo Object

- `static async fetchDocumentationAndCreate(baseApiUrl: string, method: Method = 'options', defaultHttpConfig?: AxiosRequestConfig): Promise<Pivo | undefined>`
  - A static method that fetches the OpenAPI documentation from the specified `baseApiUrl` using the provided `method` (defaulting to 'options'). It creates and returns a new instance of the `Pivo` class with the fetched documentation and the optional `defaultHttpConfig`. If fetching the documentation fails, it returns `undefined`.

- `get(data: DataSemantics, options?: PivoSearchOptions): Option<ApiOperation>`
  - Finds an operation in the documentation that returns the specified `dataSemantics`. Returns an `Option` containing an `ApiOperation` instance if found, or an empty `Option` if not found.

- `list(data: DataSemantics, options?: PivoSearchOptions): Option<ApiOperation>`
  - Finds an operation in the documentation that lists the specified `dataSemantics`. Returns an `Option` containing an `ApiOperation` instance if found, or an empty `Option` if not found.

- `fromUrl(url: string): Option<ApiOperation>`
  - Finds a GET operation in the documentation that matches the provided `url`. Returns an `Option` containing an `ApiOperation` instance if found, or an empty `Option` if not found.

### Semantic Resource

- `is(semanticKey: DataSemantics): boolean`
  - Verifies that the current semantic resource has the specified semantic key as an identifier.

- `isOneOf(semanticKey: DataSemantics[]): boolean`
  - Verifies that the current semantic resource has one of the semantic keys in the provided array as an identifier.

- `isObject(): boolean`
  - Returns `true` if the `data` object is an object, `false` otherwise.

- `isArray(): boolean`
  - Returns `true` if the `data` object is an array, `false` otherwise.

- `isPrimitive(): boolean`
  - Returns `true` if the `data` object is neither an object nor an array, `false` otherwise.

- `toArray(): SemanticResource<T>[]`
  - If the data that this semantic resource contains is an array, returns an array of semantic resources. Otherwise, returns an array with a single entry (the current semantic resource).

- `get<A = any>(semanticKey: DataSemantics): Promise<SemanticResource<A>>`
  - Gets a single or an array of semantic resources from the specified semantic key in the current semantic resource.

- `getOne<A = any>(semanticKey: DataSemantics): Promise<SemanticResource<A>>`
  - Gets a single semantic resource from the specified semantic key in the current semantic resource.

- `getArray<A = any>(semanticKey: DataSemantics): Promise<Array<SemanticResource<A>>>`
  - Gets an array of semantic resources from the specified semantic key in the current semantic resource.

- `getOneValue<A = any>(semanticKey: DataSemantics): Promise<A>`
  - Similar to `getOne()`, but gets the inner value (data) of the obtained semantic resource.

- `getArrayValue<A = any>(semanticKey: DataSemantics): Promise<Array<A>>`
  - Similar to `getArray()`, but gets the inner values (data) of each semantic resource in the array.

- `isRelationAvailable(semanticRelation: RelationSemantics): boolean`
  - Verifies that a relation is available based on the `semanticRelations` (i.e., that an operation is reachable from the current semantic resource).

- `getRelation(semanticRelation: RelationSemantics, maxRelationReturned?: number): Option<PivoRelationObject | PivoRelationObject[]>`
  - Gets a relation on the current semantic resource, from a `semanticRelation`.

- `getRelations(semanticRelations: RelationSemantics[]): PivoRelationObject[]`
  - Gets a list of relations on the current semantic resource, from a list of `semanticRelations`.

### ApiOperation
The `ApiOperation` class represents an operation in the OpenAPI documentation.

- `hasParameters(): boolean`
  - Returns `true` if the operation has parameters, `false` otherwise.

- `invoke(parameters?: object, promptForMissingParameters: boolean = true): Promise<SemanticHttpResponse>`
  - Invokes the operation with the provided parameters. If `promptForMissingParameters` is `true`, the user will be prompted to provide values for any missing required parameters.

- `missesRequiredParameters(parameters?: object): boolean`
  - Returns `true` if the operation is missing any required parameters, `false` otherwise.

- `getMissingParameters(parameters?: object, requiredOnly: boolean = true): ExpandedOpenAPIV3Semantics.ParameterObject[]`
  - Returns an array of missing parameter objects for the operation. If `requiredOnly` is `true` (default), only required parameters are considered. If `parameters` is provided, it will check for missing parameters based on the provided values.