class Scope:
    allow_api = []
    allow_module = []
    forbidden = []

    def __add__(self, other):
        self.allow_api += other.allow_api
        self.allow_api = list(set(self.allow_api))

        self.allow_module += other.allow_module
        self.allow_module = list(set(self.allow_module))

        self.forbidden += other.forbidden
        self.forbidden = list(set(self.forbidden))

        return self


class UserScope(Scope):
    # allow_api = ['api.v1.user+get_user', 'api.v1.user+delete_user']
    forbidden = ['api.v1.user+admin_get_user', 'api.v1.user+admin_delete_user',
                 'api.v1.user+admin_add_user', 'api.v1.user+admin_update_user']

    def __init__(self):
        self + AdminScope()


class AdminScope(Scope):
    allow_module = ['api.v1.member', 'api.v1.food', 'api.v1.address', 'api.v1.cart', 'api.v1.order',
                    'cms.user', 'cms.index', 'cms.account', 'cms.food', 'cms.member',
                    'cms.upload']

    # def __init__(self):
    #     self + UserScope()


# class SuperScope(Scope):
#     allow_api = ['api.v1.user+super_get_user']
#     allow_module = ['api.v1.user']

# def __init__(self):
#     self + UserScope() + AdminScope()


def is_in_scope(scope, endpoint):
    scope = globals()[scope]()
    splits = endpoint.split('+')
    red_name = splits[0]
    if endpoint in scope.forbidden:
        return False
    if endpoint in scope.allow_api:
        return True
    if red_name in scope.allow_module:
        return True
    else:
        return False
