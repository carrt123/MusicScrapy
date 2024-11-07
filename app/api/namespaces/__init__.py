from apispec import APISpec
from apispec.ext.marshmallow import MarshmallowPlugin
from flask import Flask, Response

app = Flask(__name__)
app.config.update({
    'APISPEC_SPEC': APISpec(
        title='Flask Restful API project',
        version='v1',
        plugins=[MarshmallowPlugin()],
        openapi_version='2.0.0'
    ),
    'APISPEC_SPEC_URL': '/swagger',
    'APISPEC_SPEC_UI_URL': '/swagger-ui'
})
