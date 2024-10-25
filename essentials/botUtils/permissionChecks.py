import nextcord

def has_roles(member: nextcord.Member, roles: list[str]):
    """
    Checks if the member has any role from the required_roles list by role name.

    :param member: The Nextcord Member object representing the user.
    :param required_roles: A list of role ids (strings) that grants permission.
    :return: True if the member has any of the required roles, False otherwise.
    """

    return any(role.id in roles for role in member.roles)

def has_role(member: nextcord.Member, role: str):
    """
    Checks if the member has a specific role from role paramater.

    :param member: The Nextcord member object representing the user.
    :param role: A role id that grants permission.
    :return: True if the member has any of the required roles, False otherwise.
    """

    return any(role.id in member.roles)