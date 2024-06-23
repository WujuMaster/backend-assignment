from os import makedirs, path


def prepare_output_dir(filename: str, output_dir: str):
    """
    Prepare the output directory for image extraction and new file creation. Because os.makedirs
    is recursive, it will create the entire directory tree if it does not exist.

    Args:
        filename (str): The name of the file to be processed.
        output_dir (str): The path to the output directory.

    Returns:
        str: The path to the image directory.
    """
    img_dir = path.join(
        output_dir,
        filename.split(".")[0],
        "images",
    )
    if not path.exists(img_dir):
        makedirs(img_dir)

    return img_dir
