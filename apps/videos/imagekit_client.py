import os, base64
from imagekitio import ImageKit


imagekit_public_key: str | None = os.environ.get("IMAGE_PUBLIC_kEY")
imgkit_client = ImageKit()


def upload_video(file_data: bytes, file_name: str, folder_name: str = "videos") -> dict[str, any]:
    response = imgkit_client.files.upload(
        file_data=file_data,
        file_name=file_name,
        folder=folder_name,
        public_key=imagekit_public_key
    )

    return {
        "file_id" : response.file_id,
        "url" : response.url,
    }


def upload_thumbnail(file_data: bytes, file_name: str, folder_name: str = "thumbnails") -> dict[str, any]:
    if file_data.startswith("data:"):
        base64_data = file_data.split(',', 1)[1]
        image_bytes = base64.b64decode(base64_data)
    else:
        image_bytes = base64.b64decode(file_data)

    response = imgkit_client.files.upload(
        file=image_bytes,
        file_name=file_name,
        folder=folder_name,
        public_key=imagekit_public_key
    )

    return {
        "file_id" : response.file_id,
        "url" : response.url,
    }