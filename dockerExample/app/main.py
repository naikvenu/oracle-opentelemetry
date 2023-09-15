from flask import Flask
app = Flask('OCI_OPENTELEMETRY_APM_DEMO')

from opentelemetry import trace
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource


# Trace Pipeline
resource = Resource(attributes={
    SERVICE_NAME: "OCI-APM-OTEL-DEMO"
})

provider = TracerProvider(resource=resource)

span_processor = BatchSpanProcessor(OTLPSpanExporter(endpoint="http://otel-collector.demo:4318/v1/traces"))
provider.add_span_processor(span_processor)
trace.set_tracer_provider(provider)

tracer = trace.get_tracer("OTEL-demo","1.0", provider,None)


@app.route("/oteldemo")
@tracer.start_as_current_span("oteldemo")
def oteldemo():
    current_span = trace.get_current_span()

    #current_span.set_attribute("operation.value", 1)
    current_span.set_attribute("operation-name", "Just get call on oteldemo!")
    #current_span.set_attribute("operation.other-stuff", [1, 2, 3])
    from opentelemetry.semconv.trace import SpanAttributes
    #current_span.set_attribute(SpanAttributes.HTTP_METHOD, "GET")
    #current_span.set_attribute(SpanAttributes.HTTP_URL, "/oteldemo")
    current_span.add_event("This is a OTEL OCI APM demo ..")

    return "Hello ! This is a OTEL OCI APM demo .."




if __name__ == "__main__":
    app.run(host='0.0.0.0')
