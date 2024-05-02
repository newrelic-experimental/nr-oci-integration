<a href="https://opensource.newrelic.com/oss-category/#new-relic-experimental"><picture><source media="(prefers-color-scheme: dark)" srcset="https://github.com/newrelic/opensource-website/raw/main/src/images/categories/dark/Experimental.png"><source media="(prefers-color-scheme: light)" srcset="https://github.com/newrelic/opensource-website/raw/main/src/images/categories/Experimental.png"><img alt="New Relic Open Source experimental project banner." src="https://github.com/newrelic/opensource-website/raw/main/src/images/categories/Experimental.png"></picture></a>

# New Relic OCI Integration
![GitHub forks](https://img.shields.io/github/forks/newrelic-experimental/newrelic-experimental-FIT-template?style=social)
![GitHub stars](https://img.shields.io/github/stars/newrelic-experimental/newrelic-experimental-FIT-template?style=social)
![GitHub watchers](https://img.shields.io/github/watchers/newrelic-experimental/newrelic-experimental-FIT-template?style=social)

![GitHub all releases](https://img.shields.io/github/downloads/newrelic-experimental/newrelic-experimental-FIT-template/total)
![GitHub release (latest by date)](https://img.shields.io/github/v/release/newrelic-experimental/newrelic-experimental-FIT-template)
![GitHub last commit](https://img.shields.io/github/last-commit/newrelic-experimental/newrelic-experimental-FIT-template)
![GitHub Release Date](https://img.shields.io/github/release-date/newrelic-experimental/newrelic-experimental-FIT-template)


![GitHub issues](https://img.shields.io/github/issues/newrelic-experimental/newrelic-experimental-FIT-template)
![GitHub issues closed](https://img.shields.io/github/issues-closed/newrelic-experimental/newrelic-experimental-FIT-template)
![GitHub pull requests](https://img.shields.io/github/issues-pr/newrelic-experimental/newrelic-experimental-FIT-template)
![GitHub pull requests closed](https://img.shields.io/github/issues-pr-closed/newrelic-experimental/newrelic-experimental-FIT-template)


>[Brief description - what is the project and value does it provide? How often should users expect to get releases? How is versioning set up? Where does this project want to go?]

## Value

|Metrics | Events | Logs | Traces | Visualization | Automation |
|:-:|:-:|:-:|:-:|:-:|:-:|
|:white_check_mark:|:white_check_mark:|:x:|:white_check_mark:|:x:|:x:|

### List of Metrics,Events,Logs,Traces
|Name | Type | Description |
|:-:|:-:|:-:|
|*metric.name* | Metric| *description*|
|*event.name* | Event|  *description*|
|*log.name* | Log|  *description*|
|*trace.name*| Trace| *description*
|---|---|---|

## Installation

The integration has two main components can be configured and used separetely: A "Metrics Reporter" function and a "Logs Reporter" function. The instructions to setup the function are mostly similar, they differences are on the OCI Service Connector Hubm where we configure OCI to route the proper telemetry type to the respective function.

https://cloud.oracle.com/functions?region=us-ashburn-1



Click on "Create Application"

Name your Application (e.g. New Relic OCI Integration)

select the respective Oracle VCN

select the respetive Subnets 
(the Functions need to be able to post data to our public endpoints)

select Shape: GENERIC_X86 (functions were only tested on X86)

Add tags if necessary

Click on "Create Function"

Name your function: e.g. NewRelic-MetricReporter

Click on Configuration

Add/edit the Environment Properties: 
NR-METRIC-ENDPOINT: <ADD TO FUNCTION>
NR-LOG-ENDPOINT: https://log-api.newrelic.com/log/v1 (or respective EU endpoints)
NEWRELIC_API_KEY: Your API Key
FORWARD_TO_NR: True
LOGGING_LEVEL: INFO


We suggest using CloudShell for deployment, but you can use other tooling offered by Oracle

fn list context

fn use context us-ashburn-1

fn update context {{YOUR REGISTRY}}

fn update context registry {YOUR REGISTRY}/nr-metric-reporter

Generate Auth Token

Generate Token

docker login -u '{{YOUR CREDS}} iad.ocir.io (use token)

fn init --runtime python nr-metric-reporter

cd nr-metric-reporter/

edit the func.yaml file with the content from the repo
edit the func.py file with the content from the repo
edit the requirements.txt file with the content from the repo

fn -v deploy --app NewRelic-MetricReporter


Setup Service Connector Hub to Forward Telemetry

https://cloud.oracle.com/connector-hub/service-connectors

Create Connector

Name: e.g. NewRelic-Log-Connector
Description: This connector streams OCI Logs to a New Relic OCI Integration Function
Compartment: Select your compartment

Under Configure Connector:
Source: Select Logging
Target: Select Functions

Then in Configure Source, select the log groups and logs that will be forwarded to the integration (you can add multiple entries)

(no Log Filter Tasks is needed)
Configure Task: Leave Empty

Then in Configure Target, select the function application (New Relic OCI Integration) and the function name (nr-log-reporter)

Click on "Create"

> [Include a step-by-step procedure on how to get your code installed. Be sure to include any third-party dependencies that need to be installed separately]

## Getting Started

>[Simple steps to start working with the software similar to a "Hello World"]

## Usage

>[**Optional** - Include more thorough instructions on how to use the software. This section might not be needed if the Getting Started section is enough. Remove this section if it's not needed.]

## Building

>[**Optional** - Include this section if users will need to follow specific instructions to build the software from source. Be sure to include any third party build dependencies that need to be installed separately. Remove this section if it's not needed.]

## Testing

>[**Optional** - Include instructions on how to run tests if we include tests with the codebase. Remove this section if it's not needed.]

## Support

New Relic has open-sourced this project. This project is provided AS-IS WITHOUT WARRANTY OR DEDICATED SUPPORT. Issues and contributions should be reported to the project here on GitHub.

>We encourage you to bring your experiences and questions to the [Explorers Hub](https://discuss.newrelic.com) where our community members collaborate on solutions and new ideas.


## Contributing

We encourage your contributions to improve [Project Name]! Keep in mind when you submit your pull request, you'll need to sign the CLA via the click-through using CLA-Assistant. You only have to sign the CLA one time per project. If you have any questions, or to execute our corporate CLA, required if your contribution is on behalf of a company, please drop us an email at opensource@newrelic.com.

**A note about vulnerabilities**

As noted in our [security policy](../../security/policy), New Relic is committed to the privacy and security of our customers and their data. We believe that providing coordinated disclosure by security researchers and engaging with the security community are important means to achieve our security goals.

If you believe you have found a security vulnerability in this project or any of New Relic's products or websites, we welcome and greatly appreciate you reporting it to New Relic through [HackerOne](https://hackerone.com/newrelic).

## License

[Project Name] is licensed under the [Apache 2.0](http://apache.org/licenses/LICENSE-2.0.txt) License.

>[If applicable: [Project Name] also uses source code from third-party libraries. You can find full details on which libraries are used and the terms under which they are licensed in the third-party notices document.]
