def find_named(list_with_named, name):
    list_of_one = []
    if name in [item.name for item in list_with_named]:
        list_of_one = [item for item in list_with_named if item.name == name]

    return list_of_one[0] if len(list_of_one) == 1 else None


def is_admin(user):
    return True if find_named(user.roles, "Admins") else False


def is_beta_tester(user):
    return True if find_named(user.roles, "Beta-Tester") else False
