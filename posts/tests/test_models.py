from django.test import TestCase, Client
from posts.models import Post, Group, USER_MODEL


class PostsModelTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()

        cls.client = Client()
        cls.user = USER_MODEL.objects.create_user(username='vasa88')
        cls.client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Название',
            description='Описание',
            slug='Ссылка',
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=cls.user
        )

    def test_verbose_name(self):
        post = self.post
        field_verboses = {
            'text': 'Содержание',
            'group': 'Группа',
        }
        for value, expected in field_verboses.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).verbose_name, expected
                )

    def test_help_text(self):
        post = PostsModelTest.post
        field_help_texts = {
            'text': 'Придумай содержание',
            'group': 'Выбери группу',
        }
        for value, expected in field_help_texts.items():
            with self.subTest(value=value):
                self.assertEqual(
                    post._meta.get_field(value).help_text, expected
                )

    def test_str_post_text(self):
        post = PostsModelTest.post
        text = post.text
        self.assertEqual(str(post), text[:15])

    def test_str_group_title(self):
        group = PostsModelTest.group
        title = str(group)
        self.assertEqual(title, group.title)
