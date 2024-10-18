---
title: Home
weight: -30
---

Frame is a multi-modal, multi-agent cognitive framework designed to support fully emergent characteristics. Framer agents are also fully equipped for task automation and for working together collaboratively.

## Core Components

Frame consists of three main components:

the **[[frame]]**: The main interface for creating and managing Framer instances. It acts as the central hub for initializing and orchestrating the various components of the framework.

the **[[framer]]**: Represents an individual AI agent with capabilities for task management, decision-making, and interaction with language models. Each Framer operates independently but can collaborate with others. Framers can be initialized with a `soul_seed` that is a string or a dictionary with a 'seed' key.

the **[[framed]]**: A collection of Framer objects working together to achieve complex tasks. It enables coordination and communication between multiple Framers, allowing for scalable and collaborative operations.

## Key Features

- Multi-modal cognitive agents framework
- Supports developing dynamic, emergent behaviors
- Layered memory understanding entity relationships with Mem0
- Supports global and multi-user memory storage
- Extensible architecture with plugin engine
- Integration with popular AI APIs (OpenAI GPT, Mistral, etc.) as well as local model support
- Streaming text generation support 
- Flexible behavior and decision-making mechanics that can be based off of emotions and memories
- Monitoring and metrics; built-in LLM API usage / costs tracking

## Technologies Used
- LQML
- Hugging Face
- Mem0
- DSPy (Experimental)

## Getting Started

To get started with Frame, please refer to the following sections:

- [[installation]]: Instructions for installing Frame
- [[basic usage]]: Basic usage examples and patterns
- [[api reference]]: Detailed API documentation for all components
- [[metrics]]: Accessing metrics / LLM API usage costs

## Advanced Topics

- [[plugins]]: How to create and use plugins to extend Frame's functionality
- [[memory]]: Understanding and utilizing Frame's memory systems
- [[framed]]: Working with multiple Framers in a Framed environment
- [[eq]]: Implementing and utilizing emotional traits in Framers

## Components in Detail

### Frame

The Frame component serves as the main interface for creating and managing Framer instances. It provides methods for:

- Initializing the framework with various API keys and configurations
- Creating individual Framers with specific roles and goals
- Managing LLM services and model interactions
- Creating Framed groups for multi-agent coordination

For more details, see the [[frame]].

### Framer

Framers are individual AI agents with capabilities for:

- Task management and execution
- Decision-making based on goals and context
- Interaction with language models
- Memory storage and retrieval
- Multi-modal perception processing
- Emotional intelligence simulation (work in progress)

Learn more in the [[framer]].

### Framed

Frameds (pronounced as `frames`) enable:

- Coordination of multiple Framer instances
- Task distribution and management across Framers
- Collaborative problem-solving
- Scalable architecture for complex operations
- Dynamic task allocation and parallel processing
- Inter-Framer communication

Explore further in the [[framed]].

## Research Paper

Coming soon [[#]].

## Contributing

We welcome contributions to the Frame project. Please see our [[contributing]] guide for more information on how to get involved.

## License

This project is dual-licensed under the GNU Affero General Public License version 3 (AGPLv3) and a proprietary license. See the [LICENSE](https://github.com/your-repo-link/LICENSE) file for more details.

## Custom Enterprise Support

For custom enterprise support, development of features, or plugins, please contact our team at [team@frame.dev] or visit our website at [Frame.dev].

## Support and Community

Join our community to get help, share ideas, and collaborate:

- [GitHub Issues](https://github.com/your-repo-link/issues): Report bugs or request features
- [Discord Channel](https://discord.gg/your-channel): Chat with other Frame developers and users

## Roadmap

Stay updated on our future plans and upcoming features by checking our [[roadmap]].

We hope you find Frame useful for your AI agent development needs. Happy coding!

## Plugin Marketplace

Frame will feature a robust plugin marketplace where developers can create, share, and potentially sell their custom plugins. This marketplace will include both premium and community-developed plugins, fostering a rich ecosystem of extensions and customizations.

The plugin system in Frame is designed to be as flexible and powerful as mods in games. It includes conflict resolvers and allows for essentially unlimited plugins and expansions to be developed. This approach enables developers to create a wide range of enhancements and specialized functionalities, tailoring Frame to diverse use cases and requirements.

For more information on creating and using plugins, see our [[plugins]] documentation.
