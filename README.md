# Django Cloud Provider Regions

This [Django app](https://docs.djangoproject.com/en/5.0/ref/applications/) provides a static list of region and availability zones for AWS (Amazon Web Services) and GCP (Google Cloud Platform) cloud providers.

The purpose of this app is to provide Cloud Provider Region/AZ lists easily available to Django apps. It provides stable, shortened, versions of names for provisioning  naming conventions.

The Regions/AZ list is currrent as of March 2024.

## Features
- Quick and easy access to cloud Region and AZs from other Django apps
- Provides shortened versions of Region and AZ names for use by provisioning tools
- DB primary key fields are stable, will not change as new Regions/AZs are added

## Installation


### Models

This app provides the following models:

- `CloudProvider`: Cloud provider names - currently `AWS` or `GCP` 
- `Region`: Cloud regions
- `AvailabilityZone`: Availability zones within a region

### API Endpoints

TODO: add DRF views 
The following API endpoints are available:

- `GET /api/regions/`: Retrieve a list of all regions.
- `GET /api/regions/<region_id>/`: Retrieve details of a specific region.

## Contributing

Contributions are welcome! Please feel free to open issues or submit pull requests.

## License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## Acknowledgments

- Thanks to the Django community and Django Software Foundation for Django
- Thanks to the maintainers of all dependencies on this project
- Thanks to Real Python for their [Installable Django App article](https://realpython.com/installable-django-app/)# django-cloud-provider-regions
