import time

import docker
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


class SeleniumNode:
    client = docker.from_env()

    def __init__(self, image='selenium/standalone-chrome'):
        self.image = image
        self.container = None

    def __enter__(self):
        print('Starting %s node' % self.image)
        self.container = self.client.containers.run(self.image, ports={4444: None}, detach=True, shm_size='2g')
        addr = self.client.api.inspect_container(self.container.id)['NetworkSettings']['Ports']['4444/tcp']
        self.addr = '%s:%s' % (addr[0]['HostIp'], addr[0]['HostPort'])
        time.sleep(1.5)
        self.driver = webdriver.Remote(
            command_executor='http://%s/wd/hub' % self.addr,
            desired_capabilities=DesiredCapabilities.CHROME
        )
        return self

    def __exit__(self, *args):
        self.driver.quit()
        self.container.stop()
        self.container.remove()

    def get(self, **kwargs):
        return self.driver.get(**kwargs)
