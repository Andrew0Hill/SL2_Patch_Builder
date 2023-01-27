from pathlib import Path

import json
import jsonschema.validators

if __name__ == "__main__":
    # Open the default .tsl file for testing
    with open("../default_2.tsl", "r") as f:
        test_file = json.load(f)
    # Get the path to the schema directory
    path = Path("schemas").absolute()
    # Set up a resolver to resolve the schema refs to files.
    resolver = jsonschema.validators.RefResolver(
        base_uri=f"{path.as_uri()}/",
        referrer=True,
    )
    # Validate the test .tsl file against the schema.
    res = jsonschema.validate(
        instance=test_file,
        schema={"$ref": "liveset.json"},
        resolver=resolver,
    )
    print("Done")
