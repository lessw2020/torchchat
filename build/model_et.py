# Copyright (c) Meta Platforms, Inc. and affiliates.
# All rights reserved.

# This source code is licensed under the license found in the
# LICENSE file in the root directory of this source tree.

import torch
import torch.nn as nn
from executorch.extension.pybindings import portable_lib as exec_lib

# ET changed the way it's loading the custom ops so it's not included in portable_lib but has to be loaded separately.
from executorch.examples.models.llama2.custom_ops import sdpa_with_kv_cache # no-qa

class PTEModel(nn.Module):
    def __init__(self, config, path) -> None:
        super().__init__()
        self.config = config
        self.model_ = exec_lib._load_for_executorch(str(path))

    def forward(self, x, input_pos):
        # model_.forward expects inputs to be wrapped in a tuple
        forward_inputs = (x.to(torch.long), input_pos.to(torch.long))
        logits = self.model_.forward(forward_inputs)

        # After wrapping in a tuple, we get a list back, so we need to grab
        # the first element to get the tensor
        assert len(logits) == 1
        logits = logits[0]
        return logits

    def setup_caches(self, max_batch_size, max_seq_length):
        pass
