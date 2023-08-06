* split Schema class into 3 separate classes:
  1. SchemaNode to manage the tree structure
  2. SchemaGenerator for the schema generation logic
  3. SchemaBuilder to manage the public API
* rename to_dict() => to_schema()
* include backwards compatibility layer
* deprecate merge_arrays option
* add support for patternProperties
* include ``"$schema"`` keyword
* accept schemas without ``"type"`` keyword
* use ``"anyOf"`` keyword to help combine schemas
* add ``SchemaGenerationError`` for better error handling
* empty ``"properties"`` and ``"items"`` are not included in generated schemas
* ``genson`` executable
  * new ``--schema-uri`` option
  * auto-detect object boundaries by default
