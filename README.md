# CST 8919 Assignment 1: 

This assignment combines both using the Auth0 application to log in to the webpage and monitor the application and make logs of the user activity

# running it locally

To run the program, first you need to have `python3` and `pip` installed in order to install the modules needed for this program.

Then you need to go into the directory of you program and write:

```bash
.\.venv\Scripts\activate
pip install -r .\requirements.txt
```

in the command line in order to install all the modules in the requirement.txt file which are flask to have different endpoint and Auth0 to have secure authentication.

After that, you need to run this command:

```bash
openssl rand -hex 32
```

in order to get the value of `APP_SECRET_KEY` environment variable. Copy the output and pasted into the environment variable.

Now run the program by writing:

```bash
python server.py
```
Then you will se this in the command terminal 

```bash
 * Serving Flask app 'server'
 * Debug mode: off
WARNING: This is a development server. Do not use it in a production deployment. Use a production WSGI server instead.
 * Running on all addresses (0.0.0.0)
 * Running on http://127.0.0.1:3000
 * Running on http://192.168.0.248:3000
```

Open: `http://localhost:3000` to open the webpage of the program you are running.

# running and set up the App Services 

## set up the App Service resource

Go to Azure and create an App Service resource. Then fill in the details:

- **Resource Group**: "cst8919-assignment-1"
- **Name**: "cst8919-web-service"
- **Runtime stack**: "Python 3.13"
- **Region**: "East US"
- **Pricing plan**: "Free F1 (Shared infrastructure)"

Then create the web app.

## make the environment variables

After creating the App Service, go to the `Environment variables` tab and in the `Settings` section. 

Add all of the environment variables that are stored in .env by filling in the name and value. 

Don't forget do run this command:

```bash
openssl rand -hex 32
```

and take the output and fill it in the `APP_SECRET_KEY` variable in app service.

## connect to the application by GitHub repository

Then go to Deployment Center tab and fill in the following detail:

- **Source**: "GitHub"
- **Organization**: "Mo10serek"
- **Repository**: "cst8919_Assignment_1"
- **Branch**: "master"

Then save the changes and you will see that it is connected to the repository.

## logging explanation

the function to print the logs are `app.logger.info()` where they are located in each endpoint explaning the status of the program. However in the protected and callback endpoints, it calls the log function which prints out the user id, email, and timestamp. These values are printed out because ones the user is log in, it get the json file in session and gets all of the information from the log in user. These logs are printed out in log

# Monitoring and Detection

## make the KQL Query

### Make a Log Analytics workspace resource

Create a Log Analytics workspace and fill in the following detail:

- **Resource Group**: "cst8919-assignment-1"
- **Name**: "cst8919-log-analytics-workspace"
- **Region**: "East US"

and create the resource.

### configure Diagnostic

In app services, go to the Diagnostic settings tab in the Monitoring section and add a diagnostic setting.

There is check `AppServiceConsoleLogs` and `HTTPLogs` and select the name of your Log Analytics workspace resource and save the changes you done.

### KQL Query

Go to Log tab in Log Analytics workspace and fill in the following KQL query.

AppServiceConsoleLogs 
| where ResultDescription has "protected"
| where ResultDescription has "user id"
| where TimeGenerated > ago(15m)
| extend useridStart = indexof(ResultDescription, "user id: ") + 9
| extend useridEnd = indexof(ResultDescription, "email", useridStart) - 2
| extend user_id = substring(ResultDescription, useridStart, useridEnd - useridStart)
| extend timestampStart = indexof(ResultDescription, "timestamp: ") + 11
| extend timestampEnd = indexof(ResultDescription, "description", timestampStart) - 2
| extend timestamp = substring(ResultDescription, timestampStart, timestampEnd - timestampStart)
| extend useridStart = indexof(ResultDescription, "user id: ") + 9
| extend useridEnd = indexof(ResultDescription, "email", useridStart) - 2
| extend user_id = substring(ResultDescription, useridStart, useridEnd - useridStart)
| extend timestampStart = indexof(ResultDescription, "timestamp: ") + 11
| extend timestampEnd = indexof(ResultDescription, "description", timestampStart) - 2
| extend timestamp = substring(ResultDescription, timestampStart, timestampEnd - timestampStart)
| summarize number_of_times_user_log = count() by user_id, timestamp
| where number_of_times_user_log > 10
| project user_id, timestamp, number_of_times_user_log

Test the query by entering and exiting the protected page more than ten times and you will see the `user_id`, `timestamp` and `number_of_times_user_log` columns shown.

## Create Azure Alert 

Go to the Monitor resource and then the alerts tab and create a new alert rule. 

### Scope

In the Scope section, click `Select scope` and select the Log Analytics workspace resource that is under group resource and subscription. 

### Condition

In the Condition section, select Custom log search in the Signal name and fill in the Search query:

AppServiceConsoleLogs 
| where ResultDescription has "protected"
| where ResultDescription has "user id"
| where TimeGenerated > ago(15m)
| extend useridStart = indexof(ResultDescription, "user id: ") + 9
| extend useridEnd = indexof(ResultDescription, "email", useridStart) - 2
| extend user_id = substring(ResultDescription, useridStart, useridEnd - useridStart)
| extend timestampStart = indexof(ResultDescription, "timestamp: ") + 11
| extend timestampEnd = indexof(ResultDescription, "description", timestampStart) - 2
| extend timestamp = substring(ResultDescription, timestampStart, timestampEnd - timestampStart)
| extend useridStart = indexof(ResultDescription, "user id: ") + 9
| extend useridEnd = indexof(ResultDescription, "email", useridStart) - 2
| extend user_id = substring(ResultDescription, useridStart, useridEnd - useridStart)
| extend timestampStart = indexof(ResultDescription, "timestamp: ") + 11
| extend timestampEnd = indexof(ResultDescription, "description", timestampStart) - 2
| extend timestamp = substring(ResultDescription, timestampStart, timestampEnd - timestampStart)

and fill in the remaining details:

#### Measurement

- **Measure**: "Table rows"
- **Aggregation type**: "Count"
- **Aggregation granularity** : "15 minutes"

#### Alert logic

- **Operator**: "Greater than"
- **Threshold value**: "10"
- **Frequency of evaluation**: "15 minutes"

### Action

go and create an Action group and fill in the Resource group, Region, Action group name, and Display name in basics. In notification, select `Email/SMS message/Push/Voice` and check the email box. After that, enter your email and select okay. Also put the name of the notification type as well

### Details

Fill the resource group you are in, Severity as `3 - Informational`, Alert rule name, Alert rule description, and Region as `East US`

After that create your resource. 

## Testing Azure Alert

After you created the alert rule and action group, you will receive an email that you been register to the action group. To test the alert rule, you need to enter the protected page more than 10 times. Wait for a moment and you will receive an email that a user is accessing the protected webpage more than 10 times.

## Video Demo

