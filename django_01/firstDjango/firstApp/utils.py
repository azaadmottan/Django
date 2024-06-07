from django.utils.text import slugify
import uuid

def generate_slug(title: str)->str:
    from .models import UserPost
    title = slugify(title).lower()

    while(UserPost.objects.filter(slug = title).exists()):
        title = f"{slugify(title)}-{str(uuid.uuid4())[:4]}"

    return title
