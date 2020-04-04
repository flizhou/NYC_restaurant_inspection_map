# Proposal

### 1. Motivation and Purpose

How often do you eat in a restaurant? How do you pick where to eat? Some surveys tell us that 56% Americans in the survey eat outside 2-3 times a week [1] and 95% Americans pick restaurants based on online reviews [2]. To ensure restaurant food safety, the government is responding to claims and inspecting restaurants. But many people are not aware of the existence of restaurant hygiene inspection results. The purpose of this visualization app is to provide an easy way for people to check the inspection results of restaurants in the New York city.

### 2. Description of the data

I will visualize the [DOHMH New York City Restaurant Inspection Results](https://data.cityofnewyork.us/Health/DOHMH-New-York-City-Restaurant-Inspection-Results/rs6k-p7g6) dataset from [New York City OpenData](https://opendata.cityofnewyork.us/).

The dataset was provided by the Department of Health and Mental Hygiene (DOHMH). It collects restaurant inspection results in the New York city between April, 2016 and March, 2020. The original dataset contains 402013 observations and 26 variables. Due to the purpose of the app, I picked out 16 variables.

I will focus on analyzing three variables, including `boro`, `cuisine description`, `grade`. The `boro` variable contains the borough information of the restaurant. The `cuisine description` variable indicates the cuisine type of the restaurant. The `grade` variable is the grade result of the inspection. The `grade` variable contains errors and missing values, so I need to correct errors and fill missing values based on the grading rule described [here](https://www1.nyc.gov/assets/doh/downloads/pdf/rii/inspection-cycle-overview.pdf).

The rest 12 variables are related to restaurant identification and location, and inspection details. The `camis` variable contains the unique ID number for a current registered restaurant. The `dba` is the name of the restaurant. The restaurant location/contact information is stored in `building`, `street`, `street`, `zipcode`, `phone`, `latitude`, and `longitude`. The inspection details are stored in `inspection type`, `score`, `grade`, and `inspection date`. To help correct the `grade` values, I generalized the `inspection type` into four categories as `inspection code`.

### 3. Research questions and Usage Scenarios

1) Which borough has the largest number of grade 'A' restaurants given a cuisine type?

> This research will help users find out the number of grade 'A' restaurants of a certain cuisine type or all cuisine types in a borough. This will help users decide which borough to eat in.

2) What are the cuisine types with the top five largest number of grade 'A' in a given Borough?

> This research will help users find out the number of grade 'A' restaurants of a certain cuisine type in a given borough or all boroughs. This will help users decide which cuisine type to choose.

3) What's the inspection history given a restaurant?

> This research will help users find out the inspection history of a restaurant to decide whether the restaurant is a safe place to eat.

Let's image a twenty-year-old girl named Sarah who is new to the New York city. Today she wants to pick a place to eat for dinner. Besides restaurant reviews, Sarah also cares about the food safety of the restaurant. Before looking into reviews, she want to have a sip of the food safety status in the New York city. Luckily, she knows that this NYC restaurant inspection map app is here to help.

...

#### Reference

1. [The Truth About Dining Out](https://www.fourth.com/resource/truth-about-dining-out-infographic/)

2. [Influences on Diner Decision-Making](https://www.tripadvisor.com/ForRestaurants/r3227)