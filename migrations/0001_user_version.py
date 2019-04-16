USER_COLLECTION = 'user'


def up(db):
    for user in db[USER_COLLECTION].find({'version': None}):
        user['version'] = 1
        db[USER_COLLECTION].save(user)


def down(db):
    for user in db[USER_COLLECTION].find({'version': 1}):
        user.pop('user', None)
        db[USER_COLLECTION].save(user)
