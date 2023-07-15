"""
导入 pydantic model , 导出相应 json schema
"""

if __name__ == "__main__":
    from core.interface.adapter import AdapterConfig
    import json

    export_model = AdapterConfig
    with open("schema.json", "w", encoding="utf8") as f:
        f.write(json.dumps(export_model.model_json_schema()))
