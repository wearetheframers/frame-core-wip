import argparse
import os
import subprocess
import sys
import time
import shutil
import logging
from threading import Timer
from multiprocessing import Process
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from roam_links_converter import convert_roam_links

def parse_arguments():
    parser = argparse.ArgumentParser(description="Serve documentation with optional test skipping.")
    parser.add_argument("--skip-tests", action="store_true", help="Skip running unit tests.")
    return parser.parse_args()

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

from frame.src.utils.log_manager import setup_logging

# Add the project root to the Python path
project_root = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, project_root)

# Set up logging
logger = setup_logging()


def run_command(command):
    process = subprocess.Popen(
        command, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE
    )
    stdout, stderr = process.communicate()
    if process.returncode != 0:
        print(f"Error executing command: {command}")
        print(stderr.decode())
        raise subprocess.CalledProcessError(process.returncode, command, stdout, stderr)
    return stdout.decode()


def serve_mkdocs():
    os.chdir(project_root)
    run_command("mkdocs serve --config-file ./mkdocs.yml -a localhost:3010")


def serve_pdoc():
    os.chdir(project_root)
    run_command(
        "pdoc --http localhost:3011 --output-dir ./docs/site --template-dir ./docs/custom_templates frame frame/src --force"
    )


def run_pytest_and_move_coverage():
    os.chdir(project_root)
    try:
        output = run_command("pytest -v --cov=frame --cov-report=html:docs/htmlcov")
        logger.info("Pytest completed successfully")
        logger.debug("Pytest output:\n%s", output)
    except subprocess.CalledProcessError as e:
        logger.warning("Pytest command failed with return code %d", e.returncode)
        logger.warning("Pytest output:\n%s", e.output.decode())
        logger.warning("Continuing with the script execution...")

    # Ensure htmlcov folder is only in docs
    htmlcov_src = os.path.join(project_root, "htmlcov")
    htmlcov_dest = os.path.join(project_root, "docs", "htmlcov")
    if os.path.exists(htmlcov_src):
        try:
            if os.path.exists(htmlcov_dest):
                shutil.rmtree(htmlcov_dest)
            shutil.move(htmlcov_src, htmlcov_dest)
            logger.info("Moved htmlcov folder from root to docs.")
        except Exception as e:
            logger.error("Error moving htmlcov folder: %s", e)
    else:
        logger.warning(
            "htmlcov folder not found. Coverage report may not have been generated."
        )


def rebuild_docs():
    while True:
        try:
            logger.info("Starting documentation rebuild...")
            shutil.rmtree("site", ignore_errors=True)
        except Exception as e:
            logger.error(f"Error removing 'site' directory: {e}")
            logger.info("Attempting to remove files individually...")
            for root, dirs, files in os.walk("site", topdown=False):
                for name in files:
                    try:
                        os.remove(os.path.join(root, name))
                    except Exception as e:
                        logger.error(f"Error removing file {name}: {e}")
                for name in dirs:
                    try:
                        os.rmdir(os.path.join(root, name))
                    except Exception as e:
                        logger.error(f"Error removing directory {name}: {e}")

        # Move htmlcov folder from root to docs
        htmlcov_src = os.path.join(project_root, "htmlcov")
        htmlcov_dest = os.path.join(project_root, "docs", "htmlcov")
        if os.path.exists(htmlcov_src):
            try:
                if os.path.exists(htmlcov_dest):
                    shutil.rmtree(htmlcov_dest)
                shutil.move(htmlcov_src, htmlcov_dest)
                logger.info("Moved htmlcov folder from root to docs.")
            except Exception as e:
                logger.error(f"Error moving htmlcov folder: {e}")

        try:
            # Convert and generate roam-style links in markdown files
            docs_dir = os.path.join(project_root, "docs")
            updated_files = 0
            logger.info(f"Scanning directory: {docs_dir}")
            for root, _, files in os.walk(docs_dir):
                for file in files:
                    if file.endswith(".md"):
                        file_path = os.path.join(root, file)
                        with open(file_path, "r", encoding="utf-8") as f:
                            content = f.read()
                        converted_content = convert_roam_links(content, docs_dir)
                        if converted_content != content:
                            with open(file_path, "w", encoding="utf-8") as f:
                                f.write(converted_content)
                            updated_files += 1
            if updated_files > 0:
                logger.info(f"Updated roam-style links in {updated_files} file(s)")
            else:
                logger.debug("No files were updated.")
            logger.debug("Conversion process completed.")

            # logger.info("Starting mkdocs `build`...")
            # run_command("mkdocs build --config-file ./mkdocs.yml")

            logger.info("Starting pdoc build...")
            run_command(
                "pdoc --html --output-dir ./docs/site --template-dir ./docs/custom_templates frame --force"
            )

            logger.info("Documentation rebuild completed successfully.")
            break
        except Exception as e:
            if "File 'site\\frame' already exists" in str(e):
                logger.warning(
                    "File 'site\\frame' already exists. Retrying in 5 seconds..."
                )
                time.sleep(5)
            else:
                logger.error(f"Error during documentation build: {e}")
                logger.info("Retrying in 10 seconds...")
                time.sleep(10)


def watch_for_changes():
    event_handler = ChangeHandler()
    observer = Observer()
    frame_dir = os.path.join(project_root, "frame")
    observer.schedule(event_handler, path=frame_dir, recursive=True)
    docs_dir = os.path.join(project_root, "docs")
    observer.schedule(event_handler, path=docs_dir, recursive=True)
    observer.schedule(event_handler, path=os.path.join(project_root, "mkdocs.yml"))
    for root, dirs, files in os.walk(docs_dir):
        for dir_name in dirs:
            observer.schedule(
                event_handler, path=os.path.join(root, dir_name), recursive=True
            )
    observer.start()
    try:
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
    observer.join()


import time


class ChangeHandler(FileSystemEventHandler):
    def __init__(self):
        self.last_rebuild_time = 0
        self.rebuild_delay = 60  # 1 minute delay

    def on_any_event(self, event):
        if event.is_directory:
            return
        if (
            event.src_path.endswith(".py")
            or event.src_path.endswith(".md")
            or event.src_path.endswith(".yml")
        ) and not any(folder in event.src_path for folder in ["venv", ".venv"]):
            if event.event_type in ["created", "modified", "deleted"]:
                current_time = time.time()
                if current_time - self.last_rebuild_time > self.rebuild_delay:
                    logger.info(
                        f"Detected change in {event.src_path}. Rebuilding documentation..."
                    )
                    rebuild_docs()
                    self.last_rebuild_time = current_time
                else:
                    logger.debug(
                        f"Change detected in {event.src_path}, but waiting for rebuild delay."
                    )


if __name__ == "__main__":
    args = parse_arguments()

    if not args.skip_tests:
        # Run pytest and move coverage HTML
        print("Running pytest and generating coverage report...")
        run_pytest_and_move_coverage()

    if not args.skip_tests:
        # Run pytest and move coverage HTML
        print("Running pytest and generating coverage report...")
        run_pytest_and_move_coverage()

    # Clean up and build docs
    print("Cleaning up and building documentation...")
    rebuild_docs()

    # Start mkdocs build
    print("Building mkdocs documentation...")
    run_command("mkdocs build --config-file ./mkdocs.yml")

    # Start servers
    print("Starting documentation servers...")
    mkdocs_process = Process(target=serve_mkdocs)
    pdoc_process = Process(target=serve_pdoc)
    watch_process = Process(target=watch_for_changes)

    mkdocs_process.start()
    pdoc_process.start()
    watch_process.start()

    print("Documentation servers are running:")
    print("MkDocs: http://localhost:3010")
    print("pdoc3: http://localhost:3011/frame")

    try:
        mkdocs_process.join()
        pdoc_process.join()
        watch_process.join()
    except KeyboardInterrupt:
        print("Shutting down servers...")
        mkdocs_process.terminate()
        pdoc_process.terminate()
        watch_process.terminate()
        mkdocs_process.join()
        pdoc_process.join()
        watch_process.join()
        print("Servers shut down.")
