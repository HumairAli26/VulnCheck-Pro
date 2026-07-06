from src.core.audit_engine import AuditEngine

engine = AuditEngine()

results = engine.run()

for result in results:
    print("=" * 40)
    print(result.title)
    print(result.status)
    print(result.risk)

    for key, value in result.details.items():
        print(f"{key}: {value}")