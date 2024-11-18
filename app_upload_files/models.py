from django.db import models

# Cartola Generica
class UploadCartolaBanco(models.Model):
    file_name = models.FileField(upload_to="upload_file")
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"File id: {self.file_name}"


# Compras Chile
class UploadComprasChile(models.Model):
    file_name = models.FileField(upload_to="upload_file")
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"File id: {self.file_name}"
    
    
# Ventas Chile
class UploadVentasChile(models.Model):
    file_name = models.FileField(upload_to="upload_file")
    uploaded = models.DateTimeField(auto_now_add=True)
    activated = models.BooleanField(default=False)
    
    def __str__(self):
        return f"File id: {self.file_name}"