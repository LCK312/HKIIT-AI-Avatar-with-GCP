from datetime import datetime
from flask import render_template, flash, redirect, url_for, request, g
from flask_login import login_user, logout_user, current_user, login_required
from werkzeug.urls import url_parse
from flask_babel import _, get_locale
from app import app, db
from app.forms import LoginForm, RegistrationForm, EditProfileForm, PostForm, \
    ResetPasswordRequestForm, ResetPasswordForm, BookingForm
from app.models import User, Post, Booking ,Seat
from app.email import send_password_reset_email


@app.before_request
def before_request():
    if current_user.is_authenticated:
        current_user.last_seen = datetime.utcnow()
        db.session.commit()
    g.locale = str(get_locale())

@app.route('/', methods=['GET', 'POST'])
@app.route('/booking', methods=['GET', 'POST'])
def home():
    form = BookingForm()
    if form.validate_on_submit():
        booking = Booking(movie=form.movie.data, time=form.time.data, price=form.price.data)
        db.session.add(booking)
        db.session.commit()
        for row in range(1, 11):
            for number in range(1, 11):
                seat = Seat(row=row, number=number, booking=booking)
                db.session.add(seat)
        db.session.commit()
        flash('Booking created successfully!')
        return redirect(url_for('main_bp.index'))
    return render_template('firstpage.html.j2', form=form)


@app.route('/boad', methods=['GET', 'POST'])
def boad():
    return render_template('index.html.j2')

@app.route('/movie', methods=['GET', 'POST'])
def movie():
    return render_template('movie.html.j2')

@app.route('/payment', methods=['GET', 'POST'])
def payment():
    return render_template('payment.html.j2')

@app.route('/daymovie', methods=['GET', 'POST'])
def daymovie():
    return render_template('daymovie.html.j2')

@app.route('/seatingmap', methods=['GET', 'POST'])
def seatingmap():
    return render_template('seatingmap.html.j2')


@app.route('/reviews', methods=['GET', 'POST'])
def reviews():
    return render_template('reviews.html.j2')

@app.route('/reviewa', methods=['GET', 'POST'])
def reviewa():
    return render_template('reviewa.html.j2')


@app.route('/settlement', methods=['GET', 'POST'])
def settlement():
    return render_template('settlement.html.j2')

@app.route('/movie1')
def movie1():
    return render_template('機密特務：阿蓋爾.html.j2')

@app.route('/movie2')
def movie2():
    return render_template('愛愛愛上你.html.j2')

@app.route('/movie3')
def movie3():
    return render_template('外星+人2：回到未來.html.j2')

@app.route('/movie4')
def movie4():
    return render_template('可憐的東西.html.j2')

@app.route('/movie5')
def movie5():
    return render_template('天魔：惡之初.html.j2')

@app.route('/movie6')
def movie6():
    return render_template('蜘蛛夫人.html.j2')

@app.route('/movie7')
def movie7():
    return render_template('青春18×2 通往有你的旅程.html.j2')

@app.route('/movie8')
def movie8():
    return render_template('伏慄熊.html.j2')

@app.route('/movie9')
def movie9():
    return render_template('哥吉拉與金剛：新帝國.html.j2')

@app.route('/movie10')
def movie10():
    return render_template('沙丘：第二部.html.j2')

@app.route('/movie11')
def movie11():
    return render_template('毒舌大狀2023.html.j2')

@app.route('/movie12')
def movie12():
    return render_template('飯戲攻心.html.j2')


@app.route('/movie13')
def movie13():
    return render_template('avd.html.j2')


@app.route('/movie14')
def movie14():
    return render_template('灌籃高手.html.j2')

@app.route('/movie15')
def movie15():
    return render_template('鈴芽之旅.html.j2')

@app.route('/movie16')
def movie16():
    return render_template('捍衛任務4.html.j2')

@app.route('/movie17')
def movie17():
    return render_template('玩命關頭X.html.j2')

@app.route('/movie18')
def movie18():
    return render_template('變形金剛：萬獸崛起.html.j2')

@app.route('/movie19')
def movie19():
    return render_template('金手指.html.j2')

@app.route('/index', methods=['GET', 'POST'])
def index():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'index', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'index', page=posts.prev_num) if posts.prev_num else None
    return render_template('firstpage.html.j2', title=('home'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/explore')
@login_required
def explore():
    page = request.args.get('page', 1, type=int)
    posts = Post.query.order_by(Post.timestamp.desc()).paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'explore', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'explore', page=posts.prev_num) if posts.prev_num else None
    return render_template('firstpage.html.j2', title=_('Explore'),
                           posts=posts.items, next_url=next_url,
                           prev_url=prev_url)


@app.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user is None or not user.check_password(form.password.data):
            flash(_('Invalid username or password'))
            return redirect(url_for('login'))
        login_user(user, remember=form.remember_me.data)
        next_page = request.args.get('next')
        if not next_page or url_parse(next_page).netloc != '':
            next_page = url_for('index')
        return redirect(next_page)
    return render_template('login.html.j2', title=_('Sign In'), form=form)


@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))


@app.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = RegistrationForm()
    if form.validate_on_submit():
        user = User(username=form.username.data, email=form.email.data)
        user.set_password(form.password.data)
        db.session.add(user)
        db.session.commit()
        flash(_('Congratulations, you are now a registered user!'))
        return redirect(url_for('login'))
    return render_template('register.html.j2', title=_('Register'), form=form)


@app.route('/reset_password_request', methods=['GET', 'POST'])
def reset_password_request():
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    form = ResetPasswordRequestForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_password_reset_email(user)
        flash(
            _('Check your email for the instructions to reset your password'))
        return redirect(url_for('login'))
    return render_template('reset_password_request.html.j2',
                           title=_('Reset Password'), form=form)


@app.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_password(token):
    if current_user.is_authenticated:
        return redirect(url_for('index'))
    user = User.verify_reset_password_token(token)
    if user is None:
        return redirect(url_for('index'))
    form = ResetPasswordForm()
    if form.validate_on_submit():
        user.set_password(form.password.data)
        db.session.commit()
        flash(_('Your password has been reset.'))
        return redirect(url_for('login'))
    return render_template('reset_password.html.j2', form=form)


@app.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    page = request.args.get('page', 1, type=int)
    posts = user.followed_posts().paginate(
        page=page, per_page=app.config["POSTS_PER_PAGE"], error_out=False)
    next_url = url_for(
        'index', page=posts.next_num) if posts.next_num else None
    prev_url = url_for(
        'index', page=posts.prev_num) if posts.prev_num else None
    return render_template('user.html.j2', user=user, posts=posts.items,
                           next_url=next_url, prev_url=prev_url)


@app.route('/edit_profile', methods=['GET', 'POST'])
@login_required
def edit_profile():
    form = EditProfileForm(current_user.username)
    if form.validate_on_submit():
        current_user.username = form.username.data
        current_user.about_me = form.about_me.data
        db.session.commit()
        flash(_('Your changes have been saved.'))
        return redirect(url_for('edit_profile'))
    elif request.method == 'GET':
        form.username.data = current_user.username
        form.about_me.data = current_user.about_me
    return render_template('edit_profile.html.j2', title=_('Edit Profile'),
                           form=form)


@app.route('/follow/<username>')
@login_required
def follow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot follow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.follow(user)
    db.session.commit()
    flash(_('You are following %(username)s!', username=username))
    return redirect(url_for('user', username=username))


@app.route('/unfollow/<username>')
@login_required
def unfollow(username):
    user = User.query.filter_by(username=username).first()
    if user is None:
        flash(_('User %(username)s not found.', username=username))
        return redirect(url_for('index'))
    if user == current_user:
        flash(_('You cannot unfollow yourself!'))
        return redirect(url_for('user', username=username))
    current_user.unfollow(user)
    db.session.commit()
    flash(_('You are not following %(username)s.', username=username))
    return redirect(url_for('user', username=username))

@app.route('/booking/<int:booking_id>', methods=['GET', 'POST'])
def booking(booking_id):
    booking = Booking.query.get_or_404(booking_id)
    seats = Seat.query.filter_by(booking=booking).all()
    if request.method == 'POST':
        for seat in seats:
            if seat.booked:
                seat.booked = False
        for seat_id in request.form.getlist('seats'):
            seat = Seat.query.get(seat_id)
            seat.booked = True
        db.session.commit()
        flash('Seats booked successfully!')
        return redirect(url_for('main_bp.booking', booking_id=booking.id))
    return render_template('book.html.j2', booking=booking, seats=seats)





@app.route('/user/<username>')
@login_required
def profile(username):
    user = User.query.filter_by(username=username).first_or_404()
    posts = [
        {'author': user, 'body': 'Test post #1'},
        {'author': user, 'body': 'Test post #2'}
    ]
    return render_template('user.html.j2', user=user, posts=posts)
    
@app.route('/cinema')
def cinema_location():
    return render_template('Cinema Location.html.j2')

@app.route('/<region>/cinemas/<int:cinemasid>')
def cinemas(region, cinemasid):
    # Logic to retrieve cinema data based on cinemasid and region
    # ...

    # Render the template for the specified cinema and region
    template_path = 'Cinemas/{region}/cinemasid={cinemasid}.html.j2'.format(region=region, cinemasid=cinemasid)
    return render_template(template_path)


@app.route('/cinema-details', endpoint='cinema_details')
def cinema_details():
    address = '123 Main St, Hong Kong'
    phone = '123-456-7890'
    email = 'info@cinema.com.hk'
    website = 'https://www.cinema.com.hk'
    return render_template('Cinema Location.html.j2', address=address, phone=phone, email=email, website=website)

