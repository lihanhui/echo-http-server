# echo-http-server
One simple echo http server which replies any json content as defined.

Example:

Step 1: define request path and its response

POST following content to http://your-server-host:8888/config/submit,

{
  "path": "/hello/world",
  "data": ["nihao","你好"]
}

Step 2: Send http request with POST or GET method，in which the path in request url is defined by “path” key in http body （json）as step 1，and get response which is defined in “data”，

Request: POST /hello/world HTTP／1.1

Response: ["nihao","你好"]


Hope you like it.
