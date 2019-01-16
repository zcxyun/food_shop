class BaseViewModel:

    def keys(self):
        return self.show_keys

    def __getitem__(self, item):
        return getattr(self, item)

    def hide(self, *keys):
        self.show_keys = list(set(self.show_keys) - set(keys))
        return self

    def show(self, *keys):
        self.show_keys = list(set(self.show_keys) & set(keys))
        return self
