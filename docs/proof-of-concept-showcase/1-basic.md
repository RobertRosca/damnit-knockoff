# Proof of Concept 1 - Basic

For this to be vaguely coherent, I'll go through a few different stages during the design and build up the complexity gradually instead of showing the final version from the start.

The super-duper basic proof of concept for this is very simple but:

1. Shows the basic concepts of user-defined collections (equivalent to a table).
2. Where the fields (variables) can be set by functions/methods.
3. And these functions run when a new document (a record, basic 'unit of data' in mongo, like a row) is being inserted to the DB.

Benefits of this approach are kind of spread across different sources:

## Benefit from the implementation

- Class structure is more flexible, supports multiple collections (tables) out of the box - allows for separation of user data.

## Benefit from Document-Oriented DB

- Collections (tables) do not have a schema, documents in a collection can have different fields, adding/removing fields is is simple.
- More field types supported than sqlite: list, bytes, tuple, dict, set, enum, datetime, namedtuple, path, uuid, probably more.
- Nested documents are also possible.
- Very nice time-series data support.

- Lazy parsing/loading of documents.
- Fancy indexing, e.g. multi-field indexes.
- Revision support and state management, helps avoid data loss/overwriting during concurrent operations.

## Benefit from Beanie

- Inheritance (of the classes), more complex collections can be set up which inherit shared attributes from parent classes.
- No need for additional code to handle dynamically adding in columns based on the user provided context file.
- Handles the event-based method calls: `Insert`, `Replace`, `Update`, `SaveChanges`, `Delete`, `ValidateOnSave`.
- Multiple directions supported: `before` and `after`.
- `async` support.

And from Pydantic (which Beanie heavily uses):

- By validating the types you can write frontend/GUI features more easily since you know what data you'll get from the DB.
- (list of all normal benefits of type aliases here)...
- Nice IDE integration I guess - enhances the warnings showed by the context file editor.
- BUT this can probably be achieved with `Annotated[type, "damnit#string"]`.
