# Task Batches

This directory stores one generated task batch per file.

Expected file shape:

```text
generated/task_batch_index.json
generated/task_batches/<batch_id>.json
```

Each batch file should conform to `contracts/task_batch.schema.json`.

Every task inside a batch should conform to `contracts/task.schema.json`.

Validate batches with:

```powershell
python tools\validate_task_batches.py
```
