from django.db import models

class CarouselBanner(models.Model):
    image = models.ImageField(upload_to='carousel/')
    promotion = models.CharField(max_length=120, blank=True, null=True)
    ordem = models.PositiveIntegerField(default=0)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['ordem', '-created_at']

    def __str__(self):
        return f'{self.promotion or "Banner"} #{self.id}'