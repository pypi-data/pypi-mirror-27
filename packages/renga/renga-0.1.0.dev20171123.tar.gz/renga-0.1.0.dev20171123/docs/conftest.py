# -*- coding: utf-8 -*-
#
# Copyright 2017 - Swiss Data Science Center (SDSC)
# A partnership between École Polytechnique Fédérale de Lausanne (EPFL) and
# Eidgenössische Technische Hochschule Zürich (ETHZ).
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
"""Pytest configuration."""

from __future__ import absolute_import, print_function

import io
import json
import os
import shutil
import tempfile
import time
import types

import pytest
import responses
from click.testing import CliRunner


@pytest.fixture()
def instance_path():
    """Temporary instance path."""
    path = tempfile.mkdtemp()
    yield path
    shutil.rmtree(path)


@pytest.fixture()
def base_runner(instance_path, monkeypatch):
    """Create a runner on isolated filesystem."""
    from renga.cli._config import PROJECT_DIR
    monkeypatch.setenv('RENGA_CONFIG', os.path.join(instance_path,
                                                    PROJECT_DIR))
    cli_runner = CliRunner()
    with cli_runner.isolated_filesystem():
        yield cli_runner


@pytest.fixture()
def renga_client():
    """Return a graph mutation client."""
    from renga.client import RengaClient
    return RengaClient(
        'https://example.com', token={'access_token': 'accessdemo'})


@pytest.fixture()
def graph_mutation_client():
    """Return a graph mutation client."""
    from renga.client.graph.mutation import GraphMutationClient
    client = GraphMutationClient('https://example.com')

    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:

        def request_callback(request):
            return (200, {
                'Content-Type': 'application/json'
            }, '{"access_token": "servicetoken"}')

        rsps.add_callback(
            responses.POST,
            'https://example.com/auth/realms/Renga/protocol/openid-connect'
            '/token',
            content_type='application/json',
            callback=request_callback)

        client.authorization.authorize_service(
            audience='renga-services',
            client_id='renga-services-client-id',
            client_secret='renga-services-client-secret', )
    return client


@pytest.fixture()
def auth_responses():
    """Authentication responses."""
    with responses.RequestsMock(assert_all_requests_are_fired=False) as rsps:

        def request_callback(request):
            return (200, {
                'Content-Type': 'application/json'
            }, '{"refresh_token": "demodemo", "access_token": "accessdemo", '
                    '"expires_at": 0}')

        rsps.add_callback(
            responses.POST,
            'https://example.com/auth/realms/Renga/protocol/openid-connect'
            '/token',
            content_type='application/json',
            callback=request_callback)
        yield rsps


@pytest.fixture()
def runner(base_runner, auth_responses):
    """Return authenticated runner."""
    from renga import cli

    result = base_runner.invoke(cli.cli, [
        'login', 'https://example.com', '--username', 'demo', '--password',
        'demo'
    ])
    assert result.exit_code == 0
    yield base_runner


@pytest.fixture()
def graph_mutation_responses(auth_responses, graph_mutation_client):
    """Monkeypatch requests to immitate the KnowledgeGraph."""
    rsps = auth_responses
    mutation_url = graph_mutation_client.mutation_url
    named_type_url = graph_mutation_client.named_type_url

    rsps.add(responses.POST, mutation_url, status=201, json={'uuid': '1234'})
    rsps.add(
        responses.GET,
        mutation_url + '/1234',
        status=200,
        json={
            'status': 'completed',
            'response': {
                'event': {
                    'status': 'success',
                    'results': [{
                        'id': 1234
                    }]
                }
            }
        })
    rsps.add(
        responses.GET,
        named_type_url,
        status=200,
        json=[{
            'name':
            'context',
            'properties': [{
                'name': 'context_id',
                'data_type': 'string',
                'cardinality': 'single'
            }, {
                'name': 'context_spec_image',
                'data_type': 'string',
                'cardinality': 'single'
            }, {
                'name': 'context_spec_ports',
                'data_type': 'string',
                'cardinality': 'single'
            }]
        }, {
            'name':
            'execution',
            'properties': [{
                'name': 'execution_id',
                'data_type': 'string',
                'cardinality': 'single'
            }, {
                'name': 'execution_engine',
                'data_type': 'string',
                'cardinality': 'single'
            }, {
                'name': 'execution_namespace',
                'data_type': 'string',
                'cardinality': 'single'
            }]
        }, {
            "name":
            "project",
            "properties": [{
                "name": "project_name",
                "data_type": "string",
                "cardinality": "single"
            }]
        }])

    yield rsps


@pytest.fixture()
def projects_responses(auth_responses, renga_client):
    """Monkeypatch requests to immitate the projects service."""
    rsps = auth_responses
    project = {
        'name': 'test-project',
        'identifier': '1234',
    }
    rsps.add(
        responses.POST,
        renga_client.api._url('/api/projects'),
        status=201,
        json=project, )
    rsps.add(
        responses.GET,
        renga_client.api._url('/api/projects'),
        status=200,
        json={'projects': [project]}, )
    rsps.add(
        responses.GET,
        renga_client.api._url('/api/projects/1234'),
        status=200,
        json=project, )
    rsps.add(
        responses.GET,
        renga_client.api._url('/api/projects/0'),
        status=404, )
    yield rsps


@pytest.fixture()
def deployer_responses(auth_responses, renga_client):
    """Monkeypatch requests to immitate the deployer service."""
    context = {
        'identifier': 'abcd',
        'spec': {
            'image':
            'hello-world',
            'labels': [
                'renga.context.inputs.notebook=9876',
                'renga.context.inputs.no_default',
                'renga.context.inputs.with_default=9876',
                'renga.context.outputs.result',
            ],
        }
    }
    execution = {
        'identifier': 'efgh',
        'engine': 'docker',
        'namespace': 'default',
    }

    rsps = auth_responses
    rsps.add(
        responses.POST,
        renga_client.api._url('/api/deployer/contexts'),
        status=201,
        json=context, )
    rsps.add(
        responses.GET,
        renga_client.api._url('/api/deployer/contexts'),
        status=200,
        json={
            'contexts': [context],
        })
    rsps.add(
        responses.GET,
        renga_client.api._url('/api/deployer/contexts/abcd'),
        status=200,
        json=context)
    rsps.add(
        responses.GET,
        renga_client.api._url('/api/deployer/contexts/deadbeef'),
        status=404)
    rsps.add(
        responses.POST,
        renga_client.api._url('/api/deployer/contexts/abcd/executions'),
        status=201,
        json=execution, )
    rsps.add(
        responses.GET,
        renga_client.api._url('/api/deployer/contexts/abcd/executions'),
        status=200,
        json={
            'executions': [execution],
        })
    rsps.add(
        responses.DELETE,
        renga_client.api._url('/api/deployer/contexts/abcd/executions/efgh'),
        status=200,
        json=execution, )
    rsps.add(
        responses.GET,
        renga_client.api._url(
            '/api/deployer/contexts/abcd/executions/efgh/logs'),
        status=200,
        body=b'Hello world!', )
    rsps.add(
        responses.GET,
        renga_client.api._url(
            '/api/deployer/contexts/abcd/executions/efgh/ports'),
        status=200,
        json={
            'ports': [],
        })
    yield rsps


@pytest.fixture()
def storage_responses(auth_responses, renga_client):
    """Monkeypatch requests to immitate the storage service."""
    rsps = auth_responses
    rsps.add(
        responses.POST,
        renga_client.api._url('/api/storage/authorize/create_bucket'),
        status=201,
        json={
            'id': 1234,
            'name': 'hello',
            'backend': 'local',
        })

    file_ = {'id': 9876}

    def create_file(request):
        """Create new file."""
        file_id = file_['id']
        file_['id'] -= 1
        return (201, {}, json.dumps({
            'id': file_id,
            'access_token': 'accessfile_{0}'.format(file_id),
        }))

    rsps.add_callback(
        responses.POST,
        renga_client.api._url('/api/storage/authorize/create_file'),
        callback=create_file,
    )

    def authorize_io(request):
        """Generate access token."""
        data = json.loads(request.body.decode('utf-8'))
        return (200, {}, json.dumps({
            'access_token':
            '{request_type}_{resource_id}'.format(**data)
        }))

    rsps.add_callback(
        responses.POST,
        renga_client.api._url('/api/storage/authorize/write'),
        callback=authorize_io, )

    rsps.add_callback(
        responses.POST,
        renga_client.api._url('/api/storage/authorize/read'),
        callback=authorize_io, )

    data = {}
    file_versions = []

    def file_version(file_id):
        """Return new file version metadata."""
        id_ = file_id * 10 + file_id % 10 - 1
        return {
            "id":
            id_,
            "types": ["resource:file_version"],
            "properties": [{
                "key":
                "resource:owner",
                "data_type":
                "string",
                "cardinality":
                "set",
                "values": [{
                    "parent": {
                        "type": "vertex",
                        "id": id_,
                    },
                    "key": "resource:owner",
                    "data_type": "string",
                    "value": "e144b235-793b-4e2e-bb1f-1f8baccc321f",
                    "properties": []
                }]
            }, {
                "key":
                "system:creation_time",
                "data_type":
                "long",
                "cardinality":
                "single",
                "values": [{
                    "parent": {
                        "type": "vertex",
                        "id": id_,
                    },
                    "key": "system:creation_time",
                    "data_type": "long",
                    "value": time.time() * 1000,
                    "properties": []
                }]
            }]
        }

    def io_write(request):
        """Store file data."""
        file_id = int(
            request.headers['Authorization'].split(' ')[1].split('_')[-1])

        if file_id in data:
            # Store old version
            version = file_version(file_id)
            data[version['id']] = data[file_id]
        else:
            version = file_version(file_id // 10)

        file_versions.append(version)

        if hasattr(request.body, 'read'):
            body = request.body.read()
        elif isinstance(request.body, types.GeneratorType):
            body = b''.join(request.body)
        else:
            body = request.body

        data[file_id] = body
        return (201, {}, 'ok')

    def io_read(request):
        """Read file data."""
        try:
            file_id = int(
                request.headers['Authorization'].split(' ')[1].split('_')[-1])
            return (200, {}, data[file_id])
        except KeyError:
            return (401, {}, '')

    rsps.add_callback(
        responses.POST,
        renga_client.api._url('/api/storage/io/write'),
        callback=io_write, )
    rsps.add_callback(
        responses.GET,
        renga_client.api._url('/api/storage/io/read'),
        callback=io_read, )
    rsps._matches[-1].stream = True
    rsps.add(
        responses.GET,
        renga_client.api._url('/api/storage/io/backends'),
        status=200,
        json=['local'], )
    rsps.add(
        responses.GET,
        'https://example.com/tests/data',
        status=200,
        body=b'hello world',
        stream=True, )

    rsps.add_callback(
        responses.GET,
        renga_client.api._url('/api/explorer/storage/file/9876/versions'),
        callback=lambda request: (200, {}, json.dumps(file_versions)),
        content_type='application/json', )

    yield rsps


@pytest.fixture()
def explorer_responses(auth_responses, renga_client):
    """Monkeypatch requests to immitate the explorer service."""
    rsps = auth_responses
    buckets = [{
        "id":
        1234,
        "types": ["resource:bucket"],
        "properties": [{
            "key":
            "resource:bucket_backend",
            "data_type":
            "string",
            "cardinality":
            "single",
            "values": [{
                "key": "resource:bucket_backend",
                "data_type": "string",
                "value": "local",
                "properties": []
            }]
        }, {
            "key":
            "resource:bucket_name",
            "data_type":
            "string",
            "cardinality":
            "single",
            "values": [{
                "key": "resource:bucket_name",
                "data_type": "string",
                "value": "bucket1",
                "properties": []
            }]
        }]
    }, {
        "id":
        5678,
        "types": ["resource:bucket"],
        "properties": [{
            "key":
            "resource:bucket_backend",
            "data_type":
            "string",
            "cardinality":
            "single",
            "values": [{
                "key": "resource:bucket_backend",
                "data_type": "string",
                "value": "local",
                "properties": []
            }]
        }, {
            "key":
            "resource:bucket_name",
            "data_type":
            "string",
            "cardinality":
            "single",
            "values": [{
                "key": "resource:bucket_name",
                "data_type": "string",
                "value": "bucket2",
                "properties": []
            }]
        }]
    }]

    rsps.add(
        responses.GET,
        renga_client.api._url('/api/explorer/storage/bucket'),
        status=200,
        json=buckets)

    rsps.add(
        responses.GET,
        renga_client.api._url('/api/explorer/storage/bucket/1234'),
        status=200,
        json=buckets[0])

    files = [{
        'id':
        9876,
        'types': ['resource:file'],
        'properties': [{
            'key':
            'resource:file_name',
            'data_type':
            'string',
            'cardinality':
            'single',
            'values': [{
                'parent': {
                    'type': 'vertex',
                    'id': 9876
                },
                'key': 'resource:file_name',
                'data_type': 'string',
                'value': 'hello',
                'properties': []
            }]
        }, {
            'key':
            'resource:owner',
            'data_type':
            'string',
            'cardinality':
            'set',
            'values': [{
                'parent': {
                    'type': 'vertex',
                    'id': 9876
                },
                'key': 'resource:owner',
                'data_type': 'string',
                'value': 'e144b235-793b-4e2e-bb1f-1f8baccc321f',
                'properties': []
            }]
        }]
    }]

    rsps.add(
        responses.GET,
        renga_client.api._url('/api/explorer/storage/bucket/1234/files'),
        status=200,
        json=files)

    rsps.add_callback(
        responses.GET,
        renga_client.api._url('/api/explorer/storage/file/9876'),
        callback=lambda request: (200, {}, json.dumps(
            {'data': files[0], 'bucket': buckets[0]})),
        content_type='application/json',
    )

    def rename_file(request):
        """Rename a file."""
        payload = json.loads(request.body.decode('utf-8'))
        files[0]['properties'][0]['values'][0]['value'] = payload['file_name']
        return (200, {}, '{}')

    rsps.add_callback(
        responses.PUT,
        renga_client.api._url('/api/storage/file/9876'),
        callback=rename_file,
        content_type='application/json', )

    return rsps


@pytest.fixture(autouse=True)
def add_client(doctest_namespace, renga_client, storage_responses,
               explorer_responses, projects_responses):
    """Add Renga client to doctest namespace."""
    doctest_namespace['client'] = renga_client
