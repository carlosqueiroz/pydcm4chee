# -*- coding: utf-8 -*-

import os
import logging

from utils import get_from_nested_dict


class Instance(object):

    def __repr__(self):
        return '<Instance object. SOPInstanceUID "{}">'.format(self.uid)

    def __init__(self, pacs, series, input_dict,
                 fetch_metadata=False):
        self.pacs = pacs
        self.series = series
        self.attributes = input_dict
        self.uid = get_from_nested_dict(self.attributes, ['00080018', 'Value', 0])
        self.retrieved = False  # whether or not the DICOM object has been retrieved from the PACS
        self._dicom_object = None  # retrieved DICOM object

        self.metadata = None
        if fetch_metadata:
            self.fetch_metadata()

    def fetch_metadata(self):
        self.metadata = self.pacs._make_request(
            'studies/{}/series/{}/instances/{}/metadata'.format(
                self.series.study.uid, self.series.uid, self.uid
            )
        )

    def retrieve_dicom(self):
        params = {
            'requestType': 'WADO',
            'contentType': 'application/dicom',
            'studyUID': self.series.study.uid,
            'seriesUID': self.series.uid,
            'objectUID': self.uid,
        }
        resp = self.pacs._make_request(service='wado', params=params)
        self.retrieved = True
        self._dicom_object = resp.raw.read()
        resp.close()

    def get_dicom_objects(self):
        if self.retrieved is False:
            self.retrieve_dicom()
        return self._dicom_object

    def save_dicom_to_disk(self, base_dir=None, study_dir=None, file_prefix=''):
        if not base_dir or not os.path.exists(base_dir):
            base_dir = os.getcwd()
        study_dir = study_dir.strip('/') if study_dir else 'study_{}'.format(self.series.study.uid)
        directory = os.path.join(base_dir, study_dir)
        try:
            os.mkdir(directory)
        except OSError:
            pass
        filename = '{}/{}{}.dcm'.format(directory, file_prefix, self.uid)
        with open(filename, 'wb') as f:
            f.write(self.get_dicom_objects())
