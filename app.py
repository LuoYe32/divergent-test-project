from flask import Flask, jsonify, abort, Response
from typing import Tuple
import json

app = Flask(__name__)


def data_loader() -> Tuple[dict, dict]:
    """
    Функция загружает данные из json файлов и преобразует их в dict.
    Функция не должна нарушать изначальную структуру данных.
    """
    with open('data/posts.json', 'r', encoding='utf-8') as posts_file:
        posts_data = json.load(posts_file)
        posts = posts_data['posts']

    with open('data/comments.json', 'r', encoding='utf-8') as comments_file:
        comments_data = json.load(comments_file)
        comments = comments_data['comments']

    return posts, comments


@app.route("/")
def get_posts():
    """
    На странице / вывести json в котором каждый элемент - это:
    - пост из файла posts.json.
    - для каждой поста указано кол-во комментариев этого поста из файла comments.json

    Формат ответа:
    posts: [
        {
            id: <int>,
            title: <str>,
            body: <str>, 
            author:	<str>,
            created_at: <str>,
            comments_count: <int>
        }
    ],
    total_results: <int>

    Порядок ключей словаря в ответе не важен
    """
    posts, comments = data_loader()

    comments_count = {post['id']: 0 for post in posts}
    for comment in comments:
        if comment['post_id'] in comments_count:
            comments_count[comment['post_id']] += 1

    response_posts = []
    for post in posts:
        response_post = post.copy()
        response_post['comments_count'] = comments_count[post['id']]
        response_posts.append(response_post)

    output = {
        "posts": response_posts,
        "total_results": len(response_posts)
    }

    return Response(json.dumps(output, ensure_ascii=False), content_type="application/json; charset=utf-8")

@app.route("/posts/<int:post_id>")
def get_post(post_id):
    """
    На странице /posts/<post_id> вывести json, который должен содержать:
    - пост с указанным в ссылке id
    - список всех комментариев к новости

    Отдавайте ошибку abort(404), если пост не существует.


    Формат ответа:
    id: <int>,
    title: <str>,
    body: <str>, 
    author:	<str>,
    created_at: <str>
    comments: [
        "user": <str>,
        "post_id": <int>,
        "comment": <str>,
        "created_at": <str>
    ]

    Порядок ключей словаря в ответе не важен
    """
    posts, comments = data_loader()

    post = next((p for p in posts if p['id'] == post_id), None)
    if post is None:
        abort(404)

    post_comments = [comment for comment in comments if comment['post_id'] == post_id]

    response_post = post.copy()
    response_post['comments'] = post_comments

    return Response(json.dumps(response_post, ensure_ascii=False), content_type="application/json; charset=utf-8")

if __name__ == "__main__":
    app.run(debug=True)
