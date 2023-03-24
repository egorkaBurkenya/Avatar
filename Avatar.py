import json


class Indicator:
    """Class representing an indicator of an organ.

    Attributes:
        name (str): The name of the indicator.
        data_type (type): The data type of the indicator's value.
        value (Any): The current value of the indicator.
    """

    def __init__(self, name, data_type, value=None):
        """Initialize the Indicator class.

        Args:
            name (str): The name of the indicator.
            data_type (type): The data type of the indicator's value.
            value (Any, optional): The initial value of the indicator. Defaults to None.
        """
        self.name = name
        self.data_type = data_type
        self.value = value if value is not None else data_type()


class Organ:
    """Class representing an organ of a person.

    Attributes:
        name (str): The name of the organ.
        indicators (dict[str, Indicator]): A dictionary of the indicators of the organ.
    """

    def __init__(self, name: str) -> None:
        """Initialize the Organ class.

        Args:
            name (str): The name of the organ.
        """
        self.name = name
        self.indicators = {}

    def add_indicator(self, indicator: Indicator) -> None:
        """Add an indicator to the organ.

        Args:
            indicator (Indicator): The indicator to add.
        """
        self.indicators[indicator.name] = indicator


class Avatar:
    """Class representing a person with a set of organs and indicators.

    Attributes:
        organs (dict[str, Organ]): A dictionary of the organs of the person.
        formulas (list[dict]): A list of dictionaries representing the formulas that connect the indicators.
    """

    def __init__(self, schema=None, case_data=None) -> None:
        """Initialize the Person class.

        Args:
            schema (dict, optional): A dictionary representing the schema of the person. Defaults to None.
            case_data (dict, optional): A dictionary representing the initial data of the person. Defaults to None.
        """
        self.organs = {}
        self.formulas = []
        if schema is not None:
            self.from_schema(schema)
        if case_data is not None:
            self.from_case_data(case_data)

    def add_organ(self, organ: Organ) -> None:
        """Add an organ to the person.

        Args:
            organ (Organ): The organ to add.
        """
        self.organs[organ.name] = organ

    def from_schema(self, schema: dict) -> None:
        """Create the person from a schema.

        Args:
            schema (dict): A dictionary representing the schema of the person.
        """
        for organ_name, organ_data in schema["organs"].items():
            organ = Organ(organ_name)
            for indicator_name, indicator_data in organ_data["indicators"].items():
                indicator = Indicator(indicator_name, eval(indicator_data["data_type"]))
                organ.add_indicator(indicator)
            self.add_organ(organ)
        self.formulas = schema.get("formulas", [])

    def from_case_data(self, case_data: dict) -> None:
        """
        Populates the indicators of the person with the values from a case data object.

        Args:
            case_data (Dict[str, Any]): A dictionary representing the case data for the person.

        Raises:
            ValueError: If the case data is invalid.
        """
        for organ_name, organ_data in case_data["organs"].items():
            for indicator_name, value in organ_data["indicators"].items():
                self.update_indicator(organ_name, indicator_name, value, apply_formulas=False)

    def apply_formulas(self, changed_organ, changed_indicator):
        """
        Applies all formulas to the Person object.

        Args:
            changed_organ (Organ): The organ that was changed.
            changed_indicator (Indicator): The indicator that was changed.
        """
        updated_indicators = {(changed_organ.name, changed_indicator.name)}
        while updated_indicators:
            next_updated_indicators = set()
            for formula in self.formulas:
                trigger = formula["trigger"]
                if trigger in updated_indicators:
                    target_organ = self.organs[formula["target"][0]]
                    target_indicator = target_organ.indicators[formula["target"][1]]
                    old_value = target_indicator.value
                    target_indicator.value = eval(
                        formula["expression"],
                        None,
                        {
                            "person": self,
                            "value": target_indicator.value,
                            "trigger_value": self.organs[trigger[0]].indicators[trigger[1]].value,
                        },
                    )
                    if old_value != target_indicator.value:
                        next_updated_indicators.add(formula["target"])
            updated_indicators = next_updated_indicators

    def update_indicator(self, organ_name, indicator_name, value, apply_formulas=True):
        """
        Updates an indicator in the Person object.

        Args:
            organ_name (str): The name of the organ.
            indicator_name (str): The name of the indicator.
            value (any): The new value for the indicator.
            apply_formulas (bool): Whether to apply formulas after the update.
        """
        organ = self.organs[organ_name]
        indicator = organ.indicators[indicator_name]
        t = indicator.data_type
        if not isinstance(value, t):
            raise ValueError(f"Invalid value type for {indicator_name}. Expected {indicator.data_type}.")
        indicator.value = value
        if apply_formulas:
            self.apply_formulas(organ, indicator)

    def from_json_string(self, schema_json, case_data_json):
        """
        Args:
            schema_json (str): A JSON string representing the schema.
            case_data_json (str): A JSON string representing the case data.

        Returns:
            None. The method populates the object with the schema and case data.
        """
        schema = json.loads(schema_json)
        case_data = json.loads(case_data_json)
        self.from_schema(schema)
        self.from_case_data(case_data)
