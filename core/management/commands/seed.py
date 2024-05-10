import sys
from django.conf import settings
from user.helper import usertoken
from user.models import User, UserToken
from django.core.management.base import BaseCommand
from django.contrib.auth.hashers import make_password, check_password

def progress(count, total, suffix=''):
    bar_len = 60
    filled_len = int(round(bar_len * count / float(total)))
    percents = round(100.0 * count / float(total), 1)
    bar = '=' * filled_len + '-' * (bar_len - filled_len)
    sys.stdout.write('[%s] %s%s ...%s\r' % (bar, percents, '%', suffix))
    sys.stdout.flush()


# python manage.py seed --mode=refresh


"""Clear all data and creates addresses"""
MODE_REFRESH = 'refresh'

""" Clear all data and do not create any object """
MODE_CLEAR = 'clear'

class Command(BaseCommand):
    help = "seed database for testing and development."

    def add_arguments(self, parser):
        parser.add_argument('--mode', type=str, help="Mode")

    def handle(self, *args, **options):
        self.stdout.write('seeding data...')
        run_seed(self, options['mode'])
        self.stdout.write('done.')


def clear_data():
    """Deletes all the table data"""
    user_delete = User.objects.all().delete()
    if user_delete:
        print("data cleared..")

def create_data():
    """Creates an  object combining different elements from the list"""
    try:
        email = "admin@example.com"
        password = "Admin@123"
        print("\nCreating system user...\n")
        progress(0,100,'')
        print("\n")
        if not User.objects.filter(email=email).exists():
            user = User(
                name="Administrator", 
                email=email,
                password=make_password(password),
                is_active=True,
                is_admin=True
                )
            user.save()
            progress(50,100,'')
            if user:
                user_token = UserToken.objects.create(user=user, is_active=True)
                if user_token:
                    access_token = usertoken(user_token.id)
                progress(100,100,'')
                print('\n')
                print(f"\nUser Name >>> {user.name}")
                print(f"\nUser Email >>> {user.email}")
                print(f"\nPassword >>> {password}\n")
                print(f"\nAccess token >>> {access_token}\n")
                print("\nSystem user created.\n")
            else:
                print("User creation failed")
        else:
            print("User already exists")
    except Exception as e:
        print(f"Error creating user : {repr(e)}")


def run_seed(self, mode):
    """ Seed database based on mode

    :param mode: refresh / clear 
    :return:
    """
    if mode == MODE_CLEAR:
        clear_data()
    if mode == MODE_REFRESH:
        create_data()
