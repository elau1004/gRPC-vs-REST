# Variables
PYTHON := python
PYTHONPATH := `pwd`

# Protobuf
.PHONY: protoc
protoc:
	protoc -I=./patient_data/ --python_out=./patient_data/ ./patient_data/protobuf_grpc.proto
