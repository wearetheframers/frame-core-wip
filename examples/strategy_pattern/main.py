import os
import subprocess


def list_examples():
    """
    List all example scripts in the current directory.
    """
    examples = [
        f
        for f in os.listdir(os.path.dirname(__file__))
        if f.endswith(".py") and f != "main.py"
    ]
    return examples


def run_example(example):
    """
    Run the specified example script.
    """
    print(f"Running {example}...\n")
    subprocess.run(
        [
            "cmd",
            "/c",
            "venv\\Scripts\\activate && python",
            os.path.join(os.path.dirname(__file__), example),
        ]
    )


def main():
    """
    Main function to list and run example scripts.
    """
    examples = list_examples()
    print("Available Examples:")
    descriptions = {
        "adaptive_decision_example.py": "Demonstrates adaptive decision-making using different strategies.",
        "bidding_simulation.py": "Simulates a bidding process with adaptive decision-making.",
        "task_management_simulation.py": "Simulates task management with adaptive decision-making.",
        "trading_simulation.py": "Simulates trading scenarios with adaptive decision-making.",
        "security_system_example.py": "Simulates a security system using audio transcription for threat detection. This is the most complex and real example.",
    }
    examples.sort(key=lambda x: list(descriptions.keys()).index(x))
    for i, example in enumerate(examples, 1):
        description = descriptions.get(example, "No description available.")
        print(f"{i}. {example} - {description}")

    choice = input("\nEnter the number of the example you want to run: ")

    choice = int(choice)
    if examples[choice - 1] == "security_system_example.py":
        tolerance_level = input("Set the security tolerance level (1-10): ")
        print(f"Security tolerance level set to {tolerance_level}.")
        print(
            "The AI will intelligently choose to activate security based on the time of night and this tolerance level."
        )
        print(
            "For example, if the tolerance level is low, the AI may activate security earlier in the evening."
        )
    try:
        choice = int(choice)
        if 1 <= choice <= len(examples):
            run_example(examples[choice - 1])
        else:
            print("Invalid choice. Please enter a number corresponding to an example.")
    except ValueError:
        print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()


def run_example(example):
    """
    Run the specified example script.
    """
    print(f"Running {example}...\n")
    subprocess.run(
        [
            "cmd",
            "/c",
            "venv\\Scripts\\activate && python",
            os.path.join(os.path.dirname(__file__), example),
        ]
    )


def main():
    """
    Main function to list and run example scripts.
    """
    examples = list_examples()
    print("Available Examples:")
    for i, example in enumerate(examples, 1):
        print(f"{i}. {example}")

    choice = input("\nEnter the number of the example you want to run: ")
    try:
        choice = int(choice)
        if 1 <= choice <= len(examples):
            run_example(examples[choice - 1])
        else:
            print("Invalid choice. Please enter a number corresponding to an example.")
    except ValueError:
        print("Invalid input. Please enter a number.")


if __name__ == "__main__":
    main()
