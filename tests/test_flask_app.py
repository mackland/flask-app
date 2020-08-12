import pytest, datetime
from app import create_app, db
from app.models import User, Post
from config import Config


class TestConfig(Config):
    TESTING = True
    SQLALCHEMY_DATABASE_URI = 'sqlite://'


@pytest.fixture(scope='session')
def flask_app():
    """Creates a database and flask app with context, current_app"""

    print('\n--- CREATE FLASK APPLICATION')
    app = create_app(TestConfig)

    print('\n--- CREATE FLASK APPLICATION CONTEXT')
    context = app.app_context()
    context.push()

    print('\n--- CREATE DB TABLES')
    db.create_all()

    yield app

    print('\n--- DESTROY DB TABLES')
    db.session.remove()
    db.drop_all()

    print('\n--- RELEASE FLASK APPLICATION CONTEXT')
    context.pop()


@pytest.fixture(scope='function')
def add_users(flask_app):
    """Adds 4 users to the database"""

    u1 = User(username='marcus', email='marcus@example.com')
    u2 = User(username='john', email='john@example.com')
    u3 = User(username='susan', email='susan@example.com')
    u4 = User(username='david', email='david@example.com')
    db.session.add_all([u1, u2, u3, u4])
    db.session.commit()

    yield u1, u2, u3, u4

    db.session.query(User).delete()


@pytest.fixture(scope='function')
def add_posts(flask_app, add_users):
    u1, u2, u3, u4 = add_users
    now = datetime.datetime.utcnow()

    p1 = Post(body="post from marcus", author=u1, timestamp=now + datetime.timedelta(seconds=1))
    p2 = Post(body="post from john", author=u2, timestamp=now + datetime.timedelta(seconds=4))
    p3 = Post(body="post from susan", author=u3, timestamp=now + datetime.timedelta(seconds=3))
    p4 = Post(body="post from david", author=u4, timestamp=now + datetime.timedelta(seconds=2))

    db.session.add_all([p1, p2, p3, p4])

    yield p1, p2, p3, p4

    db.session.query(Post).delete()


@pytest.mark.parametrize("password,expected", [
    ('CAT', False),
    ('Cat', False),
    ('dog', False),
    ('cat', True)
])
def test_password_hash(password, expected):
    user = User(username='marcus')
    user.set_password('cat')
    results = user.check_password(password)
    assert(results == expected)


def test_follow(flask_app, add_users):
    u1, u2, u3, u4 = add_users
    assert(len(u1.followed.all()) == 0)
    assert (len(u1.followers.all()) == 0)

    u1.follow(u2)
    db.session.commit()

    assert (u1.is_following(u2))
    assert (u1.followed.count() == 1)
    assert (u1.followed.first().username == u2.username)
    assert (u2.followers.count() == 1)
    assert (u2.followers.first().username == u1.username)


def test_users_2(flask_app, add_posts):
    p1, p2, p3, p4 = add_posts
    print('\n')
    print(User.query.all())
    assert True
