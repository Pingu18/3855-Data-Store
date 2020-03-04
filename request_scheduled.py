from sqlalchemy import Column, Integer, String, DateTime
from base import Base
import datetime


class RequestScheduled(Base):
    """ Scheduled Request """

    __tablename__ = "request_scheduled"

    id = Column(Integer, primary_key=True)
    name = Column(String(250), nullable=False)
    location = Column(String(250), nullable=False)
    destination = Column(String(250), nullable=False)
    passengers = Column(Integer, nullable=False)
    datetime = Column(String(250), nullable=False)
    date_created = Column(DateTime, nullable=False)

    def __init__(self, name, location, destination, passengers, timedate):
        """ Initializes a blood pressure reading """
        self.name = name
        self.location = location
        self.destination = destination
        self.passengers = passengers
        self.datetime = timedate
        self.date_created = datetime.datetime.now()

    def to_dict(self):
        """ Dictionary Representation of a blood pressure reading """
        dict = {}
        dict['id'] = self.id
        dict['name'] = self.name
        dict['location'] = self.location
        dict['destination'] = self.destination
        dict['passengers'] = self.passengers
        dict['datetime'] = self.datetime

        return dict
