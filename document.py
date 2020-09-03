
class Document:
    def __init__(self, file_path, confidential, friendly_name=None):
        self.file_path = file_path
        self.confidential = confidential
        self.friendly_name = friendly_name

    @property
    def file_name(self):
        return self.file_path.split('/')[-1]
