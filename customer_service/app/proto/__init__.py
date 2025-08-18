# Makes this directory a Python package
# Also makes python files generated from .proto work with relative paths

import os
import sys

sys.path.insert(0, os.path.dirname(__file__))

try:
    from . import customer_pb2
    from . import customer_pb2_grpc
    from . import order_pb2
    from . import order_pb2_grpc
    from . import common_pb2
except ImportError:
    pass  