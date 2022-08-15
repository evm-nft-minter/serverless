import json
from src.common.network_enum import NetworkEnum
from src.common.Response import Response
from src.upload.Storage import Storage
from src.upload.is_tx_valid import is_tx_valid
from src.upload.arweave.upload import upload
from src.upload.update_metadata import update_metadata

METADATA_CONTENT_TYPE = "application/json"


def main(event, context):
    try:
        network = event["pathParameters"]["network"]
        payload = json.loads(event["body"])
        txHash = payload["tx"].lower()
        data = payload["data"]
        metadata = payload["metadata"]
        content_type = payload["contentType"]

        Storage.save(txHash.lower())

        if network not in list(NetworkEnum):
            return Response(404, msg="Network isn't supported")

        if not is_tx_valid(network, txHash, data, metadata):
            return Response(400, msg="Transaction isn't valid")

        tx_upload_data = upload(data, content_type)

        data_url = f"{tx_upload_data.api_url}/{tx_upload_data.id}"

        updated_metadata = update_metadata(metadata, image=data_url)

        tx_upload_metadata = upload(updated_metadata, METADATA_CONTENT_TYPE)

        body = {"txId": tx_upload_metadata.id}

        return Response(200, body)
    except:
        return Response(400, msg="Bad request")
