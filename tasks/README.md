`django_management_commands` - run with `-h` - wraps several Django manage.py commands

## Updating Region/AZ data
### Update AWS json data files
`tasks/aws_update_regions_json` - fetch aws regions with boto3 and save to `../region_data/` json files

### Update GCP json data files
1. Save output of `gcloud compute regions list --format json --project <project>` to `region_data/unparsed_gcloud_output.json`
2.  `tasks/gcp_update_regions_json`


### Save update json data to Django db fixture
1. Run `tasks/django_management_commands django_update_fixture_from_json`
2. Run `tasks/django_management_commands django_test`
3. `poetry version patch`


TODO: add `invoke`