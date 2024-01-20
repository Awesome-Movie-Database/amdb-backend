from dataclasses import dataclass


@dataclass(frozen=True, slots=True)
class CreateMovieCommand:
    title: str
