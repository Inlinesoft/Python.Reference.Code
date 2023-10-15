def get_file_from_azure_blob(sourcekey):
    sourcebucket = os.environ.get("S3_PRICING_DATA_BUCKET")

    # Download the file to /tmp/ folder
    file_name = os.path.basename(sourcekey)
    download_path = "/tmp/" + file_name  # nosec
    logger.info(
        f"sourcebucket {sourcebucket},  sourcekey {sourcekey}"
        + f" download_path {download_path}"
    )

    s3_client.download_file(sourcebucket, sourcekey, download_path)

    return download_path, file_name