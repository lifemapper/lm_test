"""Test the controller module."""
from lmtest.base.controller import CONTROLLER_PID_FILE, Controller


# .....................................................................................
class TestController:
    """Tests for the Controller class."""

    # ........................
    def test_instantiation(self):
        """Test that a Controller instance can be created."""
        _ = Controller(CONTROLLER_PID_FILE)
