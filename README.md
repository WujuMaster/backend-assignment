# Backend Assignment - Round 1

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

### Run using Docker

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

3. **OR** to run the scripts using Docker Compose (modify the `docker-compose.yml` file if needed):

    ```bash
    docker-compose up -d --build
    ```
