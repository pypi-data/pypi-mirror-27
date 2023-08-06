"""
aggregate
~~~~~~~~~

Base classes for aggregates in a domain driven design.
"""
from collections import deque

from eventsourcing.domain.model.entity import TimestampedVersionedEntity


class AggregateRoot(TimestampedVersionedEntity):
    """
    Root entity for an aggregate in a domain driven design.
    """

    class Event(TimestampedVersionedEntity.Event):
        """Supertype for aggregate events."""

    class Created(Event, TimestampedVersionedEntity.Created):
        """Published when an AggregateRoot is created."""

    class AttributeChanged(Event, TimestampedVersionedEntity.AttributeChanged):
        """Published when an AggregateRoot is changed."""

    class Discarded(Event, TimestampedVersionedEntity.Discarded):
        """Published when an AggregateRoot is discarded."""

    def __init__(self, **kwargs):
        super(AggregateRoot, self).__init__(**kwargs)
        self.__pending_events__ = deque()

    def __save__(self):
        """
        Publishes pending events for others in application.
        """
        batch_of_events = []
        try:
            while True:
                batch_of_events.append(self.__pending_events__.popleft())
        except IndexError:
            pass
        if batch_of_events:
            self.__publish_to_subscribers__(batch_of_events)

    def __publish__(self, event):
        """
        Appends event to internal collection of pending events.
        """
        self.__pending_events__.append(event)

    def __discard__(self):
        super(AggregateRoot, self).__discard__()
        self.__save__()
