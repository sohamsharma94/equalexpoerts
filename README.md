## :warning: Please read these instructions carefully and entirely first
* Clone this repository to your local machine.
* Use your IDE of choice to complete the assignment.
* When you have completed the assignment, you need to  push your code to this repository and [mark the assignment as completed by clicking here](https://app.snapcode.review/submission_links/8245322f-fcdf-49a1-aded-6c1433de6c9a).
* Once you mark it as completed, your access to this repository will be revoked. Please make sure that you have completed the assignment and pushed all code from your local machine to this repository before you click the link.

**Table of Contents**
1. [Before you start](#before-you-start), a brief explanation for the exercise and software prerequisites/setup.  
2. [Tips for what we are looking for](#tips-on-what-were-looking-for) provides clear guidance on solution qualities we value 
3. [The Challenge](#begin-the-two-part-challenge) explains the data engineering code challenge to be tackled.
4. [Follow-up Questions](#follow-up-questions) related to the challenge which you should address  
5. [Your approach and answers to follow-up questions](#your-approach-and-answers-to-follow-up-questions-) is where you should include the answers to the follow-up question and clarify your solution approach any assumptions you have made.

## Before you start
### Why complete this task?

We want to make the interview process as simple and stress-free as possible. That’s why we ask you to complete 
the first stage of the process from the comfort of your own home.

Your submission will help us to learn about your skills and approach. If we think you’re a good fit for our 
network, we’ll use your submission in the next interview stages too.

### About the task

You’ll be creating an ingestion process to ingest files containing vote data. You’ll also create a means to 
query the ingested data to determine outlier weeks.

There’s no time limit for this task, but we expect it to take less than 2 hours.

### Setup Instructions

For instructions on how to set up and run the exercise locally or with Docker, please see [SETUP.md](SETUP.md).

### Tips on what we’re looking for


* ✅  **Test coverage**

    Demonstrate your ability to write well-structured tests that verify behavior, not just execute code for coverage.

* ✅  **Self-contained tests**

    Your tests should be self-contained, with no dependency on being run in a specific order.

* ✅  **Simplicity**

    We value simplicity as an architectural virtue and a development practice. Solutions should reflect the difficulty of the assigned task, and shouldn’t be overly complex. We prefer simple, well tested solutions over clever solutions. 

    Please avoid:

   * ❌ unnecessary layers of abstraction
   * ❌ patterns
   * ❌ custom test frameworks
   * ❌ architectural features that aren’t called for
   * ❌ libraries like **pandas** or **polars** or frameworks like **PySpark** or **ballista**
  
     We know that this exercise can be
     solved fairly trivially using these libraries and a Dataframe approach, and we'd encourage appropriate 
     use of these in daily work contexts. But for this small exercise we really 
     want to know more about how you structure, write and test your Python code,
     and want you to show some fluency in SQL -- a **pandas**
     solution won't allow us to see much of that.

* ✅  **Self-explanatory code**

    The solution you produce must speak for itself. Multiple paragraphs explaining the solution is a sign 
    that the code isn’t straightforward enough to understand on its own.
    However, please do explain your non-obvious _choices_ e.g. perhaps why you decided to load
    data a specific way.

* ✅ **Demonstrate fluency with data engineering concepts**
   
   Even though this is a toy exercise, treat DuckDB as you would an OLAP 
   data warehouse. Choose datatypes, data loading methods, optimisations and data models that 
   are suited for resilient analytics processing at scale, not transaction processing.

* ✅ **Dealing with ambiguity**

    If there’s any ambiguity, please add this in a section at the bottom of the README. 
    You should also make a choice to resolve the ambiguity and proceed.

Our review process starts with a very simplistic test set in the `tests/exercise_tests` folder which you should also
check before submission. You can run these with:
```shell
uv run exercise check-ingestion
uv run exercise check-outliers
```

Expect these to fail until you have completed the exercise.

You should not change the `tests/exercise_tests` folder and your solution should be able to pass both tests.


## Download the dataset for the exercise
Run the command
```
uv run exercise fetch-data
```

which will fetch the dataset, uncompress it and place it in `uncommitted/votes.jsonl` for you.
Explore the data to see what values and fields it contains (no need to show how you explored it).

## Begin the two-part challenge
There are two parts to the exercise, and you are expected to complete both. 
A user should be able to execute each task independently of the other. 
For example, ingestion shouldn't cause the outliers query to be executed.

### Part 1: Ingestion

Create a schema called `blog_analysis`.
Create an on-demand ingestion process that can handle incremental loads from files containing vote data. The process should be designed to run multiple times and must handle:
- **New records**: Insert records that don't exist in the target table
- **Updated records**: Reflect changes when a record with the same ID has different values

You should ensure that data scientists, who will be consumers of the data, do not need to consider duplicate records in their queries. The data should be stored in a table called `votes` in the `blog_analysis` schema.

### Part 2: Outliers calculation
Create a view named `outlier_weeks`  in the `blog_analysis` schema. It will contain the output of a SQL calculation for which weeks are regarded as outliers based on the vote data that was ingested.
The view should contain the year, week number and the number of votes for the week _for only those weeks which are determined to be outliers_, according to the following rule:

NB! If you're viewing this Markdown document in a viewer
where the math isn't rendering, try viewing this README in GitHub on your web browser, or [see this pdf](docs/calculating_outliers.pdf).

> 
> **A week is classified as an outlier when the total votes for the week deviate from the average votes per week for the complete dataset by more than 20%.**</br>  
> For the avoidance of doubt, _please use the following formula_: 
>  
> > Say the mean votes is given by $\bar{x}$ and this specific week's votes is given by $x_i$. 
> > We want to know when $x_i$ differs from $\bar{x}$ by more than $20$%. 
> > When this is true, then the ratio $\frac{x_i}{\bar{x}}$ must be further from $1$ by more than $0.2$, i.e.: </br></br> 
> > $\big|1 - \frac{x_i}{\bar{x}}\big| > 0.2$

The data should be sorted in the view by year and week number, with the earliest week first.

Running `outliers.py` should recreate the view and 
just print the contents of this `outlier_weeks` view to the terminal - don't do any more calculations after creating the view.

## Example

The sample dataset below is included in the test-resources folder and can be used when creating your tests.

Assuming a file is ingested containing the following entries:

```
{"Id":"1","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-02T00:00:00.000"}
{"Id":"2","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"}
{"Id":"4","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"}
{"Id":"5","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-09T00:00:00.000"}
{"Id":"6","PostId":"5","VoteTypeId":"3","CreationDate":"2022-01-16T00:00:00.000"}
{"Id":"7","PostId":"3","VoteTypeId":"2","CreationDate":"2022-01-16T00:00:00.000"}
{"Id":"8","PostId":"4","VoteTypeId":"2","CreationDate":"2022-01-16T00:00:00.000"}
{"Id":"9","PostId":"2","VoteTypeId":"2","CreationDate":"2022-01-23T00:00:00.000"}
{"Id":"10","PostId":"2","VoteTypeId":"2","CreationDate":"2022-01-23T00:00:00.000"}
{"Id":"11","PostId":"1","VoteTypeId":"2","CreationDate":"2022-01-30T00:00:00.000"}
{"Id":"12","PostId":"5","VoteTypeId":"2","CreationDate":"2022-01-30T00:00:00.000"}
{"Id":"13","PostId":"8","VoteTypeId":"2","CreationDate":"2022-02-06T00:00:00.000"}
{"Id":"14","PostId":"13","VoteTypeId":"3","CreationDate":"2022-02-13T00:00:00.000"}
{"Id":"15","PostId":"13","VoteTypeId":"3","CreationDate":"2022-02-20T00:00:00.000"}
{"Id":"16","PostId":"11","VoteTypeId":"2","CreationDate":"2022-02-20T00:00:00.000"}
{"Id":"17","PostId":"3","VoteTypeId":"3","CreationDate":"2022-02-27T00:00:00.000"}
```

Then the following should be the content of your `outlier_weeks` view:


| Year | WeekNumber | VoteCount |
|------|------------|-----------|
| 2022 | 0          | 1         |
| 2022 | 1          | 3         |
| 2022 | 2          | 3         |
| 2022 | 5          | 1         |
| 2022 | 6          | 1         |
| 2022 | 8          | 1         |

**Note that we strongly encourage you to use this data as a test case to ensure that you have the correct calculation!**

## Follow-up Questions

Please include instructions about your strategy and important decisions you made in the README file. You should also include answers to the following questions, please make sure these are answered without the use AI tools as we would like to understand your thought process:

1. What kind of data quality measures would you apply to your solution in production?
2. What would need to change for the solution scale to work with a 10TB dataset with 5GB new data arriving each day?
3. Please tell us in your modified README about any assumptions you have made in your solution (below).


## Your Approach and answers to follow-up questions 

### Implementation approach and assumptions

Ingestion reads the newline-delimited JSON directly into DuckDB, casts the source fields to warehouse types, and merges rows into `blog_analysis.votes` by vote ID in a transaction. The ID is the primary key, so a rerun inserts new votes and replaces changed values for existing IDs without exposing duplicates. If one file contains the same ID more than once, the staged row with the latest `CreationDate` is used; remaining ties are resolved by the other vote fields.

The outlier view first counts votes in seven-day calendar buckets starting on January 1 (week 0), matching the supplied example. It compares each observed bucket with the average count across observed buckets in the complete table, using the specified strict 20% threshold. Empty weeks are not included in that average. The script recreates the view and prints its rows in year/week order.

### Follow-up questions

1. **Production data quality:** Validate required fields and types before loading; reject or quarantine malformed rows; check non-null and unique IDs, valid timestamps, and reasonable vote-type values; record row counts and rejected records; monitor freshness and volume changes; and reconcile staged versus inserted/updated counts. Keep ingestion atomic so a failed batch does not leave partial updates.
2. **Scaling to 10 TB with 5 GB arriving daily:** Store data in partitioned columnar files such as Parquet in object storage, and use an engine/catalog designed for distributed incremental processing. Partition appropriately (for example, by date), process only new or changed partitions, and avoid repeatedly scanning the full history. Use a durable change key/manifest or CDC feed for incremental merges, compact small files, and maintain statistics and monitoring. Keep the analytical query over a materialized weekly aggregate that is incrementally maintained, rather than recounting all raw rows daily.
3. **Assumptions:** Vote IDs uniquely identify records; timestamps are valid and interpreted as the provided local/UTC-naive timestamp; the latest `CreationDate` is the best available tie-breaker for repeated IDs in one input file; a week means a fixed seven-day bucket beginning January 1 of each year; only weeks with at least one vote participate in the average; and rerunning a file should be idempotent.

### AI tool usage

1. **Specific use cases:** AI assistance was used to interpret the exercise instructions, draft the ingestion and SQL-view implementation, add tests, and update this README.
2. **Estimated AI-generated code:** Approximately 80% of the new implementation and tests were AI-drafted; this estimate excludes the pre-existing project files.
3. **Review and verification:** The implementation was checked against the sample output and the incremental/update/idempotency requirements with automated tests and the repository's exercise checks. Any remaining failing check or setup limitation is reported with the submission rather than represented as verified.

The follow-up responses above are an implementation-oriented draft and should be reviewed and rephrased to reflect the submitter's own reasoning before submission.

## AI Tool Usage

While we encourage the use of AI tools as part of the learning process but to ensure transparency, please provide the following information regarding the use of AI tools in this submission:

1.  **Specific Use Cases:** Describe for what purposes tool was used (e.g., code generation, debugging assistance, query generation etc.).
2.  **Percentage of Code Generated by AI:** Provide an estimate of the percentage of the submitted code that was generated by AI.
3.  **How AI-Generated Code Was Reviewed:** Explain how you reviewed and verified the AI-generated code to ensure its correctness and quality.

Please note, during the technical interview, which will build upon this exercise, we'll focus on your coding abilities and problem-solving skills without the use of AI tools. This will allow us to see your direct approach and thought process.
