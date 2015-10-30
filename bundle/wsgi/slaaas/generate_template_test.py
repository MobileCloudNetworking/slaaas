from bundle.wsgi.slaaas import template_generator


generator = template_generator.SLAaaSTemplateGenerator("10.0.0.1","192.168.1.200")

template = generator.generate(True)

print template