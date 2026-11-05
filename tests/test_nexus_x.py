import ipaddress
import unittest

import nexus_x


class NexusXCoreTests(unittest.TestCase):
    def test_exactly_28_unique_tools_are_registered(self):
        tools = [entry for _, group in nexus_x.GROUPS for entry in group]
        self.assertEqual(len(tools), 28)
        self.assertEqual(len({number for number, _, _ in tools}), 28)
        self.assertTrue(all(callable(handler) for _, _, handler in tools))

    def test_tool_numbers_are_contiguous(self):
        numbers = sorted(number for _, group in nexus_x.GROUPS for number, _, _ in group)
        self.assertEqual(numbers, list(range(1, 29)))

    def test_subnet_calculation(self):
        network = ipaddress.ip_interface("192.168.1.10/24").network
        self.assertEqual(str(network.network_address), "192.168.1.0")
        self.assertEqual(str(network.broadcast_address), "192.168.1.255")


if __name__ == "__main__":
    unittest.main()
