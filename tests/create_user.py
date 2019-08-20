from django.contrib.auth.models import User
user = User.objects.create_user('algomost', 'algomost@info.com', 'strong_password')
user.save()
