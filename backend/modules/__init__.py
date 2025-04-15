import os
import uuid
from typing import Any
from flask import Request, send_from_directory
from PIL import Image

class RecordContentHandler:
    """Base class for handling resource content based on type."""
    _registry: dict[str, "RecordContentHandler"] = {}

    def to_client(self, content: str) -> Any:
        return content

    def to_database(self, content: Any) -> str:
        return content

    def register_api(self, blueprint, module_name: str):
        """Base method for registering API routes. Subclasses should override this."""
        pass

    @staticmethod
    def register_handler(module_name: str, handler_obj: "RecordContentHandler"):
        # module_name can be different for one handler type
        # e.g. one resource type can be used for multiple modules
        if module_name in RecordContentHandler._registry:
            raise ValueError(f"Handler already registered for module: {module_name}")
        RecordContentHandler._registry[module_name] = handler_obj

    @staticmethod
    def get_handler(module_name: str):
        handler = RecordContentHandler._registry.get(module_name)
        if handler is None:
            raise ValueError(f"No handler registered for module: {module_name}")
        return handler

class RawHandler(RecordContentHandler):
    # store raw string into sqlite
    # and return raw string as well
    pass

class JsonHandler(RecordContentHandler):
    # store json string into sqlite
    # and return content as json
    pass

class ImageBrowserHandler(RecordContentHandler):
    def __init__(self, storage_path: str):
        super().__init__()
        self.storage_path = storage_path
        os.makedirs(self.storage_path, exist_ok=True)

    def to_client(self, content: str) -> list[dict]:
        # Return a list of image URLs and remarks
        return [
            {
                "url": line.split('|')[0],
                "thumbnail": line.split('|')[1],
                "remark": line.split('|')[2]
            }
            for line in self.content.splitlines()
            if line.strip()
        ]

    def to_database(self, request: Request) -> str:
        # Store content as newline-separated image URLs, thumbnails, and remarks

        files = request.files.getlist('files')
        remarks = request.form.getlist('remarks')

        MAX_FILE_SIZE = 5 * 1024 * 1024  # 5 MB
        saved_files = []

        for file, remark in zip(files, remarks):
            if file.filename == '':
                continue

            if len(file.read()) > MAX_FILE_SIZE:
                raise ValueError(f"File size exceeds the limit of {MAX_FILE_SIZE} bytes.")
            
            file.seek(0)  # Reset file pointer after size check

            unique_filename = f"{uuid.uuid4().hex}"
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
                    "url": unique_filename,
                    "thumbnail": thumbnail_filename,
                    "remark": remark
                }
            )

        content = "\n".join(
            [
                f"{file['url']}|{file['thumbnail']}|{file['remark']}"
                for file in saved_files
            ]
        )
        return content

    def register_api(self, blueprint, module_name: str):
        """Register API routes for the ImageBrowser module."""
        
        @blueprint.route(f"/modules/{module_name}/images/<path:filename>", methods=['GET'])
        def serve_image(filename):           
            return send_from_directory(self.storage_path, filename)

# Register handlers dynamically
RecordContentHandler.register_handler("Markdown", RawHandler())
RecordContentHandler.register_handler("ImageBrowser", ImageBrowserHandler(storage_path="storage/images"))
