# Opentelemetry Manual instrumentation with Oracle APM Back-end

In this doc, lets discuss manual Opentelemetry instrumentation process using Opentelemetry SDK's . 
We will use OCI APM as a back-end to analyze these traces.

![image](../assets/images/otel-manual-inst.jpg)

As you can see in this architecture all these application services are communicating with each other via Http or gRPC protocol and each of these services are configured to send the traces directly to APM. Do note that the services send traces to APM via OTLP protocol.

OTLP is a general-purpose telemetry data delivery protocol, it defines the encoding of telemetry data and the protocol used to exchange data between the client and the server.
This specification defines how OTLP is implemented over gRPC and HTTP 1.1 transports and specifies Protocol Buffers schema that is used for the payloads.
OTLP is a request/response style protocol: the clients send requests, and the server replies with corresponding responses.

This is how you initialize the OTLP protocols with OCI APM:
