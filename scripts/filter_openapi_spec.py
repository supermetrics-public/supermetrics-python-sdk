#!/usr/bin/env python3
"""
OpenAPI Specification Filter and Merger

Reads multiple OpenAPI YAML files from openapi-specs/ directory,
filters endpoints based on sdk-endpoints.txt configuration,
and merges them into a single openapi-spec.yaml file.

Features:
- Detects and fails on duplicate METHOD|PATH across multiple specs
- Filters paths/operations matching inclusion list
- Collects all referenced schemas via $ref traversal
- Merges filtered paths into single spec
- Uses custom metadata for general-purpose SDK
"""

import sys
from pathlib import Path
from typing import Dict, Set, List, Tuple, Any
import yaml
import re


def load_yaml_file(file_path: Path) -> Dict[str, Any]:
    """Load and parse a YAML file."""
    with open(file_path, 'r', encoding='utf-8') as f:
        return yaml.safe_load(f)


def save_yaml_file(file_path: Path, data: Dict[str, Any]) -> None:
    """Save data to a YAML file."""
    with open(file_path, 'w', encoding='utf-8') as f:
        yaml.dump(data, f, default_flow_style=False, sort_keys=False, allow_unicode=True)


def load_endpoint_filter(filter_file: Path) -> Set[Tuple[str, str]]:
    """
    Load endpoint filter from sdk-endpoints.txt.
    Returns set of (METHOD, PATH) tuples.
    """
    endpoints = set()
    with open(filter_file, 'r', encoding='utf-8') as f:
        for line in f:
            line = line.strip()
            # Skip comments and empty lines
            if not line or line.startswith('#'):
                continue

            # Parse METHOD|PATH format
            if '|' not in line:
                print(f"⚠️  Skipping invalid line (missing |): {line}")
                continue

            method, path = line.split('|', 1)
            method = method.strip().upper()
            path = path.strip()
            endpoints.add((method, path))

    return endpoints


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

    for ref in refs:
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


def main():
    """Main filter and merge logic."""
    project_root = Path(__file__).parent.parent
    specs_dir = project_root / 'openapi-specs'
    filter_file = project_root / 'sdk-endpoints.txt'
    output_file = project_root / 'openapi-spec.yaml'

    # Validate inputs
    if not specs_dir.exists():
        print(f"❌ Error: openapi-specs/ directory not found at {specs_dir}")
        sys.exit(1)

    if not filter_file.exists():
        print(f"❌ Error: sdk-endpoints.txt not found at {filter_file}")
        sys.exit(1)

    # Load endpoint filter
    print(f"📋 Loading endpoint filter from {filter_file.name}...")
    endpoint_filter = load_endpoint_filter(filter_file)
    print(f"   Found {len(endpoint_filter)} endpoints to include")

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

                    merged_spec['paths'][path][method] = path_item[method]

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

    # Resolve initial refs
    for ref in all_refs:
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

    # Copy collected components to merged spec
    for comp_type, comp_names in collected_components.items():
        for comp_name in comp_names:
            if comp_type in all_components and comp_name in all_components[comp_type]:
                merged_spec['components'][comp_type][comp_name] = all_components[comp_type][comp_name]

    total_components = sum(len(names) for names in collected_components.values())
    print(f"   Collected {total_components} component(s):")
    for comp_type, comp_names in collected_components.items():
        if comp_names:
            print(f"      {comp_type}: {len(comp_names)}")

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
