# Framed

## Overview

Framed is a powerful component of the Frame cognitive agent framework that represents a collection of Framer objects working together to achieve complex tasks. It enables coordination and communication between multiple Framers, allowing for scalable and collaborative operations. Framed groups can tackle intricate problems by leveraging the diverse capabilities of individual Framers.

## Related Components

- [[frame]]: The main interface for creating and managing Framer instances.
- [[framer]]: Individual AI agents that make up a Framed group.

## Key Features

- Coordination of multiple Framer instances
- Task distribution and management across Framers
- Collaborative problem-solving capabilities
- Scalable architecture for complex operations
- Flexible workflow management
- Inter-Framer communication
- Dynamic task allocation based on Framer capabilities
- Parallel processing of tasks
- Adaptive resource management

## API Documentation

::: frame.src.framed.Framed
    options:
      show_root_heading: false
      show_source: false

### Attributes

- `framers` (List[Framer]): A list of Framer instances included in the Framed group.
- `config` (Optional[Dict[str, Any]]): Configuration settings for the Framed group. Default is None.

## Usage Examples

### Basic Usage

```python
from frame import Frame, Framed
from frame.framer.config import FramerConfig

# Initialize Frame
frame = Frame(openai_api_key="your_api_key_here")

# Create multiple Framers
config1 = FramerConfig(name="Researcher", default_model="gpt-3.5-turbo")
config2 = FramerConfig(name="Writer", default_model="gpt-3.5-turbo")

researcher = await frame.create_framer(config=config1)
writer = await frame.create_framer(config=config2)

# Create a Framed group
framed_group = frame.create_framed([researcher, writer])

# Add a task to the group
task = {
    "name": "Create Research Report",
    "description": "Research a topic and write a comprehensive report",
    "steps": [
        {"name": "Research", "assigned_to": "Researcher"},
        {"name": "Write Report", "assigned_to": "Writer"}
    ]
}

await framed_group.distribute_task(task)

# Run the Framed group
await framed_group.run()

# Add another Framer to the group
config3 = FramerConfig(name="Editor", default_model="gpt-3.5-turbo")
editor = await frame.create_framer(config=config3)
framed_group.add_framer(editor)

# Continue running with the new Framer
await framed_group.run()
```

### Advanced Workflow Management

```python
# Create a more complex workflow
workflow = [
    {
        "name": "Research Phase",
        "assigned_to": "Researcher",
        "tasks": [
            {"name": "Gather Sources", "priority": 1},
            {"name": "Analyze Data", "priority": 2}
        ]
    },
    {
        "name": "Writing Phase",
        "assigned_to": "Writer",
        "tasks": [
            {"name": "Draft Report", "priority": 1},
            {"name": "Create Visuals", "priority": 2}
        ]
    },
    {
        "name": "Editing Phase",
        "assigned_to": "Editor",
        "tasks": [
            {"name": "Proofread", "priority": 1},
            {"name": "Finalize Report", "priority": 2}
        ]
    }
]

framed_group.create_workflow("Comprehensive Report Creation", workflow)

# Execute the workflow
await framed_group.run_workflow("Comprehensive Report Creation")
```

## Advanced Features

### Dynamic Task Allocation

Framed groups can dynamically allocate tasks based on the capabilities and current workload of each Framer.

```python
# Example of dynamic task allocation (implementation may vary)
framed_group.enable_dynamic_allocation()
await framed_group.distribute_task(complex_task)
```

### Inter-Framer Communication

Framers within a Framed group can communicate with each other to share information and coordinate their efforts.

```python
# Example of inter-Framer communication (implementation may vary)
researcher.send_message(writer, "Research data compiled. Ready for report writing.")
```

### Parallel Processing

Framed groups can process tasks in parallel, leveraging the capabilities of multiple Framers simultaneously.

```python
# Enable parallel processing
framed_group.set_parallel_processing(True)
await framed_group.run()
```

## Best Practices

1. **Diverse Framer Composition**: Create Framed groups with Framers that have complementary skills and knowledge.
2. **Clear Task Definition**: Define tasks and workflows clearly to ensure efficient distribution and execution.
3. **Balance Workload**: Distribute tasks evenly among Framers to optimize performance.
4. **Monitor Progress**: Regularly check the progress of the Framed group and individual Framers.
5. **Iterative Refinement**: Adjust the composition and configuration of the Framed group based on performance and requirements.
6. **Optimize Communication**: Minimize unnecessary inter-Framer communication to reduce overhead.
7. **Leverage Parallel Processing**: Use parallel processing for tasks that can be executed independently.
8. **Implement Error Handling**: Develop robust error handling mechanisms to manage failures in individual Framers.

## Related Topics

- [[multi-agent-coordination]]: Detailed strategies for coordinating multiple Framers in a Framed environment.
- [[memory-management]]: Understanding how memory is shared and managed across Framers in a Framed group.
- [[plugins]]: Extending Framed functionality through custom plugins.
- [[emotional-intelligence]]: Implementing emotional traits in Framed groups for more nuanced interactions.

## Conclusion

Framed groups provide a powerful mechanism for coordinating multiple AI agents to tackle complex, multi-step tasks. By leveraging the collective capabilities of multiple Framers, Framed enables the creation of sophisticated AI systems capable of handling intricate workflows and collaborative problem-solving scenarios. With features like dynamic task allocation, parallel processing, and inter-Framer communication, Framed groups can adapt to a wide range of complex challenges in various domains.
