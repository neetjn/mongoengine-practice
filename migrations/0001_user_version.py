USER_COLLECTION = 'user'


def up(db):
    for user in db[USER_COLLECTION].find():
        user['version'] = 1
        db[USER_COLLECTION].save(user)


def down(db):
    for user in db[USER_COLLECTION].find():
        user.pop('user', None)
        db[USER_COLLECTION].save(user)
