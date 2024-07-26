import os
import time
from datetime import timedelta
from typing import Dict, List, Union
import redis
from dotenv import load_dotenv
from concurrent.futures import ThreadPoolExecutor

load_dotenv()


class RedisTTLManager:
    def __init__(
        self,
        pattern: str,
        expiration_month_min: int,
        cut_key: int,
        new_token_expire_minutes: int,
        scan_count: int = 1000,
    ):
        self.redis_client = self.get_redis_client()
        self.pattern = pattern
        self.expiration_month_min = expiration_month_min
        self.cut_key = cut_key
        self.new_token_expire_minutes = new_token_expire_minutes
        self.scan_count = scan_count

    @staticmethod
    def get_redis_client() -> redis.Redis:
        redis_server = os.environ.get("REDIS_SERVER")
        redis_port = int(os.environ.get("REDIS_PORT", 6379))
        redis_ssl = os.environ.get("REDIS_SSL", "false").lower() in [
            "true",
            "1",
            "t",
            "y",
            "yes",
        ]
        redis_ssl_cert_reqs = os.environ.get("REDIS_SSL_CERT_REQS", "required")

        return redis.Redis(
            host=redis_server,
            port=redis_port,
            ssl=redis_ssl,
            ssl_cert_reqs=redis_ssl_cert_reqs,
            socket_timeout=3,
        )

    @staticmethod
    def convert_ttl(ttl: int) -> Union[str, Dict[str, Union[int, float]]]:
        if ttl == -1:
            return "No expiration"
        td = timedelta(seconds=ttl)
        days, seconds = td.days, td.seconds
        hours = seconds // 3600
        minutes = (seconds % 3600) // 60
        weeks = days // 7
        months = days // 30  # Aproximadamente 30 días por mes

        return {
            "seconds": ttl,
            "minutes": minutes,
            "hours": hours,
            "days": days,
            "weeks": weeks,
            "months": months,
        }

    def scan_keys(self, cursor: int) -> List[bytes]:
        _, keys = self.redis_client.scan(
            cursor=cursor, match=self.pattern, count=self.scan_count
        )
        return keys

    def get_keys_by_pattern(self) -> List[bytes]:
        keys = []
        cursor = 0

        with ThreadPoolExecutor() as executor:
            futures = []

            while True:
                cursor, new_keys = self.redis_client.scan(
                    cursor=cursor, match=self.pattern, count=self.scan_count
                )
                keys.extend(new_keys)

                # Realizar la siguiente búsqueda en paralelo
                if cursor != 0:
                    futures.append(executor.submit(self.scan_keys, cursor))

                if cursor == 0:
                    break

            for future in futures:
                keys.extend(future.result())

        return keys

    def change_ttl(self, key: bytes) -> None:
        new_ttl = timedelta(minutes=self.new_token_expire_minutes)
        self.redis_client.expire(key, int(new_ttl.total_seconds()))

    def process_keys(self) -> None:
        keys = self.get_keys_by_pattern()
        expiration_times: Dict[str, Union[str, Dict[str, Union[int, float]]]] = {}
        for key in keys:
            ttl = self.redis_client.ttl(key)
            expiration_times[key.decode("utf-8")] = self.convert_ttl(ttl)

        if expiration_times:
            for key, ttl_info in expiration_times.items():
                key_truncated = key[: self.cut_key]
                if isinstance(ttl_info, str):
                    print(f"Clave: {key_truncated}, Tiempo de expiración: {ttl_info}")
                else:
                    if ttl_info["months"] < self.expiration_month_min:
                        print(
                            f".Clave: {key_truncated}, Tiempo de expiración: {ttl_info}"
                        )
                        self.change_ttl(key.encode("utf-8"))  # Cambiar el TTL
                    else:
                        print(
                            f"..Clave: {key_truncated}, Tiempo de expiración: {ttl_info}"
                        )
            print(f"Se encontraron {len(keys)} claves.")
        else:
            print(
                f'No se encontraron claves que coincidan con el patrón "{self.pattern}".'
            )

    @staticmethod
    def measure_execution_time(func) -> None:
        start_time = time.time()
        func()
        end_time = time.time()
        execution_time = end_time - start_time
        print(f"El script tardó {execution_time:.2f} segundos en ejecutarse.")

    def run(self) -> None:
        self.measure_execution_time(self.process_keys)
