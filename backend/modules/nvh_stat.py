"""NVH Statistics Module

Assume an NVH module stores the statistic results from different measurements.
In one resource, it can have multiple measurements, from different sensors.

To visualize or compare the results, we can:
- Send binary data to frontend, and let the frontend parse the data and visualize it.
  But that's duplicated work that frontend needs to know how data is stored.
- Send parsed data to frontend, in readable format.
  But that's too much data.
- Backend parse the data and generate images, but it's not interactive.
"""

from . import RecordContentHandler

class NVHStatModel:
    # a model knows how to read data, construct an object
    # and then to be used for manipulation
    # and also export to format clients need
    pass

class NVHStatHandler(RecordContentHandler):
    def __init__(self, module_name: str, storage_path: str):
        super().__init__(module_name)
        self.storage_path = storage_path

    def register_api(self, blueprint):
        @blueprint.route(f"/modules/{self.module_name}/images/<string:category>/<path:filename>", methods=['GET'])
        def serve_image(category, filename):
            # read <filename> and make a data object
            # make cache
            # generate image of multiple measurements according to category
            # serve the image
            pass

        @blueprint.route(f"/x-modules/{self.module_name}/images/<string:category>/", methods=['POST'])
        def x_serve_images(category): # for visualizing multiple resources, can it return multiple images at one run?
            pass

        def serve_binary(filename):
            pass

        def serve_json(filename):
            pass