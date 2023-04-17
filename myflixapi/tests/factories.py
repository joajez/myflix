import factory
from myflixapi import models


class GenreFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Genre

    external_genre_id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: "Genre %03d" % n)


class MovieFactory(factory.django.DjangoModelFactory):
    class Meta:
        model = models.Movie

    external_movie_id = factory.Sequence(lambda n: n)
    title = factory.Sequence(lambda n: "Movie %03d" % n)

    @factory.post_generation
    def genres(self, create, extracted, **kwargs):
        if not create:
            # Simple build, do nothing.
            return

        if extracted:
            # A list of groups were passed in, use them
            for genre in extracted:
                self.genres.add(genre)
