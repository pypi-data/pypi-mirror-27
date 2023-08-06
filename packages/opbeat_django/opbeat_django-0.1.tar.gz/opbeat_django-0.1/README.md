## Opbeat-Django

A very simple API wrapper for Opbeat. Although created with Django in mind,
could be used as a plain python library.

Main goal for creating this, however, is `opbeat_release` management command.
It handles release notifications and unlike the official curl snippet behaves
nicely if Django is required for getting access settings (e.g. a complicated
docker secrets + django-environ setup).

Created mainly for internal use but feedback and contributions are always
welcome (as long as breaking core functionality is not requested).

As far as this library is concerned, nothing existed before Python 3.5 and
Django 1.8. No contributions or requests for compatibility code will be
considered. It's 2017, guys, we'll have new ways to clutter our code soon
enough :)

There is this feeling that this code might have a better life in
`opbeat.contrib.django` but preparing a proper contribution takes time and
effort and getting it accepted is a whole other matter so it might never
actually get there.

### Usage

Install with `pip` or whatever is you preferred method:

```
pip install opbeat_django
```

Add to `INSTALLED_APPS` if using with Django:

```
# settings.py
INSTALLED_APPS = [
    ...
    'opbeat_django',
    ...
]
```

That's it. Assuming, you already have official Opbeat client installed and
Django configured there's nothing else to do, management command is available,
enjoy.

In case didn't do it yet or something is no compatible, there are four ways to
configure access parameters:

#### Django settings (namespaced Opbeat-style)

```
# settings.py
OPBEAT = {
    'ORGANIZATION_ID': '<YOUR ORG ID>',
    'APP_ID': '<YOUR APP ID>',
    'SECRET_TOKEN': '<YOUR TOKEN>',
}
```
#### Django settings (env variables-style)

```
# settings.py
OPBEAT_ORGANIZATION_ID = '<YOUR ORG ID>'
OPBEAT_APP_ID = '<YOUR APP ID>'
OPBEAT_SECRET_TOKEN = '<YOUR TOKEN>'
```

#### Environment variables

```
OPBEAT_ORGANIZATION_ID=<YOUR ORG ID>
OPBEAT_APP_ID=<YOUR APP ID>
OPBEAT_SECRET_TOKEN=<YOUR TOKEN>
```

#### API wrapper kwargs

```
client = OpbeatAPI(
    org_id='<YOUR ORG ID>',
    app_id='<YOUR APP ID>',
    token='<YOUR TOKEN>',
)
```

#### `opbeat_release` command's arguments

```
manage.py opbeat_release -o <YOUR ORG ID> -a <YOUR APP ID> -t <YOUR TOKEN> -r <commit_hash>
```

or

```
manage.py opbeat_release \
    --organization-id=<YOUR ORG ID> --app-id=<YOUR APP ID> \
    --token=<YOUR TOKEN> --revision=<commit_hash>
```

it has a few optional arguments as well:

```
manage.py opbeat_release -r <commit_hash> -b <branch_name> -m <hostname_or_other_node_id>
```

the only required one is `--revision` but it and others can be provided by
environment variables:

```
RELEASE_HASH=<commit_hash>
RELEASE_BRANCH=<branch_name>
RELEASE_MACHINE=<hostname_or_other_node_id>
```

new variable names will probably be added later for compatibility with other
things. We'll try not to remove them unless there are some big time conflicts.
Command-line arguments always have precedence, in case of any doubt.

Created by [Ivan Anishchuk](https://IvanAnishchuk.com) for
[Netquity Corporation](https://netquity.com), by the way.
