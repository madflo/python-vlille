import datetime
import urllib2 as urllib
import re
import xml.etree.ElementTree
import json

class Station(object):
    """
    A single station where we get and put bikes
    """
    def __init__(self, id, name, latitude, longitude):
        self.id = int(id)
        self.name = name
        self.latitude = latitude
        self.longitude = longitude

        self.address = ""
        self.status = None
        self.bikes = 0
        self.attachs = 0
        self.payment = None
        self.last_update = None

    def refresh(self):
        handler = urllib.urlopen("http://www.vlille.fr/stations/xml-station.aspx?borne=%d" % self.id)
        
        station_xml = handler.read()

        # replace encoding, since it's wrong !
        station_xml = station_xml.replace('utf-16', 'utf-8')

        element = xml.etree.ElementTree.fromstring(station_xml)

        self.address = element.find('adress').text
        self.status = element.find('status').text
        self.bikes = element.find('bikes').text
        self.free_attachs = element.find('attachs').text
        self.payment = element.find('paiement').text
        
        self.last_update = element.find('lastupd').text
        self.last_update = datetime.datetime.now() - datetime.timedelta(seconds=int(re.match(r'\d+', self.last_update).group(0)))
        
    def __repr__(self):
        return "Station: %s - %s" % (self.name, self.address)

    def to_dict(self):
        return {
            'id':           self.id,
            'address':      self.address,
            'status':       self.status,
            'bikes':        self.bikes,
            'free_attachs': self.free_attachs,
            'payment':      self.payment }

    def to_json(self):
        return json.dumps(self.to_dict())
