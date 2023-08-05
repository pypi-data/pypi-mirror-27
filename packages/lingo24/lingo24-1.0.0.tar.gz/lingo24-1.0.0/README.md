Lingo24 Client
===============

This client library provides access to the Lingo24 translation *Business
Documents* API.


## Installation

```bash
$ pip install lingo24
```


## Usage

### Authentication

To connect to the API, an **Authenticator** needs to be created. This requires
your client ID and secret, along with a URL on your site to which the user is to
be redirected after being successfully authenticated by Lingo24.

```python
>>> from lingo24.business_documents import Authenticator
>>> authenticator = Authenticator('client-id', 'client-secret', 'https://www.example.com/callback')
```

> **IMPORTANT NOTE**<br>
> By default, the **live** API will be used. The **demo** API can be accessed by
> passing `endpoint='demo'` as a keyword argument when instantiating the
> Authenticator.

The first step is to obtain the Lingo 24 authorization URL:
```python
>>> authenticator.authorization_url
'https://ease.lingo24.com/oauth/authorize?redirect_uri=https%3A%2F%2Fwww.example.com%2Fcallback&response_type=code&client_id=client-id'
```

Upon visiting this Lingo24 URL, you will be prompted to login and authorize
access. You'll then be redirected back to the URL provided earlier, along with
an authorization code; for example:

> https://www.example.com/callback?code=XXXXXXXXXX

This code should then be passed to the authenticator's `request_access_token`
method:
```python
>>> authenticator.request_access_token('XXXXXXXXXX')
```

A **Client** for accessing the API can then be created that uses the
authenticator:
```python
>>> from lingo24.business_documents import Client
>>> client = Client(authenticator)
```

> **IMPORTANT NOTE**<br>
> By default, the **live** API will be used. The **demo** API can be accessed by
> passing `endpoint='demo'` as a keyword argument when instantiating the Client.

#### AuthenticationStore

By default, an Authenticator stores its credential data in memory.

The Authenticator's constructor takes an optional `store` keyword argument that
allows you to provide a custom class for storing and retrieving the credential
data. A custom store must simply implement `get` and `set` methods.

The following is an example of a store that persists its data to disk.

```python
>>> import json
>>> class FileAuthenticationStore(AuthenticationStore):
...     def __init__(self, filename):
...         self.filename = filename
...     def get(self):
...         with open(self.filename, 'rb') as f:
...             return json.load(f)
...     def set(self, value):
...         with open(self.filename, 'wb') as f:
...             return json.dump(value, f)
...
>>> store = FileAuthenticationStore('/tmp/lingo24.auth')
>>> authenticator = Authenticator('client-id', 'client-secret', 'https://www.example.com/callback', store=store)
```

> **IMPORTANT NOTE**<br>
> FileAuthenticationStore is for illustrative purposes only. Storing
> authentication credentials in unprotected files is probably not a good idea.


### Example workflow
A **Project** can be created as follows. By specifying the **Domain**, Lingo24
can assign the translation task to the most appropriate translators (i.e. those
with experience/expertise in the chosen topic).
```python
>>> sport = client.domains.find(name='Sport')
>>> project = client.projects.create('My project', sport)
```

To order translations, a source **File** first needs to be created:
```python
>>> source_file = client.files.create('Test.txt')
>>> source_file.content = 'Hello world'
```

> **IMPORTANT NOTE**<br>
> The filename extension is important as it is used by Lingo24 to determine the
> filetype. Only supported filetypes can be translated without manual
> intervention.

A project comprises one or more **Jobs**. The following creates a job within the
*My project* project to translate the *Test.txt* file from **British English**
to **French** using the **First Draft** service level:

```python
>>> en_gb = client.locales.find(language='en', country='GB')
>>> fr_fr = client.locales.find(language='fr', country='FR')
>>> first_draft = client.services.find(name='First Draft')
>>> job = project.jobs.create(first_draft, en_gb, source_file, fr_fr)
```

Further files and jobs can be added to the project if needed.

Once all jobs have been added, a quote can be requested. This transitions the
project into the *PENDING* state:

```python
>>> project.request_quote()
>>> project.status
'PENDING'
```

Once the quote is ready, the project's status will change to *QUOTED*:

```python
>>> project.refresh()
>>> project.status
'QUOTED'
```

The project's jobs will also now have a status of *QUOTED* and will have pricing
and metrics available:

```python
>>> job = project.jobs[0]
>>> job.status
'QUOTED'
>>> job.price
<TotalPrice: Without discount <Price GBP 123.45 net / 678.90 gross> | With discount <Price GBP 123.45 net / 678.90 gross>>
>>> import pprint
>>> pprint.pprint(job.metrics)
{'FUZZY_MATCH_75_84': <Metric: White spaces 0 | Segments 0 | Words 0 | Characters 0>,
 'FUZZY_MATCH_85_94': <Metric: White spaces 0 | Segments 0 | Words 0 | Characters 0>,
 'FUZZY_MATCH_95_99': <Metric: White spaces 0 | Segments 0 | Words 0 | Characters 0>,
 'IN_CONTEXT_EXACT_MATCH': <Metric: White spaces 0 | Segments 0 | Words 0 | Characters 0>,
 'LEVERAGED_MATCH': <Metric: White spaces 0 | Segments 0 | Words 0 | Characters 0>,
 'NON_TRANSLATABLE': <Metric: White spaces 0 | Segments 0 | Words 0 | Characters 0>,
 'NO_MATCH': <Metric: White spaces 1 | Segments 1 | Words 2 | Characters 11>,
 'REPETITION_100': <Metric: White spaces 0 | Segments 0 | Words 0 | Characters 0>,
 'REPETITION_75_84': <Metric: White spaces 0 | Segments 0 | Words 0 | Characters 0>,
 'REPETITION_85_94': <Metric: White spaces 0 | Segments 0 | Words 0 | Characters 0>,
 'REPETITION_95_99': <Metric: White spaces 0 | Segments 0 | Words 0 | Characters 0>,
 'REPETITION_ICE': <Metric: White spaces 0 | Segments 0 | Words 0 | Characters 0>,
 'TOTAL': <Metric: White spaces 1 | Segments 1 | Words 2 | Characters 11>}
```

If everything looks OK, the quote can be accepted:

```python
>>> project.accept_quote()
>>> project.status
'IN_PROGRESS'
```

The project's status will remain *IN_PROGRESS* until all its jobs have been
translated, at which point its status will become *FINISHED*:

```python
>>> project.refresh()
>>> project.status
'FINISHED'
```

The project's jobs will also now have a status of *TRANSLATED* and will have a
target file that contains the translation:

```python
>>> job = project.jobs[0]
>>> job.status
'TRANSLATED'
>>> job.target_file.name
'Test-fr_FR.txt'
>>> job.target_file.content
'Bonjour le monde'
```


### Collections

The API client has a number of *collections* of data

Collection        | Iterable | sort() | filter()  | find()   | get()  | create() | add() | remove()
----------------- | -------- | ------ | --------- | -------  | ------ | -------- | ----- | --------
`client.domains`  | ✓        | ✓      | ✓         | ✓        | ✓      | ✗        | ✗     | ✗
`client.locales`  | ✓        | ✓      | ✓         | ✓        | ✓      | ✗        | ✗     | ✗
`client.files`    | ✗        | ✗      | ✗         | ✗        | ✓      | ✓        | ✗     | ✗
`client.projects` | ✓        | ✓      | ✓         | ✓        | ✓      | ✓        | ✗     | ✗
`client.services` | ✓        | ✓      | ✓         | ✓        | ✓      | ✗        | ✗     | ✗
`job.files`       | ✓        | ✓      | ✓         | ✓        | ✓      | ✗        | ✓     | ✓
`project.charges` | ✓        | ✗      | ✗         | ✗        | ✗      | ✗        | ✗     | ✗
`project.files`   | ✓        | ✓      | ✓         | ✓        | ✓      | ✗        | ✓     | ✓
`project.jobs`    | ✓        | ✓      | ✓         | ✓        | ✓      | ✓        | ✗     | ✗


#### Iteration
Iterable collections can be looped through as follows:
```python
>>> for locale in client.locales:
...     print(locale)
...
<Locale 102: Abkhazian>
<Locale 103: Afar>
<Locale 104: Afrikaans>
<Locale 2: Akan>
<Locale 105: Amharic>
⋮
```

They can also be indexed or sliced:
```python
>>> client.locales[20]
<Locale 59: Chinese (Simplified)>
>>> for locale in client.locales[6:10]:
...     print(locale)
...
<Locale 209: Armenian>
<Locale 106: Assamese>
<Locale 107: Aymara>
<Locale 109: Bashkir>
```

#### .sort(*attribute*)
Sortable collections can be sorted by a particular attribute before iterating:
```python
>>> for locale in client.locales.sort('id'):
...     print(locale)
...
<Locale 2: Akan>
<Locale 3: Catalan (Andorra)>
<Locale 5: Estonian>
<Locale 10: Kannada>
<Locale 11: Kinyarwanda>
⋮
```

Again, collections can also be indexed or sliced once sorted:
```python
>>> client.locales.sort('id')[20]
<Locale 33: Oromo>
>>> for locale in client.locales.sorted('id')[6:10]:
...     print(locale)
...
<Locale 15: Latvian>
<Locale 16: Lingala>
<Locale 17: Lithuanian>
<Locale 18: Macedonian>
```

#### .filter(\*\**criteria*)
If supported, a collection can be filtered by one or more values before
iterating:
```python
>>> for locale in client.locales.filter(language='en'):
...     print(locale)
...
<Locale 213: English (Australia)>
<Locale 178: English (Canada)>
<Locale 215: English (Hong Kong)>
<Locale 191: English (India)>
<Locale 217: English (Ireland)>
⋮
```

#### .find(\*\**criteria*)
If supported, the first matching item in a collection can be found:
```python
>>> client.locales.find(language='en')
<Locale 213: English (Australia)>
```

If no matching item can be found, a `DoesNotExist` error will be raised.

#### .get(*id*)
A specific item can be fetched from a collection by its ID:
```python
>>> client.locales.get(97)
<Locale 97: English (UK)>
```

If no matching item can be found, a `DoesNotExist` error will be raised.

#### .create(\*\**values*)
Some collections allow new items to be created:
```python
>>> client.projects.create('My project')
<Project 123: My project>
```

#### .add(*item* or *id*) / .remove(*item* or *id*)
Some collections allow items to be added or removed:
```python
>>> my_file = project.files.get(123)
>>> project.files.add(my_file)
>>> project.files.remove(my_file)
```
