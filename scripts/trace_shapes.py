"""Optional PyTorch forward-hook helper for shape tracing.

Usage in a trusted, local PyTorch experiment:

    from scripts.trace_shapes import attach_shape_hooks

    model.eval()
    handles = attach_shape_hooks(model, leaf_only=True)
    try:
        with torch.no_grad():
            prediction = model(example_input)
    finally:
        for h in handles:
            h.remove()

Module hooks do NOT expose functional operations such as torch.reshape,
F.softmax, or Tensor.permute. Use explicit assertions/prints for these.
This module never downloads models or executes external repository scripts.
"""

from __future__ import annotations

from typing import Any


def _describe(value: Any) -> Any:
    """Recursively show tensor shape/dtype without copying tensor data."""
    try:
        import torch
    except ImportError as exc:
        raise RuntimeError("Install PyTorch in your trusted experiment environment.") from exc

    if isinstance(value, torch.Tensor):
        return f"shape={tuple(value.shape)}, dtype={value.dtype}, device={value.device}"
    if isinstance(value, (list, tuple)):
        return [_describe(x) for x in value]
    if isinstance(value, dict):
        return {str(k): _describe(v) for k, v in value.items()}
    return type(value).__name__


def attach_shape_hooks(model: Any, *, leaf_only: bool = True, max_lines: int = 500):
    """Register bounded forward hooks; caller must remove returned handles.

    Parameters
    ----------
    model: torch.nn.Module
        An already constructed model in an environment you trust.
    leaf_only: bool
        Record only modules with no children. Set False for all named modules.
    max_lines: int
        Upper bound to avoid massive log output on long models.
    """
    try:
        import torch.nn as nn
    except ImportError as exc:
        raise RuntimeError("PyTorch is needed to trace module shapes.") from exc

    if not isinstance(model, nn.Module):
        raise TypeError("model must be an existing torch.nn.Module")
    if not isinstance(max_lines, int) or max_lines <= 0:
        raise ValueError("max_lines must be a positive integer")

    count = 0
    handles = []

    def make_hook(name: str):
        def hook(_module: Any, inputs: Any, outputs: Any):
            nonlocal count
            if count >= max_lines:
                return
            count += 1
            print(f"[{count:03d}] {name}: {_describe(inputs)} -> {_describe(outputs)}")
            if count == max_lines:
                print(f"[trace_shapes] Reached max_lines={max_lines}; further records hidden")
        return hook

    for name, module in model.named_modules():
        if not name:
            continue
        if leaf_only and any(module.children()):
            continue
        handles.append(module.register_forward_hook(make_hook(name)))
    return handles


if __name__ == "__main__":
    try:
        import torch
        import torch.nn as nn
    except ImportError:
        raise SystemExit("Demo requires PyTorch; library usage does not auto-install it.")

    class ToyForecast(nn.Module):
        def __init__(self, channels=3, lookback=16, horizon=4):
            super().__init__()
            self.projection = nn.Linear(lookback, horizon)
            self.channels = channels

        def forward(self, x):
            # x: [B, L, C] -> [B, C, L] -> linear -> [B, H, C]
            return self.projection(x.transpose(1, 2)).transpose(1, 2)

    torch.manual_seed(0)
    model = ToyForecast().eval()
    x = torch.randn(2, 16, 3)
    hooks = attach_shape_hooks(model)
    try:
        with torch.no_grad():
            output = model(x)
    finally:
        for h in hooks:
            h.remove()
    assert output.shape == (2, 4, 3)
    print("Verified toy output:", tuple(output.shape))
