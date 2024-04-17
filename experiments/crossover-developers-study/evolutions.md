# Evolutions


## Present in the Open source projects
### Dialog flow
- **Change Type of Return Value**
    >The response directly contains an `intentResponse` instead of an object with `{intentResponse:intentResponse}`.

### Pagespeed api apps script
- **Change Type of Return Value**
    > The path changed from `response.score` to `response.ruleGroups.SPEED.score.`
- **Rename Method**
    > change in the version number, from www.googleapis.com/pagespeedonline/v1 to /v2

### Spaghetti makes me moody
- **Add or Remove Parameter**
    > Addition of a `historyData` parameter in the createUser Method
- **Add or Remove Parameter**
    > Addition of the `username` and `password` parameters.
- **Request Method change**
    > Change of the http verb to create a user from POST to PUT

### Utify
- **Add or Remove Parameter**
    > Addition of a `userId` to the search request.
- **Add or Remove Parameter**
    > Addition of a `tag` to the videos metadata.

### Simba
- **Add or Remove Parameter**
    > Request Body from `{ content }` to `{ auteur, content }`
- **Rename Method**
    > from `/api/polls/{slug}/comments/{userId}` to `/api/poll/comment/{slug}`
- **Add or Remove Parameter**
    > remove `userId` in the path for comment creation
- **Change Type of Return Value**
- **The set of operations to achieve a business process changed**
    > Only one operation necessary to create a comment(not needing to create a user anymore)
- **The set of operations to achieve a business process changed**
    > Only one operation necessary to answer a poll instead of 3
- **Rename Method**
    > POST /api/polls -> POST /api/poll to create a new poll
- **Remove return value**
    > Meal preferences are not associated anymore to the poll
- **Move API elements**
    > Different paths have to be used if we need the `adminSlug` or not (`/api/poll/aslug/{aslug}` or `/api/poll/slug/{slug}`)
- **Rename Method**
    > from `/api/polls/${slug}?token=${token}` to `/api/poll/update1`
- **Rename Parameter**
    > The name of `token` is changed into `slugAdmin`
- **Move Parameter**
    > `token` has been moved to the request body(also renamed to slugAdmin)
- **Move API elements**
    > `/api/poll/{id}` can also be called to get a poll
- **Change Type of Return Value**
- **Combine Methods**
    > only one call to `/api/poll/update1` to update a poll

## Correspondance in the todoMvc application
| Index | Type of evolution                                           | Actual Evolution on the API                                                                          |
| ----- | ----------------------------------------------------------- | ---------------------------------------------------------------------------------------------------- |
| 1     | Add or Remove Parameter                                     | Add a required `dueDate` body parameter of type date (not date-time) to POST /todo                   |
| 3     | Change Type of Return Value                                 | Move `status` of Task inside a `details` object                                                      |
| 5     | Rename Method                                               | Rename GET /todos into GET /todo                                                                     |
| 6     | Rename Parameter                                            | Rename `title` into `text`                                                                           |
| 10    | Combine Methods                                             | Combine two methods to add a tag to a todo `/tag/{tagName}` to create a tag and  `/todo/{id}/{tagName}` to tag a todo, to only  `/todo/{id}/{tagName}` to create it and tag the todo                                                                      |
| 17    | Move API elements                                           | !! .......... TODO ..........                                                                        |
| 23    | Request Method change (e.g. POST, PUT, etc.)                | Change PUT /todo/{todoId} into POST /todo/{todoId}                                                   |
| 26    | The set of operations to achieve a business process changed | To delete a todo, first complete it and then run delete, before it was possible to delete right away |
| 28    | Move Parameter                                              | move the location of the id parameter from the path to the query                                                                        |
| 29    | Remove Return Value                                             | Remove the `author` return value from the todo response  |