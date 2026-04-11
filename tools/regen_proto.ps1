$root = Split-Path -Parent (Split-Path -Parent $PSScriptRoot)
& python -m grpc_tools.protoc `
  -I "$root/contracts" `
  --python_out="$PSScriptRoot/../app/protos" `
  --grpc_python_out="$PSScriptRoot/../app/protos" `
  "$root/contracts/ai-agent.proto"
Write-Host "Regenerated app/protos/ai_agent_pb2*.py from contracts/ai-agent.proto"
