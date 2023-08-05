import opentracing as ot
from instana import tracer, options

opts = options.Options()
ot.global_tracer = tracer.InstanaTracer(opts)
