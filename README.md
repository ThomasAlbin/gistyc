# gistyc

gistyc is a Python-based library that enables developers to create, update and delete their GitHub GISTs. CLI capabilities allow you to execute the routines from the shell and can be integrated into your project's CI/CD pipeline to automatically create or update your GISTs (e.g., via GitHub actions). Files are separated in GIST sections depending on the separation blocks.

<i>gistyc considers currently only Python files (.py ending) in a Spyder-like code block separation (code block separator: #%%)</i>

---

## Prerequisites

1. Python 3.8 (recommendation: using a virtual environment)
2. A <i>GitHub Personal access token</i> with GIST access:
  - Click on your personal account profile (top right)
  - Click <b>Settings</b>
  - On the left menu bar go to <b>Developer settings</b> and choose <b>Personal access tokens</b>
  - <b>Generate new token</b> and write a name (note) of your token. The note does not affect the functionality, but choose a note that describes the purpose of the token e.g., <i>GIST_token</i>
  - Set a mark a <b>gist</b> (<i>Create gists</i>) and click on <b>Generate token</b> at the bottom of the page
  - IMPORTANT: The displayed token appears only once. Copy it and store it in your GitHub project as a secret and / or locally as an environment variable.

---

## Installation
```bash
pip install gistyc
```

... or install it from the main branch or this [repository](https://github.com/ThomasAlbin/gistyc). You can also download the entire repository to run the tests, download the CI/CD scripts etc.

---

## Python library calls

<i>Please note: ./tests provides some examples that can be reproduced / applied.<br>
We assume:
- AUTH_TOKEN: is the GIST access token
- FILEPATH: is the absolute or relative path to a Python file
- GIST_ID: ID of a GIST.</i>

### Create a GIST

```python
# import
import gistyc

# Initiate the GISTyc class with the auth token
gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

# Create a GIST with the sample file
response_data = gist_api.create_gist(file_name=FILEPATH)
```

### Update a GIST

Updating a GIST requires either ONLY the FILEPATH or the FILEPATH AND a corresponding GIST ID, if the GIST repository contains file names that occur more than once. Hint: keep your GIST repository clean from same-name files!

Updating using ONLY the FILEPATH:

```python
# import
import gistyc

# Initiate the GISTyc class with the auth token
gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

# Update the GIST with the updated sample file (update is based on the file's name)
response_update_data = gist_api.update_gist(file_name=FILEPATH)
```

Updating using the FILEPATH AND GIST ID:

```python
# import
import gistyc

# Initiate the GISTyc class with the auth token
gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

# Update the GIST based on the GISTs ID
response_update_data = gist_api.update_gist(file_name=FILEPATH,
                                            gist_id=GIST_ID)
```

## Get GISTs

Please note: one can obtain a list of all GISTs via:

```python
# import
import gistyc

# Initiate the GISTyc class with the auth token
gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

# Get a list of GISTs
gist_list = gist_api.get_gists()
```

## Delete a GIST

Deleting using ONLY the FILEPATH

```python
# import
import gistyc

# Initiate the GISTyc class with the auth token
gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

# Delete the GIST, based on the GIST ID
response_data = gist_api.delete_gist(file_name=FILEPATH)
```

Deleting using ONLY the GIST ID

```python
# import
import gistyc

# Initiate the GISTyc class with the auth token
gist_api = gistyc.GISTyc(auth_token=AUTH_TOKEN)

# Delete the GIST, based on the GIST ID
response_data = gist_api.delete_gist(gist_id=GIST_ID)
```


---

## CLI

<i>Please note: ./tests provides some examples that can be reproduced / applied.<br>
We assume:
- AUTH_TOKEN: is the GIST access token
- FILEPATH: is the absolute or relative path to a Python file
- GIST_ID: ID of a GIST
- DIRECTORY: A directory (with an arbitrary number of sub-directories) that contains Python files</i>

### Create a GIST

```bash
gistyc --create --auth-token AUTH_TOKEN --file-name FILEPATH
```

### Update a GIST

Updating using ONLY the FILEPATH:

```bash
gistyc --update --auth-token AUTH_TOKEN --file-name FILEPATH
```

Updating using the FILEPATH AND GIST ID:

```bash
gistyc --update --auth-token AUTH_TOKEN --file-name FILEPATH --gist-id GIST_ID
```

### Delete a GIST

Deleting using ONLY the FILEPATH

```bash
gistyc --delete --auth-token AUTH_TOKEN --file-name FILEPATH
```

Deleting using ONLY the GIST ID

```bash
gistyc --delete --auth-token AUTH_TOKEN --gist-id GIST_ID
```

### Directory Create & Update

A second gistyc CLI allows you to provide a directory as an input that recursively gets all Python files and creates or updates GISTs accordingly. Please Note: File names MUST be unique in GIST.

```bash
gistyc_dir --auth-token AUTH_TOKEN --directory DIRECTORY
```

---

## Example

Example Python files (in a directory) can be found [here](https://github.com/ThomasAlbin/gistyc/tree/main/examples).

The corresponding GISTs are embedded hereinafter:
https://gist.github.com/ThomasAlbin/b18383a86cb4396a79a551a73330ce76
https://gist.github.com/ThomasAlbin/caddb300ac663e60ae573b1117599fcc.

---

## GitHub Actions - CI/CD

The following YAML file is used by the gistyc repository to provide an example on how to use gistyc in a CI/CD pipeline. Example Python scripts are stored, added and edited in ./examples. Changes in this directory trigger the pipeline (only after a merge with the main branch).

```YAML
# CI/CD GitHub Action YAML file
#
# This YAML file executes a gistyc create / update pipeline on all Python files
# within the folder ./examples (after merging to the main branch)
name: GIST CD on main branch and example directory change

# Check if files have been pushed to ./examples
on:
  push:
    paths:
      - examples/**

# Execute the gistyc create / update pipeline
jobs:

  build:

    # Execute the pipeline only on changes on the main branche
    if: github.ref == 'refs/heads/main'

    runs-on: ubuntu-latest

    strategy:
      matrix:
        python-version: ['3.8']

    # Steps:
    # - Checkout the branch & use Python
    # - Install gistyc
    # - Use gistyc_dir, authenticate and use the ./examples directory as an input
    steps:
    - uses: actions/checkout@v2
    - name: Set up Python ${{ matrix.python-version }}
      uses: actions/setup-python@v2
      with:
        python-version: ${{ matrix.python-version }}
    - name: Install gistyc
      run: pip install gistyc
    - name: Use gistyc CLI on examples/**
      run: gistyc_dir --auth-token ${{ secrets.GIST_TOKEN }} --directory ./examples/
```

---

## Support & Contributions

 If you have requests, issues or ideas please use the GitHub Issues. Contributions are always welcome and should be provided via a Pull Request. Please note the strict coding standards and other guidelines. These standards are checked for all PRs and can be seen [here](https://github.com/ThomasAlbin/gistyc/blob/main/.github/workflows/python-package.yml). Please note that all functions must contain a pytest.

Direct messages to the author of gistyc are always welcome. Please use [Twitter](https://twitter.com/MrAstroThomas), [Reddit](https://www.reddit.com/user/MrAstroThomas) or [Medium](https://thomas-albin.medium.com/) for this purpose.

Best,<br>
Thomas
