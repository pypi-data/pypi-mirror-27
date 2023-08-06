
import os
import time
import subprocess
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SeleniumGrid:

    _compose_binary = None
    _compose_file = os.path.join(os.path.abspath(os.path.dirname(__file__)), 'docker-compose.yml')

    def __init__(self, num_nodes=1, shutdown_on_exit=False):

        self.num_nodes = num_nodes
        self.shutdown_on_exit = shutdown_on_exit

    def __enter__(self):
        self.start_grid(self.num_nodes)

    def __exit__(self, *args):
        if self.shutdown_on_exit:
            self.stop_grid()

    @property
    def compose_binary(self):
        if self._compose_binary is None:
            if 'DOCKER_COMPOSE_BIN' in os.environ:
                self._compose_binary = os.environ['DOCKER_COMPOSE_BIN']
            else:
                self._compose_binary = 'docker-compose'
        return self._compose_binary

    def compose_call(self, command):
        cmd = (
            '{compose_binary} -f {compose_file} {command}'
            .format(compose_binary=self.compose_binary, compose_file=self._compose_file, command=command)
        )
        return subprocess.check_output(cmd.split(' '))

    def start_grid(self, num_nodes=1):
        print('Starting grid with %s nodes' % num_nodes)
        self.compose_call('up -d --scale chrome={num_nodes}'.format(num_nodes=num_nodes))

    def stop_grid(self):
        print('Stopping grid')
        self.compose_call('down')


def get_remote_grid_driver():
    return webdriver.Remote(
        command_executor='http://localhost:4444/wd/hub',
        desired_capabilities=DesiredCapabilities.CHROME
    )


def grid_request(url, extra_sleep=None):
    driver = get_remote_grid_driver()
    driver.get(url)
    if extra_sleep:
        time.sleep(extra_sleep)
    source = driver.page_source
    driver.quit()
    return source
