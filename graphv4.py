# from gql import gql, Client
# from gql.transport.aiohttp import AIOHTTPTransport
#
# # Select your transport with a defined url endpoint
# transport = AIOHTTPTransport(url="https://countries.trevorblades.com/")
#
# # Create a GraphQL client using the defined transport
# client = Client(transport=transport, fetch_schema_from_transport=True)
#
# # Provide a GraphQL query
# query = gql(
#     """
#     query getContinents {
#       continents {
#         code
#         name
#       }
#     }
# """
# )
#
# # Execute the query on the transport
# result = client.execute(query)
# print(result)

import requests

url = 'https://api.github.com/graphql'
json = { 'query' : '{ repository(owner: "google", name: "gson") {namerefs(first: 100, refPrefix: "refs/heads/") {edges {node {nametarget {on Commit {idhistory(first: 0) {totalCount}}}}}}}}' }
api_token = "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"
headers = {'Authorization': 'token %s' % api_token}

r = requests.post(url=url, json=json, headers=headers)
print (r.text)