from flask import render_template, redirect, url_for, flash, request, current_app
from flask_login import login_user, logout_user, login_required, current_user
from werkzeug.security import generate_password_hash, check_password_hash
from app.auth import auth_bp
from app.auth.forms import LoginForm, RegistrationForm, RequestResetForm, ResetPasswordForm, ChangePasswordForm
from app.models import User
from app.extensions import db
# For email sending (NEW)
from flask_mail import Message
from app.extensions import mail # Assuming 'mail' is also initialized in app/extensions.py

@auth_bp.route('/login', methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:
        flash('You are already logged in.', 'info') # Inform user if already logged in
        return redirect(url_for('dashboard.index'))

    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        # Use check_password_hash from werkzeug.security instead of user.check_password if User model doesn't have it
        if user and check_password_hash(user.password_hash, form.password.data):
            login_user(user, remember=form.remember.data) # Pass remember me value
            next_page = request.args.get('next')
            flash('Logged in successfully!', 'success')
            return redirect(next_page or url_for('dashboard.index'))
        else:
            flash('Login Unsuccessful. Please check email and password', 'danger')
    return render_template('auth/login.html', title='Login', form=form)

@auth_bp.route('/register', methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:
        flash('You are already registered and logged in.', 'info')
        return redirect(url_for('dashboard.index'))

    form = RegistrationForm()
    if form.validate_on_submit():
        # The custom validators in RegistrationForm now handle email/username existence checks
        # So we can proceed directly if validate_on_submit() passes.
        hashed_password = generate_password_hash(form.password.data)
        new_user = User(
            username=form.username.data,
            email=form.email.data,
            password_hash=hashed_password
        )
        db.session.add(new_user)
        db.session.commit()
        flash('Your account has been created! You can now log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/register.html', title='Register', form=form)

@auth_bp.route('/logout')
@login_required
def logout():
    logout_user()
    flash('You have been logged out.', 'info')
    return redirect(url_for('auth.login'))

# Helper function to send password reset email (NEW)
def send_reset_email(user):
    token = user.get_reset_token() # This method needs to be added to your User model
    msg = Message('Password Reset Request',
                  sender='noreply@yourdomain.com', # Replace with your actual sender email
                  recipients=[user.email])
    msg.body = f'''To reset your password, visit the following link:
{url_for('auth.reset_token', token=token, _external=True)}

If you did not make this request then simply ignore this email and no changes will be made.
'''
    mail.send(msg)


# NEW: Route to request password reset
@auth_bp.route('/reset_password', methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        if user:
            send_reset_email(user)
            flash('An email has been sent with instructions to reset your password.', 'info')
        else:
            # Avoid telling an attacker if an email doesn't exist for security reasons,
            # just show a generic message. The form's validate_email already handles the specific message.
            flash('If an account with that email exists, a password reset email has been sent.', 'info')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_request.html', title='Reset Password', form=form)

# NEW: Route to handle password reset with token
@auth_bp.route('/reset_password/<token>', methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:
        return redirect(url_for('dashboard.index'))
    user = User.verify_reset_token(token) # This method needs to be added to your User model
    if not user:
        flash('That is an invalid or expired token.', 'danger')
        return redirect(url_for('auth.reset_request'))

    form = ResetPasswordForm()
    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data)
        user.password_hash = hashed_password
        db.session.commit()
        flash('Your password has been updated! You are now able to log in.', 'success')
        return redirect(url_for('auth.login'))
    return render_template('auth/reset_token.html', title='Reset Password', form=form)

# NEW: Route for logged-in users to change their password
@auth_bp.route('/change_password', methods=['GET', 'POST'])
@login_required
def change_password():
    form = ChangePasswordForm()
    if form.validate_on_submit():
        if check_password_hash(current_user.password_hash, form.current_password.data):
            if form.new_password.data == form.current_password.data:
                flash('New password cannot be the same as the current password.', 'warning')
            else:
                current_user.password_hash = generate_password_hash(form.new_password.data)
                db.session.commit()
                flash('Your password has been changed successfully.', 'success')
                return redirect(url_for('dashboard.index')) # Redirect to dashboard after success
        else:
            flash('Incorrect current password.', 'danger')
    return render_template('auth/change_password.html', title='Change Password', form=form)