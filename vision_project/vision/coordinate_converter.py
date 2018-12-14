import yaml
import numpy as np
import os

import vision_project
from vision_project.vision.util import WorldCoordinate


class CoordinateConverter:

    def __init__(self):
        config_file_path = os.path.dirname(vision_project.vision.__file__)
        with open(os.path.join(config_file_path, 'config/distance_calibration.yaml')) as distance_calibration_file:
            distance_calibration = yaml.load(distance_calibration_file)
        with open(os.path.join(config_file_path, 'config/camera_calibration.yaml')) as camera_calibration_file:
            camera_calibration = yaml.load(camera_calibration_file)

        self.inverse_rotation_matrix = distance_calibration.get('inverse_rotation_matrix')
        self.inverse_rotation_matrix = np.asarray(self.inverse_rotation_matrix)

        self.inverse_camera_matrix = distance_calibration.get('inverse_camera_matrix')
        self.inverse_camera_matrix = np.asarray(self.inverse_camera_matrix)

        self.distance_coefficients = camera_calibration.get('dist_coeff')
        self.distance_coefficients = np.asarray(self.distance_coefficients)

        self.translation_vector = distance_calibration.get('tvec')
        self.translation_vector = np.asarray(self.translation_vector)

    def camera_coordinate_to_projector_coordinate(self, x, y):
        uv_point = np.array([x, y, np.ones(shape=1)]).reshape(3, 1)
        t = self.inverse_rotation_matrix.dot(self.inverse_camera_matrix).dot(uv_point)
        t2 = self.inverse_rotation_matrix.dot(self.translation_vector)
        s = (t2[2]) / t[2]
        object_point = (self.inverse_rotation_matrix.dot(s.item(0) * self.inverse_camera_matrix.dot(uv_point) - self.translation_vector))
        return WorldCoordinate(object_point.item(0), object_point.item(1))
