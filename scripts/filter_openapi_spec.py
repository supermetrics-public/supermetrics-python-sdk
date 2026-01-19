#!/usr/bin/env python3
"""
OpenAPI Specification Filter and Merger

Reads multiple OpenAPI YAML files from openapi-specs/ directory,
filters endpoints based on scripts/references/sdk-endpoint-filters.yaml configuration,
and merges them into a single openapi-spec.yaml file.

Features:
- Detects and fails on duplicate METHOD|PATH across multiple specs
- Filters paths/operations matching inclusion list
- Applies patches/overrides to endpoints via merge or replace operations
- Applies patches/overrides to components (schemas, responses, etc.)
- Collects all referenced schemas via $ref traversal
- Merges filtered paths into single spec
- Uses custom metadata for general-purpose SDK
"""

import sys
from pathlib import Path
from typing import Dict, Set, List, Tuple, Any, Optional
import yaml
import re
from copy import deepcopy


def load_yaml_file(file_path: Path) -> Dict[str, Any]:
    """Load and parse a YAML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml_file(file_path: Path, data: Dict[str, Any]) -> None:
    """Save data to a YAML file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def deep_merge(base: Dict[str, Any], updates: Dict[str, Any]) -> Dict[str, Any]:
    """
    Deep merge two dictionaries. Updates are merged into base.
    Lists in updates replace lists in base (no concatenation).
    """
    result = deepcopy(base)

    for key, value in updates.items():
        if key in result and isinstance(result[key], dict) and isinstance(value, dict):
            # Recursively merge nested dictionaries
            result[key] = deep_merge(result[key], value)
        else:
            # Replace the value (includes lists, primitives, and new keys)
            result[key] = deepcopy(value)

    return result


def apply_patches(operation: Dict[str, Any], patches: Dict[str, Any]) -> Dict[str, Any]:
    """
    Apply patches to an OpenAPI operation definition.

    Supports two patch types:
    - merge: Deep merge patches into the operation
    - replace: Completely replace specific sections

    Args:
        operation: The original operation definition
        patches: Dictionary with 'merge' and/or 'replace' keys

    Returns:
        The patched operation definition
    """
    result = deepcopy(operation)

    # Apply merge patches first (deep merge)
    if 'merge' in patches and isinstance(patches['merge'], dict):
        result = deep_merge(result, patches['merge'])

    # Apply replace patches (complete replacement)
    if 'replace' in patches and isinstance(patches['replace'], dict):
        for key, value in patches['replace'].items():
            result[key] = deepcopy(value)

    return result


def load_endpoint_config(config_file: Path) -> Tuple[Set[Tuple[str, str]], Dict[Tuple[str, str], Dict[str, Any]], Dict[str, Dict[str, Dict[str, Any]]]]:
    """
    Load endpoint configuration from sdk-endpoint-filters.yaml.

    Returns:
        Tuple of (endpoints_set, endpoint_patches_dict, component_patches_dict)
        - endpoints_set: Set of (METHOD, PATH) tuples to include
        - endpoint_patches_dict: Dict mapping (METHOD, PATH) to endpoint patch configuration
        - component_patches_dict: Dict mapping component_type -> component_name -> patches
    """
    config = load_yaml_file(config_file)
    endpoints = set()
    endpoint_patches_map = {}
    component_patches = {}

    # Load endpoints
    if 'endpoints' not in config or not isinstance(config['endpoints'], list):
        print(f"⚠️  Warning: No 'endpoints' list found in {config_file.name}")
    else:
        for idx, endpoint_config in enumerate(config['endpoints']):
            if not isinstance(endpoint_config, dict):
                print(f"⚠️  Skipping invalid endpoint config at index {idx}: not a dictionary")
                continue

            # Extract method and path
            method = endpoint_config.get('method', '').strip().upper()
            path = endpoint_config.get('path', '').strip()

            if not method or not path:
                print(f"⚠️  Skipping endpoint at index {idx}: missing method or path")
                continue

            endpoint_key = (method, path)
            endpoints.add(endpoint_key)

            # Extract patches if present
            if 'patches' in endpoint_config and isinstance(endpoint_config['patches'], dict):
                endpoint_patches_map[endpoint_key] = endpoint_config['patches']

    # Load component patches
    if 'component_patches' in config and isinstance(config['component_patches'], dict):
        for comp_type, components in config['component_patches'].items():
            if not isinstance(components, dict):
                print(f"⚠️  Skipping invalid component_patches for '{comp_type}': not a dictionary")
                continue

            component_patches[comp_type] = components

    return endpoints, endpoint_patches_map, component_patches


def extract_refs(obj: Any, refs: Set[str]) -> None:
    """Recursively extract all $ref references from an object."""
    if isinstance(obj, dict):
        if '$ref' in obj:
            refs.add(obj['$ref'])
        for value in obj.values():
            extract_refs(value, refs)
    elif isinstance(obj, list):
        for item in obj:
            extract_refs(item, refs)


def resolve_component_name(ref: str) -> Tuple[str, str]:
    """
    Parse a $ref like '#/components/schemas/LoginLink'
    Returns (component_type, component_name) e.g., ('schemas', 'LoginLink')
    """
    # Remove leading '#/components/'
    if not ref.startswith('#/components/'):
        return None, None

    parts = ref.replace('#/components/', '').split('/')
    if len(parts) < 2:
        return None, None

    component_type = parts[0]  # e.g., 'schemas', 'responses', 'parameters'
    component_name = parts[1]

    return component_type, component_name


def collect_component_dependencies(
    component_obj: Any,
    all_components: Dict[str, Dict[str, Any]],
    component_type: str,
    collected: Dict[str, Set[str]]
) -> None:
    """Recursively collect all component dependencies via $ref traversal."""
    refs = set()
    extract_refs(component_obj, refs)

    # Sort refs for consistent order
    for ref in sorted(refs):
        ref_type, ref_name = resolve_component_name(ref)
        if not ref_type or not ref_name:
            continue

        # Skip if already collected
        if ref_name in collected.get(ref_type, set()):
            continue

        # Add to collected set
        if ref_type not in collected:
            collected[ref_type] = set()
        collected[ref_type].add(ref_name)

        # Recursively collect dependencies of this component
        if ref_type in all_components and ref_name in all_components[ref_type]:
            collect_component_dependencies(
                all_components[ref_type][ref_name],
                all_components,
                ref_type,
                collected
            )


def resolve_external_file_reference(
    ref_path: str,
    base_path: Path,
    ref_anchor: str,
    resolved_cache: Dict[str, Any]
) -> Dict[str, Any] | None:
    """
    Resolve an external file reference by loading the file and extracting the component.
    Recursively resolves nested external references.

    Args:
        ref_path: The file path from the $ref (e.g., "../shared/responses/CommonResponses.yaml")
        base_path: The base directory to resolve relative paths from
        ref_anchor: The anchor/fragment part after # (e.g., "/BadRequest")
        resolved_cache: Cache of already resolved references to avoid infinite loops

    Returns:
        The resolved component definition or None if file not found.
    """
    # Create a cache key for this reference
    cache_key = f"{ref_path}#{ref_anchor}"

    # Check if already resolved (avoid infinite loops)
    if cache_key in resolved_cache:
        return resolved_cache[cache_key]

    try:
        # Resolve the file path relative to base_path
        full_path = (base_path / ref_path).resolve()

        if not full_path.exists():
            return None

        # Load the YAML file
        external_spec = load_yaml_file(full_path)

        # Navigate to the component using the anchor
        # Anchor format is typically like "#/BadRequest" or "#/components/responses/BadRequest"
        anchor_parts = ref_anchor.strip('#/').split('/')

        component = external_spec
        for part in anchor_parts:
            if isinstance(component, dict) and part in component:
                component = component[part]
            else:
                return None

        # Cache this result
        resolved_cache[cache_key] = component

        # Recursively resolve any nested external references in this component
        component = resolve_nested_external_refs(component, full_path.parent, resolved_cache)

        return component

    except Exception as e:
        print(f"      Error loading external file {ref_path}: {e}")
        return None


def resolve_nested_external_refs(
    obj: Any,
    base_path: Path,
    resolved_cache: Dict[str, Any]
) -> Any:
    """
    Recursively resolve external file references within an object.

    Args:
        obj: The object to process (dict, list, or primitive)
        base_path: The base directory for resolving relative paths
        resolved_cache: Cache of already resolved references

    Returns:
        The object with all external references resolved inline.
    """
    if isinstance(obj, dict):
        result = {}
        for key, value in obj.items():
            # Check if this is an external $ref
            if key == '$ref' and isinstance(value, str):
                if '.yaml' in value or '.yml' in value:
                    # Parse and resolve the external reference
                    if '#' in value:
                        ref_file, ref_anchor = value.split('#', 1)
                    else:
                        ref_file = value
                        ref_anchor = ''

                    resolved = resolve_external_file_reference(
                        ref_file,
                        base_path,
                        ref_anchor,
                        resolved_cache
                    )

                    if resolved:
                        # Replace the $ref with the resolved content
                        return resolved
                    else:
                        # Keep the broken ref as-is
                        result[key] = value
                else:
                    # Internal ref, keep as-is
                    result[key] = value
            else:
                # Recursively process the value
                result[key] = resolve_nested_external_refs(value, base_path, resolved_cache)
        return result
    elif isinstance(obj, list):
        return [resolve_nested_external_refs(item, base_path, resolved_cache) for item in obj]
    else:
        # Primitive value, return as-is
        return obj


def resolve_external_references(
    components: Dict[str, Dict[str, Any]],
    specs_dir: Path
) -> Tuple[int, int]:
    """
    Replace external file references by loading and resolving them recursively.
    Returns (replaced_count, failed_count).
    """
    replaced_count = 0
    failed_count = 0
    resolved_cache: Dict[str, Any] = {}

    for comp_type in ['responses', 'schemas', 'parameters', 'headers']:
        if comp_type not in components:
            continue

        comp_dict = components[comp_type]
        components_to_replace = {}

        for comp_name, comp_value in list(comp_dict.items()):
            # Check if this is just an external file reference
            if isinstance(comp_value, dict) and len(comp_value) == 1 and '$ref' in comp_value:
                ref_value = comp_value['$ref']

                # Check if it's an external file reference (not internal #/components/...)
                if '.yaml' in ref_value or '.yml' in ref_value:
                    # Parse the reference: "file.yaml#/ComponentName"
                    if '#' in ref_value:
                        ref_file, ref_anchor = ref_value.split('#', 1)
                    else:
                        ref_file = ref_value
                        ref_anchor = ''

                    # Try to resolve the external reference
                    resolved_def = resolve_external_file_reference(
                        ref_file,
                        specs_dir,
                        ref_anchor,
                        resolved_cache
                    )

                    if resolved_def:
                        components_to_replace[comp_name] = resolved_def
                        replaced_count += 1
                        print(f"   ✓ Resolved external ref: {comp_type}/{comp_name}")
                        print(f"      From: {ref_value}")
                    else:
                        failed_count += 1
                        print(f"   ❌ Failed to resolve: {comp_type}/{comp_name}")
                        print(f"      File not found or invalid: {ref_value}")
                        print(f"      Removing this component (will cause validation errors)")
                        # Remove the component entirely to avoid broken refs
                        components_to_replace[comp_name] = None

        # Apply replacements and removals
        for comp_name, new_value in components_to_replace.items():
            if new_value is None:
                # Remove the component
                if comp_name in comp_dict:
                    del comp_dict[comp_name]
            else:
                # Replace with resolved definition
                comp_dict[comp_name] = new_value

    return replaced_count, failed_count


def apply_component_patches(
    components: Dict[str, Dict[str, Any]],
    component_patches: Dict[str, Dict[str, Dict[str, Any]]]
) -> int:
    """
    Apply patches to OpenAPI components (schemas, responses, etc.).

    Args:
        components: The components dictionary from the merged spec
        component_patches: Dict mapping component_type -> component_name -> patches

    Returns:
        Number of components patched
    """
    patched_count = 0

    for comp_type, comp_patches in component_patches.items():
        if comp_type not in components:
            print(f"   ⚠️  Component type '{comp_type}' not found in spec")
            continue

        for comp_name, patches in comp_patches.items():
            if not isinstance(patches, dict):
                print(f"   ⚠️  Invalid patches for {comp_type}/{comp_name}: not a dictionary")
                continue

            if comp_name not in components[comp_type]:
                print(f"   ⚠️  Component '{comp_name}' not found in {comp_type}")
                continue

            # Apply patches to this component
            print(f"   🔧 Applying patches to {comp_type}/{comp_name}")
            components[comp_type][comp_name] = apply_patches(
                components[comp_type][comp_name],
                patches
            )
            patched_count += 1

    return patched_count


def main():
    """Main filter and merge logic."""
    project_root = Path(__file__).parent.parent
    specs_dir = project_root / 'openapi-specs'
    config_file = project_root / 'scripts' / 'references' / 'sdk-endpoint-filters.yaml'
    output_file = project_root / 'openapi-spec.yaml'

    # Validate inputs
    if not specs_dir.exists():
        print(f"❌ Error: openapi-specs/ directory not found at {specs_dir}")
        sys.exit(1)

    if not config_file.exists():
        print(f"❌ Error: sdk-endpoint-filters.yaml not found at {config_file}")
        sys.exit(1)

    # Load endpoint configuration
    print(f"📋 Loading endpoint configuration from {config_file.name}...")
    endpoint_filter, endpoint_patches_map, component_patches = load_endpoint_config(config_file)
    print(f"   Found {len(endpoint_filter)} endpoints to include")
    if endpoint_patches_map:
        print(f"   Found {len(endpoint_patches_map)} endpoint(s) with patches")
    if component_patches:
        total_component_patches = sum(len(patches) for patches in component_patches.values())
        print(f"   Found {total_component_patches} component patch(es)")

    # Load all YAML specs
    print(f"\n📂 Scanning {specs_dir.name}/ for OpenAPI specs...")
    spec_files = list(specs_dir.glob('*.yaml')) + list(specs_dir.glob('*.yml'))

    if not spec_files:
        print(f"❌ Error: No .yaml or .yml files found in {specs_dir}")
        sys.exit(1)

    print(f"   Found {len(spec_files)} spec file(s): {', '.join(f.name for f in spec_files)}")

    # Track endpoints across files for duplicate detection
    endpoint_sources: Dict[Tuple[str, str], str] = {}
    duplicates_found = False

    # Merged output structure with custom metadata
    merged_spec = {
        'openapi': '3.0.3',
        'info': {
            'title': 'Supermetrics API',
            'version': '2.0.0',
            'description': 'Supermetrics API for authentication and data querying. For more information, visit https://supermetrics.com.',
            'contact': {
                'name': 'Supermetrics Support',
                'email': 'support@supermetrics.com',
                'url': 'https://supermetrics.com/support'
            },
            'license': {
                'name': 'Apache 2.0',
                'url': 'https://www.apache.org/licenses/LICENSE-2.0.html'
            }
        },
        'servers': [],
        'paths': {},
        'components': {
            'schemas': {},
            'responses': {},
            'parameters': {},
            'headers': {},
            'securitySchemes': {}
        },
        'security': []
    }

    all_components_by_file = {}
    all_servers = []
    security_schemes = {}

    # Process each spec file
    for spec_file in sorted(spec_files):
        print(f"\n🔍 Processing {spec_file.name}...")
        spec = load_yaml_file(spec_file)

        # Collect servers from all specs
        if 'servers' in spec:
            for server in spec['servers']:
                if server not in all_servers:
                    all_servers.append(server)

        # Collect security schemes
        if 'components' in spec and 'securitySchemes' in spec['components']:
            security_schemes.update(spec['components']['securitySchemes'])

        # Collect security requirements
        if 'security' in spec:
            for sec in spec['security']:
                if sec not in merged_spec['security']:
                    merged_spec['security'].append(sec)

        # Store all components for dependency resolution
        if 'components' in spec:
            all_components_by_file[spec_file.name] = spec['components']

        # Check paths
        paths = spec.get('paths', {})
        matched_count = 0

        for path, path_item in paths.items():
            for method in ['get', 'post', 'put', 'patch', 'delete', 'head', 'options']:
                if method not in path_item:
                    continue

                method_upper = method.upper()
                endpoint_key = (method_upper, path)

                # Check for duplicates
                if endpoint_key in endpoint_sources:
                    print(f"   ❌ DUPLICATE: {method_upper} {path}")
                    print(f"      Found in: {spec_file.name}")
                    print(f"      Already in: {endpoint_sources[endpoint_key]}")
                    duplicates_found = True
                    continue

                # Track this endpoint
                endpoint_sources[endpoint_key] = spec_file.name

                # Check if this endpoint matches filter
                if endpoint_key in endpoint_filter:
                    print(f"   ✓ Matched: {method_upper} {path}")
                    matched_count += 1

                    # Add path to merged spec
                    if path not in merged_spec['paths']:
                        merged_spec['paths'][path] = {}

                    # Copy the operation
                    operation = deepcopy(path_item[method])

                    # Apply endpoint patches if present
                    if endpoint_key in endpoint_patches_map:
                        print(f"      🔧 Applying endpoint patches to {method_upper} {path}")
                        operation = apply_patches(operation, endpoint_patches_map[endpoint_key])

                    merged_spec['paths'][path][method] = operation

                    # Also copy path-level parameters if present
                    if 'parameters' in path_item and 'parameters' not in merged_spec['paths'][path]:
                        merged_spec['paths'][path]['parameters'] = path_item['parameters']

        print(f"   Matched {matched_count} endpoint(s) from {spec_file.name}")

    # Fail if duplicates found
    if duplicates_found:
        print(f"\n❌ FAILURE: Duplicate METHOD|PATH found across multiple spec files")
        print(f"   Please resolve duplicates before proceeding")
        sys.exit(1)

    # Add collected servers and security schemes
    merged_spec['servers'] = all_servers
    merged_spec['components']['securitySchemes'] = security_schemes

    # Collect all referenced components
    print(f"\n🔗 Collecting referenced schemas and components...")
    collected_components: Dict[str, Set[str]] = {}

    # Extract all refs from matched paths
    all_refs = set()
    extract_refs(merged_spec['paths'], all_refs)

    # Merge all components from all files for dependency resolution
    all_components = {
        'schemas': {},
        'responses': {},
        'parameters': {},
        'headers': {},
        'securitySchemes': security_schemes
    }

    for file_components in all_components_by_file.values():
        for comp_type in all_components.keys():
            if comp_type in file_components:
                all_components[comp_type].update(file_components[comp_type])

    # Resolve initial refs (sorted for consistent order)
    for ref in sorted(all_refs):
        ref_type, ref_name = resolve_component_name(ref)
        if not ref_type or not ref_name:
            continue

        if ref_type not in collected_components:
            collected_components[ref_type] = set()
        collected_components[ref_type].add(ref_name)

        # Recursively collect dependencies
        if ref_type in all_components and ref_name in all_components[ref_type]:
            collect_component_dependencies(
                all_components[ref_type][ref_name],
                all_components,
                ref_type,
                collected_components
            )

    # Copy collected components to merged spec (sorted for consistent order)
    for comp_type in sorted(collected_components.keys()):
        comp_names = collected_components[comp_type]
        for comp_name in sorted(comp_names):
            if comp_type in all_components and comp_name in all_components[comp_type]:
                merged_spec['components'][comp_type][comp_name] = all_components[comp_type][comp_name]

    total_components = sum(len(names) for names in collected_components.values())
    print(f"   Collected {total_components} component(s):")
    for comp_type, comp_names in collected_components.items():
        if comp_names:
            print(f"      {comp_type}: {len(comp_names)}")

    # Resolve external file references
    print(f"\n🔧 Resolving external file references...")
    replaced_count, failed_count = resolve_external_references(merged_spec['components'], specs_dir)
    if replaced_count > 0:
        print(f"   ✓ Resolved {replaced_count} external reference(s)")
    if failed_count > 0:
        print(f"   ❌ Failed to resolve {failed_count} external reference(s)")

    # Apply component patches
    if component_patches:
        print(f"\n🔧 Applying component patches...")
        patched_count = apply_component_patches(merged_spec['components'], component_patches)
        if patched_count > 0:
            print(f"   ✓ Applied patches to {patched_count} component(s)")

    # Validate all endpoints from filter were found
    print(f"\n✅ Validation:")
    missing_endpoints = []
    for endpoint_key in endpoint_filter:
        if endpoint_key not in endpoint_sources:
            method, path = endpoint_key
            missing_endpoints.append(f"{method} {path}")

    if missing_endpoints:
        print(f"   ⚠️  WARNING: {len(missing_endpoints)} endpoint(s) from filter not found in specs:")
        for endpoint in missing_endpoints:
            print(f"      - {endpoint}")
    else:
        print(f"   ✓ All {len(endpoint_filter)} filtered endpoints found and included")

    # Save merged spec
    print(f"\n💾 Writing merged spec to {output_file.name}...")
    save_yaml_file(output_file, merged_spec)

    print(f"\n🎉 Success!")
    print(f"   Input specs: {len(spec_files)}")
    print(f"   Filtered endpoints: {len(merged_spec['paths'])}")
    print(f"   Servers: {len(merged_spec['servers'])}")
    print(f"   Total components: {total_components}")
    print(f"   Output: {output_file}")

    return 0


if __name__ == '__main__':
    sys.exit(main())
