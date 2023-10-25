import random


class DeterministicBehavior:
    """
    A DeterministicBehavior encapsulates deterministic behaviors for
    collections.
    """

    def iter(iterable):
        return iter(sorted(iterable))

    def pop(collection):
        return collection.pop()

    def add(element, collection):
        collection.append(element)

    def create_collection(orig=[]):
        return sorted(list(orig))

    def random():
        return 0.5


class NonDeterministicBehavior:
    """
    A _NonDeterministicBehavior encapsulates non-deterministic behaviors for
    collections.
    """

    def iter(iterable):
        return iter(iterable)

    def pop(collection):
        return collection.pop()

    def add(element, collection):
        collection.add(element)

    def create_collection(orig=[]):
        return set(orig)

    def random():
        return random.random()


class RandomicBehavior:
    """
    A RandomicBehavior encapsulates non-deterministic behaviors for
    collections.
    """

    def iter(iterable):
        asList = list(iterable)
        random.shuffle(asList)
        return iter(asList)

    def pop(collection):
        element = random.sample(collection, 1)[0]
        collection.remove(element)
        return element

    def add(element, collection):
        collection.add(element)

    def create_collection(orig=[]):
        return set(orig)

    def random():
        return random.random()
