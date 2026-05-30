# Typing Runtime Parity Matrix

## Purpose
Track runtime typing behavior coverage in this folder with two separate dimensions:
- MicroPython support status (Supported/Unsupported)
- Testability status (Covered/Partial/Missing/Unsupported)

Note: typing modules supported by MicroPython may not be available in all ports or boards



## Coverage Matrix

| Area | MicroPython | Testability | Test File(s) | Missing Sub-case / Reason |
| --- | --- | --- | --- | --- |
| typing symbol surface and aliases | Supported | Covered | tests/typing/check_typing_runtime.py | - |
| typing.Protocol runtime usage | Supported | Covered | tests/typing/check_typing_protocol_runtime.py | - |
| typing.NewType runtime behavior | Supported | Covered | tests/typing/check_typing_runtime.py | - |
| typing.Any permissive runtime behavior | Supported | Covered | tests/typing/check_typing_runtime.py | - |
| typing.AnyStr str/bytes mixed behavior | Supported | Covered | tests/typing/check_typing_runtime.py | - |
| typing.no_type_check usage | Supported | Covered | tests/typing/check_typing_runtime.py | - |
| typing.no_type_check class decorator usage | Supported | Covered | tests/typing/check_typing_runtime.py | - |
| typing.overload runtime pattern | Supported | Covered | tests/typing/check_typing_runtime.py | - |
| typing.TypedDict construction/runtime usage | Supported | Covered | tests/typing/check_typing_typeddict_runtime.py | - |
| typing.TypeVar runtime parameters | Supported | Covered | tests/typing/check_typing_runtime.py | - |
| typing.Generator annotation runtime path | Supported | Covered | tests/typing/check_typing_runtime.py | - |
| typing.NoReturn runtime raising path | Supported | Covered | tests/typing/check_typing_runtime.py | - |
| typing.Final runtime annotation path | Supported | Covered | tests/typing/check_typing_runtime.py | - |
| typing IO/TextIO/BinaryIO marker classes | Supported | Covered | tests/typing/check_typing_runtime.py | - |
| typing_extensions.TYPE_CHECKING | Supported | Covered | tests/typing/check_typing_runtime.py, tests/typing/check_typing_extensions_runtime.py | - |
| typing.TYPE_CHECKING branch runtime behavior | Supported | Covered | tests/typing/check_typing_runtime.py | Runtime-gated branch is asserted non-executing. |
| typing_extensions.TypeVar | Supported | Covered | tests/typing/check_typing_extensions_runtime.py | - |
| typing_extensions.Self | Supported | Covered | tests/typing/check_typing_extensions_runtime.py | - |
| typing_extensions.Generator | Supported | Covered | tests/typing/check_typing_extensions_runtime.py | - |
| __future__ module flags | Supported | Covered | tests/typing/check_future_module.py | - |
| __future__.annotations with cast runtime path | Supported | Covered | tests/typing/check_future_module.py | - |
| abc helper functions and abstract usage | Supported | Covered | tests/typing/check_abc_runtime.py | - |
| collections module basics | Supported | Covered | tests/typing/check_collections_runtime.py | - |
| collections.abc Mapping/Sequence | Supported | Covered | tests/typing/check_collections_abc_runtime.py | - |
| collections.abc Callable/Awaitable | Supported | Covered | tests/typing/check_collections_abc_runtime.py | - |
| collections.abc Iterable + Protocol callback | Supported | Covered | tests/typing/check_collections_abc_runtime.py | - |
| get_args/get_origin runtime behavior | Supported | Covered | tests/typing/check_typing_runtime.py | Current runtime returns minimal forms for tested parameterized cases; behavior is asserted. |
| typing.cast runtime call-arity validation | Supported | Covered | tests/typing/check_typing_runtime.py | Runtime TypeError for invalid argument count is asserted. |
| typing.LiteralString | Unsupported | Unsupported | tests/typing/check_typing_unsupported_runtime.py | Not provided by runtime typing module; asserted absent. |
| typing.reveal_type | Unsupported | Unsupported | tests/typing/check_typing_unsupported_runtime.py | Not provided by runtime typing module; asserted absent. |
| typing.TypedDict Required/NotRequired | Unsupported | Unsupported | tests/typing/check_typing_unsupported_runtime.py | Required/NotRequired are not available in runtime typing module. |
| typing.NamedTuple factory semantics | Unsupported | Covered | tests/typing/check_typing_unsupported_runtime.py | cpydiff: runtime difference is explicitly tested (MicroPython non-factory behavior). |
| typing.NewType class/introspection semantics | Unsupported | Covered | tests/typing/check_typing_unsupported_runtime.py | cpydiff: MicroPython exposes class-like semantics; CPython NewType object semantics differ. |
| typing.ParamSpec | Unsupported | Unsupported | tests/typing/check_typing_unsupported_runtime.py | Not provided by runtime typing module; asserted absent. |
| typing.final decorator | Unsupported | Unsupported | tests/typing/check_typing_unsupported_runtime.py | Decorator symbol is not available in runtime typing module; asserted absent. |
| typing_extensions.reveal_type | Unsupported | Unsupported | tests/typing/check_typing_extensions_runtime.py | Symbol is absent in this runtime package build; asserted as unsupported runtime difference. |
| typing_extensions.TypeVarTuple/Unpack | Unsupported | Unsupported | tests/typing/check_typing_extensions_runtime.py | Symbols are absent in this runtime package build; asserted as unsupported runtime difference. |
| abc.ABCMeta runtime difference | Unsupported | Covered | tests/typing/check_abc_runtime.py | cpydiff: runtime unsupported behavior is explicitly tested on MicroPython. |
| collections.namedtuple keyword arguments (rename/defaults) | Unsupported | Covered | tests/typing/check_collections_runtime.py | cpydiff: keyword arguments are unsupported in MicroPython runtime and asserted. |
| typing.runtime_checkable | Unsupported | Unsupported | tests/typing/check_typing_unsupported_runtime.py | Symbol is absent in runtime typing module; asserted absent. |
| Python 3.12 type statement syntax | Unsupported | Unsupported | tests/typing/check_typing_unsupported_syntax.py | Runtime asserts SyntaxError on MicroPython. |
| Python 3.12 type parameter syntax | Unsupported | Unsupported | tests/typing/check_typing_unsupported_syntax.py | Runtime asserts SyntaxError on MicroPython. |

## Status Legend

### MicroPython Support
- Supported: feature/behavior is available in the MicroPython runtime.
- Unsupported: feature/behavior is not available in the MicroPython runtime.

### Testability
- Covered: tests exist and verify the intended runtime behavior.
- Partial: tests exist but do not cover all scoped sub-cases.
- Missing: no runtime tests exist yet.
- Unsupported: behavior is intentionally out of runtime scope and tracked as unsupported.