import base64
from google.cloud import storage

def storage_add_fetch(data, event, context):
    """Triggered from a message on a Cloud Pub/Sub topic 'Camera_rig'. Adds image from encoded dictionary in event
        dictionary data to Google Cloud Storage and returns a URL that references that image.
    Args:
        event (dict): Event payload.
        context (google.cloud.functions.Context): Metadata for the event.
    """
    #Decodes the base64 encoded image
    
    print("The data was received! Now attempting to add to bucket...")

    # This creates a client object that then creates a bucket
    # object. This grants us the ability to edit the accessed
    # bucket
    client = storage.Client()
    bucket = client.bucket(event["bucket_name"])

    #This creates a blob object which then gets the date
    # from the upload function
    blob = bucket.blob(event["filename"])

    # if(blob.exists()):
    #     bucket.delete_blob(event["filename"])

    blob.upload_from_string(data, content_type="image/jpeg")
    
    #Finally, a url is generated for the bucket. The expire_tuple
    # is a tuple representing the time the url life expires
    urlFilename = urlencode.quote_plus(event["filename"])
    url = "/".join(
        ["https://storage.cloud.google.com", event["bucket"], urlFilename]
    )
    return url

def main(data, context):
    #This hardcodes a valid base64 encoded image
    data = base64.b64decode(event["data"])
    my_context = 0

    output = storage_add_fetch(data, event_test, my_context)
    if(output["URL"] == None):
        print("No URL constructed. Error in blob creation")
    else:
        print("The output url is: " + output["URL"])

    print("The item was successfully added! DONE!")