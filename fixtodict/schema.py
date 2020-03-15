SCHEMA = {
    "$schema":
    "http://json-schema.org/draft-07/schema",
    "$id":
    "http://example.com/root.json",
    "title":
    "FIXtodict-flavoured FIX Repository data",
    "type":
    "object",
    "required": [
        "version",
        "abbreviations",
        "datatypes",
        "sections",
        "categories",
        "components",
        "fields",
        "messages"
    ],
    "properties": {
        "meta": {
            "type": "object",
            "properties": {
                "fixtodict": {
                    "$ref": "#/definitions/fixtodict"
                }
            }
        },
        "version": {
            "$ref": "#/definitions/version"
        },
        "abbreviations": {
            "type": "object",
            "items": {
                "$ref": "#/definitions/abbreviation"
            }
        },
        "datatypes": {
            "type": "object",
            "items": {
                "$ref": "#/definitions/datatype"
            }
        },
        "sections": {
            "type": "object",
            "items": {
                "$ref": "#/definitions/section"
            }
        },
        "categories": {
            "type": "object",
            "items": {
                "$ref": "#/definitions/category"
            }
        },
        "fields": {
            "type": "object",
            "items": {
                "$ref": "#/definitions/field"
            }
        },
        "components": {
            "type": "object",
            "items": {
                "$ref": "#/definitions/component"
            }
        },
        "messages": {
            "type": "object",
            "items": {
                "$ref": "#/definitions/message"
            }
        }
    },
    "definitions": {
        "fixtodict": {
            "type": "object",
            "properties": {
                "version": {
                    "type": "string",
                    "description":
                    "The version of FIXtodict used to generate this document.",
                    "examples": ["1.1.0"]
                },
                "md5": {
                    "type": "string",
                    "description": "MD5 signature of the sourcing directory."
                },
                "command": {
                    "type":
                    "string",
                    "description":
                    "The command-line invocation string that generated this document."
                },
                "legal": {
                    "type":
                    "string",
                    "description":
                    "Legal and copyright information regarding the output."
                },
                "generated": {
                    "type": "string",
                    "format": "date-time",
                    "examples": ["2020-03-15T06:01:45Z"]
                }
            }
        },
        "version": {
            "type": "object",
            "properties": {
                "fix": {
                    "type": "string",
                    "examples": ["fix", "fixt"]
                },
                "major": {
                    "type": "string"
                },
                "minor": {
                    "type": "string"
                },
                "sp": {
                    "type": ["string", "null"]
                },
                "ep": {
                    "type": ["string", "null"]
                }
            },
            "examples": [
                {
                    "fix": "fix",
                    "major": "5",
                    "minor": "0",
                    "sp": "2",
                    "ep": None
                }
            ],
            "required": ["fix", "major", "minor", "sp", "ep"]
        },
        "description": {
            "type": "object",
            "properties": {
                "body": {
                    "type": "string"
                },
                "elaboration": {
                    "type": "string"
                },
                "examples": {
                    "type": "array",
                    "items": {
                        "type": "string"
                    }
                }
            },
            "required": ["body"]
        },
        "history": {
            "type": "object",
            "properties": {
                "added": {
                    "$ref": "#/definitions/version"
                },
                "updated": {
                    "$ref": "#/definitions/version"
                },
                "deprecated": {
                    "$ref": "#/definitions/version"
                },
                "replaced": {
                    "$ref": "#/definitions/version"
                }
            },
            "examples": [{
                "added": {
                    "fix": "fix",
                    "major": "4",
                    "minor": "4",
                    "sp": "0",
                    "ep": None},
                "updated": None,
                "deprecated": None
            }],
        },
        "abbreviation": {
            "type": "object",
            "properties": {
                "term": {
                    "type": "string",
                    "description": "The full term of this abbreviation."
                },
                "description": {
                    "$ref": "#/definitions/description"
                },
                "history": {
                    "$ref": "#/definitions/history"
                },
            },
            "required": ["base", "description", "history"]
        },
        "datatype": {
            "type": "object",
            "properties": {
                "base": {
                    "type": "string"
                },
                "description": {
                    "$ref": "#/definitions/description"
                },
                "history": {
                    "$ref": "#/definitions/history"
                },
            },
            "required": ["base", "description", "history"]
        },
        "section": {
            "type": "object",
            "properties": {
                "base": {
                    "type": "string"
                },
                "description": {
                    "$ref": "#/definitions/description"
                },
                "history": {
                    "$ref": "#/definitions/history"
                },
            }
        }
    }
}

FIX40_DESCRIPTION = """The Financial Information Exchange (FIX) Protocol is a message standard developed to facilitate the electronic exchange of information related to securities transactions. It is intended for use between trading partners wishing to automate communications.

The message protocol, as defined, will support a variety of business functions. FIX was originally defined for use in supporting US domestic equity trading with message traffic flowing directly between principals. As the protocol evolved, a number of fields were added to support limited cross-border and fixed income trading. Similarly, the protocol was expanded to allow third parties to participate in the delivery of messages between trading partners. As subsequent versions of FIX are released it is expected that functionality will continue to expand.

FIX was written to be independent of any specific communications protocol (X.25, asynch, TCP/IP, etc.) or physical medium (copper, fiber, satellite, etc.) chosen for electronic data delivery. The protocol is defined at two levels; session and application. The session level is concerned with the delivery of data while the application level defines business related data content. This document is organized to reflect the distinction."""
