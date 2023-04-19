# CTW Take-Home Assignment
Fetches stock prices, and store in the database. Also, exposes APIs to query stock prices with date range and statistics of the stock price.

# Tech stacks
- **FastAPI:** Exposes fastapi endpoints to query the data.
- **MySQL:** Stores stock information.
- **SQLAlchemy:** Popular ORM framework for SQL.
- **marshmallow:** Helps to validate requests.

# Running project in local
- Clone the repo using the following command
    ```shell
    git clone git@github.com:sayannandi/ctw_python_assignment.git && cd ctw_python_assignment
    ```
- Replace `.env.example` with `.env` and update `ALPHA_VANTAGE_API_KEY` with your `API_KEY`
    ```shell
    cp .env.example .env
    ```
- Fire up the project using
    ```shell
    docker-compose up -d
    ```
- This command will fetch new stock data and update the db with latest data. Also this will boot up the fastapi application which can be accessed using curl
    ```shell
    curl -X GET 'http://localhost:5000/api/financial_data'
    ```
- To fetch new data you can run the following:
    ```shell
    docker exec ctw-app python3 src/get_raw_data.py
    ```

# Note
In case port 5000 doesn't work on mac, it could be because of this [issue](https://stackoverflow.com/questions/69818376/localhost5000-unavailable-in-macos-v12-monterey)
