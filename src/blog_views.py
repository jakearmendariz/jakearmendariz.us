# chat_views
from app import app, mongo
from src.config import *
from src.basic_views import *

@app.route('/blog/post/<string:id>',methods=['GET'])
def blog_post(id):
    post = mongo.db.blog.find_one_or_404({'id':id})
    print('post in blog_post():', post['title'])
    return render_template('/blog/blog-post.html', post = post)


@app.route('/blog/edit/<string:id>',methods=['GET', 'POST'])
def edit(id):
    if 'admin' not in session:
        print("NOT AN ADMIN USER. REDIRECT")
        return render_template('error_pages/404.html')
    else:
        print(session['admin'])
    if request.method == 'POST':
        return newBlog()
    post = mongo.db.blog.find_one_or_404({'id':id}).copy()
    print('editing post:', post['id'])
    return render_template('/blog/new-post.html', post = post, editing = True, admin = session['admin'])

@app.route('/blog/<string:page_name>',methods=['GET'])
def blog_pages(page_name):
    return render_template('/blog/post/%s.html' % page_name)
    
@app.route('/blog/new-post',methods=['POST'])
def newBlog():
    if 'admin' not in session:
        print("NOT AN ADMIN USER. REDIRECT")
        return render_template('error_pages/404.html')
    if 'id' in request.form: #This means the post has already been created and is being updated
        print("updating exisiting blog post")
        post = mongo.db.blog.find_one({'id':request.form['id']}).copy()
        post['title'] = request.form['title']
        post['image'] = request.form['image']
        post['body'] = request.form['body']
        post['reading_time'] = request.form['reading_time']
        post['description'] =  request.form['description']
        mongo.db.blog.update_one(
            {'id': post['id']}, {"$set": post})
    else:
        print("new blog post")
        post = {}
        post['title'] = request.form['title']
        post['image'] = request.form['image']
        post['body'] = request.form['body']
        print("1")
        post['reading_time'] = request.form['reading_time']
        print("2")
        post['id'] = str(''.join((random.choice(string.digits) for i in range(8))))
        post['date'] = datetime.now().strftime("%m/%d/%Y")
        post['description'] =  request.form['description']
        print("3")
        post['time'] = time.time()
        print('created post', post['title'])
        print("4")
        mongo.db.blog.insert_one(post)
        print("5")
    return redirect(url_for('blog_post', id=post['id']))

@app.route('/blog/new-post',methods=['GET'])
def accessNewBlog():
    # admin_only()
    return render_template('/blog/new-post.html', editing = False)

@app.route('/blog/',methods=['GET'])
@app.route('/blog/index',methods=['GET'])
def blog_list():
    posts = cursorToArray(mongo.db.blog.find())
    posts.reverse()
    return render_template('/blog/index.html', posts = posts)

def cursorToArray(cursor):
    array = []
    for item in cursor:
        array.append(item)
    return array
