# Redis TTL Manager

This project provides a tool to manage the time-to-live (TTL) of keys in Redis. It allows you to search for keys that match a specific pattern, print their TTL in various time units, and change the TTL of keys that meet certain criteria.

## Project Structure

- `redis_ttl_manager.py`: Contains the `RedisTTLManager` class that implements the logic to search and manage the TTL of keys in Redis.
- `main.py`: Uses `click` to handle command-line parameters and execute the logic defined in `RedisTTLManager`.

## Installation

### Requirements

- Python 3.7 or higher
- Redis
- `pip` to install dependencies

### Dependencies

Install the project dependencies using `pip`:

```bash
pip install redis python-dotenv click
```

### Environment Variables

Create a `.env` file in the root directory of the project and define the following variables:

```
REDIS_SERVER=localhost
REDIS_PORT=6379
REDIS_SSL=false
REDIS_SSL_CERT_REQS=required
```

Make sure to adjust these values according to your Redis configuration.

## Usage

### Running the Script

To run the script, use the following command:

```bash
python main.py --pattern "YOUR_PATTERN" --expiration_month_min 3 --cut_key 50 --new_token_expire_minutes 525600
```

### Parameters

- `--pattern`: Pattern to search for in Redis keys (required).
- `--expiration_month_min`: Minimum expiration time in months (optional, default is 3).
- `--cut_key`: Number of characters to show in the truncated key (optional, default is 50).
- `--new_token_expire_minutes`: New TTL for keys in minutes (optional, default is 525600, which is 1 year).

### Example

```bash
python main.py --pattern "session:*" --expiration_month_min 6 --cut_key 30 --new_token_expire_minutes 432000
```

This command will search for all keys that match the pattern `session:*`, print their TTL, and update the TTL of keys expiring in less than 6 months to 432000 minutes (300 days).

## Origin

This script is a fork from [this gist](https://gist.github.com/pixelead0/3d28ad5a0072e7ce2ca6ebb208c022e3) by [pixelead0](https://gist.github.com/pixelead0).

## Contributing

Contributions are welcome. You can open a pull request or create an issue to discuss the changes you would like to make.

## License

This project is licensed under the MIT License. See the `LICENSE` file for more information.
