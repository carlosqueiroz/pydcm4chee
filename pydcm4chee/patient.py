# -*- coding: utf-8 -*-

from utils import get_from_nested_dict


class Patient(object):
    
    def __repr__(self):
        return '<Patient object. PatientID: "{}", PatientName "{}">'.format(self.id, self.name)

    def __init__(self, pacs, input_dict,
                 fetch_studies=False):
        self.pacs = pacs
        self.attributes = input_dict
        self.id = get_from_nested_dict(self.attributes, ['00100020', 'Value', 0])
        self.name = get_from_nested_dict(self.attributes, ['00100010', 'Value', 0, 'Alphabetic'])

        self.studies = None
        if fetch_studies:
            self.fetch_studies()

    def fetch_studies(self):
        self.studies = self.pacs.get_studies(bind_to_patient=self, filter_attributes={
            'PatientID': self.id, 'PatientName': self.name,
        })
