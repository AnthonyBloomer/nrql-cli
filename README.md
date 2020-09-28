# nrql-cli

An interactive command line interface for querying New Relic Insights event data.

https://discuss.newrelic.com/t/try-this-tool-an-interactive-command-line-interface-for-querying-insights-event-data/79425

[![asciicast](https://asciinema.org/a/271697.svg)](https://asciinema.org/a/271697)

## About

The New Relic Insights query API is a REST API for querying Insights event data. After you supply a standard NRQL query via HTTPS request, the query API returns a JSON response for parsing.

To use the API, you need a query key. You can have multiple query keys, and any query key can be used to initiate any Insights API query. If you have multiple systems querying Insights or different data destinations, New Relic recommends you use multiple query keys to enhance data security.

To create a new query key:

1. Go to [insights.newrelic.com](https://insights.newrelic.com) > Manage data > API keys.
2. Select the plus icon next to the Query keys heading.
3. Enter a short description of the key.
4. Select Save your notes.

You will also need make note of your New Relic Account ID. To find the account ID for your New Relic account:

1. Sign in to [rpm.newrelic.com](https://rpm.newrelic.com).
2. In the URL bar, copy the number after the /accounts/ portion of the URL: `https://rpm.newrelic.com/accounts/ACCOUNT_ID/`

## Installation

nrql-cli is available on the Python Package Index (PyPI) at https://pypi.python.org/pypi/nrql-cli

You can install nrql-cli using pip.

```
pip install nrql-cli
```

Export your [Query API key](https://docs.newrelic.com/docs/apis/get-started/intro-apis/understand-new-relic-api-keys) and [Account ID](https://docs.newrelic.com/docs/accounts/install-new-relic/account-setup/account-id) as environment variables:

```shell
export NR_API_KEY='YOUR_API_KEY'
export NR_ACCOUNT_ID='YOUR_ACCOUNT_ID'
```

Then, run:

```
nrql
```

This command will start the program and you can start querying your data!


Alternatively, you can run in Docker. You will need to update the [Dockerfile](https://github.com/AnthonyBloomer/nrql-cli/blob/master/Dockerfile) with your API key and account id and then run:

```shell
docker build -f Dockerfile -t nrql-cli .
docker run --rm -it nrql-cli
```

## Usage

```
usage: nrql [-h] [--region {EU,US}] [--env ENV] [--verbose]

optional arguments:
  -h, --help            show this help message and exit
  --region {EU,US}, --r {EU,US}
                        Pass this flag to set your region (EU or US) By
                        default the region is set to US.
  --env ENV, --e ENV    Environment handler.
  --verbose, --v        Pass this flag if you want the whole response.
```

## Managing multiple accounts

If you wish to easily switch between your New Relic accounts, you can use the `--env` switch:

``` bash
nrql --env PROD
```

By default, the program looks for the environment variables `NR_API_KEY` and `NR_ACCOUNT_KEY`. 

If the `env` argument is not none, then the program appends the environment string to `NR_API_KEY`. For example:

```
NR_API_KEY_PROD
```

When naming your environment variables, ensure to follow this naming convention.

## Support

Please note that this is offered for use as-is without warranty. You are free to use and modify as needed. It has been created for use with New Relic, but is not a supported product of New Relic
