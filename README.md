
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
|:white_check_mark:|:x:|:white_check_mark:|:x:|in progress|:x:|

### List of Metrics,Events,Logs,Traces
|Name | Type | Description |
|:-:|:-:|:-:|
|*metric.name* | Metric| *description*|
|*event.name* | Event|  *description*|
|*log.name* | Log|  *description*|
|*trace.name*| Trace| *description*
|---|---|---|

## Installation

The integration has two main components (functions) that can be configured and used separately: 

 - Metrics Reporter: A function that collects, parses, converts and reports OCI Metrics to New Relic  
 - Logs Reporter: A function that collects and forwards OCI Logs to New Relic

The instructions to setup the function are mostly similar, the differences are on the OCI Service Connector Hub setup,  where we configure OCI to route the proper telemetry type to the respective function.



## Create OCI Application

All OCI Functions live under an "Application". Go to OCI Functions page, and create an Application

https://cloud.oracle.com/functions

 - Click on "Create Application"
 - Name your Application
	 - *New Relic OCI Integration*
 - Select the respective Oracle VCN
 - Select the respective Subnets 
	 - (The functions need to post data to New Relic public endpoints)
 - Select Shape: GENERIC_X86 
	 - (The functions were only tested on X86)
 - Save

### Create OCI Function(s)

 - Name your function:
	 - NewRelic-MetricReporter
	 - NewRelic-LogReporter

 - Add/edit the Environment Properties: 
	 - NR-METRIC-ENDPOINT: https://metric-api.newrelic.com/metric/v1 (or respective EU endpoint)
	 - NR-LOG-ENDPOINT: https://log-api.newrelic.com/log/v1 (or respective EU endpoint)
   - NEWRELIC_API_KEY: Your API Key 
   - FORWARD_TO_NR: True
	   - You can set it to false to disable data reporting
   - LOGGING_LEVEL: INFO

You can find detailed information about OCI Function Setup here: https://docs.oracle.com/en-us/iaas/Content/Functions/Tasks/functionsquickstartcloudshell.htm

Each function has three main files:
- func.yaml: This file contains the definitions for the function
- func.py: This file contains the function code itself
- requirements.txt: This the python requirement (pip) file for the functions

So for each function, copy the content of the respective files and use the OCI CLI (or the cloud shell) to deploy the functions into your application.

## Setup Service Connector Hub to Forward Telemetry

Once you have the functions created within the application, you need to use the OCI Service Connector Hub to forward the telemetry to the functions. You can find more information about the Connector Hub Here: https://docs.oracle.com/en-us/iaas/Content/connector-hub/overview.htm

https://cloud.oracle.com/connector-hub/service-connectors

We need to create two different connectors, one for Metrics and one for Logs
### Create Connector

- Name:
	- NewRelic-Log-Connector
	- NewRelic-Metric-Connector
- Description: This connector streams OCI Logs to a New Relic OCI Integration Function
- Compartment: Select your compartment

- Under Configure Connector: (NewRelic-Log-Connector)
	- Source: Select Logging
	- Target: Select Functions
- Under Configure Source:
	- Select the log groups and logs that will be forwarded to the integration (you can add multiple entries)
- Log Filter Tasks
	- Not needed
- Under Configure Task: 
	- Leave Empty

- Under Configure Target,
	- Select the function application (New Relic OCI Integration) 
	- And select the function name (nr-log-reporter)

- Click on "Create"

Repeat the task for the Metric Reporter, using the nr-metric-reporter function instead.

## Usage

Once the functions are deployed and the Service Connector is set, we should see Logs on the Log UI and Metrics in the MetricExplorer. (OCI metrics have the oci prefix)

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
