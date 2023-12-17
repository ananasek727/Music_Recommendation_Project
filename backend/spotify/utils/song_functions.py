from ..models import Song


def delete_songs() -> None:
    Song.objects.all().delete()
