from rest_framework.viewsets import ModelViewSet
from django.core.cache import cache
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver, Signal
from rest_framework.response import Response
import logging

from apps.companies.models import Company
from apps.companies.serializers import CompanySerializer

# Set up logger
logger = logging.getLogger(__name__)

# Define signals
list_request_started = Signal()
list_data_fetched = Signal()
retrieve_request_started = Signal()
retrieve_data_fetched = Signal()

# Cache keys
COMPANIES_LIST_CACHE_KEY = 'companies_list'
COMPANY_DETAIL_CACHE_KEY_PREFIX = 'company_detail_'

# Cache timeout (1 hour)
CACHE_TTL = 60 * 60


class CompanyViewSet(ModelViewSet):
    queryset = Company.objects.all()
    serializer_class = CompanySerializer
    http_method_names = ['get', 'head']  # Only allowing GET and HEAD methods

    def get_company_cache_key(self, pk):
        """Generate cache key for a specific company"""
        return f"{COMPANY_DETAIL_CACHE_KEY_PREFIX}{pk}"

    def list(self, request, *args, **kwargs):
        """
        Override list method to implement caching with signals.
        First request fetches from database, subsequent requests use Redis cache.
        """
        # Signal that a list request is starting
        list_request_started.send(sender=self.__class__)
        logger.info("Company list request started")

        # Try to get data from cache first
        cached_data = cache.get(COMPANIES_LIST_CACHE_KEY)

        if cached_data is None:
            # Cache miss - fetch from database
            response = super().list(request, *args, **kwargs)

            # Store in cache for future requests
            cache.set(COMPANIES_LIST_CACHE_KEY, response.data, CACHE_TTL)

            # Signal that data was fetched from database
            list_data_fetched.send(sender=self.__class__, from_cache=False)
            logger.info("Company list fetched from database and cached")

            return response
        else:
            # Cache hit - use cached data
            # Signal that data was fetched from cache
            list_data_fetched.send(sender=self.__class__, from_cache=True)
            logger.info("Company list fetched from Redis cache")

            return Response(cached_data)

    def retrieve(self, request, *args, **kwargs):
        """
        Override retrieve to implement caching with signals.
        """
        company_id = kwargs.get('pk')
        cache_key = self.get_company_cache_key(company_id)

        # Signal that a retrieve request is starting
        retrieve_request_started.send(sender=self.__class__, company_id=company_id)
        logger.info(f"Company retrieve request started for ID: {company_id}")

        # Try to get from cache
        cached_company = cache.get(cache_key)

        if cached_company is None:
            # If not in cache, use the standard retrieve method
            response = super().retrieve(request, *args, **kwargs)

            # Cache the result
            cache.set(cache_key, response.data, CACHE_TTL)

            # Signal that data was fetched from database
            retrieve_data_fetched.send(sender=self.__class__, company_id=company_id, from_cache=False)
            logger.info(f"Company ID {company_id} fetched from database and cached")

            return response
        else:
            # Use cached data
            # Signal that data was fetched from cache
            retrieve_data_fetched.send(sender=self.__class__, company_id=company_id, from_cache=True)
            logger.info(f"Company ID {company_id} fetched from Redis cache")

            return Response(cached_company)


# Signal handlers for cache invalidation
@receiver(post_save, sender=Company)
def handle_company_save(sender, instance, created, **kwargs):
    """Signal handler to invalidate cache when a company is saved"""
    # Invalidate the specific company cache
    cache_key = f"{COMPANY_DETAIL_CACHE_KEY_PREFIX}{instance.id}"
    cache.delete(cache_key)

    # Invalidate the companies list cache
    cache.delete(COMPANIES_LIST_CACHE_KEY)

    action = "created" if created else "updated"
    logger.info(f"Signal: Company ID {instance.id} {action}, cache invalidated")


@receiver(post_delete, sender=Company)
def handle_company_delete(sender, instance, **kwargs):
    """Signal handler to invalidate cache when a company is deleted"""
    # Invalidate the specific company cache
    cache_key = f"{COMPANY_DETAIL_CACHE_KEY_PREFIX}{instance.id}"
    cache.delete(cache_key)

    # Invalidate the companies list cache
    cache.delete(COMPANIES_LIST_CACHE_KEY)

    logger.info(f"Signal: Company ID {instance.id} deleted, cache invalidated")
