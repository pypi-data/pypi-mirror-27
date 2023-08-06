from Crypto.PublicKey import RSA
from django.db import models
from django.utils.translation import ugettext_lazy as _
from django.conf import settings
from .utils import generate_rsa_key
from .utils import get_rsa_public_key
from .utils import export_key
from .utils import import_key


class RsaKey(models.Model):
    name = models.CharField(max_length=64, unique=True, verbose_name=_("Name"))
    title = models.CharField(max_length=64, null=True, blank=True, verbose_name=_("Title"))
    nbits = models.IntegerField(default=2048, verbose_name=_("nBits"))
    public_key = models.TextField(null=True, blank=True, verbose_name=_("Public Key"))
    private_key = models.TextField(null=True, blank=True, verbose_name=_("Private Key"))

    class Meta:
        verbose_name = _("Rsa Key")
        verbose_name_plural = _("Rsa Keys")

    def __str__(self):
        return self.name

    def save(self, *args, **kwargs):
        if not self.public_key and not self.private_key:
            rsa_private_key = generate_rsa_key(self.nbits)
            rsa_public_key = get_rsa_public_key(rsa_private_key)
            self.public_key = export_key(rsa_public_key)
            self.private_key = export_key(rsa_private_key, settings.SECRET_KEY)
        super(RsaKey, self).save(*args, **kwargs)

    @property
    def rsa_public_key(self):
        if self.public_key:
            return import_key(self.public_key)
        return None

    @property
    def rsa_private_key(self):
        if self.private_key:
            return import_key(self.private_key, passphrase=settings.SECRET_KEY)
        return None
