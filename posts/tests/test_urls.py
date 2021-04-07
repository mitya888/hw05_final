from django.test import TestCase, Client

from posts.models import Group, Post, USER_MODEL


class StaticURLTests(TestCase):
    def setUp(self):
        # Устанавливаем данные для тестирования
        # Создаём экземпляр клиента. Он неавторизован.
        self.guest_client = Client()

    def test_homepage(self):
        # Делаем запрос к главной странице и проверяем статус
        response = self.guest_client.get('/')
        # Утверждаем, что для прохождения теста код должен быть равен 200
        self.assertEqual(response.status_code, 200)


class PostURLTest(TestCase):
    @classmethod
    def setUpClass(cls):
        super().setUpClass()
        # Создаем пользователя
        cls.user = USER_MODEL.objects.create_user(username='petr')
        cls.user2 = USER_MODEL.objects.create_user(username='lex')
        cls.guest_client = Client()
        cls.authorized_client = Client()
        cls.authorized_client.force_login(cls.user)

        cls.group = Group.objects.create(
            title='Тестовый заголовок',
            description='Описание',
            slug='test-slug'
        )
        cls.post = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=cls.user
            # author=User.objects.create(username='petr'),
        )
        cls.post2 = Post.objects.create(
            text='Тестовый текст',
            group=cls.group,
            author=cls.user2
            # author=User.objects.create(username='lex'),
        )

    def test_new_posts_url_guest_client(self):
        """Страница /new/ создания поста не доступна анонимному пользователю"""
        response = self.guest_client.get('/new/')
        self.assertEqual(response.status_code, 302)

    def test_urls_template(self):
        """Какой шаблон вызывается для страниц:"""
        templates_url_names = {
            'index.html': '/',
            'group.html': '/group/test-slug/',
            'post_new.html': f'/{self.user.username}/{self.post.id}/edit/'
        }
        for template, url in templates_url_names.items():
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertTemplateUsed(response, template)

    def test_post_edit_url_guest(self):
        """Доступность страницы редактирования поста для гостя"""
        response = self.guest_client.get('/petr/1/edit/')
        self.assertEqual(response.status_code, 302)

    def test_post_edit_url_authorised_not_author(self):
        """Доступность страницы редактирования поста для не автора поста"""
        response = self.authorized_client.get('/lex/1/edit/')
        self.assertEqual(response.status_code, 404)

    def test_post_edit_redirect_not_author(self):
        """редирект со страницы /<username>/<post_id>/edit/для тех,
        у кого нет прав доступа к этой странице."""
        url = f'/{self.user.username}/{self.post2.id}/edit'
        response = self.authorized_client.get(url)
        self.assertEqual(response.status_code, 301)

    def test_urls_guest_client_200(self):
        """Тест страниц 200 для анонима"""
        test_urls = [
            '/',
            '/about/author/',
            '/about/tech/',
            '/group/test-slug/'
        ]
        for url in test_urls:
            with self.subTest(url=url):
                response = self.guest_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_urls_authorized_client_200(self):
        """Тест страниц 200 для анонима"""
        test_urls = [
            '/group/test-slug/',
            '/new/',
            '/petr/',
            '/petr/1/',
            '/petr/1/edit/'
        ]
        for url in test_urls:
            with self.subTest(url=url):
                response = self.authorized_client.get(url)
                self.assertEqual(response.status_code, 200)

    def test_url_404(self):
        """Доступность страницы 404"""
        response = self.guest_client.get('404')
        self.assertEqual(response.status_code, 404)
