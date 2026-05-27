# Test report

## Summary

Legend: **ok**=passed, **xfail**=expected failure, **xpass**=unexpected success, **skip**=test skipped (includes whole-file SKIP on this variant), **FAIL**=test failed, **ERROR**=test errored (also used when the test module crashed). Firmware sizes are reported in bytes from `size <binary>`.

| Variant | OK | xfail | xpass | skip | FAIL | ERROR | total | text | data | bss | size | Δsize |
|:---|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|---:|
| standard | 15 | 0 | 0 | 177 | 1 | 0 | 193 | 687_044 | 2_344 | 2_960 | 692_348 | ref |
| 1_mp-stubs | 134 | 24 | 0 | 10 | 2 | 23 | 193 | 691_364 | 2_344 | 2_960 | 696_668 | +4_320 |
| 2_typing_bundle | 142 | 26 | 3 | 9 | 9 | 4 | 193 | 688_868 | 2_344 | 2_960 | 694_172 | +1_824 |
| 2_typing_bundle_XL | 141 | 26 | 3 | 1 | 9 | 13 | 193 | 689_220 | 2_344 | 2_960 | 694_524 | +2_176 |
| 3_builtintypingmodule | 131 | 26 | 3 | 8 | 22 | 3 | 193 | 688_412 | 2_344 | 2_960 | 693_716 | +1_368 |

## typing/check_module.py
    probe module availability
    test import only

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestModuleIncluded | test_typing | skip | ok | ok | ok | ok |
| TestModuleIncluded | test_typing_extensions | skip | skip | ok | ok | ok |
| TestModuleIncluded | test_future | skip | ok | ok | ok | ok |
| TestModuleIncluded | test_abc | skip | ok | ok | ok | ok |
| TestModuleIncluded | test_collections | skip | ok | ok | ok | ok |
| TestModuleIncluded | test_collections_abc | skip | skip | skip | ok | skip |

## typing/check_module_collections.py
    collections module runtime checks.

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestCollectionsRuntime | test_collections_symbols_exist | **FAIL** | ok | ok | ok | **FAIL** |
| TestCollectionsRuntime | test_namedtuple_factory_path | ok | ok | ok | ok | ok |
| TestCollectionsRuntime | test_deque_and_ordereddict_basic_ops | ok | ok | ok | ok | ok |
| TestCollectionsRuntime | test_namedtuple_keyword_arguments_runtime_difference | ok | ok | ok | ok | ok |

## typing/check_module_collections_abc.py
    module: collections.abc 
    runtime parity checks.

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestCollectionsAbcRuntime | test_mapping_sequence_annotations | ok | ok | ok | ok | ok |
| TestCollectionsAbcRuntime | test_callable_awaitable_annotations | ok | ok | ok | ok | ok |
| TestCollectionsAbcRuntime | test_iterable_protocol_callback_path | ok | ok | ok | ok | ok |

## typing/check_module_future.py
    Tests for the MicroPython __future__ module runtime flags.

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestFutureModule | test_expected_feature_flags_exist | skip | ok | ok | ok | ok |
| TestFutureModule | test_feature_flags_are_true_booleans | skip | ok | ok | ok | **FAIL** |
| TestFutureModule | test_random_symbols_are_not_present | skip | ok | ok | ok | **FAIL** |
| TestFutureModule | test_future_annotations_with_cast_runtime_behavior | skip | ok | ok | ok | ok |

## typing/check_module_typing.py
    Runtime tests that mirror feat_typing execution patterns.

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestTypingRuntime | test_star_import_and_private_symbol | skip | ok | **ERROR** | **ERROR** | **ERROR** |
| TestTypingRuntime | test_self_in_callback_annotation | skip | ok | ok | ok | ok |
| TestTypingRuntime | test_no_type_check_with_stacked_decorators | skip | ok | ok | ok | ok |
| TestTypingRuntime | test_no_type_check_class_decorator_runtime | skip | ok | ok | ok | ok |
| TestTypingRuntime | test_annotated_calls_are_runtime_permissive | skip | ok | ok | ok | ok |
| TestTypingRuntime | test_typing_extensions_type_checking_import | skip | ok | ok | ok | ok |
| TestTypingRuntime | test_type_checking_gated_branch_is_runtime_false | skip | ok | ok | ok | ok |
| TestTypingRuntime | test_anystr_runtime_mixed_concat_behavior | skip | ok | ok | ok | ok |
| TestTypingRuntime | test_newtype_runtime_value_path | skip | ok | ok | ok | ok |
| TestTypingRuntime | test_overload_declaration_pattern | skip | ok | ok | ok | ok |
| TestTypingRuntime | test_typing_generator_runtime_path | skip | ok | ok | ok | ok |
| TestTypingRuntime | test_noreturn_runtime_path | skip | ok | ok | ok | ok |
| TestTypingRuntime | test_final_runtime_path | skip | ok | ok | ok | ok |
| TestTypingRuntime | test_io_marker_classes_runtime_path | skip | ok | **ERROR** | **ERROR** | ok |
| TestTypingMod | test_all_defined_names_exist | skip | ok | ok | ok | ok |
| TestTypingMod | test_constants_and_simple_aliases | skip | ok | **FAIL** | **FAIL** | **FAIL** |
| TestTypingMod | test_random_symbols_are_not_present | skip | ok | **FAIL** | **FAIL** | **FAIL** |
| TestTypingMod | test_function_return_values | skip | ok | **FAIL** | **FAIL** | **FAIL** |
| TestTypingMod | test_public_classes_instantiation_and_isinstance | skip | ok | **FAIL** | **FAIL** | ok |
| TestTypingMod | test_subscriptable_aliases | skip | ok | ok | ok | **FAIL** |
| TestTypingSpecDirectivesAndAliases | test_cast_returns_original_value | skip | ok | ok | ok | ok |
| TestTypingSpecDirectivesAndAliases | test_cast_arity_validation | skip | ok | ok | ok | **FAIL** |
| TestTypingSpecDirectivesAndAliases | test_decorator_identity_behavior | skip | ok | **FAIL** | **FAIL** | ok |
| TestTypingSpecDirectivesAndAliases | test_overload_runtime_placeholder | skip | ok | ok | ok | **FAIL** |
| TestTypingSpecDirectivesAndAliases | test_typevar_accepts_spec_parameters | skip | ok | ok | ok | **FAIL** |
| TestTypingSpecDirectivesAndAliases | test_newtype_runtime_behavior | skip | ok | ok | ok | ok |
| TestTypingSpecDirectivesAndAliases | test_origin_and_args_on_parameterized_forms | skip | ok | **FAIL** | **FAIL** | **FAIL** |

## typing/check_module_typing_extensions.py
    typing_extensions runtime parity checks from notebook scenarios.

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestTypingExtensionsRuntime | test_type_checking_bool | ok | ok | ok | ERROR | ok |
| TestTypingExtensionsRuntime | test_self_annotation_runtime_path | ok | ok | ok | ERROR | ok |
| TestTypingExtensionsRuntime | test_generator_annotation_runtime_path | ok | ok | ok | ERROR | ok |
| TestTypingExtensionsRuntime | test_reveal_type_runtime_path | ok | ok | ok | ERROR | ok |
| TestTypingExtensionsRuntime | test_typevar_tuple_symbols_optional | ok | ok | ok | ERROR | ok |
| TestTypingExtensionsRuntime | test_typevar_runtime_path | ok | ok | ok | ERROR | **FAIL** |
| TestTypingExtensionsRuntime | test_reveal_type_runtime_difference | ok | ok | ok | ERROR | **FAIL** |

## typing/check_typing_protocol_runtime.py
    Protocol runtime parity checks from the notebook scenarios.

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestTypingProtocolRuntime | test_protocol_adder_usage | skip | ok | ok | ok | ok |
| TestTypingProtocolRuntime | test_protocol_self_callback_usage | skip | ok | ok | ok | ok |

## typing/check_typing_typeddict_runtime.py
    TypedDict runtime parity checks from the notebook scenarios.

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestTypingTypedDictRuntime | test_typed_dict_construction_and_access | skip | ok | **FAIL** | **FAIL** | **FAIL** |
| TestTypingTypedDictRuntime | test_typed_dict_isinstance_runtime_difference | skip | ok | **ERROR** | **ERROR** | ok |
| TestTypingTypedDictRuntime | test_typevar_bound_typed_dict_runtime_path | skip | ok | ok | ok | ok |

## typing/check_typing_unsupported_runtime.py
    Additional typing spec coverage for runtime behavior and known unsupported parts.
    Spec index: https://typing.python.org/en/latest/spec/

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestTypingUnsupportedRuntime | test_missing_advanced_spec_symbols | skip | ok | **FAIL** | **FAIL** | **FAIL** |
| TestTypingUnsupportedRuntime | test_generic_parameterized_base_is_not_a_real_class | skip | ok | ok | ok | **ERROR** |
| TestTypingUnsupportedRuntime | test_namedtuple_factory_runtime_difference | skip | ok | **FAIL** | **FAIL** | **FAIL** |
| TestTypingUnsupportedRuntime | test_newtype_class_semantics_runtime_difference | skip | ok | ok | ok | ok |

## typing/check_typing_unsupported_syntax.py
    Unsupported syntax/runtime parity checks from notebook scenarios.

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestTypingUnsupportedSyntax | test_type_statement_runtime_difference | ok | ok | ok | ok | ok |
| TestTypingUnsupportedSyntax | test_type_parameter_syntax_runtime_difference | ok | ok | ok | ok | ok |

## typing/pep/typing_mod_collections_abc.py
    Python 3.3+
    module collections.abc
    https://peps.python.org/pep-3119/
    https://docs.python.org/3/library/collections.abc.html#module-collections.abc
    

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestCollectionsAbcImports | test_container_imports | skip | skip | skip | ok | skip |
| TestCollectionsAbcImports | test_sequence_imports | skip | skip | skip | ok | skip |
| TestCollectionsAbcImports | test_set_and_mapping_imports | skip | skip | skip | ok | skip |
| TestCollectionsAbcImports | test_async_imports | skip | skip | skip | ok | skip |
| TestCollectionsAbcImports | test_buffer_import | skip | skip | skip | ok | skip |

## typing/pep/typing_mod_typing_extensions.py
    Python 3.5
    module typing_extensions
    https://typing-extensions.readthedocs.io/

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestTypingExtensionsSpecialPrimitives | test_typing_extensions_module_imported | skip | skip | skip | ERROR | ok |
| TestTypingExtensionsSpecialPrimitives | test_typing_extensions_star_import | skip | skip | skip | ERROR | **ERROR** |

## typing/pep/typing_pep_0484.py
    Python 3.5
    PEP 484
    https://peps.python.org/topic/typing/
    https://peps.python.org/pep-0484/
    

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestPep484TypeDefinitionSyntax | test_function_annotation_runtime | skip | ok | ok | ok | ok |
| TestPep484TypeDefinitionSyntax | test_list_int_annotation_only | skip | ok | ok | ok | ok |
| TestPep484TypeAliases | test_simple_alias_runtime_path | skip | ok | ok | ok | ok |
| TestPep484Callable | test_callable_annotation_runtime | skip | ok | ok | ok | ok |
| TestPep484TypeVar | test_constrained_typevar_runtime | skip | ok | ok | ok | ok |
| TestPep484GenericUserClass | test_generic_t_base_class | skip | skip | skip | skip | skip |
| TestPep484UnionOptional | test_union_str_none_runtime | skip | ok | ok | ok | ok |
| TestPep484AnyAnnotation | test_any_dict_annotation_runtime | skip | ok | ok | ok | ok |
| TestPep484NewType | test_newtype_user_id_runtime | skip | ok | ok | ok | ok |
| TestPep484TypeCheckingGuard | test_type_checking_runtime_false | skip | ok | ok | ok | ok |
| TestPep484ForwardReference | test_forward_reference_in_method_annotation | skip | ok | ok | ok | ok |
| TestPep484NoReturn | test_noreturn_raises_runtime_error | skip | ok | ok | ok | ok |
| TestPep484Overload | test_overload_runtime_dispatch_to_impl | skip | ok | ok | ok | ok |
| TestPep484Cast | test_cast_runtime_identity | skip | ok | ok | ok | ok |

## typing/pep/typing_pep_0526.py
    Python 3.6
    PEP 526 - Syntax for variable annotations
    https://peps.python.org/pep-0526/
    
    Currently excludes tests using `Generic[T]` due to MicroPython runtime limitations

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestPep526Specification | test_basic_variable_annotation | skip | ok | ok | ok | ok |
| TestPep526GlobalLocalAnnotations | test_uninitialized_annotation | skip | ok | ok | ok | ok |
| TestPep526GlobalLocalAnnotations | test_conditional_annotated_assignment | skip | ok | ok | ok | ok |
| TestPep526GlobalLocalAnnotations | test_tuple_annotation_packing | skip | ok | ok | ok | ok |
| TestPep526GlobalLocalAnnotations | test_tuple_unpacking_annotations | skip | ok | ok | ok | ok |
| TestPep526GlobalLocalAnnotations | test_module_scope_annotation_no_binding | skip | ok | ok | ok | ok |
| TestPep526GlobalLocalAnnotations | test_local_scope_annotation_unbound | skip | xfail | xfail | xfail | xfail |
| TestPep526GlobalLocalAnnotations | test_reannotation_runtime | skip | ok | ok | ok | ok |
| TestPep526ClassAndInstanceAnnotations | test_basic_starship_class | skip | ok | ok | ok | ok |
| TestPep526ClassAndInstanceAnnotations | test_starship_with_init_and_hit | skip | ok | ok | ok | ok |
| TestPep526Generics | test_user_defined_generic_class | skip | ok | ok | ok | skip |
| TestPep526AnnotatingExpressions | test_attribute_and_subscript_annotations | skip | ok | ok | ok | ok |
| TestPep526AnnotatingExpressions | test_parenthesized_name_annotation | skip | ok | ok | ok | ok |
| TestPep526RuntimeEffects | test_annotation_with_undefined_name_in_function_body | skip | ok | ok | ok | ok |
| TestPep526RuntimeEffects | test_module_level_annotation_undefined_name_raises | skip | xfail | xfail | xfail | xfail |
| TestPep526RuntimeEffects | test_class_body_annotation_undefined_name_raises | skip | xfail | xfail | xfail | xfail |
| TestPep526RuntimeEffects | test_module_annotations_dict_runtime | skip | xfail | xfail | xfail | xfail |
| TestPep526RuntimeEffects | test_string_annotations_runtime | skip | ok | ok | ok | ok |

## typing/pep/typing_pep_0544.py
    Python 3.8
    PEP 544 - Protocols: Structural subtyping (static duck typing)
    https://peps.python.org/topic/typing/
    https://peps.python.org/pep-0544/
    

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestPep544DefiningAProtocol | test_supports_close_protocol | skip | ok | ok | ok | ok |
| TestPep544ProtocolMembers | test_protocol_with_default_and_abstract | skip | ok | ok | ok | ok |
| TestPep544ProtocolMembers | test_protocol_with_attributes | skip | ok | ok | ok | ok |
| TestPep544ExplicitlyDeclaringImplementation | test_explicit_protocol_subclass | skip | ok | ok | ok | ok |
| TestPep544ExplicitlyDeclaringImplementation | test_rgb_protocol | skip | ok | ok | ok | ok |
| TestPep544MergingAndExtending | test_sized_and_closable_with_protocol | skip | ok | ok | ok | **FAIL** |
| TestPep544MergingAndExtending | test_sized_and_closable_inheriting_protocols | skip | ok | ok | ok | **FAIL** |
| TestPep544GenericProtocols | test_generic_protocol | skip | **FAIL** | ok | ok | **FAIL** |
| TestPep544RecursiveProtocols | test_recursive_traversable | skip | ok | ok | ok | ok |
| TestPep544SelfTypesInProtocols | test_copyable_self_type | skip | ok | ok | ok | ok |
| TestPep544CallbackProtocols | test_combiner_callback_protocol | skip | ok | ok | ok | ok |
| TestPep544UnionsAndIntersections | test_finish_union_of_protocols | skip | ok | ok | ok | ok |
| TestPep544UnionsAndIntersections | test_hashable_floats_intersection | skip | ok | ok | ok | **FAIL** |
| TestPep544TypeAndClassObjectsVsProtocols | test_type_of_protocol_with_concrete | skip | ok | ok | ok | ok |
| TestPep544TypeAndClassObjectsVsProtocols | test_instantiate_abstract_protocol_raises | skip | xfail | xfail | xfail | xfail |
| TestPep544TypeAndClassObjectsVsProtocols | test_class_object_vs_protocol_assignment | skip | ok | ok | ok | ok |
| TestPep544NewTypeAndAliases | test_newtype_over_protocol | skip | ok | ok | ok | ok |
| TestPep544NewTypeAndAliases | test_sized_iterable_generic_protocol | skip | xfail | **xpass** | **xpass** | xfail |
| TestPep544RuntimeCheckable | test_runtime_checkable_supports_close | skip | xfail | xfail | xfail | xfail |
| TestPep544RuntimeCheckable | test_protocol_with_property_default | skip | ok | ok | ok | ok |
| TestPep544TypingProtocols | test_supports_protocols_importable | skip | ok | ok | ok | ok |

## typing/pep/typing_pep_0560.py
    Python 3.7
    PEP 560 - Type Hinting Generics In Standard Collections

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestPep560ClassGetItem | test_instance_getitem_on_user_class | skip | ok | ok | ok | ok |
| TestPep560ClassGetItem | test_class_getitem_on_user_class | skip | xfail | xfail | xfail | xfail |
| TestPep560MroEntries | test_generic_alias_mro_entries | skip | xfail | xfail | xfail | xfail |

## typing/pep/typing_pep_0586.py
    Python 3.8
    PEP 586 - Literal Types
    https://peps.python.org/pep-0586

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestPep586LegalParameters | test_literal_parameter_forms_runtime | skip | ok | ok | ok | ok |
| TestPep586LegalParameters | test_literal_alias_grouping | skip | ok | ok | ok | ok |
| TestPep586LegalParameters | test_literal_nested_subscription | skip | ok | ok | ok | **FAIL** |
| TestPep586ParametersAtRuntime | test_literal_annotated_function_runtime | skip | ok | ok | ok | ok |
| TestPep586ParametersAtRuntime | test_literal_function_value_assignment | skip | ok | ok | ok | ok |
| TestPep586NonLiteralsInLiteralContexts | test_literal_str_passthrough_runtime | skip | ok | ok | ok | ok |
| TestPep586NonLiteralsInLiteralContexts | test_runner_with_arbitrary_string | skip | ok | ok | ok | ok |
| TestPep586IntelligentIndexing | test_tuple_indexed_by_literal_runtime | skip | ok | ok | ok | ok |
| TestPep586IntelligentIndexing | test_getattr_literal_keys_on_class | skip | ok | ok | ok | ok |
| TestPep586OverloadsInteraction | test_overload_with_literal_modes | skip | ok | ok | ok | ok |
| TestPep586GenericsInteraction | test_generic_matrix_class_with_literal | skip | xfail | xfail | xfail | xfail |
| TestPep586EnumsAndExhaustiveness | test_status_enum_exhaustiveness | skip | xfail | xfail | xfail | xfail |

## typing/pep/typing_pep_0589.py
    Python 3.8
    PEP 589 - TypedDict
    https://peps.python.org/topic/typing/
    https://peps.python.org/pep-0589/
    https://typing.python.org/en/latest/spec/typeddict.html#typeddict

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestPep589ClassBasedSyntax | test_class_based_typeddict_definition | skip | ok | ok | ok | ok |
| TestPep589UsingTypedDictTypes | test_typed_dict_function_argument | skip | ok | ok | ok | ok |
| TestPep589TotalityAndOptionalKeys | test_typeddict_total_true | skip | xfail | xfail | xfail | xfail |
| TestPep589TotalityAndOptionalKeys | test_typeddict_total_false | skip | xfail | xfail | xfail | xfail |
| TestPep589InheritanceMix | test_point2d_typed_dict | skip | ok | ok | ok | ok |
| TestPep589InheritanceMix | test_point3d_total_false_subclass | skip | xfail | xfail | xfail | xfail |
| TestPep589RuntimeIsInstance | test_typeddict_isinstance_check | skip | xfail | xfail | xfail | xfail |
| TestPep589FunctionalSyntax | test_functional_typeddict_construction | skip | **FAIL** | ok | ok | ok |
| TestPep589FunctionalSyntax | test_functional_typeddict_constructor_kwargs | skip | xfail | xfail | xfail | xfail |
| TestPep589InheritanceExamples | test_book_based_movie_inherits_movie | skip | ok | ok | ok | ok |
| TestPep589InheritanceExamples | test_multiple_inheritance_typed_dicts | skip | xfail | **xpass** | **xpass** | xfail |
| TestPep589TotalityWithRequiredNotRequired | test_movie_mix_with_total_false | skip | xfail | xfail | xfail | xfail |
| TestPep589TotalityWithRequiredNotRequired | test_movie_mix2_with_notrequired | skip | ok | ok | ok | ok |
| TestPep589AnnotatedReadOnly | test_band_with_readonly_members | skip | ok | ok | ok | ok |
| TestPep589ExtraItemsAndClosed | test_typeddict_extra_items_int | skip | xfail | xfail | xfail | xfail |
| TestPep589ExtraItemsAndClosed | test_typeddict_closed_true | skip | xfail | xfail | xfail | xfail |
| TestPep589MappingInteraction | test_intdict_extra_items_and_clear | skip | xfail | xfail | xfail | xfail |

## typing/pep/typing_pep_0591.py
    Python 3.8
    PEP 0591 - Final qualifier for types
    https://peps.python.org/pep-0591/

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestFinalDecorator | test_final_decorator_on_class | skip | ok | ok | ok | ok |
| TestFinalDecorator | test_inherit_from_final_class_runtime | skip | ok | ok | ok | ok |
| TestFinalDecorator | test_final_decorator_on_method | skip | ok | ok | ok | ok |
| TestFinalAnnotation | test_final_annotation_with_value | skip | ok | ok | ok | ok |
| TestFinalSemantics | test_final_module_reassignment_runtime | skip | ok | ok | ok | ok |
| TestFinalSemantics | test_final_class_attribute_assignment_runtime | skip | ok | ok | ok | ok |
| TestFinalWithContainers | test_final_with_list_container_runtime | skip | ok | ok | ok | ok |
| TestFinalWithContainers | test_final_list_param_runtime | skip | ok | ok | ok | ok |
| TestFinalWithContainers | test_final_mutable_container_remains_mutable | skip | ok | ok | ok | ok |
| TestFinalWithNamedTuple | test_namedtuple_with_final_field_names | skip | xfail | xfail | xfail | **xpass** |

## typing/pep/typing_pep_3119.py
    Python 3.0+
    module abc
    https://peps.python.org/pep-3119/
    https://docs.python.org/3/library/abc.html#module-abc

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestPep3119AbcBase | test_import_abc_and_subclass | skip | ok | ok | ok | ok |
| TestPep3119AbstractMethod | test_import_abstractmethod | skip | ok | ok | ok | ok |
| TestPep3119AbstractMethod | test_define_abstract_class_with_decorators | skip | ok | ok | ok | ok |
| TestPep3119AbcGetCacheToken | test_abc_get_cache_token | skip | xfail | **xpass** | **xpass** | **xpass** |

## typing/pep/typing_runtime.py
    Testing runtime aspects of typing module
    Python 3.5+
    Miscellaneous typing module runtime tests.

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestTypingTypeCheckingFlag | test_type_checking_branch | skip | ERROR | ok | ok | ok |
| TestTypingParameterAnnotations | test_simple_annotated_functions | skip | ERROR | ok | ok | ok |
| TestTypingSelfPython311 | test_self_in_callback | skip | ERROR | ok | ok | ok |
| TestTypingNoTypeCheck | test_no_type_check_decorator | skip | ERROR | ok | ok | ok |
| TestTypingProtocolRuntime | test_adder_protocol_runtime | skip | ERROR | ok | ok | ok |
| TestTypingNewType | test_user_id_newtype | skip | ERROR | ok | ok | ok |
| TestTypingAny | test_any_assignments | skip | ERROR | ok | ok | ok |
| TestTypingAny | test_hash_b_runtime | skip | ERROR | ok | ok | ok |
| TestTypingAnyStr | test_concat_homogeneous | skip | ERROR | ok | ok | ok |
| TestTypingAnyStr | test_concat_mixed_types_raises | skip | ERROR | ok | ok | ok |
| TestTypingLiteralString | test_caller_uses_literal_and_runtime_str | skip | ERROR | ok | ok | ok |
| TestTypingOverload | test_bar_overload_runtime | skip | ERROR | ok | ok | ok |
| TestTypingTypedDictRequired | test_movie_required_notrequired | skip | ERROR | **ERROR** | **ERROR** | **FAIL** |
| TestTypingTypeVar | test_first_helper | skip | ERROR | ok | ok | ok |
| TestTypingGenerator | test_echo_generator | skip | ERROR | ok | ok | ok |
| TestTypingNoReturn | test_stop_no_return | skip | ERROR | ok | ok | ok |
| TestTypingFinalAnnotation | test_final_constant | skip | ERROR | ok | ok | ok |
| TestTypingFinalDecorator | test_final_method_and_class | skip | ERROR | xfail | xfail | xfail |
| TestTypingTypeVarTuple | test_typevar_tuple_unpack | skip | ERROR | xfail | xfail | xfail |
| TestTypingParamSpec | test_add_logging_with_paramspec | skip | ERROR | xfail | xfail | xfail |
| TestTypingGetOrigin | test_get_origin_non_none | skip | ERROR | xfail | xfail | xfail |
| TestTypingGetArgs | test_get_args_non_empty | skip | ERROR | xfail | xfail | xfail |
| TestTypingSubscriptables | test_subscriptable_aliases | skip | ERROR | ok | ok | ok |

## typing/pep/typing_syntax.py
    This doesn't quite test everything but just serves to verify that basic syntax works,
    which for MicroPython means everything typing-related should be ignored.

| Class | Test | standard | 1_mp-stubs | 2_typing_bundle | 2_typing_bundle_XL | 3_builtintypingmodule |
|---|---|---|---|---|---|---|
| TestTypingSyntax | test_typing_assigment_rejected | skip | xfail | xfail | xfail | **xpass** |
| TestTypingSyntax | test_module_level_annotations_and_function | skip | ok | ok | ok | ok |
