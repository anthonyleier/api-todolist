import factory
import factory.fuzzy

from app.models import Todo, TodoState


class TodoFactory(factory.Factory):
    class Meta: # type: ignore
        model = Todo

    title = factory.Faker('text')
    description = factory.Faker('text')
    state = factory.fuzzy.FuzzyChoice(TodoState)
    user_id = 1


def test_create_todo(client, token):
    response = client.post(
        '/todos/',
        headers={'Authorization': f'Bearer {token}'},
        json={
            'title': 'Test todo',
            'description': 'Test todo description',
            'state': 'draft',
        },
    )
    assert response.json() == {'id': 1, 'title': 'Test todo', 'description': 'Test todo description', 'state': 'draft'}


def test_list_todos_should_return_5_todos(session, client, user, token):
    expected_todos = 5

    session.bulk_save_objects(TodoFactory.create_batch(expected_todos, user_id=user.id))
    session.commit()

    response = client.get('/todos', headers={'Authorization': f'Bearer {token}'})
    assert len(response.json()['todos']) == expected_todos
