# Pivo documentation

## Use-case documentation
This part of the documentation is centered on use-cases, i.e. it provides examples of how to use the library when you want to implement certain behaviors.
TODO: add infos about how to create the pivo object

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
			<td>Getting a operation based on the return type</td>
			<td>

```yml
  /my_object:
    get:
      responses:
        '200':
          content:
            application/json:
              schema:
                $ref: '#/components/schemas/MyObject'
...
schemas:
  MyObject:
    type: object
    x-@type: http://vocabulary.io/myVoc#MyObjectType
    properties:
      ...
```

</td>
<td>

```js
const myObjectOperation = pivo
.get("http://vocabulary.io/myVoc#MyObjectType")
.getOrThrow(() => new Error('REST API operation not available'))
```

</td>
</tr>
</tbody>
</table>