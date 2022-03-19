from ariadne import QueryType, make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL

import json

# loading json data
fileObject = open("data.json", "r")
jsonContent = fileObject.read()
characterslist = json.loads(jsonContent)

# loading graphql schema
type_defs = load_schema_from_path("schema.gql")


async def get_characters(name: str):
    """
    Method to fetch character details based on name
    """
    try:
        info = dict()
        results = [char for char in characterslist if name.lower()
                   in str(char["name"]).lower()]
        count = len(results)if results else 0
        info["count"] = count
        characters = {"info": info, "results": results}
        return characters

    except Exception as error:
        raise error


async def resolve_characters(_, info, name: str):
    """
    Resolver method for finding characters based on name
    """
    character = await get_characters(name=name)
    if character["info"]["count"] == 0:
        raise Exception(f"Character {name} not found")

    return character

# Instantiation and setting fields for query
query = QueryType()
query.set_field("characters", resolve_characters)

schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)
