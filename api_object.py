import datetime
import logger as log
import requests
import time


class ApiObject:
    req20 = 0
    req100 = 0
    timer1seg = 0
    timer2min = 0
    timer_method = 0
    url = ''

    def validate(self):
        if self.req20 == 0:
            self.timer1seg = datetime.datetime.now()
        if self.req100 == 0:
            self.timer2min = datetime.datetime.now()
        self.req20 += 1
        self.req100 += 1
        now = datetime.datetime.now()
        # 20 requests / seg constraint check
        aux = now - self.timer1seg
        if aux.total_seconds() <= 1.0:
            if self.req20 > 20:
                time.sleep(1.0 - aux.total_seconds())
                self.timer1seg = datetime.datetime.now()
                self.req20 = 1
        else:
            self.timer1seg = datetime.datetime.now()
            self.req20 = 1
        # 100 requests / 2 min constraint check
        aux = now - self.timer2min
        if aux.total_seconds() <= 120.0:
            if self.req100 > 100:
                time.sleep(120.0 - aux.total_seconds())
                self.timer2min = datetime.datetime.now()
                self.req100 = 1
        else:
            self.timer2min = datetime.datetime.now()
            self.req100 = 1

    def validate_key_limit(self, header):
        api_limit = header['X-App-Rate-Limit']
        api_current = header['X-App-Rate-Limit-Count']

        if api_current.split(',')[0].split(':')[0] == '1':
            self.timer1seg = datetime.datetime.now()

        if api_current.split(',')[1].split(':')[0] == '1':
            self.timer2min = datetime.datetime.now()

        if api_current.split(',')[0].split(':')[0] == api_limit.split(',')[0].split(':')[0]:
            now = datetime.datetime.now()
            aux = now - self.timer1seg
            time.sleep(int(api_limit.split(',')[0].split(':')[1]) - aux.total_seconds())

        if api_current.split(',')[1].split(':')[0] == api_limit.split(',')[1].split(':')[0]:
            now = datetime.datetime.now()
            aux = now - self.timer2min
            time.sleep(int(api_limit.split(',')[1].split(':')[1]) - aux.total_seconds())

    def validate_method_limit(self, header):
        method_limit = header['X-Method-Rate-Limit']
        method_current = header['X-Method-Rate-Limit-Count']

        if method_current.split(':')[0] == '1':
            self.timer_method = datetime.datetime.now()

        if method_current.split(':')[0] == method_limit.split(':')[0]:
            now = datetime.datetime.now()
            aux = now - self.timer_method
            time.sleep(int(method_limit.split(':')[1]) - aux.total_seconds())

    def request_json(self):
        response = requests.get(self.url)
        self.validate_key_limit(response.headers)
        self.validate_method_limit(response.headers)
        status_code = str(response.status_code)
        tries = 0

        # Any status code different than 200 it's an error
        while status_code != "200":
            error_message = "API Error: " + status_code

            # Request error, must finalize it
            if status_code in ["400", "401", "403", "405", "415"]:
                log.inform(self.url)
                log.inform(error_message, finalize=True)
            # Can be ignored
            elif status_code == "404":
                # log.inform(error_message)
                return None
            # Types of error that can be tried again
            else:
                try:
                    seconds = int(response.headers["Retry-After"])
                except Exception:
                    seconds = 15
                tries += 1

                if tries > 5:
                    return None

                error_message += " Waiting " + str(seconds) + " seconds..."
                log.inform(error_message)
                time.sleep(seconds)
                self.validate()
                response = requests.get(self.url)
                status_code = str(response.status_code)

        return response.json()
