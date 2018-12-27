class BaseViewModel:

    def keys(self):
        return self.show_keys

    def __getitem__(self, item):
        return getattr(self, item)

    def append(self, keys):
        for key in keys:
            if key not in self.show_keys:
                self.show_keys.append(key)

    def hide(self, keys):
        for key in keys:
            if key in self.show_keys:
                self.show_keys.remove(key)
