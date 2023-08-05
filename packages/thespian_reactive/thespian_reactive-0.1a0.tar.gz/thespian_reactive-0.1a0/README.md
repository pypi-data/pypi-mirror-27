# ReactiveThespian

A reactive streaming tool for building an ETL/Ingestion backbone. This tool offers distributed and reactive streams built for Python. An attempt is made to implement at least most of the reactive streams protocol.

The end goal is to have graphical and code based managers for streams and graphs made of actors, providing ease of maintenance and a highly flexible environment capable of ETL, IOT, and everything else requiring multiple tools and a bizzarre, non-scalable backbone in today's odd world of technology.

# When to Use ReactiveThespian

Reactive Thespian should be used when in need of streaming or connecting large numbers of devices through a push or pull mechanism. ETL/Ingestion where a graphical processor is important benefit immensely from this model. The project will try to be non-blocking but due to some constant issues with streams discovered in CompAktor, this may be more difficult than it seems.

As the tool progresses, a GUI will hopefully make maintaining your custom built streams and graphs much easier.

# Thespian

Thespian is actively developed by Kevin Quick and maintained by GoDaddy. At some point, I hope to take the basic actors I have working in CompAktor and fix the streams module in that tool. However, Thespian, which does not use asyncio, is the best alternative at the moment. Asyncio needs to improve to exit a loop quickly and return control from await only when a loop exits and not a function completes (perhaps a race condition). Until then, checkout Thespian (https://github.com/godaddy/Thespian), an actively developed and strong project.

# Completing Tasks

This project is new. Please help bring a solid reactive, non-mimicked reactive model to Python. I've been looking to port Akka for a while. The basic actor and remoting were enacted in Thespian. Feel free to fork this project and help.

# Goal

The following goals need to be met:

- Better cluster control

We would also like to build a GUI for the graph interface which allows users to directly manipulate their streams, even when in progress. This idea requires:

- A QT based GUI displaying nodes and showing statistics per node and per stream
- The graph manager to dump QML on demand
- The ability to open a node and edit all properties asociated with the node
- Functions attached to the QT objects which manipulate the stream
- Classes that use the appropriate actor system to manipulate the stream through the GUI
- The ability to insert and delete nodes and have the stream make appropriate adjustments in both realtime and when streams are not running.

# Implementation

Streams implementation is based on the reactive streams model at https://github.com/reactive-streams/reactive-streams-jvm/blob/v1.0.1/README.md. However, it is a graphical interpretation. This is, after all, a directed graph engine and actor system for building custom networks and streams.

The actor model serves as the basis for implementation of the underlying core pieces of the systems. Enterprise data patterns are implemented via the routers and publishers/subscribers in this tool.

More implementation basics can actually be found on the Akka website https://akka.io/docs/. A thorough understanding of this tool will server you well here. Hopefully, we can also distribute the streams/graphs created with this tool.

# License

Copyright 2017- Andrew Evans and SimplrInsites, LLC

Licensed under the Apache License, Version 2.0 (the "License");
you may not use this file except in compliance with the License.
You may obtain a copy of the License at

    http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software
distributed under the License is distributed on an "AS IS" BASIS,
WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
See the License for the specific language governing permissions and
limitations under the License.


