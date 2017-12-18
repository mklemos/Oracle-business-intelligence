# Automated functional testing for Oracle Business Intelligence #
This project highlights the setup and usage of a continuous integration environment for Humboldt State University's Oracle Business intelligence platform.

Date Started: May 22, 2017

Oracle business intelligence requires an RPD file, this file is a binary that defines the OBI application. Typically, the OBI application requires a manual upload through Oracle Enterprise Manager with Fusion Middleware Control, when a new RPD file is ready to be used. This, however, is tedious and can be automated. Oracle uses a command line scripting environment called Web Logic Scripting Tool, known by its acronym WLST. Using WLST, this project will show how the RPD file can be deployed successfully to OBI. The New RPD won't be active until the BI Server is restarted, however, our script will handle this functionality.

Once the RPD file is deployed and active, we need a means of functionally testing the OBI environment to ensure the integrity of the data. Our testing environment includes the use of a Jenkins continuous integration server and the browser automation tool called Selenium. Using Python’s unittest and pytest libraries to write testing scripts that interact with the selenium server to test against the data presented in the DOM and/or frontend of the application.

Be sure that you setup your server environments to match your local environment. It’s very important that the software installed in both environments is the same, otherwise testing your scripts locally may produce different results when deployed to the remote servers.

Diagram: [https://www.lucidchart.com/documents/edit/a5c8c12a-7465-482e-89ca-389ce61cadd2/0](https://www.lucidchart.com/documents/edit/a5c8c12a-7465-482e-89ca-389ce61cadd2/0)

![](http://i.imgur.com/M0UUhTt.png "Diagram")

## Servers and associated ports: ##
You should have access to each of these server environments, along with access to the Oracle user on obitest and the Jenkins user on dwdb2-dev. If not talk to your friendly local sys-admin.

* [http://dwdb2-dev.humboldt.edu:8080/job/obidev/configure](http://dwdb2-dev.humboldt.edu:8080/job/obidev/configure) - Jenkins Dashboard

* [http://obitest.humboldt.edu:7001](http://obitest.humboldt.edu:7001) – T3 connection to Fusion Middleware control

* [http://obitest.humboldt.edu:7002](http://obitest.humboldt.edu:7002) – Fusion Middleware control

* [http://obi-prod-1.humboldt.edu](http://obi-prod-1.humboldt.edu) - OBI production server

* [https://obitest.humboldt.edu:9804/analytics/saw.dll?bieehome](https://obitest.humboldt.edu:9804/analytics/saw.dll?bieehome) – OBI interactive reporting tool frontend

* [http://dw-autotest-dev.humboldt.edu](http://dw-autotest-dev.humboldt.edu) – selenium server located here

Make sure you have python 2.7 on all your environments. Be sure to add it to your path variable.

### Install python libraries:
* `pip install -U pytest`

* `pip install pytest-allure-adaptor`

* `pip install -U selenium`

### Obitest:
Logging in as the oracle user you’ll find the `/home/oracle/scripts` folder. Which contains:

* deploy_restart.sh – a shell script that holds the command for calling the deploy_rpd.py script  

* deploy_rpd_orig.py - The original Rittman Mead script

* deploy_rpd.py - HSU’s modified version of the Rittman Mean script.

### Dw-autotest-dev:
With: xvfb, selenium, and firefox installed on DISPLAY:99.

java version "1.7.0_101"

This should be called on startup of the server:

`java -jar .\selenium-server-standalone-3.4.0.jar`

A softlink created at `/usr/bin/geckodriver` to point to `/usr/local/bin/geckodriver` it should work even if `/usr/local/bin` is not in the PATH of the Jenkins user. Please also make sure the port 4444 is open.

### Dwdb2-dev:
Ensure that jenkins version: 2.32.3 exists.

Interacting with WLST on obitest.humboldt.edu:

While this guide shows you how to interact with WLST using the python script, you can interact with WLST directly and independently with these steps. This is helpful for troubleshooting and possibly writing new WLST scripts.

You must have access to the oracle user on the obitest.humboldt.edu server. You may speak to a sysadmin to get yourself added to that group/user.

I would log into my normal user account and perform:

`sudo su oracle`

This prompts you for your password. Input that.

Now you are logged in as the Oracle user.

We need to know where the WLST shell interface exists. Obitest.humboldt.edu you will find the wlst shell script, which will open the wlst console. It’s located:

`cd /sdc1/oracle/Middleware/Oracle_BI1/common/bin`

It’s in this environment that you can interact with the web logic the scripting tool that controls the Oracle Enterprise Manager, located: obitest.humboldt.edu:7001
Because we have access to this environment, we can write scripts that interact on our behalf, such as uploading a new RPD, and restarting the environment to commit new changes.

You’ll find that the script called: deploy_rpd.py is an example of a python script that controls the Oracle Enterprise Manager in the WLST environment.

### Selenium on dw-autotest-dev.humboldt.edu:
Selenium is a browser automation tool, we’ll be using the Selenium Python library to write scripts that navigate “headlessly” on the server. While, locally we’ll be running selenium and launching an actual browser window on our machine to write and test our scripts.

## Jenkins:
Jenkins is our orchestrator. Like many tools it can have multiple projects running all at once.

When you first login you’ll notice that there are quite a few projects listed.
Before you select obidev:
1. click on the link in the left menu, “Manage Jenkins”
2. from the menu select “Configure System”. Located: [http://dwdb2-dev.humboldt.edu:8080/configure](http://dwdb2-dev.humboldt.edu:8080/configure)

Make sure that the SSH info for oracle is listed:

    SSH remote hosts

    Hostname: obitest.humboldt.edu

    Port: 22  

    User Name: oracle

    Password/Passphrase: •••••••••••

**Below are the different sections of the Jenkins Pipline specifically for our obidev project. You’ll find this under the URL:** [dwdb2-dev.humboldt.edu:8080/job/obidev/configure](dwdb2-dev.humboldt.edu:8080/job/obidev/configure)

We utilize Jenkins to perform testing in our server environment. For local testing view the section called: “Testing With Selenium Locally”

**Source Code Management:**

The first thing we need Jenkins to do is to retrieve the newest version of the RPD file from source control.

**Note: The Jenkins user needs to be setup with SSH keys so that the user can log into dwdb2-dev without a password. Ask your friendly local sys-admin about this.**

1. Select the radio button for Git.

2. Repository URL: git@bitbucket.org:humboldt/rpd-2017.git

3. Credentials: Jenkins@dwdb2-dev.humboldt.edu

4. Branches to build: master

Once Jenkins has made a connection to source control, it needs a branch to be specified. In our case, we want the newest version, so we pull from Master. ¬

However, while developing you may want to specify a static branch, but we’ll talk more about that in the section in the documentation called “Testing With Selenium Locally”.

Once we pull from master we have to save that RPD file to a location that Jenkins can then pass along to the WLST environment, this will be outlined in the build section below.

**Build triggers:**

Because we are relying on master to have the most up to date version of the RPD file we can set the build trigger in Jenkins to “Build when a change is pushed to BitBucket”

Pro tip: when testing the reliability of scripts we can set to build periodically, which uses chron job notation to set your tests to run on a reoccurring time table. Which can help you understand how strong/weak a test case really is.

**Build Environment:**

I like to check off the option that allows us to “Add timestamps to the Console Output”
This is a matter of preference and will not affect the functionality of the project.

####Build:

**Execute Shell:**

Because we are already in the dwdb2-dev.humboldt.edu environment we need to be in the correct directory to place the RPD file for our use:

`cd /var/lib/jenkins/workspace/obidev/`

Copy the file "obiprod.rpd" from dwdb2-dev.humboldt.edu to a remote host jenkins@obitest.humboldt.edu

The Jenkins user has a trusted set of public/private keys that were created on the OBITEST server to receive the new RPD file without prompting for password. This is achieved with this command:

`scp obiprod.rpd jenkins@obitest.humboldt.edu:/home/oracle/scripts`

The Jenkins user was granted write access to the /home/oracle/scripts directory from Patrick the sys-admin on obitest. obi-prod-1 will also require write access to the /home/oracle/scripts directory, again speak to the sys-admins for more details on how to accomplish this.

**Execute shell script on remote host using ssh:**

Using the format outlined in the original Rittman mead script that we based our own off, of we use this command, with ssh we execute this command on a remote server.

`/sdc1/oracle/Middleware/oracle_common/common/bin/wlst.sh /home/oracle/scripts/deploy_rpd.py Username pwd t3://obitest.humboldt.edu:7001 /home/oracle/scripts/obiprod.rpd pwd False`

Let’s breakdown above:

Path to WLST cmd prompt:

/sdc1/oracle/Middleware/oracle_common/common/bin/wlst.sh

Path to custom python script to deploy and restart Oracle Enterprise Manager:

/home/oracle/scripts/deploy_rpd.py

Username to Oracle Enterprise Manager

Username

Password to Oracle Enterprise Manager

pwd

Location of Oracle Enterprise Manager using t3 protocol:

t3://obitest.humboldt.edu:7001

RPD password:

pwd

Final argument(True/False):

False

Note: The reason we have False set, is we have a manual restart at the end of the script that works better than the original version we had from Rittman Mead. Look for this at the bottom of the script with the OS system calls.

**Execute Shell:**

`Py.test –junitxml /var/lib/Jenkins/workspace/obidev/CI-RPD/allure-results/results.xml /var/lib/Jenkins/workspace/obidev/CI-RPD/test_cases`

The above code utilizes the built in feature of the Py.test framework to generate an XML output of the results of testcases found in the /var/lib/Jenkins/workspace/obidev/CI-RPD/test_cases path. The results are stored in the /var/lib/Jenkins/workspace/obidev/CI-RPD/allure-results/results.xml path. The results.xml is what populates the email that gets sent with every pass or fail of the Jenkins build.

**Post-build Actions**

Publish JUnit test result report:

By selecting this you are enabling the blue and red graph that appears on the project dashboard page showing your “Test Result Trend” along with that, the XML supplies the data for the plugin: Test Results Analyzer. This can be found in the main navigation on the left side of the project dashboard.

Test report XMLs: CI-RPD/allure-results/results.xml

**Editable Email Notification:**
This area of the post-build Action section will show how we modify recipients and formatting for the email notifications generated by each build.
/var/lib/jenkins/email-templates

The file we are using here is called: groovy-html.template

This template will utilize the xml generated and display it in html so that the email can be rendered by the mailer.

**Slack:**

I have all the checkboxes set to display in a new slack channel.

You will need an integration token with slack and you will need to know the team subdomain in our case we used: hsu-its

We also specified the channel as: #edm-code

**Jenkins plugins:**

Jenkins has a huge library of plugins to add functionality to your project.

[dwdb2-dev.humboldt.edu:8080/pluginManager/installed](dwdb2-dev.humboldt.edu:8080/pluginManager/installed)

Besides the defaults plugins that come with new Jenkins installations we used:

Various: Bitbucket plugins

Email Extension Plugin v2.58

Junit Plugin v1.20

Mailer Plugin v1.20

Slack Notification Plugin v2.2

SSH plugin v2.4

Test Results Analyzer Plugin v0.3.4

### Testing With Selenium Locally

You’ll want to download the selenium server, we happen to be using version 3.4.0

Using the node packet manager you can download this jar file here:

`npm install selenium-server-standalone-jar@3.4.0`

Install locally, for example: C:\selenium\selenium-server-standalone-3.4.0.jar

Be sure to add this to your Path variable.

Pro tip: Make sure that any other zombie selenium servers from past runs are killed via the task manager before you start a fresh run of the server.

Run:

`java -jar .\selenium-server-standalone-3.4.0.jar`

Navigate to the location where you have stored your tests. In my case I have a local version of the project’s repository: C:\Users\mkl177\Documents\rpd-2017\CI-RPD\test_cases

In our tests we have a line at the top of each setup method that describes the driver being used and where that driver will live in the browser and on which port, in our case you can view active sessions on the Selenium server at: http://localhost:4444/wd/hub

You will need to make sure that if you are running these test cases locally you have modified the setup method of each test.

From:

`self.driver = webdriver.Remote(command_executor='http://dw-autotest-dev:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX) #dw-autotest-dev or localhost`

To:

`self.driver = webdriver.Remote(command_executor='http:// localhost:4444/wd/hub', desired_capabilities=DesiredCapabilities.FIREFOX) #dw-autotest-dev or localhost`

You may specify a single test case by using this syntax:

`pytest .\test_z_better_display_content.py`

Or

You can test the entire directory you are in for all python files with test in the name.

`Pyteset .`

This will kick off the pytest file collection process, it should look similar to this:

`PS C:\Users\mkl177\Documents\rpd-2017\CI-RPD\test_cases> pytest .`

      ============================= test session starts =============================

      platform win32 -- Python 2.7.13, pytest-3.1.2, py-1.4.34, pluggy-0.4.0

      rootdir: C:\Users\mkl177\Documents\rpd-2017\CI-RPD\test_cases, inifile:

      plugins: allure-adaptor-1.7.7

      collected x items

This should eventually open a new firefox browser and the tests will begin.

You will see the browser change and modify values, it will open and close itself at the start and end of each test directly on your workstation in front of you.

Once the tests have run it will report the status of each of these tests in the console.

### Intern Git workflow

        Master
          |
        Sprint
          |
        Intern
        /     \
      Max      Josh
    
### New Headline    
