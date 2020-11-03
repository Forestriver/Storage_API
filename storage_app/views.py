import json
from django.conf import settings
import redis
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response

#Connection to Redis
redis_exemplar = redis.StrictRedis(host=settings.REDIS_HOST,
                                   port=settings.REDIS_PORT, db=0)

"""
API endpoint allowing to retrieve the records set at Redis exemplar
and to create new entries by passing JSON
"""
@api_view(['GET', 'POST'])
def handle_records(request, *args, **kwargs):
    if request.method == 'GET':
        records = {}
        count = 0
        for key in redis_exemplar.keys('*'):
            records[key.decode('utf-8')] = redis_exemplar.get(key)
            count += 1
        response = {
            'count':count,
            'msg':f"{count} records found.",
            'records':records
        }
        return Response(response, status=200)

    elif request.method == 'POST':
        record = json.loads(request.body)
        key = list(record.keys())[0]
        value = record[key]
        redis_exemplar.set(key, value)
        response = {
            'msg':f"{key} successfully set to {value}"
        }
        return Response(response, 201)

"""
API endpoint providing access to the unique records in Redis exemplar.
It requires the key of the record to locate the value.
"""
@api_view(['GET', 'PUT', 'DELETE'])
def handle_record(request, *args, **kwargs):
    if request.method == 'GET':
        if kwargs['key']:
            value = redis_exemplar.get(kwargs['key'])
            if value:
                response = {
                    'key':kwargs['key'],
                    'value':value,
                    'msg':'Not found'
                }
                return Response(response, status=404)
   #Updating the value of the key
    elif request.method == 'PUT':
        if kwargs['key']:
            request_data = json.loads(request.body)
            new_value = request_data['new_value']
            value = redis_exemplar.get(kwargs['key'])
            if value:
                redis_exemplar.set(kwargs['key'], new_value)
                response = {
                    'key':kwargs['key'],
                    'value':value,
                    'msg':f"{kwargs['key']} updated successfully"
                }
                return Response(response, status=200)
            else:
                response = {
                    'key':kwargs['key'],
                    'value':None,
                    'msg':'Not found'
                }
                return Response(response, status=404)
    #Deleting key-value pair from Redis exemplar
    elif request.method == 'DELETE':
        if kwargs['key']:
            result = redis_exemplar.delete(kwargs['key'])
            if result == 1:
                response = {
                    'msg':f"{kwargs['key']} deleted successfully"
                }
                return Response(response, status=404)
            else:
                response = {
                    'key':kwargs['key'],
                    'value':None,
                    'msg':"Not found"
                }
                return Response(response, status=404)
