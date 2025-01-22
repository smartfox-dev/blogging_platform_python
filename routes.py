from flask import Flask, request, jsonify
from models import db, BlogPost, Comment

app = Flask(__name__)

@app.route('/api/posts', methods=['GET'])
def get_posts():
    posts = BlogPost.query.all()
    result = []
    for post in posts:
        post_data = {
            'id': post.id,
            'title': post.title,
            'num_comments': len(post.comments)
        }
        result.append(post_data)
    return jsonify(result)

@app.route('/api/posts', methods=['POST'])
def create_post():
    data = request.get_json()
    new_post = BlogPost(title=data['title'], content=data['content'])
    db.session.add(new_post)
    db.session.commit()
    return jsonify({'message': 'Post created successfully'})

@app.route('/api/posts/<int:id>', methods=['GET'])
def get_post(id):
    post = BlogPost.query.get_or_404(id)
    post_data = {
        'id': post.id,
        'title': post.title,
        'content': post.content,
        'comments': [{'id': comment.id, 'content': comment.content} for comment in post.comments]
    }
    return jsonify(post_data)

@app.route('/api/posts/<int:id>/comments', methods=['POST'])
def add_comment(id):
    data = request.get_json()
    post = BlogPost.query.get_or_404(id)
    new_comment = Comment(content=data['content'], post_id=post.id)
    db.session.add(new_comment)
    db.session.commit()
    return jsonify({'message': 'Comment added successfully'})
