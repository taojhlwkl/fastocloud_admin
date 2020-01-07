from flask_classy import FlaskView, route
from flask import render_template, request, jsonify
from flask_login import login_required

from app.common.subscriber.forms import SignupForm
from pyfastocloud_models.subscriber.entry import Subscriber
from pyfastocloud_models.service.entry import ServiceSettings


# routes
class SubscriberView(FlaskView):
    route_base = "/subscriber/"

    @login_required
    def show(self):
        return render_template('subscriber/show.html', subscribers=Subscriber.objects())

    @login_required
    @route('/add', methods=['GET', 'POST'])
    def add(self):
        form = SignupForm()
        if request.method == 'POST' and form.validate_on_submit():
            new_entry = form.make_entry()
            servers = ServiceSettings.objects()
            for server in servers:
                new_entry.add_server(server)
            new_entry.save()
            return jsonify(status='ok'), 200

        return render_template('subscriber/add.html', form=form)

    @login_required
    @route('/edit/<sid>', methods=['GET', 'POST'])
    def edit(self, sid):
        subscriber = Subscriber.objects(id=sid).first()
        form = SignupForm(obj=subscriber)
        if request.method == 'POST' and form.validate_on_submit():
            subscriber = form.update_entry(subscriber)
            subscriber.save()
            return jsonify(status='ok'), 200

        return render_template('subscriber/edit.html', form=form)

    @login_required
    @route('/remove', methods=['POST'])
    def remove(self):
        data = request.get_json()
        sid = data['sid']
        subscriber = Subscriber.objects(id=sid).first()
        if subscriber:
            subscriber.delete()
            return jsonify(status='ok'), 200

        return jsonify(status='failed'), 404
