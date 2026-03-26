# Knowledge Graph Extraction Tool Setup Guide

> Back to [README](README.md) | See also: [Plan.md](Plan.md) | [project.md](project.md)

This document provides a comprehensive guide to setting up the environment required for the Knowledge Graph Extraction tools.

## Prerequisites

Before running the setup, ensure that you have the following installed on your system:

- **Python**: Version 3.10 or higher.
- **Bash Shell**: The setup script is written in bash (`setup.sh`).

## What the Setup Script Does

Running `setup.sh` automates the preparation of your environment by performing the following actions:

1. **Creates Necessary Directories**: Generates the folder structure required for tool outputs (`tools/output`, `tools/output/diffs`, `tools/fixtures`).
2. **Checks Python Installation**: Verifies that Python 3 is installed and available.
3. **Virtual Environment Setup**: Creates a local Python virtual environment in the `.venv` directory to keep dependencies isolated.
4. **Activates Environment & Upgrades pip**: Automatically sources the virtual environment and upgrades the package manager `pip` to the latest version.
5. **Installs Dependencies**: Reads the `requirements.txt` file and installs the latest versions of the required packages (`spacy`, `PyYAML`, `rich`, `click`).
6. **Downloads Language Model**: Uses spaCy to download the large German language model (`de_core_news_lg`), which is essential for the NLP operations used by the extraction tools.

## How to Set Up

To configure your environment and install all dependencies, simply execute the setup script from the root of the repository:

```bash
./setup.sh
```

## Post-Setup: Activating the Virtual Environment

The setup script creates the virtual environment and uses it to install dependencies, but your current terminal session will not remain activated after the script finishes.

Whenever you want to run the Python tools, you must first manually activate the virtual environment by running:

```bash
source .venv/bin/activate
```

You will know the environment is activated when your terminal prompt is prefixed with `(.venv)`.

## Troubleshooting

- **Python 3 not found**: If the script fails because it cannot find Python 3, make sure Python 3.10+ is installed and added to your system's PATH. You can check your version by running `python3 --version`.
- **Permission Denied**: If you get a "permission denied" error when trying to run `./setup.sh`, ensure the script has executable permissions by running `chmod +x setup.sh` and try again.
