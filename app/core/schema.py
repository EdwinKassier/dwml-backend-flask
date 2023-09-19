import asyncio

import strawberry
import json
from flask import Blueprint, current_app,request
from werkzeug.local import LocalProxy
from authentication import check_auth
import traceback
from .utils import data_collector, graph_creator


@strawberry.type
class ProcessRequestResult:
    message: str
    graph_data: str

# Define a GraphQL schema
@strawberry.type
class Query:
    @strawberry.field
    def process_request(self, symbol: str, investment: int) -> ProcessRequestResult:
        try:
            collector = data_collector.DataCollector(symbol, investment)
            creator = graph_creator.GraphCreator(symbol)
            result = json.dumps(collector.driver_logic())
            graph_data = json.dumps(creator.driver_logic())
            return ProcessRequestResult(message=result, graph_data=graph_data)
        except Exception as exc:
            return ProcessRequestResult(message='Server Failure', graph_data=json.dumps([]))




schema = strawberry.Schema(query=Query)