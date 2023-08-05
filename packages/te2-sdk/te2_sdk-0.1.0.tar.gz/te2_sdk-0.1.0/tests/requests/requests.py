SAMPLE_REQUEST_WORKSPACE_BODY_HCL = {
    "data": {
        "type": "vars",
        "attributes": {
            "key": "test_key",
            "value": "test_value",
            "category": "env",
            "sensitive": True,
            "hcl": True
        }
    }
}

SAMPLE_REQUEST_WORKSPACE_FILTER = {
    "organization": {
        "username": "TestOrg"
    },
    "workspace": {
        "name": "Example_Workspace_1"
    }
}

SAMPLE_REQUEST_RUN = {
    "data": {
        "attributes": {
            "is-destroy": True
        },
        "relationships": {
            "workspace": {
                "data": {
                    "type": "workspaces",
                    "id": "ws-example1"
                }
            }
        },
        "type": "runs"
    }
}

SAMPLE_REQUEST_VARIABLE = {
  "data": {
    "type": "vars",
    "attributes": {
      "key": "key1",
      "value": "value",
      "category": "env",
      "sensitive": False
    }
  },
  "filter": {
    "filter[organization][username]": "TestOrg",
    "filter[workspace][name]": "Example_Workspace_1"
  }
}