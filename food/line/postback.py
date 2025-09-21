def parse_postback_data(postback_data: str) -> tuple[str, list[str], dict[str, str]]:
    postback_command = ""
    postback_args = []
    postback_kw = {}

    # Parse the postback_data string
    # Example format: "command,arg1,arg2,key1=value1,key2=value2"
    parts = postback_data.split(",")
    if parts:
        postback_command = parts[0]
        for part in parts[1:]:
            if "=" in part:
                key, value = part.split("=", 1)
                postback_kw[key] = value
            else:
                postback_args.append(part)

    return postback_command, postback_args, postback_kw
