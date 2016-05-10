# -*- coding: utf-8 -*-

from series import Series
from utils import get_from_nested_dict


class Study(object):

    def __repr__(self):
        return '<Study object. StudyInstanceUID: "{}">'.format(self.uid)

    def __init__(self, pacs, patient, input_dict,
                 fetch_metadata=False, fetch_series=False):
        self.pacs = pacs
        self.patient = patient
        self.attributes = input_dict
        self.uid = get_from_nested_dict(self.attributes ,['0020000D', 'Value', 0])
        self.retrieved = False  # whether or not the DICOM object has been retrieved from the PACS

        self.metadata = None
        if fetch_metadata:
            self.fetch_metadata()

        self.series = None
        if fetch_series:
            self.fetch_series()

    def fetch_metadata(self):
        self.metadata = self.pacs._make_request('studies/{}/metadata'.format(self.uid))

    def fetch_series(self):
        self.series = []
        path = 'studies/{}/series'.format(self.uid)
        for series_dict in self.pacs._make_request(path):
            self.series.append(Series(pacs=self.pacs, study=self, input_dict=series_dict))

    def retrieve_dicom(self):
        self.retrieved = True
        if self.series is None:
            self.fetch_series()
        for se in self.series:
            se.retrieve_dicom()

    def get_dicom_objects(self):
        if self.retrieved is False:
            self.retrieve_dicom()
        for se in self.instances:
            yield se.get_dicom_objects()

    def save_dicom_to_disk(self, base_dir=None, study_dir=None, file_prefix=''):
        self.retrieved = True
        if self.series is None:
            self.fetch_series()
        for se in self.series:
            se.save_dicom_to_disk(base_dir=base_dir, study_dir=study_dir, file_prefix=file_prefix)
