import os
from imagekitio import ImageKit



def upload_video(file_data: bytes, file_name: str, folder_name: str = "videos") -> dict[str, any]:
    public_key = os.environ.get("IMAGE_PUBLIC_kEY")

    client = ImageKit()
    
    response = client.files.upload(
        file_data=file_data,
        file_name=file_name,
        folder=folder_name,
        public_key=public_key
    )

    return {
        "file_id" : response.file_id,
        "url" : response.url,
    }