# LMQL Interface

This document provides an overview of the `LMQLInterface` class and how to use it within the Frame framework. The `LMQLInterface` is designed to facilitate interactions with the LMQL library, which supports constraint-based language model queries.

## Overview of LMQL

LMQL (Language Model Query Language) is a library that allows users to query language models with constraints. It provides a high-level interface for specifying expected outputs and constraints, making it easier to guide the language model's responses.

### Key Features of LMQL

- **Constraints**: Define constraints on the output to ensure it meets specific criteria.
- **Distribution**: Obtain probability distributions over possible outputs.
- **Template Variables**: Use variables in prompts to dynamically adjust queries.
- **Scoring**: Score different continuation values for a given prompt.

## LMQLInterface Methods

The `LMQLInterface` class provides several methods to interact with the LMQL library:

### `__init__(self, model_name: str)`

Initializes the interface with a specified model.

- **Parameters**:
  - `model_name` (str): The name of the model to use.

### `format_prompt_with_constraints(self, prompt: str, constraints: list, distribution: bool = False) -> str`

Formats a prompt with constraints and optionally includes a distribution clause.

- **Parameters**:
  - `prompt` (str): The input prompt.
  - `constraints` (list): A list of constraints to apply.
  - `distribution` (bool): Whether to include a distribution clause.

- **Returns**: A formatted prompt string.

### `clean_response(self, response: str) -> str`

Cleans the response by removing unwanted text patterns.

- **Parameters**:
  - `response` (str): The raw response from the language model.

- **Returns**: The cleaned response string.

### `generate(self, prompt: str, max_tokens: int = 100, constraints: list = None, distribution: bool = False, control_flow: Optional[Callable] = None) -> str`

Generates a response using LMQL with constraints and optionally obtains a distribution. Supports dynamic prompt construction with control flow.

- **Parameters**:
  - `prompt` (str): The input prompt.
  - `max_tokens` (int): Maximum number of tokens to generate.
  - `constraints` (list, optional): Constraints to apply during generation.
  - `distribution` (bool): Whether to obtain a distribution over possible values.
  - `control_flow` (Callable, optional): A function to dynamically construct the prompt with control flow.

- **Returns**: The generated response or distribution.

### `score(self, prompt: str, values: list) -> dict`

Scores different continuation values for a given prompt.

- **Parameters**:
  - `prompt` (str): The prompt to use as a common prefix for all continuations.
  - `values` (list): The continuation values to score.

- **Returns**: A dictionary with scores for each continuation.

## Decorators in LMQLInterface

The `LMQLInterface` supports the use of decorators to customize the query execution process. Decorators can be used for pre-processing, post-processing, and streaming of model outputs.

### Post-Processing Decorators

Post-processing decorators are applied after a variable has been fully generated. Here's an example of a simple decorator that converts a string to uppercase:

```python
def screaming(value):
    """Decorator to convert a string to uppercase"""
    return value.upper()

# Usage in LMQLInterface
response = await lmql_interface.generate(prompt, decorators=[screaming])
```

### Pre-Processing Decorators

Pre-processing decorators are applied before the generation of a variable begins. They can be used to modify the prompt or cache values:

```python
from lmql.language.qstrings import TemplateVariable

@lmql.decorators.pre
def cache(variable: TemplateVariable, context: ProgramState):
    """Decorator to cache variable values by name"""
    return cached_values.get(variable.name, variable)

# Usage in LMQLInterface
response = await lmql_interface.generate(prompt, decorators=[cache])
```

### Streaming Decorators

Streaming decorators are applied during the decoding process, allowing for real-time processing of intermediate values:

```python
@lmql.decorators.streaming
def stream(value: str, context: ProgramState):
    """Decorator to stream the variable value"""
    print("VALUE", [value])

# Usage in LMQLInterface
response = await lmql_interface.generate(prompt, decorators=[stream])
```

### Using LMQLInterface in Frame

To use the `LMQLInterface` in the Frame framework, instantiate it with the desired model and use its methods to format prompts, generate responses, and score outputs. The high-level API provided by Frame simplifies the integration of LMQL's powerful features into your applications.

### Example Usage

```python
from frame.src.services.llm.llm_adapters.lmql.lmql_interface import LMQLInterface

# Initialize the LMQLInterface with a model
lmql_interface = LMQLInterface(model_name="gpt-3.5-turbo")

# Define a prompt and constraints
prompt = "What is the capital of France?"
constraints = ["STOPS_AT('.', 1)"]

# Generate a response with constraints
response = await lmql_interface.generate(prompt, max_tokens=50, constraints=constraints)
print("Response:", response)

# Score different continuations
values = ["Paris", "Berlin", "Madrid"]
scores = await lmql_interface.score(prompt, values)
print("Scores:", scores)
```

### Applying Constraints

The `LMQLInterface` allows you to apply various constraints to guide the language model's output. Here are some examples:

- **Stopping Conditions**: Use `STOPS_AT` to specify where the output should stop.
- **Type Constraints**: Use `INT` to ensure the output is an integer.
- **Choice Constraints**: Use `CHOICE` to restrict the output to a set of values.
- **Length Constraints**: Use `LEN` to limit the length of the output.
- **Regex Constraints**: Use `REGEX` to match the output against a regular expression.

### Dynamic Prompt Construction

You can use the `control_flow` parameter in the `generate` method to dynamically construct prompts based on specific conditions or logic.

```python
def custom_control_flow(prompt):
    # Custom logic to modify the prompt
    return prompt + " Please provide a detailed answer."

response = await lmql_interface.generate(prompt, control_flow=custom_control_flow)
print("Controlled Response:", response)
```

For more detailed examples and usage, refer to the Frame documentation and the LMQL library documentation.

## Nested Queries

Modularize your query code with nested prompting. Nested Queries allow you to execute a query function within the context of another. By nesting multiple query functions, you can build complex programs from smaller, reusable components. For this, LMQL applies the idea of procedural programming to prompting.

To better understand this concept, let's take a look at a simple example:

```python
@lmql.query
def chain_of_thought():
    '''lmql
    "A: Let's think step by step.\n [REASONING]"
    "Therefore the answer is[ANSWER]" where STOPS_AT(ANSWER, ".")
    return ANSWER.strip()
    '''

"Q: It is August 12th, 2020. What date was it "
"100 days ago? [ANSWER: chain_of_thought]"
```

Here, the placeholder variable `ANSWER` is annotated with a reference to query function `chain_of_thought`. This means a nested instantiation of query function `chain_of_thought` will be used to generate the value for `ANSWER`.

To understand how this behaves at runtime, consider the execution trace of this program:

**Model Output**
```
Q: It is August 12th, 2020. What date was it 100 days ago?chain_of_thoughtA: Let's think step by step.REASONING100 days ago would be May 4th, 2020. Therefore the answer is ANSWERMay 4th, 2020
```

**Replay**
You can press Replay to re-run the animation.

To generate `ANSWER`, the additional prompt and constraints defined by `chain_of_thought` are inserted into our main query context. However, after `ANSWER` has been generated, the additional instructions are removed from the trace, leaving only the return value of the nested query call. This mechanic is comparable to a function's stack frame in procedural programming.

Nesting allows you to use variable-specific instructions that are only locally relevant, without interfering with other parts of the program, encapsulating the logic of your prompts into reusable components.

### Parameterized Queries

You can also pass parameters to nested queries, allowing you to customize their behavior:

```python
@lmql.query
def one_of(choices: list):
    '''lmql
    "Among {choices}, what do you consider \
    most likely? [ANSWER]" where ANSWER in choices
    return ANSWER
    '''

"Q: What is the capital of France? \
 [ANSWER: one_of(['Paris', 'London', 'Berlin'])]"
```

**Model Output**
```
Q: What is the capital of France?one_ofAmong ['Paris', 'London', 'Berlin'], what do you consider most likely?ANSWERParis
```

**Replay**
For instance, here we employ `one_of` to generate the answer to a multiple-choice question. The choices are passed as a parameter to the nested query, allowing us to reuse the same code for different questions.

### Multi-Part Programs

You can also use multiple nested queries in sequence, allowing you to repeatedly inject instructions into your prompt without interfering with the overall flow:

```python
@lmql.query
def dateformat():
    '''lmql
    "(respond in DD/MM/YYYY) [ANSWER]"
    return ANSWER.strip()
    '''

"Q: When was Obama born? [ANSWER: dateformat]\n"
"Q: When was Bruno Mars born? [ANSWER: dateformat]\n"
"Q: When was Dua Lipa born? [ANSWER: dateformat]\n"

"Out of these, who was born last?[LAST]"
```

**Model Output**
```
Q: When was Obama born?ANSWER04/08/1961
Q: When was Bruno Mars born?ANSWER08/10/1985
Q: When was Dua Lipa born?ANSWER22/08/1995

Out of these, who was born last?LASTDua Lipa
```

**Replay**
We instruct the model to use a specific date format when answering our initial questions. Because of the use of `dateformat` as a nested function, the instructions are only temporarily included, once per generated answer, and removed before moving on to the next question.

Once we have generated all intermediate answers, we query the LLM to compare the individual dates and determine the latest one, where this last query is not affected by the instructions of `dateformat`.

### Return Values

If a query function does not return a value, calling it as a nested function does not remove the inserted instructions after execution. The effect of a nested function without return value therefore corresponds to a macro expansion, as shown below:

This can be helpful when you want to use a fixed template in several locations, e.g. for list items. Further, as shown below, a nested function can also be parameterized to customize its behavior.

```python
@lmql.query
def items_list(n: int):
    '''lmql
    for i in range(n):
        "-[ITEM]" where STOPS_AT(ITEM, "\n")
    '''

"A list of things not to forget to pack for your \
 next trip:\n[ITEMS: items_list(4)]"
```

**Model Output**
```
A list of things not to forget to pack for your next trip:
ITEM- Passport
ITEM- Toothbrush
ITEM- Phone charger
ITEM- Sunscreen
```

### Nested Queries in Python

To use nested queries from a Python context, you can just reference one `@lmql.query` function from another.

```python
@lmql.query
def dateformat():
    '''lmql
    "(respond in DD/MM/YYYY)[ANSWER]"
    return ANSWER.strip()
    '''

@lmql.query
def main_query():
    '''lmql
    "Q: It is August 12th, 2020. What date was it \
    100 days ago? [ANSWER: dateformat]"
    '''
```

Here, `main_query` references `dateformat` as a nested query, where both functions are defined on the top level of the same file. However, you can also import and reuse query code from other files, as long as they are accessible from the scope of your main query function. Using this ability you can write libraries of reusable query functions to be used across your application or even by other users.

## Using LMQLInterface in Frame

To use the `LMQLInterface` in the Frame framework, instantiate it with the desired model and use its methods to format prompts, generate responses, and score outputs. The high-level API provided by Frame simplifies the integration of LMQL's powerful features into your applications.

For more detailed examples and usage, refer to the Frame documentation and the LMQL library documentation.
## Nested Queries

Modularize your query code with nested prompting. Nested Queries allow you to execute a query function within the context of another. By nesting multiple query functions, you can build complex programs from smaller, reusable components. For this, LMQL applies the idea of procedural programming to prompting.

To better understand this concept, let's take a look at a simple example:

```python
@lmql.query
def chain_of_thought():
    '''lmql
    "A: Let's think step by step.\n [REASONING]"
    "Therefore the answer is[ANSWER]" where STOPS_AT(ANSWER, ".")
    return ANSWER.strip()
    '''

"Q: It is August 12th, 2020. What date was it "
"100 days ago? [ANSWER: chain_of_thought]"
```

Here, the placeholder variable `ANSWER` is annotated with a reference to query function `chain_of_thought`. This means a nested instantiation of query function `chain_of_thought` will be used to generate the value for `ANSWER`.

To understand how this behaves at runtime, consider the execution trace of this program:

**Model Output**
```
Q: It is August 12th, 2020. What date was it 100 days ago?chain_of_thoughtA: Let's think step by step.REASONING100 days ago would be May 4th, 2020. Therefore the answer is ANSWERMay 4th, 2020
```

**Replay**
You can press Replay to re-run the animation.

To generate `ANSWER`, the additional prompt and constraints defined by `chain_of_thought` are inserted into our main query context. However, after `ANSWER` has been generated, the additional instructions are removed from the trace, leaving only the return value of the nested query call. This mechanic is comparable to a function's stack frame in procedural programming.

Nesting allows you to use variable-specific instructions that are only locally relevant, without interfering with other parts of the program, encapsulating the logic of your prompts into reusable components.

### Parameterized Queries

You can also pass parameters to nested queries, allowing you to customize their behavior:

```python
@lmql.query
def one_of(choices: list):
    '''lmql
    "Among {choices}, what do you consider \
    most likely? [ANSWER]" where ANSWER in choices
    return ANSWER
    '''

"Q: What is the capital of France? \
 [ANSWER: one_of(['Paris', 'London', 'Berlin'])]"
```

**Model Output**
```
Q: What is the capital of France?one_ofAmong ['Paris', 'London', 'Berlin'], what do you consider most likely?ANSWERParis
```

**Replay**
For instance, here we employ `one_of` to generate the answer to a multiple-choice question. The choices are passed as a parameter to the nested query, allowing us to reuse the same code for different questions.

### Multi-Part Programs

You can also use multiple nested queries in sequence, allowing you to repeatedly inject instructions into your prompt without interfering with the overall flow:

```python
@lmql.query
def dateformat():
    '''lmql
    "(respond in DD/MM/YYYY) [ANSWER]"
    return ANSWER.strip()
    '''

"Q: When was Obama born? [ANSWER: dateformat]\n"
"Q: When was Bruno Mars born? [ANSWER: dateformat]\n"
"Q: When was Dua Lipa born? [ANSWER: dateformat]\n"

"Out of these, who was born last?[LAST]"
```

**Model Output**
```
Q: When was Obama born?ANSWER04/08/1961
Q: When was Bruno Mars born?ANSWER08/10/1985
Q: When was Dua Lipa born?ANSWER22/08/1995

Out of these, who was born last?LASTDua Lipa
```

**Replay**
We instruct the model to use a specific date format when answering our initial questions. Because of the use of `dateformat` as a nested function, the instructions are only temporarily included, once per generated answer, and removed before moving on to the next question.

Once we have generated all intermediate answers, we query the LLM to compare the individual dates and determine the latest one, where this last query is not affected by the instructions of `dateformat`.

### Return Values

If a query function does not return a value, calling it as a nested function does not remove the inserted instructions after execution. The effect of a nested function without return value therefore corresponds to a macro expansion, as shown below:

This can be helpful when you want to use a fixed template in several locations, e.g. for list items. Further, as shown below, a nested function can also be parameterized to customize its behavior.

```python
@lmql.query
def items_list(n: int):
    '''lmql
    for i in range(n):
        "-[ITEM]" where STOPS_AT(ITEM, "\n")
    '''

"A list of things not to forget to pack for your \
 next trip:\n[ITEMS: items_list(4)]"
```

**Model Output**
```
A list of things not to forget to pack for your next trip:
ITEM- Passport
ITEM- Toothbrush
ITEM- Phone charger
ITEM- Sunscreen
```

### Nested Queries in Python

To use nested queries from a Python context, you can just reference one `@lmql.query` function from another.

```python
@lmql.query
def dateformat():
    '''lmql
    "(respond in DD/MM/YYYY)[ANSWER]"
    return ANSWER.strip()
    '''

@lmql.query
def main_query():
    '''lmql
    "Q: It is August 12th, 2020. What date was it \
    100 days ago? [ANSWER: dateformat]"
    '''
```

Here, `main_query` references `dateformat` as a nested query, where both functions are defined on the top level of the same file. However, you can also import and reuse query code from other files, as long as they are accessible from the scope of your main query function. Using this ability you can write libraries of reusable query functions to be used across your application or even by other users.
