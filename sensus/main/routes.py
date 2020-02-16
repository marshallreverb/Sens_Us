from flask import Blueprint, request, render_template

from sensus.models import Post

main = Blueprint('main',__name__)




@main.route('/')
@main.route('/home')
def index():
    page = request.args.get('page',1,type=int)
    posts = Post.query.order_by(Post.date_posted.desc()).paginate(per_page=2)
    return render_template("/index.html",posts=posts)


@main.route("/send", methods=['POST'])
def sends():
    text = request.form.get("txt_chat","nothing")
    return render_template('/send.html',text=text)


@main.route("/about")
def about():
    return render_template('/about.html')
