from django.forms.models import model_to_dict


class ModelDiffMixin(object):
    """
    A model mixin that tracks model fields' values and provide some useful api
    to know what fields have been changed.
    """

    def __init__(self, *args, **kwargs):
        super(ModelDiffMixin, self).__init__(*args, **kwargs)
        self._saving_change_callbacks = False
        self.__initial = self._get_model_dict()

    def save(self, *args, **kwargs):
        """
        Saves model and set initial state.
        """
        if not self._saving_change_callbacks:
            self._saving_change_callbacks = True
            try:
                for field in self.changed_fields:
                    on_change_func = getattr(self, 'on_%s_change' % field, None)
                    if callable(on_change_func):
                        on_change_func(*self.get_field_diff(field))
            finally:
                self._saving_change_callbacks = False
        super(ModelDiffMixin, self).save(*args, **kwargs)
        self.__initial = self._get_model_dict()

    def _get_model_dict(self):
        """

        :return:
        :rtype: dict
        """
        return model_to_dict(self, fields=[field.name for field in self._meta.fields])

    def _get_diff(self):
        d1 = self.__initial
        d2 = self._get_model_dict()
        diffs = [(k, (v, d2[k])) for k, v in d1.items() if v != d2[k]]
        return dict(diffs)

    @property
    def has_changed(self):
        """True if the model has changed
        :rtype: bool
        """
        return bool(self._get_diff())

    @property
    def changed_fields(self):
        """

        :return:
        :rtype: list(str)
        """
        return self._get_diff().keys()

    def get_field_diff(self, field_name):
        """
        Returns a diff for field if it's changed and None otherwise.

        :rtype: tuple(any)
        """
        return self._get_diff().get(field_name, None)
