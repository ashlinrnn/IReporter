import cloudinary.uploader


# IMAGE UPLOAD
def upload_image(file):
    if not file:
        return None

    try:
        result = cloudinary.uploader.upload(
            file,
            resource_type="image"
        )
        return result.get("secure_url")
    except Exception as e:
        print("Image upload error:", e)
        return None


# VIDEO UPLOAD
def upload_video(file):
    if not file:
        return None

    try:
        result = cloudinary.uploader.upload(
            file,
            resource_type="video"
        )
        return result.get("secure_url")
    except Exception as e:
        print("Video upload error:", e)
        return None