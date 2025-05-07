import os, uuid, json
from os import path
from typing import Any
from flask import Request, send_from_directory
from PIL import Image

class RecordContentHandler:
    """Base class for handling resource content based on type."""
    _registry: dict[str, "RecordContentHandler"] = {}

    def __init__(self, module_name: str):
        self.module_name = module_name

    def to_client(self, content: str) -> Any:
        return content

    def to_database(self, content: Any) -> str:
        return content

    def register_api(self, blueprint):
        """Base method for registering API routes. Subclasses should override this."""
        pass

    @staticmethod
    def register_handler(handler_obj: "RecordContentHandler"):
        # module_name can be different for one handler type
        # e.g. one resource type can be used for multiple modules
        module_name = handler_obj.module_name
        if module_name in RecordContentHandler._registry:
            raise ValueError(f"Handler already registered for module: {module_name}")
        RecordContentHandler._registry[module_name] = handler_obj

    @staticmethod
    def get_handler(module_name: str):
        handler = RecordContentHandler._registry.get(module_name)
        if handler is None:
            return RawHandler("Unhandled")
        return handler

class RawHandler(RecordContentHandler):
    # store raw string into sqlite
    # and return raw string as well

    # TODO: to_database() for unhandled case with non-string content

    pass

class JsonHandler(RecordContentHandler):
    # store json string into sqlite
    # and return content as json
    def to_client(self, content: str) -> dict | list:
        return json.loads(content)

    def to_database(self, content: dict | list) -> str:
        return json.dumps(content)

class ImageBrowserHandler(RecordContentHandler):
    def __init__(self, module_name: str, storage_path: str):
        super().__init__(module_name)
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    def to_client(self, content: str) -> list[dict]:
        # Return a list of image URLs and remarks

        data = json.loads(content)
        image_urls = []
        for item in data:
            image_url = item.get("fname")
            remark = item.get("remark")
            if image_url and remark:
                image_urls.append(
                    {
                        "url": f"/api/modules/{self.module_name}/images/{image_url}",
                        "remark": remark
                    }
                )
        return image_urls

    def to_database(self, request: Request) -> str:
        # Store content as newline-separated image URLs, thumbnails, and remarks

        files = request.files.getlist('files[]')
        remarks = request.form.getlist('remarks[]')

        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
        saved_files = []

        for file, remark in zip(files, remarks):
            if file.filename == '':
                continue

            if len(file.read()) > MAX_FILE_SIZE:
                raise ValueError(f"File size exceeds the limit of {MAX_FILE_SIZE} bytes.")
            
            file.seek(0)  # Reset file pointer after size check

            unique_filename = f"{uuid.uuid4().hex}.png"
            file_path = os.path.join(self.storage_path, unique_filename)
            file.save(file_path)

            # Generate thumbnail
            thumbnail_filename = f"thumb_{unique_filename}"
            thumbnail_path = os.path.join(self.storage_path, thumbnail_filename)
            with Image.open(file_path) as img:
                img.thumbnail((200, 200))  # Limit thumbnail size to 200x200
                img.save(thumbnail_path)

            saved_files.append(
                {
                    "fname": unique_filename,
                    "remark": remark
                }
            )

        return json.dumps(saved_files)

    def register_api(self, blueprint):
        """Register API routes for the ImageBrowser module."""
        
        @blueprint.route(f"/modules/{self.module_name}/images/<path:filename>", methods=['GET'])
        def serve_image(filename):
            return send_from_directory(self.storage_path, filename)

# Register handlers dynamically
RecordContentHandler.register_handler(RawHandler("MarkdownPage"))
RecordContentHandler.register_handler(RawHandler("MermaidDiagram"))
RecordContentHandler.register_handler(ImageBrowserHandler("ImageBrowser", storage_path=path.join(path.dirname(__file__), "../../storage/images")))
