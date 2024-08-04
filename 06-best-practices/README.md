## Q1. Refactoring
Before we can start covering our code with tests, we need to refactor it. We'll start by getting rid of all the global variables.
Let's create a function main with two parameters: year and month.
Move all the code (except read_data) inside main
Make categorical a parameter for read_data and pass it inside main
Now we need to create the "main" block from which we'll invoke the main function. How does the if statement that we use for this looks like?
Hint: after refactoring, check that the code still works. Just run it e.g. for March 2023 and see if it finishes successfully.
[Modified script](batch_task1.py)

## Q2. Installing pytest
Now we need to install pytest
Next, create a folder tests and create two files. One will be the file with tests. We can name it test_batch.py.
What should be the other file?
### __init__.py

## Q3. Writing first unit test
Now let's cover our code with unit tests.
We'll start with the pre-processing logic inside read_data.
It's difficult to test right now because first reads the file and then performs some transformations. We need to split this code into two parts: reading (I/O) and transformation.
So let's create a function prepare_data that takes in a dataframe (and some other parameters too) and applies some transformation to it.
(That's basically the entire read_data function after reading the parquet file)
Now create a test and use this as input:
```
data = [
    (None, None, dt(1, 1), dt(1, 10)),
    (1, 1, dt(1, 2), dt(1, 10)),
    (1, None, dt(1, 2, 0), dt(1, 2, 59)),
    (3, 4, dt(1, 2, 0), dt(2, 2, 1)),      
]
columns = ['PULocationID', 'DOLocationID', 'tpep_pickup_datetime', 'tpep_dropoff_datetime']
df = pd.DataFrame(data, columns=columns)
Where dt is a helper function:
from datetime import datetime
def dt(hour, minute, second=0):
    return datetime(2023, 1, 1, hour, minute, second)
```
Define the expected output and use the assert to make sure that the actual dataframe matches the expected one.
Tip: When you compare two Pandas DataFrames, the result is also a DataFrame. The same is true for Pandas Series. Also, a DataFrame could be turned into a list of dictionaries.
How many rows should be there in the expected dataframe?
### 2
![img.png](img.png)
[Test](test_batch_task3.py)

## Q4. Mocking S3 with Localstack
Now let's prepare for an integration test. In our script, we write data to S3. So we'll use Localstack to mimic S3.
First, let's run Localstack with Docker compose. Let's create a docker-compose.yaml file with just one service: localstack. Inside localstack, we're only interested in running S3.
Start the service and test it by creating a bucket where we'll keep the output. Let's call it "nyc-duration".
With AWS CLI, this is how we create a bucket:
aws s3 mb s3://nyc-duration
Then we need to check that the bucket was successfully created. With AWS, this is how we typically do it:
aws s3 ls
In both cases we should adjust commands for localstack. What option do we need to use for such purposes?
### --endpoint-url

## Make input and output paths configurable
Right now the input and output paths are hardcoded, but we want to change it for the tests.
One of the possible ways would be to specify INPUT_FILE_PATTERN and OUTPUT_FILE_PATTERN via the env variables. Let's do that:
Let's modify our read_data function:
-check if S3_ENDPOINT_URL is set, and if it is, use it for reading
-otherwise use the usual way
[Modified script](batch_task4.py)

## Q5. Creating test data
Now let's create integration_test.py
We'll use the dataframe we created in Q3 (the dataframe for the unit test) and save it to S3. You don't need to do anything else: just create a dataframe and save it.
We will pretend that this is data for January 2023.
Run the integration_test.py script. After that, use AWS CLI to verify that the file was created.
Use this snipped for saving the file:
```
df_input.to_parquet(
    input_file,
    engine='pyarrow',
    compression=None,
    index=False,
    storage_options=options
)
```
What's the size of the file?
### 3620
![img_1.png](img_1.png)

## Q6. Finish the integration test
We can read from our localstack s3, but we also need to write to it.
Create a function save_data which works similarly to read_data, but we use it for saving a dataframe.
Let's run the batch.py script for January 2023 (the fake data we created in Q5).
We can do that from our integration test in Python: we can use os.system for doing that (there are other options too).
Now it saves the result to localstack.
The only thing we need to do now is to read this data and verify the result is correct.
What's the sum of predicted durations for the test dataframe?
###

