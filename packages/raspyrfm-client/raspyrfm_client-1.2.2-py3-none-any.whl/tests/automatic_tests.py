import unittest
from builtins import print

import rstr

from raspyrfm_client import RaspyRFMClient
from raspyrfm_client.device_implementations.gateway.manufacturer.gateway_constants import GatewayModel
from raspyrfm_client.device_implementations.manufacturer_constants import Manufacturer


class TestStringMethods(unittest.TestCase):
    def test_random_controlunit_config(self):
        """
        Tests all device_implementations with random configurations.
        """

        rfm_client = RaspyRFMClient()

        from raspyrfm_client.device_implementations.controlunit.base import ControlUnit

        def test_device(device: ControlUnit):
            """
            Tests random device_implementations configurations for the specified device_implementations
            
            :param device: the device_implementations to test 
            """

            self.assertIsNotNone(device.get_manufacturer())
            self.assertIsNotNone(device.get_model())
            self.assertIsNotNone(device.get_supported_actions())

            channel_config_args = device.get_channel_config_args()

            # tests 50 randomly chosen configurations
            for i in range(50):
                channel_config = {}

                for arg in channel_config_args:
                    channel_config[arg] = rstr.xeger(channel_config_args[arg])

                device.set_channel_config(**channel_config)

                # create gateway instance
                gateway = rfm_client.get_gateway(Manufacturer.INTERTECHNO, GatewayModel.ITGW)

                for action in device.get_supported_actions():
                    generated_code = gateway.generate_code(device, action)
                    self.assertIsNotNone(generated_code)

        def test_models(manufacturer: Manufacturer):
            """
            Tests all models of the specified manufacturer
            
            :param manufacturer:  manufacturer to test all available models
            """
            for model in rfm_client.get_supported_controlunit_models(manufacturer):
                print("Testing " + model.value)
                device = rfm_client.get_controlunit(manufacturer, model)
                test_device(device)

        for manufacturer in rfm_client.get_supported_controlunit_manufacturers():
            test_models(manufacturer)

        print("All random config device_implementations tests passed!")

    def test_gateway_init(self):

        rfm_client = RaspyRFMClient()

        from raspyrfm_client.device_implementations.gateway.base import Gateway

        def test_gateway(gateway: Gateway):
            self.assertIsNotNone(gateway)

        def test_models(manufacturer: Manufacturer):
            for model in rfm_client.get_supported_gateway_models(manufacturer):
                gateway = rfm_client.get_gateway(manufacturer, model)
                test_gateway(gateway)

        for manufacturer in rfm_client.get_supported_gateway_manufacturers():
            test_models(manufacturer)


if __name__ == '__main__':
    unittest.main()
