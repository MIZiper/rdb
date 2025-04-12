import os
from typing import Any
from flask import request

class ResourceContentHandler:
    """Base class for handling resource content based on type."""
    _registry: dict[str, type["ResourceContentHandler"]] = {}

    def __init__(self, content: str):
        self.content = content

    def to_client(self) -> Any:
        raise NotImplementedError

    def to_database(self) -> str:
        raise NotImplementedError

    @classmethod
    def register_handler(cls, module_name: str, handler_cls: type):
        # module_name can be different for one handler
        # e.g. one resource type can be used for multiple modules
        cls._registry[module_name] = handler_cls

    @classmethod
    def get_handler(cls, module_name: str, content: str):
        handler_cls = cls._registry.get(module_name, cls)
        return handler_cls(content)

    @classmethod
    def register_api(cls, blueprint, module_name: str):
        """Base method for registering API routes. Subclasses should override this."""
        pass

class RawHandler(ResourceContentHandler):
    # store raw string into sqlite
    # and return raw string as well
    pass

class JsonHandler(ResourceContentHandler):
    # store json string into sqlite
    # and return content as json
    pass

class ImageBrowserHandler(ResourceContentHandler):
    def __init__(self, content: str, storage_path: str = "./image_storage"):
        super().__init__(content)
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    def to_client(self) -> list[dict]:
        # Example: Return a list of image URLs
        return self.content.splitlines()

    def to_database(self) -> str:
        # Store content as newline-separated image URLs
        return self.content

    def handle_request(self):
        """Handle API requests for the ImageBrowser module."""
        if 'file' not in request.files:
            return {"error": "No file part in the request"}, 400

        file = request.files['file']
        if file.filename == '':
            return {"error": "No selected file"}, 400

        if file:
            file_path = os.path.join(self.storage_path, file.filename)
            file.save(file_path)
            return {"message": f"File saved to {file_path}"}, 201

    @classmethod
    def register_api(cls, blueprint, module_name: str):
        """Register API routes for the ImageBrowser module."""
        @blueprint.route(f"/modules/{module_name}/upload", methods=['POST'])
        def upload():
            handler = cls("", storage_path=module_name)
            response, status_code = handler.handle_request()
            return response, status_code


# Register handlers dynamically
ResourceContentHandler.register_handler("Markdown", RawHandler)
ResourceContentHandler.register_handler("ImageBrowser", ImageBrowserHandler)
