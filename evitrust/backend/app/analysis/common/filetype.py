def detect_filetype(filename: str) -> str:
    return filename.split(".")[-1].lower() if "." in filename else "unknown"
