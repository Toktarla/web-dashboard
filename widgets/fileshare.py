import os
from datetime import datetime
from features.component import Component

class FileShare(Component):
    def __init__(self):
        super().__init__("FileShare", "File Sharing", 50, 50)
        self.env['path'] = "shared_files"
        self.events.extend(['upload', 'download', 'delete'])
        self.content = []
        
    def upload(self, params):
        if 'filename' in params and 'content' in params:
            filepath = os.path.join(self.env['path'], params['filename'])
            os.makedirs(self.env['path'], exist_ok=True)
            with open(filepath, 'w') as f:
                f.write(params['content'])
            self.refresh()
            
    def download(self, params):
        if 'filename' in params:
            filepath = os.path.join(self.env['path'], params['filename'])
            if os.path.exists(filepath):
                with open(filepath, 'r') as f:
                    return {'content': f.read()}
            return {'error': 'File not found'}
            
    def delete(self, params):
        if 'filename' in params:
            filepath = os.path.join(self.env['path'], params['filename'])
            if os.path.exists(filepath):
                os.remove(filepath)
                self.refresh()
                
    def refresh(self):
        self.content = []
        if os.path.exists(self.env['path']):
            for filename in os.listdir(self.env['path']):
                filepath = os.path.join(self.env['path'], filename)
                stats = os.stat(filepath)
                self.content.append({
                    'filename': filename,
                    'size': stats.st_size,
                    'modified': datetime.fromtimestamp(stats.st_mtime)
                })
                
    def view(self):
        if not self.content:
            return "No files in shared directory"
        
        output = ["Shared Files:"]
        for file in self.content:
            output.append(f"{file['filename']} - {file['size']} bytes - {file['modified']}")
        return "\n".join(output)