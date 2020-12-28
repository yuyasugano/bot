# Sample Bot program
 
CCXT + Binance python program.
 
## setup steps
 
1. Copy the template `configuration.json.template` and rename it to `configuration.json`. You need to configure API key and Secret in the file.
2. Prepare `strategy.py` with your own trading strategy.
3. Modify `configuration.json` with your own parameters.
4. Run a bot program as below

once.py is just a one-time runner for your testing purpose.
```sh
$ python main.py configuration.json strategy.py
$ python once.py configuration.json strategy.py
```
