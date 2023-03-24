# Описание проекта

Проект представляет собой реализацию классов `Indicator`, `Organ` и `Avatar` для моделирования показателей здоровья человека. 
* Класс `Indicator` представляет отдельный показатель здоровья, 
* класс `Organ` - орган, 
* а класс `Avatar` - человека.

## Класс Indicator

### Атрибуты
- `name` - строка, имя показателя здоровья
- `data_type` - тип данных показателя здоровья
- `value` - значение показателя здоровья

### Методы
- `__init__(self, name, data_type, value=None)` - конструктор класса
- Нет других публичных методов

## Класс Organ

### Атрибуты
- `name` - строка, имя органа
- `indicators` - словарь показателей здоровья органа

### Методы
- `__init__(self, name)` - конструктор класса
- `add_indicator(self, indicator)` - добавление показателя здоровья в орган

## Класс Avatar

### Атрибуты
- `organs` - словарь органов человека
- `formulas` - список формул связывающих показатели здоровья

### Методы
- `__init__(self, schema=None, case_data=None)` - конструктор класса
- `add_organ(self, organ)` - добавление органа в человека
- `from_schema(self, schema)` - создание человека из схемы
- `from_case_data(self, case_data)` - обновление показателей здоровья из исходных данных
- `apply_formulas(self, changed_organ, changed_indicator)` - применение всех формул для обновления показателей здоровья
- `update_indicator(self, organ_name, indicator_name, value, apply_formulas=True)` - обновление показателя здоровья органа
- `from_json_string(self, schema_json, case_data_json)` - создание человека из JSON-строки с схемой и данными

## Формулы:
Формулы - это правила, которые описывают взаимосвязь между показателями внутри организма человека. Они могут использоваться для расчета значений показателей на основе других показателей.

Принцип написания формул состоит в том, что вы должны указать:

* Триггерный показатель - показатель, который запускает расчет формулы.
* Целевой показатель - показатель, который будет изменен в результате расчета формулы.
* Выражение - выражение на языке Python, которое будет использоваться для расчета нового значения целевого показателя.

Например, если у вас есть показатель "сахар в крови" и показатель "инсулин", то вы можете создать формулу, которая будет использоваться для расчета значения показателя "сахар в крови" на основе показателя "инсулин".

### Пример формулы:
```json
{
    "trigger": ("pancreas", "insulin"),
    "target": ("blood", "glucose"),
    "expression": "max(80, min(120, value + (value - trigger_value) * 0.05))"
}

```
**В этом примере:**
* Триггерный показатель - "инсулин", находящийся в поджелудочной железе ("pancreas").
* Целевой показатель - "сахар в крови", находящийся в крови ("blood").
* Выражение - "max(80, min(120, value + (value - trigger_value) * 0.05))", которое используется для расчета нового значения показателя "сахар в крови" на основе показателя "инсулин".

**Выражение использует следующие переменные:**
* "value" - текущее значение целевого показателя.
* "trigger_value" - текущее значение триггерного показателя.

Формулы можно добавлять в класс Avatar с помощью метода from_schema. После того, как формулы добавлены, они могут быть автоматически применены к показателям при их изменении, используя метод apply_formulas.

Формулы - это мощный инструмент для моделирования работы организма человека и могут использоваться для обучения и исследования различных заболеваний и состояний.

## Пример использования

```python
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
    print("❤️ Heart rate:", person.organs["heart"].indicators["rate"].value)
    print("〽️ Heart ecg:", person.organs["heart"].indicators["ecg"].value)
    print("🫁 Lung capacity:", person.organs["lungs"].indicators["capacity"].value)
    print("🧠 Brain size:", person.organs["brain"].indicators["size"].value)

    person.update_indicator("heart", "rate", 70.0)

    print("\nUpdated values:")
    print("❤️ Heart rate:", person.organs["heart"].indicators["rate"].value)
    print("〽️ Heart ecg:", person.organs["heart"].indicators["ecg"].value)
    print("🫁 Lung capacity:", person.organs["lungs"].indicators["capacity"].value)
    print("🧠 Brain size:", person.organs["brain"].indicators["size"].value)
```
### Ответ:
```bash
Initial values:
❤️ Heart rate: 60.0
〽️ Heart ecg: [1, 2, 3]
🫁 Lung capacity: 6.0
🧠 Brain size: 100.0

Updated values:
❤️ Heart rate: 70.0
〽️ Heart ecg: [1, 2, 3, 1]
🫁 Lung capacity: 76.0
🧠 Brain size: 1076.0
```
### Пояснения:

`Формула №1` связывает ЧСС и ёмкость лёгких: ёмкость лёгких становится равной сумме её и ЧСС. В нашем случае, ЧСС увеличилась с 60 до 70, поэтому ёмкость лёгких увеличилась на 10 и стала равна 76.

`Формула №2` связывает ЧСС и ЭКГ сердца: ЭКГ сердца становится списком из старых значений плюс единица в конце. В нашем случае, ЧСС увеличилась на 10, поэтому в конец списка была добавлена единица.

`Формула №3` связывает ЧСС и размер мозга: размер мозга становится равен старому значению, умноженному на 10. В нашем случае, ЧСС увеличилась с 60 до 70, поэтому размер мозга увеличился с 100 до 1000 + 70*10 = 1070.

`Формула №4` связывает ёмкость лёгких и размер мозга: размер мозга становится равен сумме старого значения размера мозга и ёмкости лёгких. В нашем случае, ёмкость лёгких увеличилась с 6 до 76, поэтому размер мозга увеличился с 1070 до 1070 + 76 = 1076.