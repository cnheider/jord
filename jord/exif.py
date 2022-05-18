from PIL.ExifTags import TAGS
from warg import invert_dict

__all__ = ["EXIF_TAG_IDS"]

EXIF_TAG_IDS = invert_dict(TAGS)


if __name__ == "__main__":
    print(EXIF_TAG_IDS)
