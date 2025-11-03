import uuid
from flask import Flask, request, render_template, url_for

app = Flask(__name__)

# This is still our simple, temporary in-memory "database".
secrets_storage = {}

@app.route('/')
def home():
    """Display the homepage with the form to create a secret."""
    return render_template('index.html')


@app.route('/create', methods=['POST'])
def create_secret():
    """Create a new secret, store it, and show the unique link."""
    secret = request.form.get('secret')
    if not secret:
        return "You must provide a secret.", 400

    token = str(uuid.uuid4())
    secrets_storage[token] = secret
    
    # _external=True makes it a full URL (e.g., http://...)
    link = url_for('view_secret', token=token, _external=True)

    # Show the link page
    return render_template('show_link.html', link=link)


@app.route('/secret/<token>')
def view_secret(token):
    """
    Retrieve the secret *one time* and pass it to the view template.
    The .pop() method gets the value AND deletes it in one step.
    """
    secret = secrets_storage.pop(token, None)

    if secret:
        # The secret existed. Show it.
        return render_template('view_secret.html', secret=secret)
    else:
        # The secret was not found (already viewed or invalid).
        return render_template('not_found.html'), 404


if __name__ == '__main__':
    # Run on 0.0.0.0 to be accessible from your network
    # on port 5004.
    app.run(debug=True, host='0.0.0.0', port=5004)