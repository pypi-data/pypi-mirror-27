from cStringIO import StringIO
from django.conf import settings
from PIL import Image

from . import tasks


def delete_playbook_workspace(sender, instance, **kwargs):
    if not settings.WALDUR_ANSIBLE.get('PRESERVE_PLAYBOOK_WORKSPACE_AFTER_DELETION', False):
        tasks.delete_playbook_workspace.delay(instance.workspace)


def resize_playbook_image(sender, instance, **kwargs):
    if not instance.tracker.has_changed('image') or not instance.image:
        return

    size = settings.WALDUR_ANSIBLE['PLAYBOOK_ICON_SIZE']
    field = instance.image
    image = Image.open(field.file)
    image.thumbnail(size, Image.ANTIALIAS)

    image_file = StringIO()
    image.save(image_file, 'png')
    field.file = image_file
