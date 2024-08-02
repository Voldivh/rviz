from resource_retriever_msgs.srv import ResourceRetrieverService

import rclpy
from rclpy.executors import ExternalShutdownException
from rclpy.node import Node

from urllib.request import urlopen
from urllib.error import URLError


class ResourceRetrieverServer(Node):

    def __init__(self):
        super().__init__('resource_retriever_server')
        self.srv = self.create_service(ResourceRetrieverService, 'resource_retriever', self.resource_retriever_callback)

    def resource_retriever_callback(self, request, response):
        self.get_logger().info('Incoming request\n: %s' % (request.path))
        filename = 'file://' + request.path
        try:
            response.status_code = 1
            response.body = urlopen(filename).read()
        except URLError as e:
            raise Exception('Invalid URL: {} \nError {}'.format(filename, e))

        return response


def main():
    try:
        with rclpy.init():
            resource_retriever_server = ResourceRetrieverServer()
            rclpy.spin(resource_retriever_server)
    except (KeyboardInterrupt, ExternalShutdownException):
        pass


if __name__ == '__main__':
    main()