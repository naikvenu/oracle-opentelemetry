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
  
  print("doing some work at this span...")
  current_span = trace.get_current_span()

  # Setting Span Attributes
  current_span.set_attribute("operation.value", 8888)
  current_span.set_attribute("operation.name", "Just a OTEL Demo")

  # Adding a Event
  current_span.add_event("Hello This is a message from OCI APM OTEL demo")

  # Using Semantic Conventions
  from opentelemetry.semconv.trace import SpanAttributes
  current_span.set_attribute(SpanAttributes.HTTP_METHOD, "GET")
  current_span.set_attribute(SpanAttributes.HTTP_URL, "https://opentelemetry.io/")

  return "Hello ! This is a OTEL OCI APM demo .."

if __name__ == "__main__":
    app.run(host='0.0.0.0')
