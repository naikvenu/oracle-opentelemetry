from opentelemetry import trace
from opentelemetry.sdk.trace.export import ConsoleSpanExporter, BatchSpanProcessor
from opentelemetry.sdk.trace import TracerProvider
from opentelemetry.exporter.otlp.proto.http.trace_exporter import OTLPSpanExporter
from opentelemetry.sdk.resources import SERVICE_NAME, Resource

def init_trace_pipeline():
  resource = Resource(attributes={
      SERVICE_NAME: "OCI-APM-OTEL-DEMO"
      })

  provider = TracerProvider(resource=resource)
  exporter = OTLPSpanExporter(endpoint="https://APM_DATA_UPLOAD_ENDPOINT.<region>.oci.oraclecloud.com/20200101/opentelemetry/public/v1/traces",
                              headers={"authorization": "dataKey xxxxxxx"})
  span_processor = BatchSpanProcessor(exporter)
  provider.add_span_processor(span_processor)
  trace.set_tracer_provider(provider)
  return trace.get_tracer("otel-demo", "1.0")

tracer = init_trace_pipeline()

@tracer.start_as_current_span("single-span")
def single_span():
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


if __name__ == "__main__":
  single_span()