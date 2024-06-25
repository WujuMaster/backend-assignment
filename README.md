# Backend Assignment

## Table of Contents

- [Problem Statement](#problem-statement)
- [Solution Summary](#solution-summary)
- [Directory Structure](#directory-structure)
- [Instructions](#instructions)
  - [Run natively](#run-natively)
  - [Run with Docker](#run-with-docker)
  - [Run with Docker Compose](#run-with-docker-compose)

## Problem Statement

1. Write a script that:

   - Extracts all text/images from a PDF/DOCX file and saves images to disk.
   - Extracts all paragraphs' content, font type/size, styling (bold/italic) and text color.
   - Converts paragraphs to uppercase (keep font styling) and saves to a new PDF/DOCX file.

2. Write another script that:

   - Extracts all text/images from a PPTX file and translates the text to Vietnamese.
   - Appends the translated text under the original text back in the original slides.

3. Use containers to run the scripts.

4. Submit to Github and provide a link to the repository.

## Solution Summary

- The solution consists of two scripts:
  - `script-1.py`:
    - Create a folder (in the `output` folder) whose name is same as each input file to save extraction result.
    - Extracts paragraphs' text formattings (font, size, color,...) and save to a json file in the extraction folder.
    - Extracts text/images from the given PDF/DOCX files (in the `data` folder) and converts paragraphs to uppercase.
    - Save extracted images to the `images` folder inside the extraction folder. Save the uppercased text to a new PDF/DOCX file in the extraction folder.
  - `script-2.py`:
    - Extracts text/images from PPTX file and translates text from English to Vietnamese. Save the images to the extraction folder.
    - Appends the translated text under the original text back in the original PPTX file.
- The scripts are written in Python and containerized using Docker.

## Directory Structure

```text
backend-assignment/
├── data/                           <- Contains input data files (PDF, DOCX, PPTX)
├── services/                       <- Contains main business logic handlers
|   ├── docx_service.py             <- Service to handle DOCX file operations
|   ├── pdf_service.py              <- Service to handle PDF file operations
|   └── pptx_service.py             <- Service to handle PPTX file operations
├── utils/                          <- Contains utility functions
├── .dockerignore                   <- List of files/folders to ignore when building the Docker image
├── .gitignore                      <- List of files/folders to ignore when pushing to the Git repository
├── docker-compose.yml              <- Docker Compose file to run the containers
├── Dockerfile                      <- Dockerfile to build the image
├── README.md                       <- The file you're reading :)
├── requirements.txt                <- Contains dependencies for the project
├── script-1.py                     <- Script to extract text/images from PDF/DOCX file
└── script-2.py                     <- Script to extract text/images from PPTX file and translate text to Vietnamese
```

## Instructions

### Run natively

1. Setup a virtual environment [*Optional*]:

   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:

   ```bash
    pip install -r requirements.txt
    ```

3. Run the scripts:

    ```bash
    # Replace ${script_name} with script-1 or script-2
    python ${script_name}.py
    ```

### Run with Docker

1. Build the Docker image [*Optional*]:

    ```bash
    docker build -t sbach2411/backend-assignment:latest .
    ```

2. Run the Docker container (replace `${script_name}` with `script-1` or `script-2`):

    ```bash
    docker run -it \
    --rm \
    -v "/$(pwd)/data":/app/data \
    -v "/$(pwd)/output":/app/output \
    sbach2411/backend-assignment:latest python3 ${script_name}.py
    ```

### Run with Docker Compose

```bash
# Pull image from Docker Hub and run the container
docker-compose up -d

# OR build the image yourself and run the container
docker-compose up -d --build
```

**Note**: The current configuration mounts the `data` and `output` folders (in the current working directory) to the container. Modify if needed.
