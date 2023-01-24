# First-party imports
from accounts.models import AccountProfile, Account


def run():
    """Create a AccountProfile for all existing users.
    If already AccountProfile exist then skip it"""

    # Fetch users who has AccountProfile created
    user_ids_with_profile = AccountProfile.objects.all().values_list(
        "user__id", flat=True
    )

    # Get Users without profile
    user_without_profile = Account.objects.exclude(id__in=user_ids_with_profile)

    # Bulk Create Profiles for these users
    profile_list = []
    for user in user_without_profile:
        profile = AccountProfile(
            user=user,
            profile_picture="default/default-user.png",
        )
        profile_list.append(profile)

    AccountProfile.objects.bulk_create(profile_list)


if __name__ == "__main__":
    run()
