from conductr_cli.test.cli_test_case import strip_margin, as_error
from conductr_cli.test.conduct_run_test_base import ConductRunTestBase
from conductr_cli import conduct_run, logging_setup
from unittest.mock import MagicMock


class TestConductRunCommand(ConductRunTestBase):

    def __init__(self, method_name):
        super().__init__(method_name)

        self.bundle_id = '45e0c477d3e5ea92aa8d85c0d8f3e25c'
        self.scale = 3
        self.default_args = {
            'dcos_mode': False,
            'command': 'conduct',
            'scheme': 'http',
            'host': '127.0.0.1',
            'port': 9005,
            'base_path': '/',
            'api_version': '1',
            'disable_instructions': False,
            'verbose': False,
            'quiet': False,
            'no_wait': False,
            'long_ids': False,
            'cli_parameters': '',
            'bundle': self.bundle_id,
            'scale': self.scale,
            'affinity': None,
            'conductr_auth': self.conductr_auth,
            'server_verification_file': self.server_verification_file
        }

        self.default_url = 'http://127.0.0.1:9005/bundles/45e0c477d3e5ea92aa8d85c0d8f3e25c?scale=3'

        self.output_template = """|Bundle run request sent.
                                  |Stop bundle with:         conduct stop{params} {bundle_id}
                                  |Print ConductR info with: conduct info{params}
                                  |Print bundle info with:   conduct info{params} {bundle_id}
                                  |"""

    def test_success(self):
        self.base_test_success()

    def test_success_verbose(self):
        self.base_test_success_verbose()

    def test_success_long_ids(self):
        self.base_test_success_long_ids()

    def test_success_with_custom_ip_port(self):
        self.base_test_success_with_custom_ip_port()

    def test_success_with_custom_host_port(self):
        self.base_test_success_with_custom_host_port()

    def test_success_ip(self):
        self.base_test_success_ip()

    def test_success_no_wait(self):
        self.base_test_success_no_wait()

    def test_failure(self):
        self.base_test_failure()

    def test_failure_invalid_address(self):
        self.base_test_failure_invalid_address()

    def test_failure_scale_timeout(self):
        self.base_test_failure_scale_timeout()

    def test_error_with_affinity_switch(self):
        args = {
            'host': '127.0.0.1',
            'port': 9005,
            'api_version': '1',
            'verbose': False,
            'no_wait': False,
            'long_ids': False,
            'cli_parameters': '',
            'bundle': self.bundle_id,
            'scale': self.scale,
            'affinity': 'other-bundle'
        }

        stderr = MagicMock()

        logging_setup.configure_logging(MagicMock(**args), err_output=stderr)
        result = conduct_run.run(MagicMock(**args))
        self.assertFalse(result)

        self.assertEqual(
            as_error(strip_margin("""|Error: Affinity feature is only available for v1.1 onwards of ConductR
                            |""")),
            self.output(stderr))
