import random
import datetime
import decimal

from django.utils import timezone

from apps.users.models import User
from apps.users.constants import UserRoles
from apps.food.models import Food


def load_data():
    USERS = [
        User(first_name='Bartosz', last_name='Zapałowski', user_id='bartosz',
             role=UserRoles.ADMIN, daily_calorie_threshold=2100, monthly_price_threshold=1000),
        User(first_name='Kamalesh', last_name='Tangudu', user_id='kamal',
             role=UserRoles.ROUTINE, daily_calorie_threshold=1800, monthly_price_threshold=800),
        User(first_name='Phanindra', last_name='Thatavarthi', user_id='phani',
             role=UserRoles.ROUTINE, daily_calorie_threshold=2000, monthly_price_threshold=900),
        User(first_name='Shivam', last_name='Kapoor', user_id='shivam',
             role=UserRoles.ADMIN, daily_calorie_threshold=1700, monthly_price_threshold=1100),
        User(first_name='Smith', last_name='Rowe', user_id='smith', role=UserRoles.ROUTINE,
             daily_calorie_threshold=2500, monthly_price_threshold=1500),
        User(first_name='Bukayo', last_name='Saka', user_id='bukayo',
             role=UserRoles.ROUTINE, daily_calorie_threshold=2700, monthly_price_threshold=1200)
    ]
    User.objects.bulk_create(USERS)

    user_count = len(USERS)

    FOOD_NAMES = [
        'Idly', 'Dosa', 'Sambar Rice', 'Rajma Chawal', 'South Indian Thali', 'North Indian Thali',
        'Hamburger', 'Pasta', 'Pizza', 'Chicken Lasagne', 'Steak', 'Tuna', 'Hotdog',
        'Milk and Bread', 'Maggi', 'Omlette', 'Cake', 'Honey and Waffles', 'Pancakes', 'Chocolate Brownie'
    ]
    food_name_count = len(FOOD_NAMES)

    FOOD_ROWS = [
        Food(
            name=FOOD_NAMES[random.randint(0, food_name_count - 1)],
            user_id=USERS[random.randint(0, user_count - 1)].user_id,
            taken_at=timezone.now() - datetime.timedelta(
                days=random.randint(0, 90),
                hours=random.randint(0, 23),
                minutes=random.randint(0, 59),
                seconds=random.randint(0, 59)
            ),
            calories=float(decimal.Decimal(random.randrange(10000, 80000)) / 100),
            price=float(decimal.Decimal(random.randrange(100, 2500)) / 100),
        )
        for _ in range(1800)
    ]

    Food.objects.bulk_create(FOOD_ROWS)
