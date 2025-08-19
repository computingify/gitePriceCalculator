## To run localy
Source the virtual env:
```shell
source env/bin/activate
```
Launch the flask application
```shell
python2 app.py
```
## To run unit test
```shell
python -m unittest tests.test_utils.TestUtils
```
## To run specific unit test
```shell
python -m unittest tests.test_utils.TestUtils.test_calculate_price_last_minutes_4days
```