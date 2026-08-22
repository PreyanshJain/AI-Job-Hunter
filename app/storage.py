import json


def save_json(model, path):
    if isinstance(model, list):
        json_data = [i.model_dump(mode="json") for i in model]
    else:
        json_data = model.model_dump(mode="json")

    with open(path, "w", encoding="utf-8") as file:
        json.dump(json_data, file, indent=4)


def load_json(path):
    try:
        with open(path, "r", encoding="utf-8") as file:
            file_data = json.load(file)
            return file_data
    except FileNotFoundError:
        print(f"File not found: '{path}'")
        return None

    except json.JSONDecodeError as e:
        print(f"Invalid JSON: '{path}'")
        print(f"Error: {e}")
        return None


