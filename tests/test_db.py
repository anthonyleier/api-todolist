from dataclasses import asdict

from sqlalchemy import select

from app.models import Todo, TodoState, User


def test_create_user(session, mock_db_time):
    with mock_db_time(model=User) as time:
        new_user = User(username='alice', password='secret', email='alice@gmail.com')
        session.add(new_user)
        session.commit()

        user = session.scalar(select(User).where(User.username == 'alice'))

        assert asdict(user) == {
            'id': 1,
            'username': 'alice',
            'password': 'secret',
            'email': 'alice@gmail.com',
            'created_at': time,
            'updated_at': time,
            'todos': [],
        }


def test_create_todo(session, user: User):
    todo = Todo(title='Test Todo', description='Test Description', state=TodoState.draft, user_id=user.id)

    session.add(todo)
    session.commit()
    session.refresh(todo)

    user = session.scalar(select(User).where(User.id == user.id))
    assert todo in user.todos
