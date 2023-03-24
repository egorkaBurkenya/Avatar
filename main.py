from Avatar import Avatar

def create_schema():
    return {
        "organs": {
            "heart": {"indicators": {"rate": {"data_type": "float"}, "ecg": {"data_type": "list"}}},
            "lungs": {"indicators": {"capacity": {"data_type": "float"}}},
            "brain": {"indicators": {"size": {"data_type": "float"}}},
        },
        "formulas": [
            {"trigger": ("heart", "rate"), "target": ("lungs", "capacity"), "expression": "value + trigger_value"},
            {"trigger": ("heart", "rate"), "target": ("heart", "ecg"), "expression": "[*value, 1]"},
            {"trigger": ("heart", "rate"), "target": ("brain", "size"), "expression": "value * 10"},
            {"trigger": ("lungs", "capacity"), "target": ("brain", "size"), "expression": "value + trigger_value"},
        ],
    }


def create_case_data():
    return {
        "organs": {
            "heart": {"indicators": {"rate": 60.0, "ecg": [1, 2, 3]}},
            "lungs": {"indicators": {"capacity": 6.0}},
            "brain": {"indicators": {"size": 100.0}},
        }
    }

if __name__ == "__main__":
    schema = create_schema()
    case_data = create_case_data()

    person = Avatar(schema, case_data)

    print("\nInitial values:")
    print("❤️  Heart rate:", person.organs["heart"].indicators["rate"].value)
    print("〽️ Heart ecg:", person.organs["heart"].indicators["ecg"].value)
    print("🫁  Lung capacity:", person.organs["lungs"].indicators["capacity"].value)
    print("🧠 Brain size:", person.organs["brain"].indicators["size"].value)

    person.update_indicator("heart", "rate", 70.0)

    print("\nUpdated values:")
    print("❤️  Heart rate:", person.organs["heart"].indicators["rate"].value)
    print("〽️ Heart ecg:", person.organs["heart"].indicators["ecg"].value)
    print("🫁  Lung capacity:", person.organs["lungs"].indicators["capacity"].value)
    print("🧠 Brain size:", person.organs["brain"].indicators["size"].value)