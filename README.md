# Django Cloud Provider Regions

This [Django app](https://docs.djangoproject.com/en/5.0/ref/applications/) provides a static list of region and availability zones for AWS (Amazon Web Services) and GCP (Google Cloud Platform) cloud providers.

The purpose of this app is to provide Cloud Provider Region/AZ lists easily available to Django apps. It provides stable, shortened, versions of names for provisioning  naming conventions.

The Regions/AZ list is currrent as of March 2024.

## Features
- Quick and easy access to cloud Region and AZs from other Django apps
- Provides shortened versions of Region and AZ names for use by provisioning tools
- DB primary key fields are stable, will not change as new Regions/AZs are added

## Installation

`pip install django-cloud-provider-zones`

Add to project's settings.py INSTALLED_APPS:
```
'rest_framework',
'django_cloud_provider_zones',
```

Optionally, include the DRF REST urls in your project's `urls.py`:
```python
from django.contrib import admin
from django.urls import path, include
import django_cloud_provider_zones

urlpatterns = [
    path('admin/', admin.site.urls),
    path('api/cloudzones/', include('django_cloud_provider_zones.urls')),
]
```
Import model data

`./manage.py loaddata django_cloud_provider_zones-CloudProvider django_cloud_provider_zones-CloudRegion django_cloud_provider_zones-CloudAvailabilityZone`

If exposed via the Django admin, it is recommended that these App's models are "read only" so grant only View permissions.

### Models
[model diagram](https://github.com/yolabingo/django-cloud-provider-zones/blob/main/django_models.png)

This app provides the following models:
- `CloudProvider`: Cloud provider names - currently `AWS` or `GCP` 
- `CloudRegion`: Cloud regions
- `CloudAvailabilityZone`: Availability zones within a region

Each region and AZ provides, as properties, short name versions with dashes removed. For example, `AWS us-east-1` has names
```
short_name: use1
short_name_with_provider: awsuse1
```

```
## CloudProvider ##
>>> CloudProvider.objects.values().first()
{'provider': 'aws'}

## CloudRegion ##
>>> CloudRegion.objects.values().first()
{'cardinality': 'northeast',
 'created': datetime.date(2024, 3, 27),
 'geographic_region': 'ap',
 'id': 11,
 'number': '1',
 'original_region_name': 'ap-northeast-1',
 'provider_id': 'aws'}

>>> CloudRegion.objects.first().short_name
'apne1'
>>> CloudRegion.objects.first().short_name_with_provider
'awsapne1'

## CloudAvailabilityZone ##
>>> CloudAvailabilityZone.objects.values().first()
{'az': 'a', 'created': datetime.date(2024, 3, 27), 'id': 27, 'region_id': 11}

>>> CloudAvailabilityZone.objects.first().short_name
'apne1a'
>>> CloudAvailabilityZone.objects.first().short_name_with_provider
'awsapne1a'
```

### API Endpoints

Basic REST Get endpoints available see [urls.py](https://github.com/yolabingo/django-cloud-provider-zones/blob/main/src/django_cloud_provider_zones/urls.py)

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Django community and Django Software Foundation for Django
- Thanks to the maintainers of all dependencies on this project
- Thanks to Real Python for their [Installable Django App article](https://realpython.com/installable-django-app/)# django-cloud-provider-regions
