from ariadne import QueryType, make_executable_schema, load_schema_from_path
from ariadne.asgi import GraphQL
import uvicorn
import json

# loading characters data
file_object = open("data.json", "r")
CHARACTERS_DATA = json.loads(file_object.read())

# loading graphql schema
type_defs = load_schema_from_path("schema.gql")


async def get_characters(name: str):
    """
    | Method to filter character details from characters_list based on name
    """
    try:
        info = dict()
        results = [char for char in CHARACTERS_DATA if name.lower()
                   in str(char["name"]).lower()]
        count = len(results)if results else 0
        info["count"] = count
        characters = {"info": info, "results": results}
        return characters

    except Exception as error:
        raise error


async def resolve_characters(_, info, name: str):
    """
    | Resolver method for querying characters based on name
    """
    character = await get_characters(name=name)
    if character["info"]["count"] == 0:
        raise Exception(f"Character {name} not found")

    return character

# Instantiation and setting fields for query
query = QueryType()
query.set_field("characters", resolve_characters)

# Making the schema executable by adding the type definitions and resolvers for query fields
schema = make_executable_schema(type_defs, query)
app = GraphQL(schema, debug=True)

if __name__ == "__main__":
    # starting web server
    uvicorn.run("main:app", port=8000, reload=True,  host='localhost')
