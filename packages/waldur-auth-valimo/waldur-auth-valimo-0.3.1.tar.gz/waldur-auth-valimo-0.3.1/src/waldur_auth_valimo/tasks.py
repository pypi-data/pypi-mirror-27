from datetime import timedelta
import logging

from celery import shared_task

from django.conf import settings
from django.contrib.auth import get_user_model
from django.utils import timezone
from rest_framework.authtoken.models import Token

from waldur_core.core import tasks

from . import client, models


logger = logging.getLogger(__name__)


class AuthTask(tasks.StateTransitionTask):
    """ Execute request for authentication """

    def execute(self, auth_result):
        response = client.SignatureRequest.execute(
            transaction_id=auth_result.uuid.hex,
            phone=auth_result.phone,
            message=auth_result.message)
        auth_result.backend_transaction_id = response.backend_transaction_id
        auth_result.save(update_fields=['backend_transaction_id'])


class PollTask(tasks.Task):
    max_retries = 25
    default_retry_delay = 12

    def execute(self, auth_result):
        response = client.StatusRequest.execute(
            transaction_id=auth_result.uuid.hex,
            backend_transaction_id=auth_result.backend_transaction_id)
        if response.status == client.Statuses.OK:
            self._associate_with_user(auth_result, response.civil_number)
        elif response.status == client.Statuses.PROCESSING:
            self.retry()
        elif response.status == client.Statuses.ERRED:
            auth_result.set_canceled()
            auth_result.details = response.details
            auth_result.save(update_fields=['state', 'details'])
            logger.info('PKI login failed for user with phone %s, details: %s.', auth_result.phone, auth_result.details)

    def _associate_with_user(self, auth_result, civil_number):
        User = get_user_model()
        try:
            user = User.objects.get(civil_number=civil_number)
            token, _ = Token.objects.get_or_create(user=user)
            lifetime = settings.WALDUR_CORE.get('TOKEN_LIFETIME', timezone.timedelta(hours=1))
            if token.created < timezone.now() - lifetime:
                token.delete()
                token = Token.objects.create(user=user)
            else:
                token.created = timezone.now()
                token.save()
            auth_result.user = user
            auth_result.set_ok()
            logger.info('PKI login was successfully done for user %s.', user.username)
        except User.DoesNotExist:
            auth_result.details = 'User is not registered.'
            auth_result.set_canceled()
            logger.info('PKI login failed for user with civil number %s - user record does not exist in Waldur.', civil_number)
        auth_result.save()


@shared_task(name='waldur_auth_valimo.cleanup_auth_results')
def cleanup_auth_results():
    models.AuthResult.objects.filter(modified__lte=timezone.now() - timedelta(days=7)).delete()
