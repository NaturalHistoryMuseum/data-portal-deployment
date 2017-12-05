# data-portal-deployment

### Deployment tool for the Data Portal. 

### Overview

Script loops through all repositories defined in config - `default.cfg:main.directory`. 

If the repository is a CKAN plugin owned by the Natural History Museum organisation, the script pulls either the latest master (for staging / development) or latest release (for production).

### CLI

To update all repositories to latest commit on master branch:

```bash
deploy master
```

To update all repositories to latest tagged release:

```bash
deploy release
```

Note: Repositories without a tagged release are not updated.

To update a particular repository only:

```bash
deploy -n ckanext-nhm master
```


### Automation

On staging `deploy master` is run on cron every 5 minutes. If source code changes are detected, Apache WSGI will be restarted so all updates merged into master are automatically deployed onto staging.

On production `deploy release` and Apache WSGI will need to be manually run. 